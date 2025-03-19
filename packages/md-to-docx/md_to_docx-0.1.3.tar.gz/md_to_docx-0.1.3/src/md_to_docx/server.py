"""Server module for md_to_docx.

This module re-exports server functionality from the package's __init__ for backward compatibility.
"""

import os
import sys

# Handle imports for both package usage and direct script execution
try:
    # When used as a package
    from md_to_docx import serve
except ImportError:
    # When run directly
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from src.md_to_docx import serve

if __name__ == "__main__":
    serve() 