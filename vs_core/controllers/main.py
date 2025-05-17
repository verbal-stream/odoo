from odoo import http
from odoo.http import request


class VSCoreController(http.Controller):
    """Controller for VerbalStream Core module."""

    @http.route("/vs/health", type="http", auth="public", csrf=False)
    def health_check(self):
        """Simple health check endpoint."""
        return {"status": "ok", "message": "VerbalStream Core is running"}
