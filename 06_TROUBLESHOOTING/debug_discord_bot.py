#!/usr/bin/env python3
"""
Debug version of Discord bot to check API key issues
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

print("🔍 DEBUG: Loading environment variables...")

# Get Discord bot token
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
print(f"Discord token found: {'Yes' if DISCORD_BOT_TOKEN else 'No'}")

# Get Hugging Face API key
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE")
print(f"Hugging Face key found: {'Yes' if HUGGINGFACE_API_KEY else 'No'}")

if HUGGINGFACE_API_KEY:
    print(f"API Key starts with: {HUGGINGFACE_API_KEY[:10]}...")
    print(f"API Key length: {len(HUGGINGFACE_API_KEY)} characters")
    
    if HUGGINGFACE_API_KEY == "your_huggingface_api_key_here":
        print("❌ API key is placeholder")
        hf_client = None
    else:
        print("✅ API key looks valid")
        try:
            hf_client = InferenceClient(token=HUGGINGFACE_API_KEY)
            print("✅ Hugging Face client created successfully")
        except Exception as e:
            print(f"❌ Failed to create HF client: {e}")
            hf_client = None
else:
    print("❌ No Hugging Face API key found")
    hf_client = None

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot logged in as {bot.user}')
    print(f'HF Client status: {"Available" if hf_client else "Not available"}')
    
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

@bot.tree.command(name="debug", description="Debug API status")
async def debug_command(interaction: discord.Interaction):
    await interaction.response.defer()
    
    status_msg = f"""
🔍 **Debug Information:**

**Environment Variables:**
- Discord Token: {'✅ Found' if DISCORD_BOT_TOKEN else '❌ Missing'}
- HuggingFace Key: {'✅ Found' if HUGGINGFACE_API_KEY else '❌ Missing'}

**API Client Status:**
- HuggingFace Client: {'✅ Ready' if hf_client else '❌ Not Available'}

**Key Details:**
- HF Key Length: {len(HUGGINGFACE_API_KEY) if HUGGINGFACE_API_KEY else 'N/A'}
- HF Key Preview: {HUGGINGFACE_API_KEY[:10] + '...' if HUGGINGFACE_API_KEY else 'N/A'}
"""
    
    await interaction.followup.send(status_msg)

@bot.tree.command(name="testai", description="Test AI response")
async def testai_command(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    
    if not hf_client:
        await interaction.followup.send("❌ Hugging Face client not available. Using fallback response.")
        return
    
    try:
        response = hf_client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
            model="HuggingFaceH4/zephyr-7b-beta",
            max_tokens=200,
            temperature=0.2
        )
        ai_response = response.choices[0].message.content
        await interaction.followup.send(f"✅ AI Response: {ai_response}")
    except Exception as e:
        await interaction.followup.send(f"❌ API Error: {str(e)}")

def main():
    print("🚀 Starting debug Discord bot...")
    if not DISCORD_BOT_TOKEN:
        print("❌ No Discord token found!")
        return
    
    bot.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    main()
