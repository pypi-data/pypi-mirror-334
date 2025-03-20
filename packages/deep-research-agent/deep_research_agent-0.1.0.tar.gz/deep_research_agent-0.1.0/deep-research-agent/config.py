# research_agent/config.py
from pydantic import BaseModel
from typing import List, Optional

class ResearchConfig(BaseModel):
    """Configuration for the research agent."""
    max_research_cycles: int = 3
    max_search_results_per_query: int = 5
    max_urls_to_scrape_per_cycle: int = 3
    search_engine: str = "duckduckgo"
    summary_max_tokens: int = 2000
    topic: Optional[str] = None
