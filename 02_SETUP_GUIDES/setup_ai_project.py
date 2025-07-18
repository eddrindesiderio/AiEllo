#!/usr/bin/env python3
"""
AI-Assisted AI Project Setup Script
This script helps you set up your personal AI development environment
using AI tools to build AI systems.
"""

import os
import sys
import subprocess
import json

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                  🤖 AI Building AI Setup 🤖                  ║
    ║              Use AI Tools to Create Your Own AI              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print("✅ Python version:", sys.version.split()[0])
    return True

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    
    packages = [
        "openai",           # OpenAI API
        "transformers",     # Hugging Face models
        "torch",           # PyTorch for ML
        "streamlit",       # Web interface
        "langchain",       # LLM framework
        "requests",        # HTTP requests
        "python-dotenv",   # Environment variables
        "gradio",          # Quick UI creation
        "anthropic",       # Claude API
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")

def create_config_file():
    """Create configuration file"""
    print("\n⚙️ Creating configuration...")
    
    config = {
        "openai_api_key": "your-openai-api-key-here",
        "anthropic_api_key": "your-anthropic-api-key-here",
        "model_settings": {
            "default_model": "gpt-3.5-turbo",
            "max_tokens": 1000,
            "temperature": 0.7
        },
        "local_models": {
            "enabled": True,
            "model_name": "microsoft/DialoGPT-medium",
            "cache_dir": "./models"
        }
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created config.json")

def create_env_file():
    """Create .env file for API keys"""
    env_content = """# AI API Keys - Replace with your actual keys
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
HUGGINGFACE_API_KEY=your-huggingface-api-key-here

# Optional: For advanced features
PINECONE_API_KEY=your-pinecone-api-key-here
GOOGLE_API_KEY=your-google-api-key-here
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ Created .env file")

def create_directory_structure():
    """Create project directories"""
    print("\n📁 Creating project structure...")
    
    directories = [
        "examples",
        "deployment",
        "models",
        "data",
        "logs",
        "tests"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}/ directory")

def show_next_steps():
    """Display next steps for the user"""
    print("""
    🎉 Setup Complete! Here's what you can do next:
    
    🟢 BEGINNER PATH (Start here!):
    1. Get an OpenAI API key: https://platform.openai.com/api-keys
    2. Add your API key to .env file
    3. Run: python simple_ai_chat.py
    
    🟡 INTERMEDIATE PATH:
    1. Run: python local_ai_setup.py
    2. This uses free local models (no API key needed)
    
    🔴 ADVANCED PATH:
    1. Check out fine_tuning_guide.md
    2. Explore custom model training
    
    💡 QUICK START:
    - Run: streamlit run deployment/streamlit_app.py
    - This creates a web interface for your AI
    
    📚 LEARN MORE:
    - Read the examples/ directory
    - Check deployment/ for different interfaces
    - Use AI tools like ChatGPT to help you code!
    
    Remember: You can ask AI (ChatGPT, Claude, etc.) to help you 
    modify and improve any of this code! 🤖✨
    """)

def main():
    print_banner()
    
    if not check_python_version():
        return
    
    print("🚀 Setting up your AI-assisted AI development environment...")
    
    install_dependencies()
    create_config_file()
    create_env_file()
    create_directory_structure()
    
    show_next_steps()

if __name__ == "__main__":
    main()
