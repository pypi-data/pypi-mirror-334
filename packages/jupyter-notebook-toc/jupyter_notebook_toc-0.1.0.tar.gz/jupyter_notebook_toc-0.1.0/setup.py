from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jupyter-notebook-toc",
    version="0.1.0",
    author="Viktor Sjöberg",
    author_email="viktor@alfrida.se",
    description="A tool to generate table of contents for Jupyter notebooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Viktor-Sjoberg/jupyter-notebook-toc",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "nbformat>=5.0.0",
        "jupyter>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "jupyter-toc=jupyter_toc_generator.cli:main",
        ],
    },
) 