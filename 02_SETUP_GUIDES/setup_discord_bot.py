#!/usr/bin/env python3
"""
Discord Bot Setup Helper
This script helps you set up your Discord bot with the required API keys.
"""

import os
from dotenv import load_dotenv

def check_env_file():
    """Check if .env file exists and has required keys"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        create_env_file()
        return False
    
    load_dotenv()
    
    discord_token = os.getenv('DISCORD_BOT_TOKEN')
    huggingface_key = os.getenv('HUGGINGFACE')
    
    missing_keys = []
    if not discord_token or discord_token == 'your_discord_bot_token_here':
        missing_keys.append('DISCORD_BOT_TOKEN')
    
    if not huggingface_key or huggingface_key == 'your_huggingface_api_key_here':
        missing_keys.append('HUGGINGFACE')
    
    if missing_keys:
        print(f"❌ Missing or invalid API keys: {', '.join(missing_keys)}")
        print("\n📝 Please update your .env file with valid API keys:")
        for key in missing_keys:
            print(f"   {key}=your_actual_key_here")
        return False
    
    print("✅ All API keys found in .env file!")
    return True

def create_env_file():
    """Create a template .env file"""
    env_content = """# Discord Bot Configuration
DISCORD_BOT_TOKEN=your_discord_bot_token_here
HUGGINGFACE=your_huggingface_api_key_here

# How to get these keys:
# 1. Discord Bot Token: https://discord.com/developers/applications
# 2. Hugging Face API Key: https://huggingface.co/settings/tokens
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env template file!")
    print("📝 Please edit .env file and add your actual API keys")

def test_discord_imports():
    """Test if required packages are installed"""
    try:
        import discord
        print("✅ discord.py is installed")
    except ImportError:
        print("❌ discord.py not installed. Run: pip install discord.py")
        return False
    
    try:
        from huggingface_hub import InferenceClient
        print("✅ huggingface_hub is installed")
    except ImportError:
        print("❌ huggingface_hub not installed. Run: pip install huggingface_hub")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv is installed")
    except ImportError:
        print("❌ python-dotenv not installed. Run: pip install python-dotenv")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🤖 Discord Bot Setup Helper")
    print("=" * 40)
    
    # Check if required packages are installed
    print("\n1. Checking required packages...")
    if not test_discord_imports():
        print("\n❌ Please install missing packages first:")
        print("   pip install discord.py huggingface_hub python-dotenv")
        return
    
    # Check .env file
    print("\n2. Checking .env file...")
    if not check_env_file():
        print("\n📋 Next steps:")
        print("1. Get Discord Bot Token:")
        print("   - Go to https://discord.com/developers/applications")
        print("   - Create new application → Bot → Copy token")
        print("2. Get Hugging Face API Key:")
        print("   - Go to https://huggingface.co/settings/tokens")
        print("   - Create new token")
        print("3. Update .env file with your actual keys")
        print("4. Run this script again to verify")
        return
    
    # Check if personal_info.txt exists
    print("\n3. Checking personal information...")
    if os.path.exists('personal_info.txt'):
        print("✅ personal_info.txt found!")
    else:
        print("⚠️  personal_info.txt not found - bot won't have personal information")
    
    print("\n🎉 Setup complete! You can now run:")
    print("   python deployment/discord_bot.py")
    
    print("\n💡 To test your bot:")
    print("1. Make sure bot is invited to your Discord server")
    print("2. Mention the bot: @YourBotName Hello")
    print("3. Try: @YourBotName What is 2+2?")
    print("4. Try: @YourBotName Who is Eddrin?")

if __name__ == "__main__":
    main()
