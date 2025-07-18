#!/usr/bin/env python3
"""
Simple Discord Bot Connection Test
This will test if your bot can connect to Discord.
"""

import discord
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Discord bot token
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not DISCORD_BOT_TOKEN:
    print("❌ Discord bot token not found in .env file")
    print("Make sure your .env file has: DISCORD_BOT_TOKEN=your_token_here")
    exit(1)

print(f"✅ Found Discord token starting with: {DISCORD_BOT_TOKEN[:20]}...")

# Simple bot setup
intents = discord.Intents.default()
intents.message_content = True  # This requires Message Content Intent to be enabled
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot connected successfully!')
    print(f'   Logged in as: {bot.user}')
    print(f'   Bot ID: {bot.user.id}')
    print(f'   Connected to {len(bot.guilds)} server(s):')
    
    for guild in bot.guilds:
        print(f'   - {guild.name} (ID: {guild.id})')
    
    print('\n🤖 Bot is ready to receive messages!')
    print('Try mentioning the bot in Discord now...')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    print(f"📨 Received message: '{message.content}' from {message.author}")
    
    # Respond to mentions
    if bot.user.mentioned_in(message):
        print("🎯 Bot was mentioned! Sending response...")
        await message.channel.send("Hello! I can see your mention. The bot is working!")
    else:
        print("   (Bot was not mentioned)")

print("🚀 Starting Discord bot connection test...")

try:
    bot.run(DISCORD_BOT_TOKEN)
except discord.errors.PrivilegedIntentsRequired:
    print("\n❌ PRIVILEGED INTENTS ERROR!")
    print("This means 'Message Content Intent' is not enabled.")
    print("\nTo fix this:")
    print("1. Go to: https://discord.com/developers/applications")
    print("2. Select your bot application")
    print("3. Go to 'Bot' section")
    print("4. Scroll down to 'Privileged Gateway Intents'")
    print("5. Enable 'Message Content Intent'")
    print("6. Save changes and restart the bot")
    print("\nOR use the slash commands bot instead:")
    print("   python deployment/discord_bot_slash.py")
except Exception as e:
    print(f"❌ Connection failed: {e}")
