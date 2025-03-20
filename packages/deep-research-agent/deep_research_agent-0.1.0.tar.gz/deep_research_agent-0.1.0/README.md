# Deep Research Agent

[![PyPI version](https://badge.fury.io/py/deep-research-agent.svg)](https://badge.fury.io/py/deep-research-agent)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered research agent that autonomously searches the web, analyzes content, and generates comprehensive research reports on any topic.

## Features

- **Automated Web Research**: Generate search queries, scrape content, and synthesize information
- **Multi-cycle Research**: Progressively build deeper understanding with multiple research cycles
- **Reflective Analysis**: Identify knowledge gaps and areas for further exploration
- **Structured Reports**: Generate well-organized markdown reports with clear sections
- **Multiple Interfaces**: Use via command line, Python API, or Streamlit web UI

## Installation

```bash
pip install deep-research-agent
```

## Usage

### Command Line

```bash
deep-research --topic "Your research topic" --cycles 2 --output report.md
```

### Streamlit UI

```bash
deep-research-ui
```

Then open your browser to the URL shown (typically http://localhost:8501).

### Python API

```python
from deep_research_agent import ResearchConfig, ResearchController

# Configure research parameters
config = ResearchConfig(
    topic="Your research topic",
    max_research_cycles=2,
    max_search_results_per_query=5,
    max_urls_to_scrape_per_cycle=3
)

# Initialize and run the research controller
controller = ResearchController(config)
results = controller.run_full_research()

# Access the final report
print(results["final_report"])
```

## Requirements

- Python 3.9+
- Local LLM (Ollama with QwQ model recommended)

## Environment Configuration

Create a `.env` file with:

```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwq
```

## How It Works

1. **Query Generation**: Creates effective search queries based on the topic and current knowledge
2. **Web Search**: Retrieves search results from DuckDuckGo
3. **Content Scraping**: Extracts and cleans content from web pages
4. **Summary Generation**: Integrates new information with existing knowledge
5. **Reflection**: Identifies gaps and contradictions to guide further research
6. **Report Generation**: Creates a comprehensive final report

## License

MIT License - see LICENSE file for details.