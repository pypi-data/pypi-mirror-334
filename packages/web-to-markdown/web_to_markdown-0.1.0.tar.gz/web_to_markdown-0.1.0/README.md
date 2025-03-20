# Web to Markdown

A Python library for crawling web pages and converting them to markdown format. This tool helps you easily convert web documentation, blogs, or any web content into clean markdown files while preserving the content structure.

## Features

- Depth-limited web crawling
- Domain/path boundary respect
- Smart content extraction using readability-lxml
- Clean HTML to Markdown conversion
- Metadata extraction
- Command-line interface with configurable options

## Installation

```bash
pip install web-to-markdown
```

## Usage

### Command Line Interface

```bash
# Basic usage
web-to-markdown -u https://example.com/docs -o output.md

# Specify crawl depth
web-to-markdown -u https://example.com/docs -d 2 -o output.md

# Enable verbose logging
web-to-markdown -u https://example.com/docs -v
```

### Python API

```python
from web_to_markdown import WebCrawler, MarkdownConverter

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

## Command Line Options

- `-u, --url`: Base URL to crawl (required)
- `-d, --depth`: Maximum crawl depth (default: 3)
- `-o, --output`: Output markdown file path (default: output.md)
- `-v, --verbose`: Enable verbose logging

## Dependencies

- beautifulsoup4
- requests
- urllib3
- markdown
- readability-lxml
- html2text

## License

MIT License
