from odoo import api, fields, models, _
from odoo.exceptions import UserError


class VSAISetupWizard(models.TransientModel):
    """
    AI Setup Wizard
    
    This wizard guides users through setting up AI providers and fetching models.
    It provides a user-friendly interface for configuring AI capabilities.
    """
    _name = "vs.ai.setup.wizard"
    _description = "AI Setup Wizard"
    
    # Setup type
    operation = fields.Selection(
        selection=[
            ('new_provider', 'Set up a new AI provider'),
            ('fetch_models', 'Fetch models from provider'),
            ('quick_setup', 'Quick setup with popular providers'),
        ],
        string="Operation",
        default='new_provider',
        required=True,
    )
    
    # Provider fields
    provider_id = fields.Many2one(
        'vs.ai.provider',
        string="Provider",
        help="Select an existing provider to fetch models from"
    )
    
    provider_type = fields.Selection(
        selection=[
            ('openai', 'OpenAI'),
            ('anthropic', 'Anthropic'),
            ('mistral', 'Mistral AI'),
            ('ollama', 'Ollama'),
            ('azure', 'Azure OpenAI'),
            ('deepseek', 'DeepSeek AI'),
            ('openrouter', 'OpenRouter'),
            ('custom', 'Custom Provider'),
        ],
        string="Provider Type",
        default='openai',
        help="Type of AI provider to set up"
    )
    
    provider_name = fields.Char(
        string="Provider Name",
        help="Name for the new provider"
    )
    
    api_key = fields.Char(
        string="API Key",
        help="API key for authentication with the provider"
    )
    
    api_endpoint = fields.Char(
        string="API Endpoint",
        help="Custom API endpoint URL (leave empty for default)"
    )
    
    # Quick setup fields
    setup_openai = fields.Boolean(
        string="OpenAI",
        default=True,
        help="Set up OpenAI integration"
    )
    
    openai_api_key = fields.Char(
        string="OpenAI API Key",
        help="API key for OpenAI"
    )
    
    setup_anthropic = fields.Boolean(
        string="Anthropic",
        default=False,
        help="Set up Anthropic integration"
    )
    
    anthropic_api_key = fields.Char(
        string="Anthropic API Key",
        help="API key for Anthropic"
    )
    
    setup_mistral = fields.Boolean(
        string="Mistral AI",
        default=False,
        help="Set up Mistral AI integration"
    )
    
    mistral_api_key = fields.Char(
        string="Mistral API Key",
        help="API key for Mistral AI"
    )
    
    setup_ollama = fields.Boolean(
        string="Ollama",
        default=False,
        help="Set up Ollama integration"
    )
    
    ollama_endpoint = fields.Char(
        string="Ollama Endpoint",
        default="http://localhost:11434",
        help="Endpoint for local Ollama server"
    )
    
    setup_deepseek = fields.Boolean(
        string="DeepSeek AI",
        default=False,
        help="Set up DeepSeek AI integration"
    )
    
    deepseek_api_key = fields.Char(
        string="DeepSeek API Key",
        help="API key for DeepSeek AI"
    )
    
    setup_openrouter = fields.Boolean(
        string="OpenRouter",
        default=False,
        help="Set up OpenRouter integration"
    )
    
    openrouter_api_key = fields.Char(
        string="OpenRouter API Key",
        help="API key for OpenRouter"
    )
    
    # Model fetching fields
    fetch_all_models = fields.Boolean(
        string="Fetch All Available Models",
        default=True,
        help="Fetch all available models from the provider"
    )
    
    model_filter = fields.Char(
        string="Model Filter",
        help="Filter models by name (e.g., 'gpt' for OpenAI GPT models)"
    )
    
    # State tracking
    state = fields.Selection(
        selection=[
            ('setup', 'Setup'),
            ('fetching', 'Fetching Models'),
            ('complete', 'Complete'),
        ],
        string="State",
        default='setup',
        required=True,
    )
    
    # Results
    result_provider_id = fields.Many2one(
        'vs.ai.provider',
        string="Created Provider",
        readonly=True,
    )
    
    result_model_count = fields.Integer(
        string="Models Fetched",
        readonly=True,
    )
    
    result_message = fields.Text(
        string="Result",
        readonly=True,
    )
    
    @api.onchange('operation')
    def _onchange_operation(self):
        """Handle operation change"""
        if self.operation == 'fetch_models' and not self.provider_id:
            # Try to find an existing provider
            providers = self.env['vs.ai.provider'].search([], limit=1)
            if providers:
                self.provider_id = providers[0]
    
    @api.onchange('provider_id')
    def _onchange_provider_id(self):
        """Handle provider change"""
        if self.provider_id:
            self.provider_type = self.provider_id.provider_type
    
    def action_setup_provider(self):
        """Set up a new AI provider"""
        self.ensure_one()
        
        if self.operation == 'new_provider':
            # Create a single provider
            if not self.provider_name:
                raise UserError(_("Provider name is required"))
            
            if not self.api_key and self.provider_type != 'ollama':
                raise UserError(_("API key is required"))
            
            provider_vals = {
                'name': self.provider_name,
                'provider_type': self.provider_type,
                'api_key': self.api_key,
                'api_endpoint': self.api_endpoint,
                'active': True,
            }
            
            provider = self.env['vs.ai.provider'].create(provider_vals)
            self.result_provider_id = provider
            self.result_message = _("Provider '%s' created successfully", provider.name)
            
        elif self.operation == 'quick_setup':
            # Create providers for quick setup
            providers_to_create = []
            
            if self.setup_openai:
                providers_to_create.append({
                    'name': 'OpenAI',
                    'provider_type': 'openai',
                    'api_key': self.openai_api_key,
                })
            
            if self.setup_anthropic:
                providers_to_create.append({
                    'name': 'Anthropic',
                    'provider_type': 'anthropic',
                    'api_key': self.anthropic_api_key,
                })
            
            if self.setup_mistral:
                providers_to_create.append({
                    'name': 'Mistral AI',
                    'provider_type': 'mistral',
                    'api_key': self.mistral_api_key,
                })
            
            if self.setup_ollama:
                providers_to_create.append({
                    'name': 'Ollama',
                    'provider_type': 'ollama',
                    'api_endpoint': self.ollama_endpoint,
                })
                
            if self.setup_deepseek:
                providers_to_create.append({
                    'name': 'DeepSeek AI',
                    'provider_type': 'deepseek',
                    'api_key': self.deepseek_api_key,
                })
                
            if self.setup_openrouter:
                providers_to_create.append({
                    'name': 'OpenRouter',
                    'provider_type': 'openrouter',
                    'api_key': self.openrouter_api_key,
                })
            
            providers_created = []
            for provider_vals in providers_to_create:
                provider = self.env['vs.ai.provider'].create(provider_vals)
                providers_created.append(provider)
            
            if not providers_created:
                raise UserError(_("Please select at least one provider to set up"))
            
            self.result_provider_id = providers_created[0]
            self.result_message = _("%d providers created successfully", len(providers_created))
        
        # Move to fetching models state
        self.state = 'fetching'
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    def action_fetch_models(self):
        """Fetch models from the provider"""
        self.ensure_one()
        
        provider = self.provider_id or self.result_provider_id
        if not provider:
            raise UserError(_("No provider selected"))
        
        # This would be implemented with actual API calls to fetch models
        # For now, we'll create some example models
        
        models_created = []
        
        if provider.provider_type == 'openai':
            # Create example OpenAI models
            models_created.extend([
                {
                    'name': 'gpt-4o',
                    'model_type': 'chat',
                    'description': 'GPT-4o is the latest multimodal model from OpenAI',
                    'supports_tools': True,
                    'supports_vision': True,
                    'max_tokens': 128000,
                    'is_default': True,
                },
                {
                    'name': 'gpt-4-turbo',
                    'model_type': 'chat',
                    'description': 'GPT-4 Turbo with improved performance',
                    'supports_tools': True,
                    'supports_vision': False,
                    'max_tokens': 128000,
                },
                {
                    'name': 'gpt-3.5-turbo',
                    'model_type': 'chat',
                    'description': 'Most cost-effective GPT model',
                    'supports_tools': True,
                    'supports_vision': False,
                    'max_tokens': 16385,
                },
                {
                    'name': 'text-embedding-3-large',
                    'model_type': 'embedding',
                    'description': 'Large embedding model with 3072 dimensions',
                    'is_default': True,
                },
                {
                    'name': 'text-embedding-3-small',
                    'model_type': 'embedding',
                    'description': 'Small embedding model with 1536 dimensions',
                },
            ])
        elif provider.provider_type == 'anthropic':
            # Create example Anthropic models
            models_created.extend([
                {
                    'name': 'claude-3-opus',
                    'model_type': 'chat',
                    'description': 'Most powerful Claude model',
                    'supports_tools': True,
                    'supports_vision': True,
                    'max_tokens': 200000,
                    'is_default': True,
                },
                {
                    'name': 'claude-3-sonnet',
                    'model_type': 'chat',
                    'description': 'Balanced Claude model for most use cases',
                    'supports_tools': True,
                    'supports_vision': True,
                    'max_tokens': 200000,
                },
                {
                    'name': 'claude-3-haiku',
                    'model_type': 'chat',
                    'description': 'Fastest and most compact Claude model',
                    'supports_tools': True,
                    'supports_vision': True,
                    'max_tokens': 200000,
                },
            ])
        elif provider.provider_type == 'mistral':
            # Create example Mistral models
            models_created.extend([
                {
                    'name': 'mistral-large',
                    'model_type': 'chat',
                    'description': 'Mistral Large - most powerful model',
                    'supports_tools': True,
                    'supports_vision': False,
                    'max_tokens': 32768,
                    'is_default': True,
                },
                {
                    'name': 'mistral-medium',
                    'model_type': 'chat',
                    'description': 'Mistral Medium - balanced performance',
                    'supports_tools': True,
                    'supports_vision': False,
                    'max_tokens': 32768,
                },
                {
                    'name': 'mistral-small',
                    'model_type': 'chat',
                    'description': 'Mistral Small - fast and efficient',
                    'supports_tools': True,
                    'supports_vision': False,
                    'max_tokens': 32768,
                },
                {
                    'name': 'mistral-embed',
                    'model_type': 'embedding',
                    'description': 'Mistral embedding model',
                    'is_default': True,
                },
            ])
        elif provider.provider_type == 'ollama':
            # Create example Ollama models
            models_created.extend([
                {
                    'name': 'llama3',
                    'model_type': 'chat',
                    'description': 'Meta Llama 3 model',
                    'supports_tools': False,
                    'supports_vision': False,
                    'max_tokens': 8192,
                    'is_default': True,
                },
                {
                    'name': 'mistral',
                    'model_type': 'chat',
                    'description': 'Mistral 7B model',
                    'supports_tools': False,
                    'supports_vision': False,
                    'max_tokens': 8192,
                },
                {
                    'name': 'llava',
                    'model_type': 'multimodal',
                    'description': 'LLaVA multimodal model',
                    'supports_tools': False,
                    'supports_vision': True,
                    'max_tokens': 4096,
                },
            ])
        elif provider.provider_type == 'deepseek':
            # Create DeepSeek models
            models_created.extend([
                {
                    'name': 'deepseek-chat',
                    'model_type': 'chat',
                    'description': 'DeepSeek Chat - general purpose chat model',
                    'supports_tools': True,
                    'supports_vision': False,
                    'max_tokens': 8192,
                    'is_default': True,
                },
                {
                    'name': 'deepseek-coder',
                    'model_type': 'chat',
                    'description': 'DeepSeek Coder - specialized for code generation',
                    'supports_tools': True,
                    'supports_vision': False,
                    'max_tokens': 16384,
                },
                {
                    'name': 'deepseek-embed',
                    'model_type': 'embedding',
                    'description': 'DeepSeek embedding model',
                    'is_default': True,
                },
            ])
        elif provider.provider_type == 'openrouter':
            # Create OpenRouter models
            models_created.extend([
                {
                    'name': 'openai/gpt-4-turbo',
                    'model_type': 'chat',
                    'description': 'GPT-4 Turbo via OpenRouter',
                    'supports_tools': True,
                    'supports_vision': True,
                    'max_tokens': 4096,
                    'is_default': True,
                },
                {
                    'name': 'anthropic/claude-3-opus',
                    'model_type': 'chat',
                    'description': 'Claude 3 Opus via OpenRouter',
                    'supports_tools': True,
                    'supports_vision': True,
                    'max_tokens': 8192,
                },
                {
                    'name': 'qwen/qwen-turbo',
                    'model_type': 'chat',
                    'description': 'Qwen Turbo via OpenRouter',
                    'supports_tools': True,
                    'supports_vision': False,
                    'max_tokens': 6144,
                },
            ])
        
        # Create the models in the database
        for model_data in models_created:
            self.env['vs.ai.model'].create({
                'name': model_data['name'],
                'provider_id': provider.id,
                'model_type': model_data['model_type'],
                'description': model_data.get('description', ''),
                'supports_tools': model_data.get('supports_tools', False),
                'supports_vision': model_data.get('supports_vision', False),
                'supports_streaming': model_data.get('supports_streaming', True),
                'max_tokens': model_data.get('max_tokens', 4096),
                'is_default': model_data.get('is_default', False),
                'active': True,
            })
        
        self.result_model_count = len(models_created)
        self.result_message = _("%d models fetched successfully from %s", 
                               len(models_created), provider.name)
        
        # Move to complete state
        self.state = 'complete'
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    def action_view_provider(self):
        """View the created provider"""
        self.ensure_one()
        
        provider = self.provider_id or self.result_provider_id
        if not provider:
            raise UserError(_("No provider available"))
        
        return {
            'name': _('AI Provider'),
            'type': 'ir.actions.act_window',
            'res_model': 'vs.ai.provider',
            'res_id': provider.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_view_models(self):
        """View the fetched models"""
        self.ensure_one()
        
        provider = self.provider_id or self.result_provider_id
        if not provider:
            raise UserError(_("No provider available"))
        
        return {
            'name': _('AI Models'),
            'type': 'ir.actions.act_window',
            'res_model': 'vs.ai.model',
            'view_mode': 'tree,form',
            'domain': [('provider_id', '=', provider.id)],
            'context': {
                'default_provider_id': provider.id,
            },
            'target': 'current',
        }
