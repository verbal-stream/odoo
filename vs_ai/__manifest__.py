{
    "name": "VerbalStream AI",
    "summary": """
        Seamlessly integrate AI capabilities into your Odoo system with support for OpenAI, Anthropic, Mistral and more
    """,
    "description": """
        VerbalStream AI brings the power of artificial intelligence to your Odoo system with an 
        intuitive, user-friendly interface. This module serves as the foundation for all AI 
        capabilities in your Odoo environment.
        
        Key Features:
        - Connect to multiple AI providers (OpenAI, Anthropic, etc.)
        - Simple configuration with guided setup
        - Secure API key management
        - Intelligent model selection and management
        - Unified interface for all AI operations
        - Comprehensive documentation and examples
        
        This module provides core functionality for:
        - Chat completions and conversations
        - Text embeddings and vector operations
        - Function calling and tool integration
        - Model management and configuration
    """,
    "author": "VerbalStream",
    "website": "https://verbalstream.com",
    "category": "Productivity/Artificial Intelligence",
    "version": "16.0.1.0.0",
    "depends": ["mail", "web"],
    'data': [
        'security/vs_ai_security.xml',
        'security/ir.model.access.csv',
        'views/vs_ai_menu_views.xml',
        'views/vs_ai_provider_views.xml',
        'views/vs_ai_model_views.xml',
        'wizards/vs_ai_setup_wizard_views.xml',
    ],
    "demo": [
        "data/vs_ai_demo_data.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "vs_ai/static/src/js/vs_ai_widget.js",
            "vs_ai/static/src/css/vs_ai_style.css",
        ],
    },
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False,
    "images": [
        "static/description/banner.png",
    ],
}
