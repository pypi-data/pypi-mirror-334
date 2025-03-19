"""
MD to DOCX converter with Mermaid diagram support.

This package provides tools for converting Markdown files to DOCX format,
with special handling for Mermaid diagrams and code blocks.
"""

__version__ = "0.1.1"

import click
import sys
import asyncio
import logging
import os
from pathlib import Path
from typing import Any

# Handle imports for both package usage and direct script execution
try:
    # When used as a package
    from .core import md_to_docx, render_mermaid_to_image
except ImportError:
    # When run directly
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from src.md_to_docx.core import md_to_docx, render_mermaid_to_image

from mcp.server.fastmcp import FastMCP

__all__ = ["md_to_docx", "render_mermaid_to_image"]

# Initialize FastMCP server
mcp = FastMCP("md_to_docx")


@mcp.tool()
async def md_to_docx_tool(md_content: str, output_file: str = None, debug_mode: bool = False, table_style: str = 'Table Grid') -> str:
    """Convert Markdown file to DOCX, rendering Mermaid diagrams as images.
    
    Args:
        md_content: Markdown content to convert
        output_file: Optional output file path, defaults to 'output.docx'
        debug_mode: Whether to enable debug mode
        table_style: Style to apply to tables, defaults to 'Table Grid',options:['Normal Table', 'Table Grid', 'Light Shading', 'Light Shading Accent 1', 'Light Shading 
Accent 2', 'Light Shading Accent 3', 'Light Shading Accent 4', 'Light Shading Accent 5', 'Light Shading Accent 6', 'Light List', 'Light List Accent 1', 'Light List Accent 2', 'Light List Accent 3', 'Light List 
Accent 4', 'Light List Accent 5', 'Light List Accent 6', 'Light Grid', 'Light Grid Accent 1', 'Light Grid Accent 2', 'Light Grid Accent 3', 'Light Grid Accent 4', 'Light Grid Accent 5', 'Light Grid Accent 6', 'Medium Shading 1', 'Medium Shading 1 Accent 1', 'Medium Shading 1 Accent 2', 'Medium Shading 1 Accent 3', 'Medium Shading 1 Accent 4', 'Medium Shading 1 Accent 5', 'Medium Shading 1 Accent 6', 'Medium Shading 2', 'Medium Shading 2 Accent 1', 'Medium Shading 2 Accent 2', 'Medium Shading 2 Accent 3', 'Medium Shading 2 Accent 4', 'Medium Shading 2 Accent 5', 'Medium Shading 2 Accent 6', 'Medium List 1', 'Medium List 1 Accent 1', 'Medium List 1 Accent 2', 'Medium List 1 Accent 3', 'Medium List 1 Accent 4', 'Medium List 1 Accent 5', 'Medium List 1 Accent 6', 'Medium List 2', 'Medium List 2 Accent 1', 'Medium List 2 Accent 2', 'Medium List 2 Accent 3', 'Medium List 2 Accent 4', 'Medium List 2 Accent 5', 'Medium List 2 Accent 6', 'Medium Grid 1', 'Medium Grid 1 Accent 1', 'Medium Grid 1 Accent 2', 'Medium Grid 1 Accent 3', 'Medium Grid 1 Accent 4', 'Medium Grid 1 Accent 5', 'Medium Grid 1 Accent 6', 'Medium Grid 2', 'Medium Grid 2 Accent 
1', 'Medium Grid 2 Accent 2', 'Medium Grid 2 Accent 3', 'Medium Grid 2 Accent 4', 'Medium Grid 2 Accent 5', 'Medium Grid 2 Accent 6', 'Medium Grid 3', 'Medium Grid 3 Accent 1', 'Medium Grid 3 Accent 2', 'Medium Grid 3 Accent 3', 'Medium Grid 3 Accent 4', 'Medium Grid 3 Accent 5', 'Medium Grid 3 Accent 6', 'Dark List', 'Dark List Accent 1', 'Dark List Accent 2', 'Dark List Accent 3', 'Dark List Accent 4', 'Dark List Accent 5', 'Dark List Accent 6', 'Colorful Shading', 'Colorful Shading Accent 1', 'Colorful Shading Accent 2', 'Colorful Shading Accent 3', 'Colorful Shading Accent 4', 'Colorful Shading Accent 5', 'Colorful Shading Accent 6', 'Colorful List', 'Colorful List Accent 1', 'Colorful List Accent 2', 'Colorful List Accent 3', 'Colorful List Accent 4', 'Colorful List Accent 5', 'Colorful List Accent 6', 'Colorful Grid', 'Colorful Grid Accent 1', 'Colorful Grid Accent 2', 'Colorful Grid Accent 3', 'Colorful Grid Accent 4', 'Colorful Grid Accent 5', 'Colorful Grid Accent 6']
        
    Returns:
        The path to the saved DOCX file
    """
    return md_to_docx(md_content, output_file, debug_mode, table_style)


def serve():
    """Run the MCP server."""
    mcp.run(transport='stdio')


@click.group()
def cli():
    """MD to DOCX converter with Mermaid diagram support."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', type=str, help='Path to the output DOCX file (default: input_file_name.docx)')
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode')
@click.option('-t', '--table-style', type=str, default='Table Grid', 
              help='Style to apply to tables (default: Table Grid). Common styles include: Table Normal, Table Grid, Light Shading, Light List, Light Grid, Medium Shading 1, Medium Shading 2, etc.')
def convert(input_file, output, debug, table_style):
    """Convert Markdown file to DOCX file with Mermaid diagram support."""
    # Process input file path
    input_path = Path(input_file)
    
    # Determine output file path
    if output:
        output_path = output
    else:
        # Replace .md extension with .docx, or add .docx if no extension
        if input_path.suffix.lower() == '.md':
            output_path = str(input_path.with_suffix('.docx'))
        else:
            output_path = f"{input_file}.docx"
    
    try:
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        click.echo(f"Converting {input_file} to {output_path}...")
        click.echo(f"Using table style: {table_style}")
        
        # Convert to DOCX
        result = md_to_docx(md_content, output_path, debug, table_style)
        
        click.echo(f"Conversion completed successfully! Output file: {result}")
        return 0
    
    except Exception as e:
        click.echo(f"Error during conversion: {e}", err=True)
        import traceback
        traceback.print_exc()
        return 1


@cli.command()
@click.option("-v", "--verbose", count=True, help="Increase verbosity (can be used multiple times)")
def server(verbose):
    """Run as an MCP server."""
    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)
    # Don't use asyncio.run() here as mcp.run() handles the event loop itself
    serve()


def main():
    """Entry point for the application."""
    return cli()


if __name__ == "__main__":
    sys.exit(main()) 