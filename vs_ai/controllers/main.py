from odoo import http
from odoo.http import request, Response
import json


class VSAIController(http.Controller):
    """
    Controller for VerbalStream AI module
    
    Provides API endpoints for interacting with AI features from external systems
    and handles streaming responses.
    """
    
    @http.route('/vs_ai/health', type='http', auth='public', csrf=False)
    def health_check(self):
        """Simple health check endpoint to verify the module is running"""
        return Response(
            json.dumps({"status": "ok", "module": "vs_ai"}),
            content_type='application/json'
        )
    
    @http.route('/vs_ai/providers', type='http', auth='user')
    def list_providers(self):
        """List available AI providers for the current user"""
        providers = request.env['vs.ai.provider'].search([('active', '=', True)])
        result = [{
            'id': provider.id,
            'name': provider.name,
            'provider_type': provider.provider_type,
            'status': provider.status,
            'model_count': provider.model_count,
        } for provider in providers]
        
        return Response(
            json.dumps({"providers": result}),
            content_type='application/json'
        )
    
    @http.route('/vs_ai/models', type='http', auth='user')
    def list_models(self, provider_id=None, model_type=None):
        """
        List available AI models
        
        Args:
            provider_id: Optional provider ID to filter by
            model_type: Optional model type to filter by
        """
        domain = [('active', '=', True)]
        
        if provider_id:
            domain.append(('provider_id', '=', int(provider_id)))
        
        if model_type:
            domain.append(('model_type', '=', model_type))
        
        models = request.env['vs.ai.model'].search(domain)
        result = [{
            'id': model.id,
            'name': model.name,
            'display_name': model.display_name,
            'provider_id': model.provider_id.id,
            'provider_name': model.provider_id.name,
            'model_type': model.model_type,
            'is_default': model.is_default,
        } for model in models]
        
        return Response(
            json.dumps({"models": result}),
            content_type='application/json'
        )
    
    @http.route('/vs_ai/chat', type='json', auth='user', csrf=False)
    def generate_chat_completion(self, messages, model_id=None, provider_id=None, stream=False, **kwargs):
        """
        Generate a chat completion
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model_id: Specific model ID to use
            provider_id: Provider ID to use (if model_id not specified)
            stream: Whether to stream the response
            **kwargs: Additional parameters for the completion
        """
        if not messages:
            return {"error": "No messages provided"}
        
        # Get the model to use
        model = None
        if model_id:
            model = request.env['vs.ai.model'].browse(int(model_id))
            if not model.exists() or not model.active:
                return {"error": "Model not found or inactive"}
        elif provider_id:
            provider = request.env['vs.ai.provider'].browse(int(provider_id))
            if not provider.exists() or not provider.active:
                return {"error": "Provider not found or inactive"}
            
            # Find default chat model for this provider
            model = request.env['vs.ai.model'].search([
                ('provider_id', '=', provider.id),
                ('model_type', '=', 'chat'),
                ('is_default', '=', True),
                ('active', '=', True),
            ], limit=1)
            
            if not model:
                # Fallback to any chat model from this provider
                model = request.env['vs.ai.model'].search([
                    ('provider_id', '=', provider.id),
                    ('model_type', '=', 'chat'),
                    ('active', '=', True),
                ], limit=1)
        
        if not model:
            # Fallback to any default chat model
            model = request.env['vs.ai.model'].search([
                ('model_type', '=', 'chat'),
                ('is_default', '=', True),
                ('active', '=', True),
            ], limit=1)
            
            if not model:
                return {"error": "No suitable model found"}
        
        try:
            # Generate the completion
            response = model.generate_chat_completion(messages, stream=stream, **kwargs)
            return {"response": response}
        except Exception as e:
            return {"error": str(e)}
    
    @http.route('/vs_ai/embed', type='json', auth='user', csrf=False)
    def generate_embeddings(self, texts, model_id=None, provider_id=None, **kwargs):
        """
        Generate embeddings for the given texts
        
        Args:
            texts: List of text strings to embed
            model_id: Specific model ID to use
            provider_id: Provider ID to use (if model_id not specified)
            **kwargs: Additional parameters for the embedding generation
        """
        if not texts:
            return {"error": "No texts provided"}
        
        # Get the model to use
        model = None
        if model_id:
            model = request.env['vs.ai.model'].browse(int(model_id))
            if not model.exists() or not model.active:
                return {"error": "Model not found or inactive"}
        elif provider_id:
            provider = request.env['vs.ai.provider'].browse(int(provider_id))
            if not provider.exists() or not provider.active:
                return {"error": "Provider not found or inactive"}
            
            # Find default embedding model for this provider
            model = request.env['vs.ai.model'].search([
                ('provider_id', '=', provider.id),
                ('model_type', '=', 'embedding'),
                ('is_default', '=', True),
                ('active', '=', True),
            ], limit=1)
            
            if not model:
                # Fallback to any embedding model from this provider
                model = request.env['vs.ai.model'].search([
                    ('provider_id', '=', provider.id),
                    ('model_type', '=', 'embedding'),
                    ('active', '=', True),
                ], limit=1)
        
        if not model:
            # Fallback to any default embedding model
            model = request.env['vs.ai.model'].search([
                ('model_type', '=', 'embedding'),
                ('is_default', '=', True),
                ('active', '=', True),
            ], limit=1)
            
            if not model:
                return {"error": "No suitable embedding model found"}
        
        try:
            # Generate the embeddings
            embeddings = model.generate_embeddings(texts, **kwargs)
            return {"embeddings": embeddings}
        except Exception as e:
            return {"error": str(e)}
