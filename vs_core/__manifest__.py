{
    "name": "VerbalStream Core",
    "summary": "Core module for VerbalStream AI integration with Odoo",
    "description": """
        This module provides the core functionality for VerbalStream's AI integration with Odoo.
        It serves as the foundation for all other VerbalStream modules.
    """,
    "author": "VerbalStream",
    "website": "https://verbalstream.com",
    "category": "AI/Core",
    "version": "16.0.1.0.0",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/vs_menu_views.xml",
        "views/vs_config_views.xml",
    ],
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
