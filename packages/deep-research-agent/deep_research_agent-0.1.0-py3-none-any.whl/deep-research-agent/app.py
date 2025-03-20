# app.py
import streamlit as st
import logging
import json
import os
from research_agent.config import ResearchConfig
from research_agent.research_controller import ResearchController

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_research(topic, cycles, max_results, max_urls, output_file):
    """Run the deep research agent and return results."""
    
    # Create configuration
    config = ResearchConfig(
        topic=topic,
        max_research_cycles=cycles,
        max_search_results_per_query=max_results,
        max_urls_to_scrape_per_cycle=max_urls
    )
    
    logger.info(f"Starting deep research on topic: {config.topic}")
    
    # Initialize and run the research controller
    controller = ResearchController(config)
    research_results = controller.run_full_research()
    
    # Save the final report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(research_results["final_report"])
    
    logger.info(f"Research completed. Final report saved to {output_file}")
    
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
    
    return research_results

def main():
    st.set_page_config(
        page_title="Deep Research Agent",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("Deep Research Agent")
    st.subheader("Generate comprehensive research reports on any topic")
    
    with st.sidebar:
        st.header("Research Settings")
        
        topic = st.text_input("Research Topic", placeholder="Enter your research topic here...")
        
        col1, col2 = st.columns(2)
        with col1:
            cycles = st.number_input("Research Cycles", min_value=1, max_value=5, value=2, 
                                    help="Number of research cycles to perform")
        with col2:
            output_file = st.text_input("Output Filename", value="research_report.md", 
                                       help="Filename for the output markdown report")
        
        col3, col4 = st.columns(2)
        with col3:
            max_results = st.number_input("Max Search Results", min_value=1, max_value=10, value=5, 
                                         help="Maximum search results per query")
        with col4:
            max_urls = st.number_input("Max URLs to Scrape", min_value=1, max_value=5, value=3, 
                                      help="Maximum URLs to scrape per cycle")
        
        run_button = st.button("Start Research", type="primary", use_container_width=True)
    
    # Main content area
    if 'research_results' not in st.session_state:
        st.session_state.research_results = None
        st.session_state.current_cycle = 0
        st.session_state.is_researching = False
        st.session_state.research_complete = False
    
    if run_button and topic:
        # Reset session state
        st.session_state.research_results = None
        st.session_state.current_cycle = 0
        st.session_state.is_researching = True
        st.session_state.research_complete = False
        
        # Start a spinner
        with st.spinner(f"Researching '{topic}'... This may take several minutes."):
            try:
                # Run the research
                research_results = run_research(
                    topic=topic,
                    cycles=cycles,
                    max_results=max_results,
                    max_urls=max_urls,
                    output_file=output_file
                )
                st.session_state.research_results = research_results
                st.session_state.is_researching = False
                st.session_state.research_complete = True
                st.success(f"Research completed! Report saved to {output_file}")
            except Exception as e:
                st.error(f"An error occurred during research: {str(e)}")
                st.session_state.is_researching = False
    
    # Display research results if available
    if st.session_state.research_complete and st.session_state.research_results:
        results = st.session_state.research_results
        
        st.header("Research Report")
        
        tabs = st.tabs(["Final Report", "Research Summary", "Research Data"])
        
        with tabs[0]:  # Final Report tab
            st.markdown(results["final_report"])
            
            # Download button for the report
            st.download_button(
                label="Download Report (Markdown)",
                data=results["final_report"],
                file_name=output_file,
                mime="text/markdown"
            )
        
        with tabs[1]:  # Research Summary tab
            st.subheader("Research Summary")
            st.write(f"Topic: {results['topic']}")
            st.write(f"Research Cycles Completed: {results['research_cycles_completed']}")
            st.text_area("Final Summary", results["final_summary"], height=300)
        
        with tabs[2]:  # Research Data tab
            st.subheader("Search Results")
            if results.get("all_search_results"):
                for i, result in enumerate(results["all_search_results"]):
                    with st.expander(f"Result {i+1}: {result.get('title', 'Untitled')}"):
                        st.write(f"**Source:** {result.get('href', 'N/A')}")
                        st.write(f"**Summary:** {result.get('body', 'No summary available')}")
            else:
                st.info("No search results available.")
            
            # Download button for research data
            if os.path.exists("research_data.json"):
                with open("research_data.json", "r") as f:
                    research_data = f.read()
                    
                st.download_button(
                    label="Download Complete Research Data (JSON)",
                    data=research_data,
                    file_name="research_data.json",
                    mime="application/json"
                )
    
    # Display instructions if no research has been run
    if not st.session_state.is_researching and not st.session_state.research_complete:
        st.info("""
        ### How to use this tool:
        1. Enter your research topic in the sidebar
        2. Adjust the research parameters if needed
        3. Click "Start Research" to begin
        
        The agent will search the web, analyze the results, and generate a comprehensive research report.
        """)

if __name__ == "__main__":
    main()