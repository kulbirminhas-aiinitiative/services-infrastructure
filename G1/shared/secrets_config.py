#!/usr/bin/env python3
"""
Secrets Configuration Module for OOM Microservices
Compatible interface for service configuration with hybrid secrets management
"""

import os
import asyncio
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

# Try to import the shared secrets client
try:
    from services.shared.secrets_client import get_service_config as async_get_service_config, ServiceConfig
    ASYNC_SECRETS_AVAILABLE = True
except ImportError:
    ASYNC_SECRETS_AVAILABLE = False
    
logger = logging.getLogger(__name__)

@dataclass
class SimpleServiceConfig:
    """Simple service configuration for synchronous access"""
    service_name: str
    port: int
    database_url: str
    redis_url: str
    jwt_secret: str
    api_key: str
    openai_api_key: str
    anthropic_api_key: str
    
    def get_port(self) -> int:
        return self.port
    
    def get_database_url(self) -> str:
        return self.database_url
    
    def get_redis_url(self) -> str:
        return self.redis_url
    
    def get_jwt_secret(self) -> str:
        return self.jwt_secret
    
    def get_api_key(self) -> str:
        return self.api_key
    
    def get_openai_api_key(self) -> str:
        return self.openai_api_key
    
    def get_anthropic_api_key(self) -> str:
        return self.anthropic_api_key

def get_service_config(service_name: str) -> SimpleServiceConfig:
    """
    Get service configuration using hybrid approach
    1. Try async secrets management if available
    2. Fallback to environment variables
    """
    
    # For microservices, we'll use synchronous environment variable fallback
    # since the async secrets client requires more complex initialization
    
    # Port allocation based on service name and current registrations
    port_map = {
        'ai-manager': 8002,
        'rag-engine': 8003, 
        'personas-service': 4025,
        'secrets-api': 4020,
        'port-management': 8080,
        'database-service': 5432,
        'queue-manager': 8004,
        'ethics-engine': 4002,
    }
    
    default_port = port_map.get(service_name, 8000)
    
    # Get configuration from environment with service-specific overrides
    config = SimpleServiceConfig(
        service_name=service_name,
        port=int(os.getenv('PORT', os.getenv(f'{service_name.upper()}_PORT', default_port))),
        database_url=os.getenv('DATABASE_URL', f'sqlite:///./{service_name}.db'),
        redis_url=os.getenv('REDIS_URL', 'redis://localhost:6379'),
        jwt_secret=os.getenv('JWT_SECRET', f'{service_name}-jwt-secret-dev'),
        api_key=os.getenv('API_KEY', f'{service_name}-api-key-dev'),
        openai_api_key=os.getenv('OPENAI_API_KEY', ''),
        anthropic_api_key=os.getenv('ANTHROPIC_API_KEY', ''),
    )
    
    logger.info(f"Configuration loaded for {service_name} on port {config.port}")
    
    return config

async def get_service_config_async(service_name: str) -> SimpleServiceConfig:
    """
    Async version that tries secrets management API first
    """
    
    if ASYNC_SECRETS_AVAILABLE:
        try:
            # Try async secrets client
            async_config = await async_get_service_config(service_name)
            
            # Convert to SimpleServiceConfig
            return SimpleServiceConfig(
                service_name=service_name,
                port=async_config.port,
                database_url=async_config.database_config.get('postgres_url', f'sqlite:///./{service_name}.db'),
                redis_url=async_config.database_config.get('redis_url', 'redis://localhost:6379'),
                jwt_secret=async_config.api_keys.get('jwt_secret', f'{service_name}-jwt-secret-dev'),
                api_key=async_config.api_keys.get('api_key', f'{service_name}-api-key-dev'),
                openai_api_key=async_config.api_keys.get('openai', ''),
                anthropic_api_key=async_config.api_keys.get('anthropic', ''),
            )
        except Exception as e:
            logger.warning(f"Async secrets management failed, using fallback: {e}")
    
    # Fallback to synchronous method
    return get_service_config(service_name)

# Backward compatibility aliases
def get_config(service_name: str) -> SimpleServiceConfig:
    """Alias for backward compatibility"""
    return get_service_config(service_name)
