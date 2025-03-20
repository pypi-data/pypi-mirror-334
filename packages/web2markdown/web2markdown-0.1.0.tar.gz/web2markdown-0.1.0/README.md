# Web2Markdown

By Roger Sindreu

A Python library for crawling web pages and converting them to markdown format. This tool is particularly useful for creating context files for Large Language Models (LLMs), especially when working with new AI frameworks or technologies where documentation is constantly evolving. It helps you easily convert web documentation, blogs, or any web content into clean markdown files while preserving the content structure.

## Features

- Depth-limited web crawling
- Domain/path boundary respect
- Smart content extraction using trafilatura
- Clean HTML to Markdown conversion
- Metadata extraction
- Command-line interface with configurable options

## Installation

```bash
pip install web2markdown
```

## Usage

### Command Line Interface

```bash
# Basic usage
web2markdown -u https://example.com/docs -o output.md

# Specify crawl depth
web2markdown -u https://example.com/docs -d 2 -o output.md

# Enable verbose logging
web2markdown -u https://example.com/docs -v
```

### Python API

```python
from web2markdown import WebCrawler, MarkdownConverter

# Initialize crawler
crawler = WebCrawler(base_url="https://example.com/docs", max_depth=3)

# Crawl pages
pages = crawler.crawl()

# Convert to markdown
converter = MarkdownConverter()
markdown_content = converter.convert_to_markdown(pages)

# Save the result
converter.save_markdown(markdown_content, "output.md")
```

### Using with LLMs through the UI

You can use Web2Markdown by manually downloading the documentation pages as markdown and then manually attaching them to your conversation with the LLM.


### Using with LLMs (Programmatically)

Web2Markdown is particularly valuable when you need to provide up-to-date context to LLMs about new frameworks or technologies. Here's how you can use it with popular LLM APIs:

```python
from web2markdown import WebCrawler, MarkdownConverter
from openai import OpenAI  # or import google.generativeai as genai

# Download latest documentation
crawler = WebCrawler("https://python.langchain.com/docs/expression_language/", max_depth=2)
pages = crawler.crawl()

converter = MarkdownConverter()
markdown_content = converter.convert_to_markdown(pages)
converter.save_markdown(markdown_content, "langgraph.md")

# Use with OpenAI
client = OpenAI()
with open("langgraph.md", "r") as f:
    context = f.read()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an AI expert. Use the context provided to answer questions."},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: How do I create a simple LangGraph?"}]
)

# Or use with Google's Gemini
'''
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-pro")

with open("langgraph.md", "r") as f:
    context = f.read()

response = model.generate_content(
    f"Context: {context}\n\nQuestion: How do I create a simple LangGraph?"
)
'''
```

## Command Line Options

- `-u, --url`: Base URL to crawl (required)
- `-d, --depth`: Maximum crawl depth (default: 3)
- `-o, --output`: Output markdown file path (default: output.md)
- `-v, --verbose`: Enable verbose logging

## Dependencies

- beautifulsoup4>=4.12.0
- requests>=2.31.0
- urllib3>=2.1.0
- markdown>=3.5.0
- trafilatura>=0.8.1

## License

MIT License
