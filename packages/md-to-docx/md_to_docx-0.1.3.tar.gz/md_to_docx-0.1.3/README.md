# MD_TO_DOCX

A tool for converting Markdown files to DOCX format with support for Mermaid diagrams and code block formatting.

## Features

- Convert Markdown files to DOCX format
- Support for rendering Mermaid diagrams as images
- Code block formatting with borders and language highlighting
- Support for tables, lists, and other Markdown elements
- Detailed debugging functionality

## Installation

### From PyPI

```bash
pip install md-to-docx
```

### From Source

```bash
git clone https://github.com/yourusername/md-to-docx.git
cd md-to-docx
pip install -e .
```

## Usage

### Command Line

```bash
# Basic usage
md-to-docx input.md -o output.docx

# With debugging enabled
md-to-docx input.md -o output.docx -d
```

### As a Python Library

```python
from md_to_docx import md_to_docx

# Convert Markdown content to DOCX
result = md_to_docx(markdown_content, "output.docx")
print(f"Output file: {result}")
```

### As an MCP Server

```bash
# Start the MCP server
python -m md_to_docx.server
```

Then you can use it in your MCP client code:

```python
from mcp.client import Client

client = Client()
md_content = "# Hello World\n\nThis is a test."
result = await client.md_to_docx_tool(md_content=md_content)
print(f"Output file: {result}")
```

## Debugging Code Block Issues

If you encounter issues with code blocks, you can use these debugging features:

1. **Enable debug mode**:
   ```bash
   md-to-docx input.md -o output.docx -d
   ```
   This will show detailed information about code block extraction and processing.

2. **Use as a library with debug mode**:
   ```python
   from md_to_docx import md_to_docx
   
   result = md_to_docx(markdown_content, "output.docx", debug_mode=True)
   ```

## Common Issues

### Code Blocks Not Displaying Correctly

If code blocks aren't displaying correctly, it might be due to:

1. Special characters in the code that affect the regex pattern matching
2. Improper code block formatting (e.g., missing newlines)
3. Incorrect handling of line breaks in the code

### Mermaid Diagrams Not Rendering

If Mermaid diagrams aren't rendering correctly, it might be due to:

1. Mermaid CLI not being installed
2. Network connection issues preventing access to the Mermaid.ink API
3. Syntax errors in the Mermaid diagram code

## Advanced Usage

### Customizing Code Block Formatting

You can modify the `format_code_block` function in the source code to customize code block formatting, such as changing fonts, sizes, or border styles.

### Adding New Markdown Extensions

You can add new Markdown extensions to support additional Markdown features by modifying the `md_to_docx` function:

```python
from md_to_docx import md_to_docx
from md_to_docx.core import format_code_block

# Your custom implementation here
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
