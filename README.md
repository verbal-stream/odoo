# VerbalStream AI for Odoo

A comprehensive, user-friendly AI module for Odoo, developed by VerbalStream - experts in AI integration and business solutions.

## Overview

This repository contains an Odoo module that integrates AI capabilities into the Odoo ERP system using Pydantic AI for unified provider access. The module is designed to be:

- User-friendly while being technically sophisticated
- Feature-rich with extensive configuration options
- Optimized for performance and maintainability
- Foundation for a SaaS business model
- Leveraging the power of Pydantic AI for provider-agnostic integration

## Key Features

- **Unified AI Provider Management**: Connect to multiple AI providers through a single interface powered by Pydantic AI
- **LLM-Agnostic Architecture**: Support for OpenAI, Anthropic, Mistral, DeepSeek, Ollama, OpenRouter, and more
- **Model Management**: Easily configure and use different AI models for various tasks
- **User-Friendly Setup**: Guided setup wizards for configuring providers and models
- **API Integration**: RESTful API endpoints for AI capabilities
- **Security**: Role-based access control for AI features

## Project Structure

The repository is organized with the following structure:

```
odoo/
├── vs_core/                 # Core functionality and shared components
├── vs_ai/                   # AI integration module
├── vs_ai_knowledge/         # Knowledge management and RAG (planned)
├── vs_ai_assistant/         # AI assistant framework (planned)
└── vs_ai_tools/             # Tool integration for Odoo actions (planned)
```

## Installation

### Prerequisites

- Python 3.10+
- Odoo 16.0+
- PostgreSQL 12+

### Setup

1. Clone the repository
   ```bash
   git clone https://github.com/verbalstream/odoo.git
   cd odoo
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add the modules to your Odoo addons path or symlink them to your existing Odoo installation

5. Install the modules through the Odoo Apps menu or using the `-i` flag when starting Odoo
   ```bash
   ./odoo-bin -i vs_core,vs_ai
   ```

## Usage

### Setting Up AI Providers

1. Navigate to the AI menu in Odoo
2. Use the Setup Wizard to configure your AI providers
3. Enter your API keys for the providers you want to use
4. The wizard will automatically fetch available models

### Using AI Features

- **Chat Completions**: Use the API endpoints or the UI to generate text completions
- **Embeddings**: Generate vector embeddings for text to use in semantic search
- **Model Management**: Configure which models to use for different tasks

### API Integration

The module provides RESTful API endpoints for integration with other systems:

- `/api/v1/vs_ai/health` - Check the health of the AI service
- `/api/v1/vs_ai/providers` - List available providers
- `/api/v1/vs_ai/chat/completions` - Generate chat completions
- `/api/v1/vs_ai/embeddings` - Generate embeddings

## Roadmap

- **Pydantic AI Integration**: Implement a unified provider interface using Pydantic AI
- **Structured Output Models**: Create Pydantic models for common business use cases
- **Vector Database Integration**: Add support for pgvector, Chroma, and Qdrant
- **RAG Framework**: Build a retrieval-augmented generation system for Odoo documents
- **Function Calling**: Enable AI models to call Odoo functions and actions
- **Multi-modal Support**: Add capabilities for image and audio processing
- **Fine-tuning Interface**: Provide tools for fine-tuning models on business data

## License

This project contains both open-source and proprietary components. See individual module directories for specific licensing information.

## About VerbalStream

VerbalStream is a company specializing in AI integration and business solutions, with expertise in development and quality assurance for intelligent systems.
