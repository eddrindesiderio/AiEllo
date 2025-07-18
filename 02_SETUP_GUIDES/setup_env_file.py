#!/usr/bin/env python3
"""
Setup .env file with your Discord bot token and Hugging Face API key
"""

import os

def setup_env_file():
    """Create or update .env file with the correct tokens"""
    
    print("🔧 Setting up your .env file...")
    
    # Your tokens
    discord_token = "MTM5NTM5MDk0MjY1OTM0NjU1NA.G07Vdg.HPNZ5_GW3KTw3t22D4euTy_0eCpRRRwe35KSoU"
    openai_api_key = "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"
    claude_api_key = "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"
    blackbox_api_key = "sk-BtiFdMb6OKw95pLEGknfhQ"
    
    # Create .env content
    env_content = f"""# Discord Bot Configuration
DISCORD_BOT_TOKEN={discord_token}

# OpenAI API Configuration (Primary)
OPENAI_API_KEY={openai_api_key}

# BlackBox AI Configuration (Secondary)
BLACKBOX_API_KEY={blackbox_api_key}

# Claude API Configuration (OpenRouter - Backup)
CLAUDE_API_KEY={claude_api_key}
OPENROUTER_API_KEY={claude_api_key}

# Legacy Hugging Face (for fallback)
HUGGINGFACE_API_KEY=
HUGGINGFACE=

# Optional: Other configurations
DEBUG=True
"""
    
    # Write to .env file
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ .env file created successfully!")
        print("\n📝 Your .env file contains:")
        print(f"   DISCORD_BOT_TOKEN={discord_token[:20]}...")
        print(f"   CLAUDE_API_KEY={claude_api_key[:15]}...")
        
        # Test if tokens can be loaded
        from dotenv import load_dotenv
        load_dotenv()
        
        discord_test = os.getenv('DISCORD_BOT_TOKEN')
        claude_test = os.getenv('CLAUDE_API_KEY')
        
        if discord_test and claude_test:
            print("\n✅ Tokens loaded successfully!")
            print("🚀 You can now run your Discord bot:")
            print("   python deployment/discord_bot_slash.py")
            print("\n🌐 Or run your web app:")
            print("   streamlit run deployment/streamlit_app.py")
        else:
            print("\n❌ Error loading tokens from .env file")
            
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        print("\n📝 Please manually create a .env file with this content:")
        print(env_content)

if __name__ == "__main__":
    setup_env_file()
