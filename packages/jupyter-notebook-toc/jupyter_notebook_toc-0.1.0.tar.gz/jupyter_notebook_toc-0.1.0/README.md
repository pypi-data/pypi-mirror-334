# Jupyter Notebook Table of Contents Generator

A Python library that automatically generates a table of contents for Jupyter notebooks by scanning markdown cells for headers.

## Features

- Scans Jupyter notebooks for markdown cells
- Identifies headers (H1, H2, H3) using "#", "##", and "###" syntax
- Generates a formatted table of contents with proper indentation
- Supports numbered sections
- Easy to integrate into existing notebooks

## Installation

```bash
pip install jupyter-toc-generator
```

## Usage

```python
from jupyter_toc_generator import generate_toc

# Generate TOC from a notebook file
toc = generate_toc("path/to/your/notebook.ipynb")

# Print the generated TOC
print(toc)

# Or save it to a file
with open("table_of_contents.md", "w") as f:
    f.write(toc)
```

## Example Output

```markdown
# Table of Contents

1. Introduction
   1.1. Background
   1.2. Purpose
2. Methodology
   2.1. Data Collection
   2.2. Analysis
3. Results
   3.1. Findings
   3.2. Discussion
```

## Development

To set up the development environment:

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT License - see LICENSE file for details 