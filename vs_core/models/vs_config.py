from odoo import api, fields, models


class VSConfig(models.Model):
    """Configuration settings for VerbalStream modules."""

    _name = "vs.config"
    _description = "VerbalStream Configuration"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(default=True)
    description = fields.Text(string="Description")
    
    # Company relation
    company_id = fields.Many2one(
        "res.company", 
        string="Company", 
        default=lambda self: self.env.company
    )
    
    # Configuration parameters
    debug_mode = fields.Boolean(
        string="Debug Mode", 
        default=False,
        help="Enable debug mode for additional logging"
    )
    
    log_level = fields.Selection(
        [
            ("error", "Error"),
            ("warning", "Warning"),
            ("info", "Info"),
            ("debug", "Debug"),
        ],
        string="Log Level",
        default="info",
        help="Set the logging level for VerbalStream modules"
    )
    
    @api.model
    def get_config(self, company=None):
        """Get configuration for the specified company or current company."""
        if not company:
            company = self.env.company
            
        config = self.search([
            ("company_id", "=", company.id),
            ("active", "=", True)
        ], limit=1)
        
        if not config:
            # Create default config if none exists
            config = self.create({
                "name": f"{company.name} Configuration",
                "company_id": company.id,
            })
            
        return config
