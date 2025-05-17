from setuptools import setup, find_packages

setup(
    name="verbalstream-odoo-ai",
    version="0.1.0",
    description="VerbalStream AI-enhanced modules for Odoo",
    author="VerbalStream",
    author_email="info@verbalstream.com",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    install_requires=[
        "openai>=1.0.0",
        "anthropic>=0.5.0",
        "pgvector>=0.2.0",
        "chromadb>=0.4.0",
        "qdrant-client>=1.1.0",
        "PyMuPDF>=1.22.0",
        "markdown2>=2.4.0",
        "markdownify>=0.11.0",
        "nltk>=3.8.0",
        "numpy>=1.24.0",
        "pydantic>=2.0.0",
        "requests>=2.31.0",
    ],
)
