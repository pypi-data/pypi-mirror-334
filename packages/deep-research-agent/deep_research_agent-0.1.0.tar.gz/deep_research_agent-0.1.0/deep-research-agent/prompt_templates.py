# research_agent/prompt_templates.py

# Prompt for generating search queries
SEARCH_QUERY_GENERATION_PROMPT = """
You are a research assistant tasked with generating effective search queries for web research.

TOPIC: {topic}

Based on the current state of research:
{current_summary}

Please generate a search query that will help gather more information about this topic.
Focus on any knowledge gaps or aspects that need deeper exploration.

The search query should be specific, concise, and designed to retrieve relevant information.
DO NOT format it as a question, but as search keywords. Your response should only contain the search query.
"""

# Prompt for summarizing search results
SUMMARIZATION_PROMPT = """
You are a research assistant tasked with summarizing web search results about a specific topic.

TOPIC: {topic}

Here are the search results to summarize:
{search_results}

Previous summary (if any):
{current_summary}

Please provide a comprehensive, well-organized summary that incorporates these new search results with any previous summary.
Focus on factual information, and include specific details, figures, and dates when available.
Ensure the summary is coherent and flows logically from one point to the next.
"""

# Prompt for reflection on current research
REFLECTION_PROMPT = """
You are a research assistant tasked with reflecting on the current state of research on a topic.

TOPIC: {topic}

Current summary of research:
{current_summary}

Based on this summary, please:
1. Identify any knowledge gaps or areas that need deeper exploration
2. Highlight any contradictions or inconsistencies in the information
3. Suggest specific aspects that should be researched further

Your reflection should be thorough and critical, helping to guide the next steps in the research process.
"""

# Add to prompt_templates.py
CHAIN_OF_THOUGHT_QUERY_PROMPT = """
You are a research assistant tasked with generating effective search queries for web research.

TOPIC: {topic}

Based on the current state of research:
{current_summary}

Let's think step by step about what would make an effective search query.
1. What are the key aspects of the topic we need to explore?
2. What knowledge gaps exist in our current understanding?
3. What specific terms would help find relevant information?
4. How can we make the query specific but not too narrow?

After thinking through these steps, provide ONLY the final search query.
The search query should be specific, concise, and designed to retrieve relevant information.
DO NOT format it as a question, but as search keywords.
"""


# Prompt for the final research report
FINAL_REPORT_PROMPT = """
You are a research assistant tasked with creating a final research report on a specific topic.

TOPIC: {topic}

Research summary:
{current_summary}

Please create a comprehensive, well-structured research report based on the summary above.
The report should include:

1. An introduction explaining the topic and its significance
2. Main sections covering the key aspects of the topic
3. A conclusion summarizing the findings and their implications

Format the report with clear headings and subheadings using Markdown syntax.
Ensure the information is organized logically and flows well from one section to the next.
"""
