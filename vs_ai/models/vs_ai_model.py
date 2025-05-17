from odoo import api, fields, models, _
from odoo.exceptions import UserError


class VSAIModel(models.Model):
    """
    AI Model
    
    This model represents a specific AI model from a provider, such as GPT-4 from OpenAI
    or Claude 3 Opus from Anthropic. It stores model capabilities and configuration.
    """
    _name = "vs.ai.model"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "AI Model"
    _order = "provider_id, sequence, name"
    
    name = fields.Char(
        string="Name",
        required=True,
        tracking=True,
        help="Name of the AI model (e.g., 'gpt-4', 'claude-3-opus')"
    )
    
    display_name = fields.Char(
        string="Display Name",
        compute="_compute_display_name",
        store=True,
        help="User-friendly display name for the model"
    )
    
    provider_id = fields.Many2one(
        'vs.ai.provider',
        string="Provider",
        required=True,
        ondelete='cascade',
        tracking=True,
        help="The AI provider this model belongs to"
    )
    
    provider_type = fields.Selection(
        related="provider_id.provider_type",
        string="Provider Type",
        store=True,
        help="Type of AI provider"
    )
    
    model_type = fields.Selection(
        selection=[
            ('chat', 'Chat Completion'),
            ('completion', 'Text Completion'),
            ('embedding', 'Embedding'),
            ('image', 'Image Generation'),
            ('multimodal', 'Multimodal'),
        ],
        string="Model Type",
        required=True,
        default='chat',
        tracking=True,
        help="The primary capability of this model"
    )
    
    description = fields.Text(
        string="Description",
        help="Description of the model's capabilities"
    )
    
    active = fields.Boolean(
        default=True,
        tracking=True,
        help="Whether this model is active and available for use"
    )
    
    company_id = fields.Many2one(
        'res.company',
        related="provider_id.company_id",
        string="Company",
        store=True,
        help="Company this model belongs to"
    )
    
    # Model capabilities
    supports_tools = fields.Boolean(
        string="Supports Tools",
        default=False,
        help="Whether this model supports function/tool calling"
    )
    
    supports_vision = fields.Boolean(
        string="Supports Vision",
        default=False,
        help="Whether this model can process images"
    )
    
    supports_streaming = fields.Boolean(
        string="Supports Streaming",
        default=True,
        help="Whether this model supports streaming responses"
    )
    
    max_tokens = fields.Integer(
        string="Max Tokens",
        default=4096,
        help="Maximum number of tokens this model can process in a single request"
    )
    
    # Usage settings
    is_default = fields.Boolean(
        string="Default Model",
        default=False,
        tracking=True,
        help="Whether this is the default model for its type"
    )
    
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Sequence for ordering models"
    )
    
    # Technical fields
    model_id = fields.Char(
        string="Model ID",
        help="Internal ID used by the provider API"
    )
    
    config = fields.Json(
        string="Configuration",
        default={},
        help="Additional configuration for this model"
    )
    
    # UI helpers
    color = fields.Integer(string="Color Index", default=0)
    
    @api.depends('name', 'provider_id.name')
    def _compute_display_name(self):
        """Compute a user-friendly display name for the model"""
        for model in self:
            if model.provider_id:
                model.display_name = f"{model.name} ({model.provider_id.name})"
            else:
                model.display_name = model.name
    
    @api.constrains('is_default')
    def _check_default_model(self):
        """Ensure only one default model per type per provider"""
        for model in self.filtered(lambda m: m.is_default):
            domain = [
                ('id', '!=', model.id),
                ('provider_id', '=', model.provider_id.id),
                ('model_type', '=', model.model_type),
                ('is_default', '=', True),
            ]
            if self.search_count(domain):
                # If another default exists, unset it
                other_defaults = self.search(domain)
                other_defaults.write({'is_default': False})
    
    def action_make_default(self):
        """Set this model as the default for its type"""
        self.ensure_one()
        self.is_default = True
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Default Model"),
                'message': _("%s is now the default %s model for %s", 
                            self.name, self.model_type, self.provider_id.name),
                'sticky': False,
                'type': 'success',
            }
        }
    
    def action_test_model(self):
        """Test the model with a simple prompt"""
        self.ensure_one()
        
        try:
            if self.model_type == 'chat':
                messages = [{"role": "user", "content": "Hello, please respond with a short greeting."}]
                response = self.provider_id.generate_chat_completion(messages, model=self)
                message = _("Model response: %s", response.get('content', 'No response'))
            elif self.model_type == 'completion':
                prompt = "Complete this sentence: The quick brown fox"
                response = self.provider_id.generate_completion(prompt, model=self)
                message = _("Model response: %s", response)
            elif self.model_type == 'embedding':
                texts = ["Test embedding generation"]
                response = self.provider_id.generate_embeddings(texts, model=self)
                message = _("Embedding generated with %d dimensions", len(response[0]))
            else:
                raise UserError(_("Testing not implemented for this model type"))
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Model Test"),
                    'message': message,
                    'sticky': False,
                    'type': 'success',
                }
            }
            
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Model Test Failed"),
                    'message': str(e),
                    'sticky': True,
                    'type': 'danger',
                }
            }
    
    # Core AI functionality methods
    def generate_completion(self, prompt, **kwargs):
        """Generate a text completion using this model"""
        if self.model_type not in ['completion', 'chat']:
            raise UserError(_("This model does not support text completion"))
        
        return self.provider_id.generate_completion(prompt, model=self, **kwargs)
    
    def generate_chat_completion(self, messages, stream=False, **kwargs):
        """Generate a chat completion using this model"""
        if self.model_type not in ['chat', 'multimodal']:
            raise UserError(_("This model does not support chat completion"))
        
        return self.provider_id.generate_chat_completion(messages, model=self, stream=stream, **kwargs)
    
    def generate_embeddings(self, texts, **kwargs):
        """Generate embeddings for the given texts"""
        if self.model_type != 'embedding':
            raise UserError(_("This model does not support embedding generation"))
        
        return self.provider_id.generate_embeddings(texts, model=self, **kwargs)
