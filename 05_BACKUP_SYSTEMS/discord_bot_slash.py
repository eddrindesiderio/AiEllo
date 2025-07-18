#!/usr/bin/env python3
"""
Discord Bot for Your Personal AI (Using Slash Commands)
This version uses slash commands to avoid privileged intent requirements.

Prerequisites:
- A Discord Bot Token (see Discord Developer Portal)
- The bot must be invited to your server with necessary permissions.

Run with: python deployment/discord_bot_slash.py
"""

import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables from multiple possible locations
load_dotenv()  # Load from current directory
load_dotenv(".env")  # Explicit .env file
load_dotenv("../.env")  # Parent directory

# Get Discord bot token
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not DISCORD_BOT_TOKEN:
    raise ValueError("❌ Discord bot token not found in .env file")

# Initialize Hugging Face client with better detection
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE")
print(f"🔍 Debug: HF API Key found: {'Yes' if HUGGINGFACE_API_KEY else 'No'}")
if HUGGINGFACE_API_KEY:
    print(f"🔍 Debug: HF API Key starts with: {HUGGINGFACE_API_KEY[:15]}...")
    print(f"🔍 Debug: HF API Key length: {len(HUGGINGFACE_API_KEY)} characters")

if not HUGGINGFACE_API_KEY or HUGGINGFACE_API_KEY == "your_huggingface_api_key_here":
    print("⚠️  Hugging Face API key not configured - using fallback responses")
    hf_client = None
else:
    try:
        hf_client = InferenceClient(token=HUGGINGFACE_API_KEY)
        print("✅ Hugging Face client initialized successfully")
        
        # Test the API connection
        try:
            test_response = hf_client.chat_completion(
                messages=[{"role": "user", "content": "test"}],
                model="HuggingFaceH4/zephyr-7b-beta",
                max_tokens=10,
                temperature=0.1
            )
            print("✅ Hugging Face API test successful")
        except Exception as test_error:
            print(f"⚠️  Hugging Face API test failed: {test_error}")
            print("🔄 Will use fallback responses when API fails")
            
    except Exception as e:
        print(f"❌ Failed to initialize Hugging Face client: {e}")
        hf_client = None

# Bot setup - Use only non-privileged intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Load personal information if available
PERSONAL_INFO = ""
if os.path.exists("personal_info.txt"):
    with open("personal_info.txt", "r", encoding="utf-8") as f:
        PERSONAL_INFO = f.read()

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
        if hf_client:
            return "Hello! I'm your personal AI assistant with full AI capabilities. How can I help you today?"
        else:
            return "Hello! I'm your personal AI assistant. I'm currently running in basic mode - add your Hugging Face API key for full AI capabilities."
    
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
    print('🤖 Bot is ready to chat!')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

@bot.tree.command(name="chat", description="Chat with your personal AI assistant")
async def chat_command(interaction: discord.Interaction, message: str):
    """Slash command for chatting with AI"""
    try:
        # Respond immediately to avoid timeout
        await interaction.response.defer()
        
        # Get AI response with timeout or use fallback
        if not hf_client:
            # Use fallback responses when API key is not configured
            ai_response = f"🔧 DEBUG: No HF client - using fallback for: {message}\n\n" + get_fallback_response(message)
        else:
            try:
                print(f"🔍 DEBUG: Attempting API call for message: {message}")
                # Prepare messages for AI
                system_prompt = get_system_prompt(message)
                messages_for_ai = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ]
                
                print(f"🔍 DEBUG: Using model: HuggingFaceH4/zephyr-7b-beta")
                response = await asyncio.wait_for(
                    asyncio.to_thread(
                        hf_client.chat_completion,
                        messages=messages_for_ai,
                        model="HuggingFaceH4/zephyr-7b-beta",
                        max_tokens=1000,  # Reduced to prevent long responses
                        temperature=0.2
                    ),
                    timeout=12.0  # Reduced timeout to avoid Discord limits
                )
                ai_response = response.choices[0].message.content
                print(f"✅ DEBUG: API Success! Response: {ai_response[:100]}...")
            except asyncio.TimeoutError:
                print(f"⏰ DEBUG: API Timeout after 12 seconds")
                ai_response = f"🔧 DEBUG: API Timeout - using fallback for: {message}\n\n" + get_fallback_response(message)
            except Exception as api_error:
                print(f"❌ DEBUG: API Error: {api_error}")
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

    except discord.NotFound:
        # Interaction expired, send a new message
        try:
            ai_response = get_fallback_response(message)
            await interaction.channel.send(f"**{interaction.user.mention}** asked: {message}\n\n{ai_response}")
        except Exception as fallback_error:
            print(f"❌ Fallback error: {fallback_error}")
    except Exception as e:
        print(f"❌ Error: {e}")
        try:
            await interaction.followup.send("Sorry, I encountered an error. Please try again later.")
        except:
            print(f"❌ Failed to send error message: {e}")

@bot.tree.command(name="hello", description="Say hello to your AI assistant")
async def hello_command(interaction: discord.Interaction):
    """Simple hello command"""
    await interaction.response.defer()
    
    try:
        # Get AI response for greeting
        system_prompt = get_system_prompt("Hello")
        messages_for_ai = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Hello"}
        ]

        if not hf_client:
            ai_response = "Hello! I'm your personal AI assistant. How can I help you today?"
        else:
            try:
                response = await asyncio.wait_for(
                    asyncio.to_thread(
                        hf_client.chat_completion,
                        messages=messages_for_ai,
                        model="HuggingFaceH4/zephyr-7b-beta",
                        max_tokens=500,
                        temperature=0.2
                    ),
                    timeout=10.0  # 10 second timeout for simple greeting
                )
                ai_response = response.choices[0].message.content
            except asyncio.TimeoutError:
                ai_response = "Hello! I'm your personal AI assistant. How can I help you today?"
            except Exception as api_error:
                print(f"❌ API Error: {api_error}")
                ai_response = "Hello! I'm your personal AI assistant. How can I help you today?"

        # Send response (handle length)
        if len(ai_response) > 1900:
            await interaction.followup.send(ai_response[:1900] + "...")
        else:
            await interaction.followup.send(ai_response)

    except Exception as e:
        print(f"❌ Error: {e}")
        await interaction.followup.send("Hello! I'm your personal AI assistant. How can I help you today?")

@bot.tree.command(name="about", description="Ask about Eddrin's background and skills")
async def about_command(interaction: discord.Interaction):
    """Command to get information about Eddrin"""
    await interaction.response.defer()
    
    try:
        # Get AI response about personal info
        system_prompt = get_system_prompt("Tell me about Eddrin")
        messages_for_ai = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Tell me about Eddrin Desiderio"}
        ]

        if not hf_client:
            ai_response = get_about_response()
        else:
            try:
                response = await asyncio.wait_for(
                    asyncio.to_thread(
                        hf_client.chat_completion,
                        messages=messages_for_ai,
                        model="HuggingFaceH4/zephyr-7b-beta",
                        max_tokens=1000,
                        temperature=0.2
                    ),
                    timeout=15.0  # 15 second timeout
                )
                ai_response = response.choices[0].message.content
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
        print(f"❌ Error: {e}")
        await interaction.followup.send("I can tell you about Eddrin Desiderio, but I'm having trouble accessing that information right now.")

def main():
    """Main function to run the bot"""
    print("🚀 Starting Discord bot with slash commands...")
    try:
        bot.run(DISCORD_BOT_TOKEN, reconnect=True)
    except Exception as e:
        print(f"❌ Bot crashed: {e}")
        print("🔄 This is usually a temporary Discord connection issue.")
        print("💡 Try running the bot again in a few minutes.")
        print("🌐 Or test the Streamlit app instead: streamlit run deployment/streamlit_app.py")

if __name__ == "__main__":
    main()
