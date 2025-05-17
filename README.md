# VerbalStream Odoo AI

A comprehensive suite of AI-enhanced modules for Odoo, developed by VerbalStream - experts in development and QAI.

## Overview

This monorepo contains a collection of Odoo modules that integrate AI capabilities into the Odoo ERP system. The modules are designed to be:

- Simple for users but technically sophisticated
- Feature-rich with extensive configuration options
- Optimized to avoid repetition and over-complication
- Foundation for a SaaS business model
- Mix of open-source and proprietary components

## Project Structure

The repository is organized as a Python monorepo with the following structure:

```
verbalstream-odoo-ai/
├── vs_core/                 # Core functionality and shared components
├── vs_llm/                  # Base LLM integration module
├── vs_llm_openai/           # OpenAI provider integration
├── vs_llm_anthropic/        # Anthropic/Claude provider integration
├── vs_llm_deepseek/         # DeepSeek provider integration
├── vs_knowledge/            # Knowledge management and RAG
├── vs_assistant/            # AI assistant framework
└── vs_tools/                # Tool integration for Odoo actions
```

## Development

### Prerequisites

- Python 3.10+
- Odoo 16.0+
- PostgreSQL 12+

### Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## License

This project contains both open-source and proprietary components. See individual module directories for specific licensing information.

## About VerbalStream

VerbalStream is a company specializing in AI and consultancy, with expertise in development and quality assurance for intelligent systems.
