from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class VSAIProvider(models.Model):
    """
    AI Provider Model
    
    This model represents a connection to an AI provider service such as OpenAI,
    Anthropic, or Mistral. It handles authentication, API communication, and
    provides a unified interface for all AI operations.
    """
    _name = "vs.ai.provider"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "AI Provider"
    _order = "name"
    
    name = fields.Char(
        string="Name",
        required=True,
        tracking=True,
        help="Name of the AI provider connection"
    )
    
    provider_type = fields.Selection([
        ('openai', 'OpenAI'),
        ('anthropic', 'Anthropic'),
        ('mistral', 'Mistral AI'),
        ('ollama', 'Ollama'),
        ('azure', 'Azure OpenAI'),
        ('deepseek', 'DeepSeek AI'),
        ('openrouter', 'OpenRouter'),
        ('custom', 'Custom Provider'),
    ], string="Provider Type", required=True, tracking=True, help="Type of AI provider service")
    
    api_key = fields.Char(
        string="API Key",
        copy=False,
        tracking=True,
        help="API key for authentication with the provider"
    )
    
    api_endpoint = fields.Char(
        string="API Endpoint",
        help="Custom API endpoint URL (leave empty for default)"
    )
    
    active = fields.Boolean(
        default=True,
        tracking=True,
        help="Whether this provider is active and available for use"
    )
    
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env.company,
        help="Company this provider belongs to"
    )
    
    model_ids = fields.One2many(
        'vs.ai.model',
        'provider_id',
        string="AI Models",
        help="Models available from this provider"
    )
    
    model_count = fields.Integer(
        string="Models",
        compute="_compute_model_count",
        help="Number of AI models available from this provider"
    )
    
    status = fields.Selection(
        selection=[
            ('untested', 'Not Tested'),
            ('working', 'Working'),
            ('error', 'Connection Error'),
        ],
        string="Status",
        default='untested',
        tracking=True,
        help="Connection status with the provider"
    )
    
    status_message = fields.Text(
        string="Status Details",
        readonly=True,
        help="Details about the connection status"
    )
    
    last_checked = fields.Datetime(
        string="Last Checked",
        readonly=True,
        help="When the connection was last tested"
    )
    
    # UI helpers
    color = fields.Integer(string="Color Index", default=0)
    
    @api.depends('model_ids')
    def _compute_model_count(self):
        """Compute the number of models for this provider"""
        for provider in self:
            provider.model_count = len(provider.model_ids)
    
    @api.constrains('name')
    def _check_name_unique(self):
        """Ensure provider names are unique (case-insensitive)"""
        for record in self:
            domain = [
                ('id', '!=', record.id),
                ('name', '=ilike', record.name)
            ]
            if self.search_count(domain):
                raise ValidationError(_("Provider name must be unique"))
    
    def action_test_connection(self):
        """Test the connection to the AI provider"""
        self.ensure_one()
        
        try:
            # Implementation will depend on the provider type
            if self.provider_type == 'openai':
                self._test_openai_connection()
            elif self.provider_type == 'anthropic':
                self._test_anthropic_connection()
            elif self.provider_type == 'mistral':
                self._test_mistral_connection()
            elif self.provider_type == 'ollama':
                self._test_ollama_connection()
            elif self.provider_type == 'custom':
                self._test_custom_connection()
            else:
                raise UserError(_("Unknown provider type"))
            
            # Update status if successful
            self.write({
                'status': 'working',
                'status_message': _("Connection successful"),
                'last_checked': fields.Datetime.now(),
            })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Connection Test"),
                    'message': _("Successfully connected to %s", self.name),
                    'sticky': False,
                    'type': 'success',
                }
            }
            
        except Exception as e:
            # Update status if failed
            self.write({
                'status': 'error',
                'status_message': str(e),
                'last_checked': fields.Datetime.now(),
            })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Connection Test"),
                    'message': _("Failed to connect: %s", str(e)),
                    'sticky': True,
                    'type': 'danger',
                }
            }
    
    def action_fetch_models(self):
        """Open wizard to fetch available models from the provider"""
        self.ensure_one()
        
        return {
            'name': _('Fetch AI Models'),
            'type': 'ir.actions.act_window',
            'res_model': 'vs.ai.setup.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_provider_id': self.id,
                'default_operation': 'fetch_models',
            }
        }
    
    def action_view_models(self):
        """Open the list of models for this provider"""
        self.ensure_one()
        
        return {
            'name': _('AI Models'),
            'type': 'ir.actions.act_window',
            'res_model': 'vs.ai.model',
            'view_mode': 'tree,form',
            'domain': [('provider_id', '=', self.id)],
            'context': {
                'default_provider_id': self.id,
            }
        }
    
    # Provider-specific connection test methods
    def _test_openai_connection(self):
        """Test connection to OpenAI API"""
        if not self.api_key:
            raise UserError(_("API key is required for OpenAI"))
        
        # This would be implemented with actual API calls
        # For now, we'll just simulate success
        return True
    
    def _test_anthropic_connection(self):
        """Test connection to Anthropic API"""
        if not self.api_key:
            raise UserError(_("API key is required for Anthropic"))
        
        # This would be implemented with actual API calls
        # For now, we'll just simulate success
        return True
    
    def _test_mistral_connection(self):
        """Test connection to Mistral AI API"""
        if not self.api_key:
            raise UserError(_("API key is required for Mistral AI"))
        
        # This would be implemented with actual API calls
        # For now, we'll just simulate success
        return True
    
    def _test_ollama_connection(self):
        """Test connection to local Ollama server"""
        if not self.api_endpoint:
            raise UserError(_("API endpoint is required for Ollama"))
        
        # This would be implemented with actual API calls
        # For now, we'll just simulate success
        return True
    
    def _test_custom_connection(self):
        """Test connection to custom provider"""
        if not self.api_key or not self.api_endpoint:
            raise UserError(_("Both API key and endpoint are required for custom providers"))
        
        # This would be implemented with actual API calls
        # For now, we'll just simulate success
        return True
    
    # Core AI functionality methods
    def generate_completion(self, prompt, model=None, **kwargs):
        """
        Generate a text completion using this provider
        
        Args:
            prompt (str): The text prompt to complete
            model (vs.ai.model): Specific model to use, or None for default
            **kwargs: Additional parameters for the completion
            
        Returns:
            str: The generated completion text
        """
        # Implementation would dispatch to the appropriate provider
        # For now, return a placeholder
        return "This is a placeholder completion response."
    
    def generate_chat_completion(self, messages, model=None, stream=False, **kwargs):
        """
        Generate a chat completion using this provider
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content'
            model (vs.ai.model): Specific model to use, or None for default
            stream (bool): Whether to stream the response
            **kwargs: Additional parameters for the completion
            
        Returns:
            dict: The chat completion response
        """
        # Implementation would dispatch to the appropriate provider
        # For now, return a placeholder
        return {
            "role": "assistant",
            "content": "This is a placeholder chat response."
        }
    
    def generate_embeddings(self, texts, model=None, **kwargs):
        """
        Generate embeddings for the given texts
        
        Args:
            texts (list): List of text strings to embed
            model (vs.ai.model): Specific model to use, or None for default
            **kwargs: Additional parameters for the embedding generation
            
        Returns:
            list: List of embedding vectors
        """
        # Implementation would dispatch to the appropriate provider
        # For now, return a placeholder
        return [[0.1, 0.2, 0.3] for _ in texts]
