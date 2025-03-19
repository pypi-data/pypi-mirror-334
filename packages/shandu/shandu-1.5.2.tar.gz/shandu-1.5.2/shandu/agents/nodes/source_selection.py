"""Source selection node."""
import os
import re
from rich.console import Console
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from ..processors.content_processor import AgentState
from ..utils.agent_utils import log_chain_of_thought, _call_progress_callback
from ...prompts import SYSTEM_PROMPTS, USER_PROMPTS

console = Console()

# Structured output model for source selection
class SourceSelection(BaseModel):
    """Structured output for source selection."""
    selected_sources: list[str] = Field(
        description="List of URLs for the most valuable sources to include in the report",
        min_items=1
    )
    selection_rationale: str = Field(
        description="Explanation of why these sources were selected"
    )

async def smart_source_selection(llm, progress_callback, state: AgentState) -> AgentState:
    """Select relevant sources for the report using structured output."""
    state["status"] = "Selecting most valuable sources"
    console.print("[bold blue]Selecting most relevant and high-quality sources...[/]")

    all_source_urls = []
    for analysis in state["content_analysis"]:
        if "sources" in analysis and isinstance(analysis["sources"], list):
            for url in analysis["sources"]:
                if url not in all_source_urls:
                    all_source_urls.append(url)
    
    # If we have too many sources, use smart selection to filter them
    if len(all_source_urls) > 25:

        sources_text = ""
        for i, url in enumerate(all_source_urls, 1):

            source_meta = {}
            for source in state["sources"]:
                if source.get("url") == url:
                    source_meta = source
                    break

            sources_text += f"Source {i}:\nURL: {url}\n"
            if source_meta.get("title"):
                sources_text += f"Title: {source_meta.get('title')}\n"
            if source_meta.get("snippet"):
                sources_text += f"Summary: {source_meta.get('snippet')}\n"
            if source_meta.get("date"):
                sources_text += f"Date: {source_meta.get('date')}\n"
            sources_text += "\n"
        
        try:
            # Use a completely direct approach to avoid template issues
            direct_prompt = f"""You must carefully select the most valuable sources for this research report. 

RESEARCH TOPIC: {state['query']}

SOURCES TO EVALUATE:
{sources_text}

SELECTION CRITERIA:
1. DIRECT RELEVANCE: The source must explicitly address core aspects of the research question
2. INFORMATION QUALITY: The source should provide significant unique data or insights
3. CREDIBILITY: The source should be authoritative and reliable
4. RECENCY: The source should be up-to-date enough for the topic
5. DIVERSITY: Sources should cover different perspectives or aspects

INSTRUCTIONS:
- Select 15-20 of the most valuable sources from the list
- Return ONLY the exact URLs of your selected sources
- List the URLs in order of importance (most valuable first)
- One URL per line, no explanation or numbering
"""
            # Send the prompt directly to the model
            response = await llm.ainvoke(direct_prompt)

            response_text = response.content

            selected_urls = []
            lines = response_text.split('\n')
            
            # Iterate through each line looking for URLs
            for line in lines:

                for url in all_source_urls:
                    if url in line:
                        if url not in selected_urls:
                            selected_urls.append(url)
                            break

            rationale = "Sources were selected based on relevance, credibility, and coverage of key aspects."
            rationale_section = re.search(r'(?:rationale|reasoning|explanation|justification)(?:\s*:|\s*\n)([^#]*?)(?:$|#)', response_text.lower(), re.IGNORECASE | re.DOTALL)
            if rationale_section:
                rationale = rationale_section.group(1).strip()
            
            # Log the selection rationale
            log_chain_of_thought(state, f"Source selection rationale: {rationale}")
            
        except Exception as e:
            console.print(f"[dim red]Error in structured source selection: {str(e)}. Using simpler approach.[/dim red]")
            from ...utils.logger import log_error
            log_error("Error in structured source selection", e, 
                 context=f"Query: {state['query']}, Function: smart_source_selection")
            current_file = os.path.basename(__file__)
            #with open('example.txt', 'a') as file:
                # Append the current file's name and some text
                #file.write(f'This line was written by: {current_file}\n')
                #file.write(f'Error {e}.\n')

            # Fallback to non-structured approach
            try:
                # Even simpler fallback approach
                response = await llm.ainvoke(f"""Select 15 best sources for: {state['query']}

From these sources:
{sources_text}

Return ONLY the URLs, one per line.
""")

                selected_urls = []
                for url in all_source_urls:
                    if url in response.content:
                        selected_urls.append(url)
            except Exception as e2:
                console.print(f"[dim red]Error in fallback source selection: {str(e2)}. Using default selection.[/dim red]")
                selected_urls = []
        
        # Make sure we have at least some sources
        if not selected_urls and all_source_urls:
            # If selection failed, take the first 15-20 sources
            selected_urls = all_source_urls[:min(20, len(all_source_urls))]
            
        state["selected_sources"] = selected_urls
        log_chain_of_thought(state, f"Selected {len(selected_urls)} most relevant sources from {len(all_source_urls)} total sources")
    else:
        # If we don't have too many sources, use all of them
        state["selected_sources"] = all_source_urls
        log_chain_of_thought(state, f"Using all {len(all_source_urls)} sources for final report")
    
    if progress_callback:
        await _call_progress_callback(progress_callback, state)
    return state
