#!/usr/bin/env python3
"""Command-line interface for web-to-markdown."""

import argparse
import logging
from typing import Optional

from .crawler import WebCrawler
from .converter import MarkdownConverter

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Crawl web pages and convert them to markdown format.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-u', '--url',
        required=True,
        help='Base URL to crawl (e.g., https://example.com/docs)'
    )
    parser.add_argument(
        '-d', '--depth',
        type=int,
        default=3,
        help='Maximum crawl depth'
    )
    parser.add_argument(
        '-o', '--output',
        default='output.md',
        help='Output markdown file path'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    return parser.parse_args()

def run(url: str, depth: int = 3, output: str = 'output.md', verbose: bool = False) -> Optional[str]:
    """
    Run the web-to-markdown conversion process.
    
    Args:
        url: Base URL to crawl
        depth: Maximum crawl depth
        output: Output markdown file path
        verbose: Enable verbose logging
    
    Returns:
        Path to the output file if successful
    """
    if verbose:
        logging.basicConfig(level=logging.INFO)
    
    try:
        # Initialize and run crawler
        crawler = WebCrawler(base_url=url, max_depth=depth)
        pages = crawler.crawl()
        
        # Convert to markdown
        converter = MarkdownConverter()
        markdown_content = converter.convert_to_markdown(pages)
        
        # Save the result
        converter.save_markdown(markdown_content, output)
        print(f"Successfully crawled {len(pages)} pages and saved to {output}")
        return output
    except Exception as e:
        logging.error(f"Error during conversion: {str(e)}")
        return None

def main() -> None:
    """Main entry point for the CLI."""
    args = parse_args()
    run(args.url, args.depth, args.output, args.verbose)

if __name__ == "__main__":
    main()
