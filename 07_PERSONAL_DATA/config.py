#!/usr/bin/env python3
"""
Configuration Settings for Personal AI Project
This file contains all the configuration settings for your AI systems.

You can modify these settings to customize your AI's behavior,
performance, and capabilities.
"""

import os
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIConfig:
    """Main configuration class for AI settings"""
    
    # API Keys and Authentication
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', 'your-anthropic-api-key-here')
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', 'your-huggingface-api-key-here')
    
    # Model Settings
    DEFAULT_MODEL = "gpt-3.5-turbo"
    FALLBACK_MODEL = "gpt-3.5-turbo"
    LOCAL_MODEL = "microsoft/DialoGPT-medium"
    
    # Generation Parameters
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    TOP_P = 1.0
    FREQUENCY_PENALTY = 0.0
    PRESENCE_PENALTY = 0.0
    
    # Local AI Settings
    LOCAL_AI_ENABLED = True
    MODEL_CACHE_DIR = "./models"
    USE_GPU = True  # Set to False if you don't have a GPU
    
    # Memory and Context
    MAX_CONVERSATION_HISTORY = 20
    CONTEXT_WINDOW_SIZE = 4000
    MEMORY_PERSISTENCE = True
    
    # File Paths
    LOGS_DIR = "./logs"
    DATA_DIR = "./data"
    MODELS_DIR = "./models"
    CONVERSATIONS_DIR = "./logs/conversations"
    
    # Web Interface Settings
    STREAMLIT_PORT = 8501
    GRADIO_PORT = 7860
    API_PORT = 8000
    
    # Agent Settings
    AGENT_MAX_ITERATIONS = 10
    AGENT_TIMEOUT = 300  # seconds
    AGENT_REFLECTION_ENABLED = True

class PersonalityProfiles:
    """Pre-defined AI personality profiles"""
    
    HELPFUL_ASSISTANT = {
        "name": "Alex",
        "role": "Helpful Assistant",
        "system_prompt": """You are Alex, a helpful and friendly AI assistant. You are:
        - Always polite and encouraging
        - Great at explaining things clearly
        - Patient with questions and learning
        - Supportive of the user's goals
        
        Your goal is to be as helpful as possible while being honest about your limitations.""",
        "temperature": 0.7,
        "traits": ["helpful", "friendly", "patient", "encouraging"]
    }
    
    TECH_EXPERT = {
        "name": "TechBot",
        "role": "Technology Expert",
        "system_prompt": """You are TechBot, a knowledgeable technology expert. You are:
        - Highly knowledgeable about programming, AI, and technology
        - Able to explain complex technical concepts clearly
        - Up-to-date with latest tech trends and best practices
        - Practical and solution-oriented
        
        You help users with technical problems and learning about technology.""",
        "temperature": 0.5,
        "traits": ["technical", "knowledgeable", "practical", "precise"]
    }
    
    CREATIVE_PARTNER = {
        "name": "CreativeAI",
        "role": "Creative Partner",
        "system_prompt": """You are CreativeAI, a creative and imaginative partner. You are:
        - Highly creative and imaginative
        - Great at brainstorming and ideation
        - Encouraging of creative expression
        - Able to think outside the box
        
        You help users explore creative ideas and solutions.""",
        "temperature": 0.9,
        "traits": ["creative", "imaginative", "inspiring", "innovative"]
    }
    
    CODE_MENTOR = {
        "name": "CodeMentor",
        "role": "Programming Mentor",
        "system_prompt": """You are CodeMentor, a patient programming teacher. You are:
        - Excellent at teaching programming concepts
        - Patient with beginners and encouraging
        - Able to provide clear code examples
        - Focused on best practices and clean code
        
        You help users learn programming and improve their coding skills.""",
        "temperature": 0.6,
        "traits": ["educational", "patient", "thorough", "encouraging"]
    }
    
    @classmethod
    def get_all_profiles(cls) -> Dict[str, Dict[str, Any]]:
        """Get all available personality profiles"""
        return {
            "Helpful Assistant": cls.HELPFUL_ASSISTANT,
            "Tech Expert": cls.TECH_EXPERT,
            "Creative Partner": cls.CREATIVE_PARTNER,
            "Code Mentor": cls.CODE_MENTOR
        }

class ModelConfigurations:
    """Configuration for different AI models"""
    
    OPENAI_MODELS = {
        "gpt-3.5-turbo": {
            "max_tokens": 4096,
            "cost_per_1k_tokens": 0.002,
            "speed": "fast",
            "capabilities": ["chat", "code", "analysis"]
        },
        "gpt-4": {
            "max_tokens": 8192,
            "cost_per_1k_tokens": 0.03,
            "speed": "medium",
            "capabilities": ["chat", "code", "analysis", "reasoning"]
        },
        "gpt-4-turbo-preview": {
            "max_tokens": 128000,
            "cost_per_1k_tokens": 0.01,
            "speed": "medium",
            "capabilities": ["chat", "code", "analysis", "reasoning", "long_context"]
        }
    }
    
    LOCAL_MODELS = {
        "microsoft/DialoGPT-medium": {
            "size": "medium",
            "memory_usage": "2GB",
            "speed": "fast",
            "capabilities": ["chat"]
        },
        "microsoft/DialoGPT-large": {
            "size": "large",
            "memory_usage": "4GB",
            "speed": "medium",
            "capabilities": ["chat"]
        },
        "facebook/blenderbot-400M-distill": {
            "size": "small",
            "memory_usage": "1GB",
            "speed": "very_fast",
            "capabilities": ["chat"]
        }
    }

class FeatureFlags:
    """Feature flags to enable/disable functionality"""
    
    # Core Features
    ENABLE_CHAT = True
    ENABLE_LOCAL_AI = True
    ENABLE_WEB_INTERFACE = True
    ENABLE_API_SERVER = True
    
    # Advanced Features
    ENABLE_AGENTS = True
    ENABLE_MEMORY_PERSISTENCE = True
    ENABLE_CONVERSATION_EXPORT = True
    ENABLE_VOICE_INPUT = False  # Requires additional setup
    ENABLE_IMAGE_PROCESSING = False  # Requires additional setup
    
    # Experimental Features
    ENABLE_AUTO_IMPROVEMENT = False
    ENABLE_MULTI_AGENT_COLLABORATION = False
    ENABLE_CUSTOM_TRAINING = False

class SecuritySettings:
    """Security and safety settings"""
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE = 60
    MAX_REQUESTS_PER_HOUR = 1000
    
    # Content Filtering
    ENABLE_CONTENT_FILTER = True
    BLOCKED_TOPICS = [
        "harmful_content",
        "illegal_activities",
        "personal_information_extraction"
    ]
    
    # API Security
    REQUIRE_API_KEY = False  # Set to True for production
    ALLOWED_ORIGINS = ["localhost", "127.0.0.1"]
    
    # Data Privacy
    LOG_CONVERSATIONS = True
    ANONYMIZE_LOGS = False
    AUTO_DELETE_LOGS_DAYS = 30

def get_config() -> AIConfig:
    """Get the main configuration object"""
    return AIConfig()

def get_personality(name: str) -> Dict[str, Any]:
    """Get a specific personality profile"""
    profiles = PersonalityProfiles.get_all_profiles()
    return profiles.get(name, PersonalityProfiles.HELPFUL_ASSISTANT)

def get_model_config(model_name: str) -> Dict[str, Any]:
    """Get configuration for a specific model"""
    all_models = {**ModelConfigurations.OPENAI_MODELS, **ModelConfigurations.LOCAL_MODELS}
    return all_models.get(model_name, {})

def validate_config() -> List[str]:
    """Validate configuration and return any issues"""
    issues = []
    
    # Check API keys
    if AIConfig.OPENAI_API_KEY == 'your-openai-api-key-here':
        issues.append("OpenAI API key not configured")
    
    # Check directories
    import os
    for directory in [AIConfig.LOGS_DIR, AIConfig.DATA_DIR, AIConfig.MODELS_DIR]:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                issues.append(f"Cannot create directory {directory}: {e}")
    
    # Check model availability
    if FeatureFlags.ENABLE_LOCAL_AI:
        try:
            import torch
            import transformers
        except ImportError:
            issues.append("Local AI enabled but required packages not installed")
    
    return issues

def print_config_summary():
    """Print a summary of the current configuration"""
    config = get_config()
    
    print("🔧 AI Configuration Summary")
    print("=" * 40)
    print(f"Default Model: {config.DEFAULT_MODEL}")
    print(f"Local AI: {'Enabled' if config.LOCAL_AI_ENABLED else 'Disabled'}")
    print(f"GPU Usage: {'Enabled' if config.USE_GPU else 'Disabled'}")
    print(f"Max Tokens: {config.MAX_TOKENS}")
    print(f"Temperature: {config.TEMPERATURE}")
    print(f"Conversation History: {config.MAX_CONVERSATION_HISTORY} messages")
    
    print(f"\n📁 Directories:")
    print(f"Logs: {config.LOGS_DIR}")
    print(f"Data: {config.DATA_DIR}")
    print(f"Models: {config.MODELS_DIR}")
    
    print(f"\n🌐 Ports:")
    print(f"Streamlit: {config.STREAMLIT_PORT}")
    print(f"API: {config.API_PORT}")
    
    # Check for issues
    issues = validate_config()
    if issues:
        print(f"\n⚠️  Configuration Issues:")
        for issue in issues:
            print(f"   • {issue}")
    else:
        print(f"\n✅ Configuration looks good!")

if __name__ == "__main__":
    print_config_summary()
