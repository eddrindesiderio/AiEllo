#!/usr/bin/env python3
"""
Discord Bot for Your Personal AI
This script connects your AI to Discord, allowing you to interact with it in a server.

Prerequisites:
- A Discord Bot Token (see Discord Developer Portal)
- The bot must be invited to your server with necessary permissions.

Run with: python deployment/discord_bot.py
"""

import discord
import os
import asyncio
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

# Get Discord bot token
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not DISCORD_BOT_TOKEN:
    raise ValueError("❌ Discord bot token not found in .env file")

# Initialize Hugging Face client
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE")
if not HUGGINGFACE_API_KEY:
    raise ValueError("❌ Hugging Face API key not found in .env file")

hf_client = InferenceClient(token=HUGGINGFACE_API_KEY)

# Bot setup - Use only non-privileged intents
intents = discord.Intents.default()
# Remove privileged intents to avoid permission issues
intents.message_content = False
bot = discord.Client(intents=intents)

# Load personal information if available
PERSONAL_INFO = ""
if os.path.exists("personal_info.txt"):
    with open("personal_info.txt", "r", encoding="utf-8") as f:
        PERSONAL_INFO = f.read()

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

@bot.event
async def on_message(message):
    """Event handler for when a message is received"""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Respond to mentions (handle both old and new mention formats)
    if bot.user.mentioned_in(message):
        # Clean the message content by removing bot mentions
        user_message = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
        
        # If message content is empty due to privileged intents, use a default response
        if not user_message:
            user_message = "Hello"
        
        async with message.channel.typing():
            try:
                # Prepare messages for AI
                system_prompt = get_system_prompt(user_message)
                messages_for_ai = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]

                # Get AI response with timeout
                try:
                    response = await asyncio.wait_for(
                        asyncio.to_thread(
                            hf_client.chat_completion,
                            messages=messages_for_ai,
                            model="HuggingFaceH4/zephyr-7b-beta",
                            max_tokens=1000,  # Reduced to prevent long responses
                            temperature=0.2
                        ),
                        timeout=15.0  # 15 second timeout
                    )
                    ai_response = response.choices[0].message.content
                except asyncio.TimeoutError:
                    ai_response = "Sorry, I'm taking too long to respond. Please try a simpler question."
                except Exception as api_error:
                    print(f"❌ API Error: {api_error}")
                    ai_response = "I'm having trouble connecting to my AI service. Please try again in a moment."

                # Send response (split if too long)
                if len(ai_response) > 2000:
                    # Split long messages into chunks
                    chunks = [ai_response[i:i+2000] for i in range(0, len(ai_response), 2000)]
                    for chunk in chunks:
                        await message.channel.send(chunk)
                else:
                    await message.channel.send(ai_response)

            except Exception as e:
                print(f"❌ Error: {e}")
                await message.channel.send("Sorry, I encountered an error. Please try again later.")

def main():
    """Main function to run the bot"""
    print("🚀 Starting Discord bot...")
    bot.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    main()
