#!/usr/bin/env python3
"""
Discord Bot for Your Personal AI (Using Claude via OpenRouter) - FIXED VERSION
This version fixes the "command is outdated" issue and includes better error handling.

Prerequisites:
- A Discord Bot Token (see Discord Developer Portal)
- An OpenRouter API Key for Claude access
- The bot must be invited to your server with necessary permissions.

Run with: python deployment/discord_bot_fixed.py
"""

import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
import aiohttp
import json
import time

# Load environment variables from multiple possible locations
load_dotenv()  # Load from current directory
load_dotenv(".env")  # Explicit .env file
load_dotenv("../.env")  # Parent directory

# Get Discord bot token
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not DISCORD_BOT_TOKEN:
    raise ValueError("❌ Discord bot token not found in .env file")

# Initialize OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("CLAUDE_API_KEY")
print(f"🔍 Debug: OpenRouter API Key found: {'Yes' if OPENROUTER_API_KEY else 'No'}")
if OPENROUTER_API_KEY:
    print(f"🔍 Debug: OpenRouter API Key starts with: {OPENROUTER_API_KEY[:15]}...")
    print(f"🔍 Debug: OpenRouter API Key length: {len(OPENROUTER_API_KEY)} characters")

if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "your_openrouter_api_key_here":
    print("⚠️  OpenRouter API key not configured - using fallback responses")
    openrouter_available = False
else:
    openrouter_available = True
    print("✅ OpenRouter API key configured")

# Bot setup - Use only non-privileged intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent for better compatibility
bot = commands.Bot(command_prefix='!', intents=intents)

# Load personal information if available
PERSONAL_INFO = ""
if os.path.exists("personal_info.txt"):
    with open("personal_info.txt", "r", encoding="utf-8") as f:
        PERSONAL_INFO = f.read()

# OpenRouter API function
async def call_openrouter_api(messages, system_prompt=""):
    """Call OpenRouter API for Claude 3.5 Sonnet"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/your-repo",  # Optional
        "X-Title": "Personal AI Assistant"  # Optional
    }
    
    # Prepare messages for OpenRouter
    api_messages = []
    if system_prompt:
        api_messages.append({"role": "system", "content": system_prompt})
    
    for msg in messages:
        api_messages.append(msg)
    
    data = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": api_messages,
        "max_tokens": 1000,
        "temperature": 0.2
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
            else:
                error_text = await response.text()
                raise Exception(f"OpenRouter API error {response.status}: {error_text}")

# Fallback response functions
def get_fallback_response(message):
    """Get fallback response when AI API is not available"""
    message_lower = message.lower()
    
    # Check for personal questions
    personal_keywords = [
        "who am i", "my name", "about me", "my skills", "my education", 
        "my background", "my experience", "my contact", "my portfolio",
        "tell me about myself", "what do you know about me", "eddrin"
    ]
    
    if any(keyword in message_lower for keyword in personal_keywords):
        return get_about_response()
    
    # Math questions - Enhanced detection
    if any(op in message_lower for op in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided', '=', 'equals']) or "math" in message_lower:
        # Handle specific math problems
        if "2+2" in message_lower or "2 + 2" in message_lower:
            return "2 + 2 = 4"
        elif "1+1" in message_lower or "1 + 1" in message_lower:
            return "1 + 1 = 2"
        elif "3+3" in message_lower or "3 + 3" in message_lower:
            return "3 + 3 = 6"
        elif "5+5" in message_lower or "5 + 5" in message_lower:
            return "5 + 5 = 10"
        # Handle questions with equals sign
        elif "1+1=" in message_lower or "1 + 1 =" in message_lower:
            return "1 + 1 = 2"
        elif "2+2=" in message_lower or "2 + 2 =" in message_lower:
            return "2 + 2 = 4"
        elif "basic" in message_lower and "math" in message_lower:
            return """Here are basic mathematics concepts:

**Basic Operations:**
- Addition (+): 2 + 3 = 5
- Subtraction (-): 5 - 2 = 3  
- Multiplication (×): 4 × 3 = 12
- Division (÷): 12 ÷ 3 = 4

**Order of Operations (PEMDAS):**
1. Parentheses first
2. Exponents (powers)
3. Multiplication and Division (left to right)
4. Addition and Subtraction (left to right)

**Examples:**
- 2 + 3 × 4 = 2 + 12 = 14
- (2 + 3) × 4 = 5 × 4 = 20

**Fractions:**
- 1/2 = 0.5
- 3/4 = 0.75

What specific math topic would you like help with?"""
        elif any(char.isdigit() for char in message):
            return "I can help with simple math problems. For complex calculations, I need my AI service for full functionality."
    
    # Greetings
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        if openrouter_available:
            return "Hello! I'm your personal AI assistant powered by Claude 3.5 Sonnet via OpenRouter. How can I help you today?"
        else:
            return "Hello! I'm your personal AI assistant. I'm currently running in basic mode - add your OpenRouter API key for full AI capabilities."
    
    # Programming/AI questions
    if any(keyword in message_lower for keyword in ["ai", "artificial intelligence", "code", "coding", "programming", "python", "javascript", "html", "css"]):
        if "basic" in message_lower and ("ai" in message_lower or "code" in message_lower):
            return """Here are some basic AI and coding concepts:

**Basic AI Concepts:**
- Machine Learning: Teaching computers to learn from data
- Neural Networks: Computer systems inspired by the human brain
- Natural Language Processing: Helping computers understand human language

**Basic Programming:**
- Variables: Store data (like `name = "John"`)
- Functions: Reusable blocks of code
- Loops: Repeat actions (for, while)
- Conditionals: Make decisions (if, else)

**Popular Languages:**
- Python: Great for AI and beginners
- JavaScript: For web development
- HTML/CSS: For creating websites

Would you like me to explain any of these topics in more detail?"""
        else:
            return "I can help with programming and AI concepts! What specific topic would you like to learn about? (Python, JavaScript, HTML, CSS, machine learning, etc.)"
    
    # Default response - More helpful fallback
    if "essay" in message_lower:
        return "For essay writing, I can help with structure, tips, and guidance. Here are some basics: Start with an introduction, develop your main points in body paragraphs, and conclude with a summary. Would you like specific help with any part?"
    elif "help" in message_lower:
        return "I'm here to help! I can assist with math problems, answer questions about Eddrin's background and skills, provide general information, programming help, and more. What would you like to know?"
    elif "how" in message_lower and "are" in message_lower:
        return "I'm doing well, thank you for asking! I'm your personal AI assistant. How can I help you today?"
    else:
        return f"I can help you with '{message}'! I can assist with math problems, programming questions, AI concepts, personal questions about Eddrin, and general information. What would you like to know more about?"

def get_about_response():
    """Get information about Eddrin"""
    if PERSONAL_INFO:
        return f"Here's what I know about Eddrin Desiderio:\n\n{PERSONAL_INFO}\n\nHe specializes in web development using HTML, CSS, and JavaScript, and is committed to delivering user-friendly solutions."
    else:
        return "Eddrin Desiderio is a web developer with a Bachelor of Science in Information Technology from STI College Tanauan. He specializes in turning design concepts into interactive digital experiences using HTML, CSS, and JavaScript. He was recognized as the best programmer during his senior high school years and focuses on delivering user-friendly, custom web solutions that meet client needs on time and within budget."

# System prompt for the AI
def get_system_prompt(user_message=""):
    """Get system prompt based on whether user is asking personal questions"""
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
    
    user_asking_personal = any(keyword in user_message.lower() for keyword in personal_keywords)
    
    if user_asking_personal and PERSONAL_INFO:
        return base_prompt + f"\n\nThe user is asking about themselves. Here is their personal information:\n{PERSONAL_INFO}\n\nUse this information to answer their question about themselves."
    else:
        return base_prompt + "\n\nAnswer the user's question naturally and accurately. Do not mention any personal information unless specifically asked."

@bot.event
async def on_ready():
    """Event handler for when the bot is ready"""
    print(f'✅ Logged in as {bot.user}')
    print('🤖 Bot is ready to chat with Claude 3.5 Sonnet via OpenRouter!')
    
    # Force sync slash commands with retry logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"🔄 Syncing commands (attempt {attempt + 1}/{max_retries})...")
            
            # Clear existing commands first
            bot.tree.clear_commands()
            
            # Add commands again
            await setup_commands()
            
            # Sync commands
            synced = await bot.tree.sync()
            print(f"✅ Successfully synced {len(synced)} command(s)")
            
            # Print command details
            for cmd in synced:
                print(f"   - /{cmd.name}: {cmd.description}")
            
            break
            
        except Exception as e:
            print(f"❌ Failed to sync commands (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                print("⏳ Waiting 5 seconds before retry...")
                await asyncio.sleep(5)
            else:
                print("❌ All sync attempts failed. Commands may not work properly.")

async def setup_commands():
    """Setup slash commands"""
    
    @bot.tree.command(name="chat", description="Chat with your personal AI assistant powered by Claude via OpenRouter")
    async def chat_command(interaction: discord.Interaction, message: str):
        """Slash command for chatting with AI"""
        try:
            # Respond immediately to avoid timeout
            await interaction.response.defer(ephemeral=False)
            
            # Get AI response with timeout or use fallback
            if not openrouter_available:
                # Use fallback responses when API key is not configured
                ai_response = f"🔧 DEBUG: No OpenRouter API key - using fallback for: {message}\n\n" + get_fallback_response(message)
            else:
                try:
                    print(f"🔍 DEBUG: Attempting OpenRouter API call for message: {message}")
                    
                    # Prepare system prompt and messages
                    system_prompt = get_system_prompt(message)
                    messages = [{"role": "user", "content": message}]
                    
                    print(f"🔍 DEBUG: Using Claude 3.5 Sonnet via OpenRouter")
                    ai_response = await asyncio.wait_for(
                        call_openrouter_api(messages, system_prompt),
                        timeout=15.0  # 15 second timeout
                    )
                    print(f"✅ DEBUG: OpenRouter API Success! Response: {ai_response[:100]}...")
                except asyncio.TimeoutError:
                    print(f"⏰ DEBUG: OpenRouter API Timeout after 15 seconds")
                    ai_response = f"🔧 DEBUG: API Timeout - using fallback for: {message}\n\n" + get_fallback_response(message)
                except Exception as api_error:
                    print(f"❌ DEBUG: OpenRouter API Error: {api_error}")
                    print(f"❌ DEBUG: Error type: {type(api_error).__name__}")
                    ai_response = f"🔧 DEBUG: API Error ({type(api_error).__name__}) - using fallback for: {message}\n\n" + get_fallback_response(message)

            # Send the actual response
            if len(ai_response) > 1900:  # Leave some buffer for Discord
                # Split long messages into chunks
                chunks = []
                current_chunk = ""
                
                # Split by sentences to avoid cutting words
                sentences = ai_response.split('. ')
                for sentence in sentences:
                    if len(current_chunk + sentence + '. ') > 1900:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                            current_chunk = sentence + '. '
                        else:
                            # Single sentence too long, force split
                            chunks.append(sentence[:1900])
                            current_chunk = sentence[1900:] + '. '
                    else:
                        current_chunk += sentence + '. '
                
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # Send chunks
                for i, chunk in enumerate(chunks):
                    if i == 0:
                        await interaction.followup.send(chunk)
                    else:
                        await interaction.followup.send(chunk)
            else:
                await interaction.followup.send(ai_response)

        except discord.errors.InteractionResponded:
            print("⚠️ Interaction already responded to")
        except discord.NotFound:
            # Interaction expired, send a new message
            try:
                ai_response = get_fallback_response(message)
                await interaction.channel.send(f"**{interaction.user.mention}** asked: {message}\n\n{ai_response}")
            except Exception as fallback_error:
                print(f"❌ Fallback error: {fallback_error}")
        except Exception as e:
            print(f"❌ Error in chat command: {e}")
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message("Sorry, I encountered an error. Please try again later.", ephemeral=True)
                else:
                    await interaction.followup.send("Sorry, I encountered an error. Please try again later.")
            except:
                print(f"❌ Failed to send error message: {e}")

    @bot.tree.command(name="hello", description="Say hello to your Claude-powered AI assistant")
    async def hello_command(interaction: discord.Interaction):
        """Simple hello command"""
        try:
            await interaction.response.defer(ephemeral=False)
            
            if not openrouter_available:
                ai_response = "Hello! I'm your personal AI assistant. How can I help you today?"
            else:
                try:
                    system_prompt = get_system_prompt("Hello")
                    messages = [{"role": "user", "content": "Hello"}]
                    
                    ai_response = await asyncio.wait_for(
                        call_openrouter_api(messages, system_prompt),
                        timeout=10.0
                    )
                except asyncio.TimeoutError:
                    ai_response = "Hello! I'm your personal AI assistant powered by Claude via OpenRouter. How can I help you today?"
                except Exception as api_error:
                    print(f"❌ API Error: {api_error}")
                    ai_response = "Hello! I'm your personal AI assistant powered by Claude via OpenRouter. How can I help you today?"

            # Send response (handle length)
            if len(ai_response) > 1900:
                await interaction.followup.send(ai_response[:1900] + "...")
            else:
                await interaction.followup.send(ai_response)

        except Exception as e:
            print(f"❌ Error in hello command: {e}")
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message("Hello! I'm your personal AI assistant. How can I help you today?", ephemeral=True)
                else:
                    await interaction.followup.send("Hello! I'm your personal AI assistant. How can I help you today?")
            except:
                print(f"❌ Failed to send hello response: {e}")

    @bot.tree.command(name="about", description="Ask about Eddrin's background and skills")
    async def about_command(interaction: discord.Interaction):
        """Command to get information about Eddrin"""
        try:
            await interaction.response.defer(ephemeral=False)
            
            if not openrouter_available:
                ai_response = get_about_response()
            else:
                try:
                    system_prompt = get_system_prompt("Tell me about Eddrin")
                    messages = [{"role": "user", "content": "Tell me about Eddrin Desiderio"}]
                    
                    ai_response = await asyncio.wait_for(
                        call_openrouter_api(messages, system_prompt),
                        timeout=15.0
                    )
                except asyncio.TimeoutError:
                    ai_response = get_about_response()
                except Exception as api_error:
                    print(f"❌ API Error: {api_error}")
                    ai_response = get_about_response()

            # Send response (handle length)
            if len(ai_response) > 1900:
                await interaction.followup.send(ai_response[:1900] + "...")
            else:
                await interaction.followup.send(ai_response)

        except Exception as e:
            print(f"❌ Error in about command: {e}")
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message("I can tell you about Eddrin Desiderio, but I'm having trouble accessing that information right now.", ephemeral=True)
                else:
                    await interaction.followup.send("I can tell you about Eddrin Desiderio, but I'm having trouble accessing that information right now.")
            except:
                print(f"❌ Failed to send about response: {e}")

    @bot.tree.command(name="refresh", description="Refresh bot commands (admin only)")
    async def refresh_command(interaction: discord.Interaction):
        """Command to refresh bot commands"""
        try:
            await interaction.response.defer(ephemeral=True)
            
            print("🔄 Manual command refresh requested...")
            
            # Clear and re-sync commands
            bot.tree.clear_commands()
            await setup_commands()
            synced = await bot.tree.sync()
            
            await interaction.followup.send(f"✅ Refreshed {len(synced)} commands successfully!", ephemeral=True)
            print(f"✅ Manual refresh completed: {len(synced)} commands synced")
            
        except Exception as e:
            print(f"❌ Error in refresh command: {e}")
            try:
                await interaction.followup.send(f"❌ Failed to refresh commands: {e}", ephemeral=True)
            except:
                print(f"❌ Failed to send refresh error: {e}")

# Add message-based commands as backup
@bot.event
async def on_message(message):
    """Handle message-based commands as backup"""
    if message.author == bot.user:
        return
    
    # Simple message-based commands for backup
    if message.content.lower().startswith('!chat '):
        query = message.content[6:]  # Remove '!chat '
        
        if not openrouter_available:
            response = get_fallback_response(query)
        else:
            try:
                system_prompt = get_system_prompt(query)
                messages = [{"role": "user", "content": query}]
                response = await asyncio.wait_for(
                    call_openrouter_api(messages, system_prompt),
                    timeout=15.0
                )
            except Exception as e:
                print(f"❌ Message command error: {e}")
                response = get_fallback_response(query)
        
        # Send response (handle length)
        if len(response) > 1900:
            await message.channel.send(response[:1900] + "...")
        else:
            await message.channel.send(response)
    
    elif message.content.lower() in ['!hello', '!hi']:
        await message.channel.send("Hello! I'm your personal AI assistant. Use `/chat` for full functionality or `!chat <message>` as backup.")
    
    elif message.content.lower() == '!about':
        response = get_about_response()
        if len(response) > 1900:
            await message.channel.send(response[:1900] + "...")
        else:
            await message.channel.send(response)
    
    # Process other commands
    await bot.process_commands(message)

def main():
    """Main function to run the bot"""
    print("🚀 Starting FIXED Discord bot with Claude 3.5 Sonnet via OpenRouter...")
    print("🔧 This version includes:")
    print("   - Better command syncing")
    print("   - Improved error handling")
    print("   - Command refresh functionality")
    print("   - Message-based backup commands")
    
    try:
        bot.run(DISCORD_BOT_TOKEN, reconnect=True)
    except Exception as e:
        print(f"❌ Bot crashed: {e}")
        print("🔄 This is usually a temporary Discord connection issue.")
        print("💡 Try running the bot again in a few minutes.")
        print("🌐 Or test the Streamlit app instead: streamlit run deployment/streamlit_app_openrouter.py")

if __name__ == "__main__":
    main()
