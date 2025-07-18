#!/usr/bin/env python3
"""
Simple Discord Bot for Your Personal AI (Using Claude via OpenRouter)
This version focuses on reliable command registration and basic functionality.

Prerequisites:
- A Discord Bot Token (see Discord Developer Portal)
- An OpenRouter API Key for Claude access
- The bot must be invited to your server with necessary permissions.

Run with: python deployment/discord_bot_simple.py
"""

import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
import aiohttp
import json

# Load environment variables
load_dotenv()
load_dotenv(".env")
load_dotenv("../.env")

# Get tokens
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("CLAUDE_API_KEY")

if not DISCORD_BOT_TOKEN:
    raise ValueError("❌ Discord bot token not found in .env file")

print(f"🔍 Discord Token: {'Found' if DISCORD_BOT_TOKEN else 'Missing'}")
print(f"🔍 OpenRouter API Key: {'Found' if OPENROUTER_API_KEY else 'Missing'}")

# Bot setup with minimal intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load personal info
PERSONAL_INFO = ""
if os.path.exists("personal_info.txt"):
    with open("personal_info.txt", "r", encoding="utf-8") as f:
        PERSONAL_INFO = f.read()

# Simple OpenRouter API call
async def get_ai_response(message):
    """Get AI response from OpenRouter or fallback"""
    if not OPENROUTER_API_KEY:
        return get_fallback_response(message)
    
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [{"role": "user", "content": message}],
            "max_tokens": 800,
            "temperature": 0.2
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data, timeout=10) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    print(f"❌ API Error {response.status}")
                    return get_fallback_response(message)
                    
    except Exception as e:
        print(f"❌ API Exception: {e}")
        return get_fallback_response(message)

def get_fallback_response(message):
    """Fallback responses when API is unavailable"""
    message_lower = message.lower()
    
    # Personal questions
    personal_keywords = ["who am i", "about me", "my skills", "eddrin", "tell me about myself"]
    if any(keyword in message_lower for keyword in personal_keywords):
        if PERSONAL_INFO:
            return f"Here's what I know about Eddrin:\n\n{PERSONAL_INFO[:500]}..."
        else:
            return "Eddrin Desiderio is a web developer with a Bachelor of Science in Information Technology from STI College Tanauan. He specializes in HTML, CSS, and JavaScript."
    
    # Math questions
    if "2+2" in message_lower or "2 + 2" in message_lower:
        return "2 + 2 = 4"
    elif "1+1" in message_lower or "1 + 1" in message_lower:
        return "1 + 1 = 2"
    elif any(op in message_lower for op in ['+', '-', '*', '/', 'math']):
        return "I can help with basic math! Try asking me simple calculations like '2+2' or '5*3'."
    
    # Greetings
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey"]):
        return "Hello! I'm your personal AI assistant. Ask me about math, programming, or Eddrin's background!"
    
    # Programming
    if any(keyword in message_lower for keyword in ["code", "programming", "python", "javascript"]):
        return "I can help with programming concepts! What specific topic would you like to learn about?"
    
    # Default
    return f"I can help you with '{message}'! Try asking me about math, programming, or Eddrin's background and skills."

@bot.event
async def on_ready():
    """Bot ready event"""
    print(f'✅ Bot logged in as {bot.user}')
    print(f'🤖 Ready to chat! Bot is in {len(bot.guilds)} server(s)')
    
    # Simple command sync
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")
        print("💡 Slash commands may not work, but message commands will work")

# Simple slash command
@bot.tree.command(name="chat", description="Chat with AI")
async def chat_slash(interaction: discord.Interaction, message: str):
    """Simple chat slash command"""
    try:
        await interaction.response.defer()
        
        print(f"🔍 Processing: {message}")
        response = await get_ai_response(message)
        
        # Handle long responses
        if len(response) > 1900:
            response = response[:1900] + "..."
        
        await interaction.followup.send(response)
        print(f"✅ Sent response: {response[:50]}...")
        
    except Exception as e:
        print(f"❌ Slash command error: {e}")
        try:
            await interaction.followup.send("Sorry, I encountered an error. Try using `!chat <message>` instead.")
        except:
            pass

@bot.tree.command(name="hello", description="Say hello")
async def hello_slash(interaction: discord.Interaction):
    """Simple hello slash command"""
    try:
        await interaction.response.defer()
        response = "Hello! I'm your personal AI assistant powered by Claude 3.5 Sonnet. How can I help you today?"
        await interaction.followup.send(response)
    except Exception as e:
        print(f"❌ Hello command error: {e}")

# Message-based commands (more reliable)
@bot.event
async def on_message(message):
    """Handle message commands"""
    if message.author == bot.user:
        return
    
    content = message.content.strip()
    
    # Chat command
    if content.startswith('!chat '):
        query = content[6:]  # Remove '!chat '
        print(f"🔍 Message command: {query}")
        
        try:
            response = await get_ai_response(query)
            
            # Handle long responses
            if len(response) > 1900:
                response = response[:1900] + "..."
            
            await message.channel.send(response)
            print(f"✅ Message response sent: {response[:50]}...")
            
        except Exception as e:
            print(f"❌ Message command error: {e}")
            await message.channel.send("Sorry, I encountered an error processing your request.")
    
    # Simple commands
    elif content.lower() in ['!hello', '!hi']:
        await message.channel.send("Hello! I'm your AI assistant. Use `!chat <message>` to chat with me!")
    
    elif content.lower() == '!about':
        response = get_fallback_response("tell me about eddrin")
        if len(response) > 1900:
            response = response[:1900] + "..."
        await message.channel.send(response)
    
    elif content.lower() == '!help':
        help_text = """🤖 **AI Assistant Commands:**

**Slash Commands:**
• `/chat <message>` - Chat with AI
• `/hello` - Say hello

**Message Commands:**
• `!chat <message>` - Chat with AI
• `!hello` - Say hello  
• `!about` - Learn about Eddrin
• `!help` - Show this help

**Examples:**
• `!chat What is 2+2?`
• `!chat Tell me about programming`
• `!chat Who is Eddrin?`

Try both slash commands and message commands!"""
        await message.channel.send(help_text)
    
    # Process other bot commands
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore unknown commands
    print(f"❌ Command error: {error}")

def main():
    """Run the bot"""
    print("🚀 Starting Simple Discord Bot...")
    print("🔧 Features:")
    print("   - Slash commands: /chat, /hello")
    print("   - Message commands: !chat, !hello, !about, !help")
    print("   - Claude 3.5 Sonnet via OpenRouter")
    print("   - Smart fallback responses")
    
    try:
        bot.run(DISCORD_BOT_TOKEN)
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Check your Discord token in .env file")
        print("2. Make sure the bot is invited to your server")
        print("3. Try the Streamlit app: streamlit run deployment/streamlit_app_openrouter.py")

if __name__ == "__main__":
    main()
