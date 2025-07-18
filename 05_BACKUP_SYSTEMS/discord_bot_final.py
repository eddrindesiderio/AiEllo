#!/usr/bin/env python3
"""
Discord Bot - FINAL VERSION (No Duplicates)
This version prevents duplicate responses and ensures clean single responses.

Prerequisites:
- A Discord Bot Token
- An OpenRouter API Key for Claude access
- Bot invited to server with "Send Messages" permission

Run with: python deployment/discord_bot_final.py
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

# Bot setup - Minimal intents to prevent conflicts
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Load personal info
PERSONAL_INFO = ""
if os.path.exists("personal_info.txt"):
    with open("personal_info.txt", "r", encoding="utf-8") as f:
        PERSONAL_INFO = f.read()

# Track processed messages to prevent duplicates
processed_messages = set()

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
            "max_tokens": 800,
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
    message_lower = message.lower()
    
    # HTML/Portfolio requests
    if any(keyword in message_lower for keyword in ["html", "portfolio", "website", "basic html"]):
        return """Here's a basic HTML portfolio template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eddrin Desiderio - Portfolio</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .header { text-align: center; background: #333; color: white; padding: 20px; }
        .section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; }
        .skills { display: flex; gap: 10px; flex-wrap: wrap; }
        .skill { background: #007bff; color: white; padding: 5px 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Eddrin Desiderio</h1>
        <p>Web Developer & IT Professional</p>
    </div>
    
    <div class="section">
        <h2>About Me</h2>
        <p>Bachelor of Science in Information Technology from STI College Tanauan. Passionate about creating user-friendly web solutions.</p>
    </div>
    
    <div class="section">
        <h2>Skills</h2>
        <div class="skills">
            <span class="skill">HTML</span>
            <span class="skill">CSS</span>
            <span class="skill">JavaScript</span>
            <span class="skill">PHP</span>
            <span class="skill">MySQL</span>
        </div>
    </div>
    
    <div class="section">
        <h2>Contact</h2>
        <p>Email: eddrin.desiderio@gmail.com</p>
        <p>Portfolio: https://eddrin.netlify.app/</p>
    </div>
</body>
</html>
```

This creates a clean, responsive portfolio page!"""
    
    # Philippines description
    if any(keyword in message_lower for keyword in ["philippines", "pilipinas", "filipino"]):
        return """The Philippines is a beautiful archipelago in Southeast Asia consisting of over 7,000 islands. Here are key facts:

🏝️ **Geography:**
- Located between the South China Sea and Pacific Ocean
- Major islands: Luzon, Visayas, and Mindanao
- Capital: Manila (Metro Manila is the largest urban area)

🏛️ **Government & History:**
- Republic with a presidential system
- Gained independence from Spain (1898) and USA (1946)
- Rich cultural heritage influenced by Malay, Spanish, American, and Chinese cultures

👥 **People & Culture:**
- Population: Over 110 million people
- Languages: Filipino (Tagalog) and English are official languages
- Religion: Predominantly Catholic (80%+)
- Known for hospitality ("Filipino hospitality")

🌾 **Economy:**
- Major industries: Services, manufacturing, agriculture
- Key exports: Electronics, garments, coconut products
- Growing IT and business process outsourcing sector
- Overseas Filipino Workers (OFWs) contribute significantly

🎭 **Culture:**
- Famous for festivals (fiestas), music, and dance
- Cuisine: Adobo, lechon, lumpia, halo-halo
- Strong family values and community spirit
- Beautiful beaches, diving spots, and natural wonders

The Philippines is known as the "Pearl of the Orient Seas" for its natural beauty and warm, welcoming people!"""
    
    # Use regular fallback for other queries
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
    
    # Greetings
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
    print("🔧 Using MESSAGE COMMANDS ONLY (no slash commands)")
    print("💬 Available commands:")
    print("   !chat <message> - Chat with AI")
    print("   !hello - Say hello")
    print("   !about - Learn about Eddrin")
    print("   !help - Show help")
    print("   !test - Test the bot")
    
    # Clear processed messages on startup
    processed_messages.clear()

@bot.event
async def on_message(message):
    """Handle message commands - SINGLE RESPONSE ONLY"""
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Create unique message ID to prevent duplicates
    message_id = f"{message.id}_{message.author.id}_{message.content}"
    
    # Check if we already processed this message
    if message_id in processed_messages:
        print(f"🔄 Skipping duplicate message: {message.content[:30]}...")
        return
    
    # Add to processed messages
    processed_messages.add(message_id)
    
    # Clean up old processed messages (keep last 100)
    if len(processed_messages) > 100:
        processed_messages.clear()
    
    content = message.content.strip()
    
    # Main chat command
    if content.startswith('!chat '):
        query = content[6:]  # Remove '!chat '
        print(f"🔍 Processing chat command: {query}")
        
        try:
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
            
        except Exception as e:
            print(f"❌ Chat command error: {e}")
            await message.channel.send("Sorry, I encountered an error processing your request. Please try again.")
    
    # Hello command
    elif content.lower() in ['!hello', '!hi']:
        try:
            response = await get_ai_response("Hello")
            await message.channel.send(response)
        except:
            await message.channel.send("Hello! I'm your AI assistant powered by Claude 3.5 Sonnet. Use `!chat <message>` to chat with me!")
    
    # About command
    elif content.lower() == '!about':
        try:
            response = await get_ai_response("Tell me about Eddrin Desiderio")
            if len(response) > 1900:
                response = response[:1900] + "..."
            await message.channel.send(response)
        except:
            fallback = get_fallback_response("tell me about eddrin")
            if len(fallback) > 1900:
                fallback = fallback[:1900] + "..."
            await message.channel.send(fallback)
    
    # Test command
    elif content.lower() == '!test':
        await message.channel.send("✅ Bot is working! Try these commands:\n• `!chat What is 2+2?`\n• `!chat Tell me about Eddrin`\n• `!chat Hello`\n• `!hello`\n• `!about`")
    
    # Help command
    elif content.lower() == '!help':
        help_text = """🤖 **Personal AI Assistant - MESSAGE COMMANDS**

**Available Commands:**
• `!chat <message>` - Chat with Claude 3.5 Sonnet AI
• `!hello` - Say hello to the AI
• `!about` - Learn about Eddrin Desiderio
• `!test` - Test if the bot is working
• `!help` - Show this help message

**Examples:**
• `!chat What is 2+2?` - Math questions
• `!chat Tell me about programming` - Learning topics
• `!chat Who is Eddrin?` - Personal questions
• `!chat Write a short poem` - Creative tasks
• `!chat Explain Python` - Technical help

**Features:**
✅ Powered by Claude 3.5 Sonnet via OpenRouter
✅ Smart context awareness
✅ Accurate math and calculations
✅ Programming and technical help
✅ Creative writing assistance
✅ Personal information about Eddrin

**Note:** This bot uses MESSAGE COMMANDS only (no slash commands) for maximum reliability!"""
        await message.channel.send(help_text)
    
    # Math shortcuts
    elif content.lower() in ['!math', '!calculate']:
        await message.channel.send("I can help with math! Try:\n• `!chat What is 2+2?`\n• `!chat Calculate 15 * 7`\n• `!chat What is 100 divided by 4?`")
    
    # Programming shortcuts
    elif content.lower() in ['!code', '!programming']:
        await message.channel.send("I can help with programming! Try:\n• `!chat Explain Python basics`\n• `!chat How to create a website?`\n• `!chat What is machine learning?`")
    
    # Don't process other commands to avoid conflicts
    # await bot.process_commands(message)  # REMOVED to prevent duplicates

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore unknown commands
    print(f"❌ Command error: {error}")

def main():
    """Run the bot"""
    print("🚀 Starting FINAL Discord Bot (No Duplicates)...")
    print("🔧 Features:")
    print("   - MESSAGE COMMANDS ONLY (no slash commands)")
    print("   - NO DUPLICATE RESPONSES")
    print("   - Claude 3.5 Sonnet via OpenRouter")
    print("   - Smart context awareness")
    print("   - Accurate math and personal responses")
    print("   - Comprehensive fallback system")
    print("\n💬 Commands to try:")
    print("   !chat What is 2+2?")
    print("   !chat Tell me about Eddrin")
    print("   !hello")
    print("   !about")
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
