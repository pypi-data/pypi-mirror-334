# research_agent/web_scraper.py
import requests
from bs4 import BeautifulSoup
import html2text
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class WebScraper:
    """Scrapes web content from URLs."""
    
    def __init__(self):
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True
        self.html_converter.ignore_tables = False
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def scrape_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape content from a given URL."""
        logger.info(f"Scraping URL: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Failed to fetch URL: {url}, status code: {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            
            # Get the text content
            text = self.html_converter.handle(str(soup))
            
            # Extract title
            title = ""
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text()
            
            return {
                "url": url,
                "title": title,
                "content": text[:50000],  # Limit content size
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error scraping URL {url}: {e}")
            return None
