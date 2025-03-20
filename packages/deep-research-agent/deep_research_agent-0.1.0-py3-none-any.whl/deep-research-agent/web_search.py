# research_agent/web_search.py
from duckduckgo_search import DDGS
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def clean_query(query: str) -> str:
        """Remove thinking process and clean up the query."""
        # Remove content between <think> and </think> tags
        import re
        clean_query = re.sub(r'<think>.*?</think>', '', query, flags=re.DOTALL)
        
        # Remove any remaining tags
        clean_query = re.sub(r'<.*?>', '', clean_query)
        
        # Clean up whitespace
        clean_query = re.sub(r'\s+', ' ', clean_query).strip()
        
        return clean_query

class WebSearcher:
    """Handles web searches using DuckDuckGo."""
    
    def __init__(self, max_results: int = 5):
        self.max_results = max_results
        self.ddgs = DDGS()

    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Perform a web search with the given query."""
        # Clean the query first
        cleaned_query = clean_query(query)
        logger.info(f"Original query: {query}")
        logger.info(f"Cleaned query: {cleaned_query}")
        
        try:
            results = list(self.ddgs.text(cleaned_query, max_results=self.max_results))
            logger.info(f"Found {len(results)} results")
            
            # Format the results for better processing
            formatted_results = []
            for i, result in enumerate(results):
                formatted_results.append({
                    "index": i,
                    "title": result.get("title", ""),
                    "body": result.get("body", ""),
                    "href": result.get("href", ""),
                    "source": "duckduckgo"
                })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error during web search: {e}")
            return []

