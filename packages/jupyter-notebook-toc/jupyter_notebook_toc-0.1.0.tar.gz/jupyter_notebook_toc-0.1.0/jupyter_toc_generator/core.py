"""
Core functionality for generating table of contents from Jupyter notebooks.
"""

import re
from typing import List, Dict, Tuple
import subprocess
import sys
import nbformat

def _ensure_nbformat():
    """Ensure nbformat is installed, install it if not present."""
    try:
        import nbformat
    except ImportError:
        print("Installing required package: nbformat")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nbformat"])
        import nbformat
    return nbformat

# Import nbformat after ensuring it's installed
nbformat = _ensure_nbformat()

def _extract_headers(cell_content: str) -> List[Tuple[int, str]]:
    """
    Extract headers from markdown cell content.
    
    Args:
        cell_content: The content of a markdown cell
        
    Returns:
        List of tuples containing (level, text) for each header
    """
    headers = []
    lines = cell_content.split('\n')
    
    for line in lines:
        # Match headers with 1-3 # symbols
        match = re.match(r'^(#{1,3})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headers.append((level, text))
    
    return headers


def _generate_numbered_toc(headers: List[Tuple[int, str]]) -> str:
    """
    Generate a numbered table of contents from headers.
    
    Args:
        headers: List of (level, text) tuples
        
    Returns:
        Formatted table of contents as string
    """
    toc_lines = ["# Table of Contents\n"]
    current_numbers = [0, 0, 0]
    
    for level, text in headers:
        # Update numbering
        current_numbers[level - 1] += 1
        for i in range(level, 3):
            current_numbers[i] = 0
            
        # Create number string (e.g., "1.2.3")
        number = '.'.join(str(n) for n in current_numbers[:level])
        
        # Add indentation based on level
        indent = '    ' * (level - 1)
        toc_lines.append(f"{indent}{number}. {text}")
    
    return '\n'.join(toc_lines)


def generate_toc(notebook_path: str) -> str:
    """
    Generate a table of contents from a Jupyter notebook.
    
    Args:
        notebook_path: Path to the Jupyter notebook file
        
    Returns:
        Formatted table of contents as string
        
    Raises:
        FileNotFoundError: If the notebook file doesn't exist
        nbformat.reader.NotJSONError: If the notebook is not valid JSON
    """
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    # Collect all headers from markdown cells
    all_headers = []
    for cell in notebook.cells:
        if cell.cell_type == 'markdown':
            headers = _extract_headers(cell.source)
            all_headers.extend(headers)
    
    # Generate the table of contents
    return _generate_numbered_toc(all_headers) 