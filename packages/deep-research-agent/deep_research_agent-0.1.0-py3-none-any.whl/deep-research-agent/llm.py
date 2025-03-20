# research_agent/llm.py
from langchain_community.llms import Ollama
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """Initialize and return the Ollama QwQ model."""
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model_name = os.getenv("OLLAMA_MODEL", "qwq")
    
    return Ollama(
        base_url=base_url,
        model=model_name,
        temperature=0.1,  # Lower temperature for more deterministic outputs
        num_ctx=4096,     # Context window size
    )

def create_structured_output_chain(prompt_template, output_parser):
    """Create a chain that produces structured outputs."""
    llm = get_llm()
    prompt = PromptTemplate.from_template(prompt_template)
    
    return (
        RunnablePassthrough.assign(prompt=prompt) 
        | (lambda x: {"output": llm.invoke(x["prompt"])})
        | (lambda x: output_parser.parse(x["output"]))
    )
