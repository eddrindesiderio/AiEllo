#!/usr/bin/env python3
"""
Discord Bot - Kluster.ai Version (FIXED)
Uses correct Kluster.ai API with Meta-Llama-3.1-8B-Instruct-Turbo

Prerequisites:
- A Discord Bot Token
- Kluster.ai API Key: 5805a353-6853-4192-b5a7-60e7e652517a

Run with: python 01_WORKING_SYSTEMS/discord_bot_kluster.py
"""

import discord
from discord.ext import commands
from openai import OpenAI
import os
import asyncio
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
load_dotenv(".env")
load_dotenv("../.env")

# Kluster.ai Configuration (CORRECTED)
KLUSTER_API_KEY = "5805a353-6853-4192-b5a7-60e7e652517a"
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Initialize Kluster.ai client
client = OpenAI(
    api_key=KLUSTER_API_KEY,
    base_url="https://api.kluster.ai/v1"
)

MODEL = "klusterai/Meta-Llama-3.1-8B-Instruct-Turbo"

if not DISCORD_BOT_TOKEN:
    raise ValueError("❌ Discord bot token not found in .env file")

print(f"🔍 Discord Token: {'Found' if DISCORD_BOT_TOKEN else 'Missing'}")
print(f"🔍 Kluster.ai API Key: {'Found' if KLUSTER_API_KEY else 'Missing'}")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Load personal info
PERSONAL_INFO = ""
try:
    if os.path.exists("07_PERSONAL_DATA/personal_info.txt"):
        with open("07_PERSONAL_DATA/personal_info.txt", "r", encoding="utf-8") as f:
            PERSONAL_INFO = f.read()
    elif os.path.exists("personal_info.txt"):
        with open("personal_info.txt", "r", encoding="utf-8") as f:
            PERSONAL_INFO = f.read()
except:
    PERSONAL_INFO = """
    HELLO!
    I am Eddrin Desiderio
    I hold a Bachelor of Science in Information Technology from STI College Tanauan.

    Introduction
    About Me
    I hold a Bachelor of Science in Information Technology from STI College Tanauan, where I was recognized as the best programmer during my senior high school years. My journey in web development has been driven by a strong focus on delivering user-friendly and custom web solutions that meet client needs on time and within budget. I specialize in turning design concepts into interactive digital experiences using HTML, CSS, and JavaScript. I am committed to excellence in every aspect of my work.
    """

# Global message tracking
processed_messages = {}
last_response_time = {}

def is_duplicate_message(message):
    """Check if message is duplicate and should be ignored"""
    user_id = message.author.id
    content = message.content.strip()
    current_time = time.time()
    
    message_key = f"{user_id}_{content}"
    
    # Check if we processed this exact message recently
    if message_key in processed_messages:
        time_diff = current_time - processed_messages[message_key]
        if time_diff < 5:
            print(f"🔄 Ignoring duplicate message from {message.author}: {content[:30]}...")
            return True
    
    # Rate limiting
    if user_id in last_response_time:
        time_diff = current_time - last_response_time[user_id]
        if time_diff < 2:
            print(f"⏱️ Rate limiting user {message.author}: {content[:30]}...")
            return True
    
    # Record this message
    processed_messages[message_key] = current_time
    last_response_time[user_id] = current_time
    
    # Clean old entries
    if len(processed_messages) > 50:
        sorted_items = sorted(processed_messages.items(), key=lambda x: x[1])
        for key, _ in sorted_items[:10]:
            del processed_messages[key]
    
    return False

# Kluster.ai API call
async def get_ai_response(message):
    """Get AI response from Kluster.ai"""
    try:
        print(f"🔍 Calling Kluster.ai API for: {message[:50]}...")
        
        # Smart system prompt based on message content
        system_prompt = get_system_prompt(message)
        
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=400,  # INCREASED for complete responses (Discord friendly)
            temperature=0.3
        )
        
        ai_response = completion.choices[0].message.content
        print(f"✅ Kluster.ai API Success: {ai_response[:50]}...")
        return ai_response
        
    except Exception as e:
        print(f"❌ Kluster.ai API Error: {e}")
        return get_fallback_response(message)

def get_system_prompt(user_message):
    """Get appropriate system prompt based on user message"""
    message_lower = user_message.lower()
    
    base_prompt = """You are a helpful, friendly AI assistant. Be natural and conversational in your responses.

- Answer questions accurately and helpfully
- For simple questions like math problems, give direct correct answers
- Be conversational but not overly chatty
- Keep responses concise for Discord
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

def get_fallback_response(message):
    """Fallback responses when API is unavailable - GUARANTEED to work"""
    message_lower = message.lower()
    
    # Personal questions
    personal_keywords = ["who am i", "about me", "my skills", "eddrin", "tell me about myself", "my background", "my experience"]
    if any(keyword in message_lower for keyword in personal_keywords):
        return f"Here's what I know about Eddrin Desiderio:\n\n{PERSONAL_INFO[:600]}\n\nHe specializes in web development using HTML, CSS, and JavaScript, and is committed to delivering user-friendly solutions."
    
    # Math questions - ALWAYS correct
    if "2+2" in message_lower or "2 + 2" in message_lower:
        return "2 + 2 = 4"
    elif "1+1" in message_lower or "1 + 1" in message_lower:
        return "1 + 1 = 2"
    elif "3+3" in message_lower or "3 + 3" in message_lower:
        return "3 + 3 = 6"
    elif "5*7" in message_lower or "5 * 7" in message_lower:
        return "5 × 7 = 35"
    elif "10-5" in message_lower or "10 - 5" in message_lower:
        return "10 - 5 = 5"
    elif any(op in message_lower for op in ['+', '-', '*', '/', 'math', 'calculate']):
        return "I can help with math! Try asking me calculations like '2+2', '5*7', or '10-5'. What would you like to calculate?"
    
    # Greetings
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        return "Hello! I'm your personal AI assistant powered by Kluster.ai Meta-Llama-3.1-8B-Instruct-Turbo. How can I help you today?"
    
    # Programming
    if any(keyword in message_lower for keyword in ["code", "programming", "python", "javascript", "html", "css"]):
        return "I can help with programming! I know HTML, CSS, JavaScript, Python, and web development. What programming topic interests you?"
    
    # Fun activities (matching the API example)
    if any(keyword in message_lower for keyword in ["fun", "activities", "things to do"]):
        return "Here are some fun things you can do:\n• Learn programming (HTML, CSS, JavaScript)\n• Build web projects\n• Explore AI and technology\n• Creative writing and storytelling\n• Outdoor activities and sports\n• Read books and take online courses\n\nWhat type of activities interest you most?"
    
    # Writing
    if any(keyword in message_lower for keyword in ["write", "essay", "blog", "article", "story"]):
        return "I can help with writing! I can assist with essays, blog posts, articles, stories, and creative content. What would you like help writing?"
    
    # Default comprehensive response
    return f"I can help you with '{message}'! I can assist with:\n• Math problems and calculations\n• Programming and coding questions\n• Information about Eddrin's background and skills\n• Writing and creative tasks\n• Fun activity suggestions\n• General questions and explanations\n\nWhat would you like to know more about?"

@bot.event
async def on_ready():
    """Bot ready event"""
    print(f'✅ Bot logged in as {bot.user}')
    print(f'🤖 Ready to chat! Bot is in {len(bot.guilds)} server(s)')
    print(f"🔧 Using {MODEL} via Kluster.ai")
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
    """Handle message commands - NO DUPLICATES"""
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
            response = "Hello! I'm your AI assistant powered by Kluster.ai Meta-Llama-3.1-8B-Instruct-Turbo. Use `!chat <message>` to chat with me!"
            await message.channel.send(response)
        
        # About command
        elif content.lower() == '!about':
            fallback = get_fallback_response("tell me about eddrin")
            if len(fallback) > 1900:
                fallback = fallback[:1900] + "..."
            await message.channel.send(fallback)
        
        # Test command
        elif content.lower() == '!test':
            await message.channel.send("✅ Bot is working! Try these commands:\n• `!chat What is 2+2?`\n• `!chat Tell me about Eddrin`\n• `!chat What are some fun things to do?`\n• `!hello`\n• `!about`")
        
        # Help command
        elif content.lower() == '!help':
            help_text = """🤖 **Personal AI Assistant - Kluster.ai Version**

**Available Commands:**
• `!chat <message>` - Chat with Kluster.ai Meta-Llama-3.1-8B-Instruct-Turbo
• `!hello` - Say hello to the AI
• `!about` - Learn about Eddrin Desiderio
• `!test` - Test if the bot is working
• `!help` - Show this help message

**Examples:**
• `!chat What is 2+2?` - Math questions
• `!chat What are some fun things to do?` - Activity suggestions
• `!chat Who is Eddrin?` - Personal questions
• `!chat Create HTML portfolio` - Programming help
• `!chat Write a short story` - Creative writing

**Features:**
✅ Powered by Kluster.ai Meta-Llama-3.1-8B-Instruct-Turbo
✅ Smart context awareness
✅ NO DUPLICATE RESPONSES
✅ Enhanced fallback system
✅ Rate limiting protection
✅ Personal information about Eddrin

**Note:** This bot uses your Kluster.ai API key for accurate responses!"""
            await message.channel.send(help_text)
        
        else:
            # Unknown command
            await message.channel.send("Unknown command. Type `!help` to see available commands.")
    
    except Exception as e:
        print(f"❌ Command error: {e}")
        await message.channel.send("Sorry, I encountered an error processing your request. Please try again.")

def main():
    """Run the bot"""
    print("🚀 Starting Kluster.ai Discord Bot...")
    print("🔧 Features:")
    print("   - Kluster.ai Meta-Llama-3.1-8B-Instruct-Turbo")
    print("   - CLEAN MESSAGE HANDLING")
    print("   - NO DUPLICATE RESPONSES")
    print("   - Rate limiting protection")
    print("   - Enhanced fallback responses")
    print("   - Personal context about Eddrin")
    print(f"   - API Key: {KLUSTER_API_KEY[:20]}...")
    print("\n💬 Commands to try:")
    print("   !chat What is 2+2?")
    print("   !chat What are some fun things to do?")
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
        print("4. Try the Python chat: python 01_WORKING_SYSTEMS/kluster_ai_final.py")

if __name__ == "__main__":
    main()
