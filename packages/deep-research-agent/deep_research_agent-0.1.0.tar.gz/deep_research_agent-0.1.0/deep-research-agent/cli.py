#!/usr/bin/env python3
# cli.py
import argparse
import json
import logging
from .config import ResearchConfig
from .research_controller import ResearchController

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run the deep research agent from the command line."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Deep Research Agent')
    parser.add_argument('--topic', type=str, required=True, help='Research topic')
    parser.add_argument('--cycles', type=int, default=3, help='Number of research cycles')
    parser.add_argument('--max-results', type=int, default=5, help='Max search results per query')
    parser.add_argument('--max-urls', type=int, default=3, help='Max URLs to scrape per cycle')
    parser.add_argument('--output', type=str, default='research_report.md', help='Output file for the research report')
    args = parser.parse_args()
    
    # Create configuration
    config = ResearchConfig(
        topic=args.topic,
        max_research_cycles=args.cycles,
        max_search_results_per_query=args.max_results,
        max_urls_to_scrape_per_cycle=args.max_urls
    )
    
    logger.info(f"Starting deep research on topic: {config.topic}")
    
    # Initialize and run the research controller
    controller = ResearchController(config)
    research_results = controller.run_full_research()
    
    # Save the final report
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(research_results["final_report"])
    
    logger.info(f"Research completed. Final report saved to {args.output}")
    
    # Save all research data for reference
    with open('research_data.json', 'w', encoding='utf-8') as f:
        # Convert to serializable format
        serializable_results = {
            "topic": research_results["topic"],
            "research_cycles_completed": research_results["research_cycles_completed"],
            "final_summary": research_results["final_summary"],
            "all_search_results": research_results["all_search_results"]
        }
        json.dump(serializable_results, f, indent=2)
    
    logger.info("Complete research data saved to research_data.json")
    
    # Print a snippet of the final report
    print("\n" + "="*50)
    print("RESEARCH REPORT PREVIEW")
    print("="*50)
    preview_length = min(500, len(research_results["final_report"]))
    print(research_results["final_report"][:preview_length] + "...")
    print("\nFull report saved to:", args.output)

if __name__ == "__main__":
    main()