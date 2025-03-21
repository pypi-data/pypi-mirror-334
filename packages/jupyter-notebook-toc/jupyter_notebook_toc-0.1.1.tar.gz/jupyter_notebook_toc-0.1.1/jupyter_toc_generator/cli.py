"""
Command-line interface for the Jupyter TOC Generator.
"""

import argparse
import sys
from .core import generate_toc


def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Generate a table of contents for a Jupyter notebook"
    )
    parser.add_argument(
        "notebook_path",
        help="Path to the Jupyter notebook file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: print to stdout)"
    )
    
    args = parser.parse_args()
    
    try:
        toc = generate_toc(args.notebook_path)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(toc)
        else:
            print(toc)
            
    except FileNotFoundError:
        print(f"Error: Notebook file '{args.notebook_path}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 