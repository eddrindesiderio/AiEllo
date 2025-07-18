#!/usr/bin/env python3
"""
Discord Bot Troubleshooting Script
This script helps diagnose common Discord bot issues.
"""

import os
from dotenv import load_dotenv

def check_environment():
    """Check environment setup"""
    print("🔍 Checking Environment Setup...")
    print("=" * 40)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        return False
    else:
        print("✅ .env file found")
    
    # Load environment variables
    load_dotenv()
    
    # Check Discord token
    discord_token = os.getenv('DISCORD_BOT_TOKEN')
    if not discord_token:
        print("❌ DISCORD_BOT_TOKEN not found in .env")
        return False
    elif discord_token == 'your_discord_bot_token_here':
        print("❌ DISCORD_BOT_TOKEN is still placeholder")
        return False
    else:
        print("✅ DISCORD_BOT_TOKEN found")
        print(f"   Token starts with: {discord_token[:20]}...")
    
    # Check Hugging Face token
    hf_token = os.getenv('HUGGINGFACE')
    if not hf_token:
        print("❌ HUGGINGFACE token not found in .env")
        return False
    elif hf_token == 'your_huggingface_api_key_here':
        print("❌ HUGGINGFACE token is still placeholder")
        return False
    else:
        print("✅ HUGGINGFACE token found")
        print(f"   Token starts with: {hf_token[:20]}...")
    
    return True

def check_packages():
    """Check if required packages are installed"""
    print("\n🔍 Checking Required Packages...")
    print("=" * 40)
    
    packages = ['discord', 'dotenv', 'huggingface_hub']
    all_good = True
    
    for package in packages:
        try:
            if package == 'dotenv':
                import python_dotenv
                print("✅ python-dotenv is installed")
            else:
                __import__(package)
                print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            all_good = False
    
    return all_good

def check_personal_info():
    """Check if personal info file exists"""
    print("\n🔍 Checking Personal Information...")
    print("=" * 40)
    
    if os.path.exists('personal_info.txt'):
        print("✅ personal_info.txt found")
        with open('personal_info.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"   Content length: {len(content)} characters")
        return True
    else:
        print("⚠️  personal_info.txt not found")
        print("   Bot will work but won't have personal information")
        return False

def test_bot_connection():
    """Test basic bot connection"""
    print("\n🔍 Testing Bot Connection...")
    print("=" * 40)
    
    try:
        import discord
        from dotenv import load_dotenv
        
        load_dotenv()
        token = os.getenv('DISCORD_BOT_TOKEN')
        
        if not token:
            print("❌ Cannot test - no Discord token")
            return False
        
        # Create a simple client to test connection
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            print(f"✅ Bot connected successfully as {client.user}")
            print(f"   Bot ID: {client.user.id}")
            print(f"   Bot is in {len(client.guilds)} server(s)")
            await client.close()
        
        print("🔄 Testing connection (this may take a moment)...")
        client.run(token)
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def main():
    """Main troubleshooting function"""
    print("🤖 Discord Bot Troubleshooting")
    print("=" * 50)
    
    # Check environment
    env_ok = check_environment()
    
    # Check packages
    packages_ok = check_packages()
    
    # Check personal info
    personal_ok = check_personal_info()
    
    print("\n📋 Summary:")
    print("=" * 20)
    print(f"Environment Setup: {'✅' if env_ok else '❌'}")
    print(f"Required Packages: {'✅' if packages_ok else '❌'}")
    print(f"Personal Info: {'✅' if personal_ok else '⚠️'}")
    
    if not env_ok:
        print("\n🔧 To Fix Environment Issues:")
        print("1. Make sure .env file exists")
        print("2. Add your Discord bot token")
        print("3. Add your Hugging Face API key")
        print("4. Restart the bot")
    
    if not packages_ok:
        print("\n🔧 To Fix Package Issues:")
        print("Run: pip install discord.py python-dotenv huggingface_hub")
    
    if env_ok and packages_ok:
        print("\n✅ Environment looks good!")
        print("\n🔧 Common Discord Bot Issues:")
        print("1. Bot not invited to server properly")
        print("2. Bot lacks permissions in the channel")
        print("3. Message Content Intent not enabled")
        print("4. Bot is offline/not running")
        print("\n💡 Try the slash commands bot instead:")
        print("   python deployment/discord_bot_slash.py")

if __name__ == "__main__":
    main()
