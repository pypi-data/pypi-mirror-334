"""
Core functionality for generating table of contents from Jupyter notebooks.
"""

import re
from typing import List, Dict, Tuple
import subprocess
import sys
import nbformat
import os
import json

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

def _extract_headers(cell_content: str) -> List[Tuple[int, str, str]]:
    """
    Extract headers from markdown cell content.
    
    Args:
        cell_content: The content of a markdown cell
        
    Returns:
        List of tuples containing (level, number, text) where number can be empty
    """
    headers = []
    lines = cell_content.split('\n')
    
    for line in lines:
        # Match headers with 1-3 # symbols
        match = re.match(r'^(#{1,3})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            full_text = match.group(2).strip()
            
            # Try to extract number and text
            number_match = re.match(r'^(\d+\.?\d*\.?\d*)\s+(.+)$', full_text)
            if number_match:
                number = number_match.group(1)
                text = number_match.group(2).strip()
            else:
                number = ""
                text = full_text
            
            headers.append((level, number, text))
    
    return headers


def _generate_numbered_toc(headers: List[Tuple[int, str, str]]) -> str:
    """
    Generate a table of contents from headers, using only existing numbers.
    
    Args:
        headers: List of (level, number, text) tuples
        
    Returns:
        Formatted table of contents as string with hyperlinks
    """
    toc_lines = ["# Table of Contents\n"]
    
    for level, number, text in headers:
        # Create anchor link from text (without numbers)
        # Convert text to lowercase, replace spaces with hyphens, remove special characters
        anchor = text.lower()
        anchor = re.sub(r'[^a-z0-9\s-]', '', anchor)
        anchor = re.sub(r'\s+', '-', anchor)
        
        # Add indentation based on level
        indent = '    ' * (level - 1)
        # Create markdown link, adding the number only if it exists
        if number:
            toc_lines.append(f"{indent}{number} [{text}](#{anchor})")
        else:
            toc_lines.append(f"{indent}[{text}](#{anchor})")
    
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
    """
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    headers = []
    
    # Collect headers from markdown cells
    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            lines = cell.source.split('\n')
            for line in lines:
                if line.startswith('#'):
                    # Count the header level
                    level = len(line) - len(line.lstrip('#'))
                    if level <= 3:  # Only include headers up to level 3
                        # Remove the # symbols and leading/trailing whitespace
                        header_text = line.lstrip('#').strip()
                        # Add indentation based on level
                        indent = '    ' * (level - 1)
                        headers.append((indent, header_text))

    # Generate TOC
    toc_lines = ["# Table of Contents\n"]
    for indent, header_text in headers:
        # Remove everything after and including (#) if it exists
        if '#' in header_text:
            header_text = header_text.split('#')[0].strip()
        toc_lines.append(f"{indent}{header_text}")

    return '\n'.join(toc_lines) 