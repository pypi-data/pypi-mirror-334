from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="deep-research-agent",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI-powered deep research agent for autonomous web research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/deep-research-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    python_requires=">=3.9",
    install_requires=[
        "langchain>=0.3.0",
        "langchain-community>=0.0.5",
        "pydantic>=2.0.0",
        "duckduckgo-search>=3.0.0",
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "html2text>=2020.1.16",
        "python-dotenv>=1.0.0",
        "streamlit>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "deep-research=deep_research_agent.cli:main",
            "deep-research-ui=deep_research_agent.ui.streamlit_app:main",
        ],
    },
)