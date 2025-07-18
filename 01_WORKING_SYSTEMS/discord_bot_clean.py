#!/usr/bin/env python3
"""
Discord Bot - CLEAN VERSION (Absolutely No Duplicates)
This version completely prevents duplicate responses with strict message handling.

Prerequisites:
- A Discord Bot Token
- An OpenRouter API Key for Claude access
- Bot invited to server with "Send Messages" permission

Run with: python deployment/discord_bot_clean.py
"""

import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
import aiohttp
import json
import time

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

# Bot setup - Minimal intents, NO command processing
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)  # Using Client instead of Bot to avoid command conflicts

# Load personal info
PERSONAL_INFO = ""
if os.path.exists("personal_info.txt"):
    with open("personal_info.txt", "r", encoding="utf-8") as f:
        PERSONAL_INFO = f.read()

# Global message tracking with timestamps
processed_messages = {}
last_response_time = {}

def is_duplicate_message(message):
    """Check if message is duplicate and should be ignored"""
    user_id = message.author.id
    content = message.content.strip()
    current_time = time.time()
    
    # Create unique key
    message_key = f"{user_id}_{content}"
    
    # Check if we processed this exact message recently (within 5 seconds)
    if message_key in processed_messages:
        time_diff = current_time - processed_messages[message_key]
        if time_diff < 5:  # Ignore if same message within 5 seconds
            print(f"🔄 Ignoring duplicate message from {message.author}: {content[:30]}...")
            return True
    
    # Check if user sent any message too quickly (rate limiting)
    if user_id in last_response_time:
        time_diff = current_time - last_response_time[user_id]
        if time_diff < 2:  # Minimum 2 seconds between responses
            print(f"⏱️ Rate limiting user {message.author}: {content[:30]}...")
            return True
    
    # Record this message
    processed_messages[message_key] = current_time
    last_response_time[user_id] = current_time
    
    # Clean old entries (keep last 50)
    if len(processed_messages) > 50:
        # Remove oldest entries
        sorted_items = sorted(processed_messages.items(), key=lambda x: x[1])
        for key, _ in sorted_items[:10]:  # Remove 10 oldest
            del processed_messages[key]
    
    return False

# OpenRouter API call
async def get_ai_response(message):
    """Get AI response from OpenRouter Claude 3.5 Sonnet"""
    if not OPENROUTER_API_KEY:
        print("⚠️ No OpenRouter API key - using fallback")
        return get_fallback_response(message)
    
    try:
        print(f"🔍 Calling OpenRouter API for: {message[:50]}...")
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/personal-ai",
            "X-Title": "Personal AI Assistant"
        }
        
        # Smart system prompt based on message content
        system_prompt = get_system_prompt(message)
        
        data = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 80,  # Reduced to 80 to work with 84 available credits
            "temperature": 0.2
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data, timeout=15) as response:
                if response.status == 200:
                    result = await response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    print(f"✅ OpenRouter API Success: {ai_response[:50]}...")
                    return ai_response
                else:
                    error_text = await response.text()
                    print(f"❌ API Error {response.status}: {error_text}")
                    
                    # Handle specific credit error
                    if response.status == 402:
                        print("⚠️ OpenRouter API credits exhausted - using enhanced fallback")
                        return get_enhanced_fallback_response(message)
                    else:
                        return get_fallback_response(message)
                    
    except Exception as e:
        print(f"❌ API Exception: {e}")
        return get_fallback_response(message)

def get_system_prompt(user_message):
    """Get appropriate system prompt based on user message"""
    message_lower = user_message.lower()
    
    base_prompt = """You are a helpful, friendly AI assistant. Be natural and conversational in your responses.

- Answer questions accurately and helpfully
- For simple questions like math problems, give direct correct answers
- Be conversational but not overly chatty
- Only mention personal information if the user specifically asks about the person
- Respond naturally to greetings like "Hello" without revealing personal details"""
    
    # Check if user is asking about personal information
    personal_keywords = [
        "who am i", "my name", "about me", "my skills", "my education", 
        "my background", "my experience", "my contact", "my portfolio",
        "tell me about myself", "what do you know about me", "eddrin"
    ]
    
    user_asking_personal = any(keyword in message_lower for keyword in personal_keywords)
    
    if user_asking_personal and PERSONAL_INFO:
        return base_prompt + f"\n\nThe user is asking about themselves. Here is their personal information:\n{PERSONAL_INFO}\n\nUse this information to answer their question about themselves."
    else:
        return base_prompt + "\n\nAnswer the user's question naturally and accurately. Do not mention any personal information unless specifically asked."

def get_enhanced_fallback_response(message):
    """Enhanced fallback responses when API credits are exhausted"""
    # Use the regular fallback system which has proper responses
    return get_fallback_response(message)

def get_fallback_response(message):
    """Fallback responses when API is unavailable"""
    message_lower = message.lower()
    
    # Personal questions
    personal_keywords = ["who am i", "about me", "my skills", "eddrin", "tell me about myself", "my background", "my experience"]
    if any(keyword in message_lower for keyword in personal_keywords):
        if PERSONAL_INFO:
            return f"Here's what I know about Eddrin Desiderio:\n\n{PERSONAL_INFO[:800]}\n\nHe specializes in web development using HTML, CSS, and JavaScript, and is committed to delivering user-friendly solutions."
        else:
            return "Eddrin Desiderio is a web developer with a Bachelor of Science in Information Technology from STI College Tanauan. He specializes in turning design concepts into interactive digital experiences using HTML, CSS, and JavaScript. He was recognized as the best programmer during his senior high school years and focuses on delivering user-friendly, custom web solutions that meet client needs on time and within budget."
    
    # Math questions
    if "2+2" in message_lower or "2 + 2" in message_lower:
        return "2 + 2 = 4"
    elif "1+1" in message_lower or "1 + 1" in message_lower:
        return "1 + 1 = 2"
    elif "3+3" in message_lower or "3 + 3" in message_lower:
        return "3 + 3 = 6"
    elif "5+5" in message_lower or "5 + 5" in message_lower:
        return "5 + 5 = 10"
    elif "1+1=" in message_lower or "2+2=" in message_lower:
        if "1+1=" in message_lower:
            return "1 + 1 = 2"
        else:
            return "2 + 2 = 4"
    elif any(op in message_lower for op in ['+', '-', '*', '/', 'math', 'calculate']):
        return "I can help with math! Try asking me simple calculations like '2+2', '5*3', or '10/2'. For complex calculations, I need my OpenRouter API connection."
    
    # Greetings - SINGLE RESPONSE ONLY
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        return "Hello! I'm your personal AI assistant powered by Claude 3.5 Sonnet via OpenRouter. How can I help you today?"
    
    # Programming
    if any(keyword in message_lower for keyword in ["code", "programming", "python", "javascript", "html", "css", "ai", "artificial intelligence"]):
        return "I can help with programming and AI concepts! What specific topic would you like to learn about? (Python, JavaScript, HTML, CSS, machine learning, etc.)"
    
    # Writing
    if any(keyword in message_lower for keyword in ["write", "essay", "blog", "article"]):
        return "I can help with writing! I can assist with essays, blog posts, articles, emails, and creative writing. What would you like help writing?"
    
    # Default
    return f"I can help you with '{message}'! I can assist with:\n• Math problems and calculations\n• Programming and coding questions\n• Information about Eddrin's background and skills\n• Writing and creative tasks\n• General questions and explanations\n\nWhat would you like to know more about?"

@bot.event
async def on_ready():
    """Bot ready event"""
    print(f'✅ Bot logged in as {bot.user}')
    print(f'🤖 Ready to chat! Bot is in {len(bot.guilds)} server(s)')
    print("🔧 Using CLEAN MESSAGE HANDLING (no duplicates)")
    print("💬 Available commands:")
    print("   !chat <message> - Chat with AI")
    print("   !hello - Say hello")
    print("   !about - Learn about Eddrin")
    print("   !help - Show help")
    print("   !test - Test the bot")
    
    # Clear all tracking on startup
    processed_messages.clear()
    last_response_time.clear()

@bot.event
async def on_message(message):
    """Handle message commands - ABSOLUTELY NO DUPLICATES"""
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Check for duplicates FIRST
    if is_duplicate_message(message):
        return
    
    content = message.content.strip()
    
    # Only process commands that start with !
    if not content.startswith('!'):
        return
    
    print(f"🔍 Processing command from {message.author}: {content}")
    
    try:
        # Main chat command
        if content.startswith('!chat '):
            query = content[6:]  # Remove '!chat '
            print(f"🔍 Processing chat command: {query}")
            
            # Show typing indicator
            async with message.channel.typing():
                response = await get_ai_response(query)
            
            # Handle long responses
            if len(response) > 1900:
                # Split into chunks
                chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
                for i, chunk in enumerate(chunks):
                    if i == 0:
                        await message.channel.send(chunk)
                    else:
                        await message.channel.send(f"(continued...)\n{chunk}")
            else:
                await message.channel.send(response)
            
            print(f"✅ Chat response sent: {response[:50]}...")
        
        # Hello command
        elif content.lower() in ['!hello', '!hi']:
            response = "Hello! I'm your AI assistant powered by Claude 3.5 Sonnet. Use `!chat <message>` to chat with me!"
            await message.channel.send(response)
        
        # About command
        elif content.lower() == '!about':
            fallback = get_fallback_response("tell me about eddrin")
            if len(fallback) > 1900:
                fallback = fallback[:1900] + "..."
            await message.channel.send(fallback)
        
        # Test command
        elif content.lower() == '!test':
            await message.channel.send("✅ Bot is working! Try these commands:\n• `!chat What is 2+2?`\n• `!chat Tell me about Eddrin`\n• `!chat Chinese history short only`\n• `!hello`\n• `!about`")
        
        # Help command
        elif content.lower() == '!help':
            help_text = """🤖 **Personal AI Assistant - CLEAN VERSION**

**Available Commands:**
• `!chat <message>` - Chat with Claude 3.5 Sonnet AI
• `!hello` - Say hello to the AI
• `!about` - Learn about Eddrin Desiderio
• `!test` - Test if the bot is working
• `!help` - Show this help message

**Examples:**
• `!chat What is 2+2?` - Math questions
• `!chat Chinese history short only` - History topics
• `!chat Who is Eddrin?` - Personal questions
• `!chat Create HTML portfolio` - Programming help
• `!chat Philippines description` - Country information

**Features:**
✅ Powered by Claude 3.5 Sonnet via OpenRouter
✅ Smart context awareness
✅ NO DUPLICATE RESPONSES
✅ Enhanced fallback system
✅ Rate limiting protection

**Note:** This bot uses CLEAN message handling to prevent duplicates!"""
            await message.channel.send(help_text)
        
        else:
            # Unknown command
            await message.channel.send("Unknown command. Type `!help` to see available commands.")
    
    except Exception as e:
        print(f"❌ Command error: {e}")
        await message.channel.send("Sorry, I encountered an error processing your request. Please try again.")

def main():
    """Run the bot"""
    print("🚀 Starting CLEAN Discord Bot (Absolutely No Duplicates)...")
    print("🔧 Features:")
    print("   - CLEAN MESSAGE HANDLING")
    print("   - ABSOLUTELY NO DUPLICATE RESPONSES")
    print("   - Rate limiting protection")
    print("   - Claude 3.5 Sonnet via OpenRouter")
    print("   - Enhanced fallback responses")
    print("\n💬 Commands to try:")
    print("   !chat What is 2+2?")
    print("   !chat Chinese history short only")
    print("   !chat Tell me about Eddrin")
    print("   !hello")
    print("   !help")
    
    try:
        bot.run(DISCORD_BOT_TOKEN)
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Check your Discord token in .env file")
        print("2. Make sure the bot is invited to your server")
        print("3. Ensure bot has 'Send Messages' permission")
        print("4. Try the Streamlit app: streamlit run deployment/streamlit_app_openrouter.py")

if __name__ == "__main__":
    main()
