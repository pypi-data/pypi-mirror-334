from typing import Dict
import logging

logger = logging.getLogger(__name__)

class MarkdownConverter:
    def __init__(self):
        """Initialize the markdown converter."""
        pass
        
    def convert_to_markdown(self, pages: Dict[str, Dict]) -> str:
        """
        Convert crawled pages to a markdown document.
        
        Args:
            pages (Dict[str, Dict]): Dictionary of pages with their content
            
        Returns:
            str: Markdown formatted string
        """
        markdown_content = []
        
        for url, page in pages.items():
            if not page:
                continue
            
            markdown_content.append("---\n\n")
            
            # Add URL reference
            markdown_content.append(f"**Source**: {url}\n\n")
            
            # Add metadata if available
            metadata = page.get('metadata', {})
            if any(metadata.values()):
                markdown_content.append("### Page Metadata\n\n")
                if metadata.get('author'):
                    markdown_content.append(f"- **Author**: {metadata['author']}\n")
                if metadata.get('date'):
                    markdown_content.append(f"- **Published**: {metadata['date']}\n")
                if metadata.get('description'):
                    markdown_content.append(f"- **Description**: {metadata['description']}\n")
                if metadata.get('keywords'):
                    markdown_content.append(f"- **Keywords**: {metadata['keywords']}\n")
                markdown_content.append("\n")
            
            # Add main content (already in markdown format)
            content = page['content']
            if content:
                # Clean up any excessive newlines
                content = '\n'.join(line for line in content.splitlines() if line.strip())
                markdown_content.append(f"{content}\n\n")
        
        # Add final separator
        markdown_content.append("---\n")
        
        return ''.join(markdown_content)
        
        return ''.join(markdown_content)
        
    def save_markdown(self, markdown_content: str, output_file: str):
        """
        Save markdown content to a file.
        
        Args:
            markdown_content (str): The markdown formatted content
            output_file (str): Path to the output file
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            logger.info(f"Markdown saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving markdown: {str(e)}")
