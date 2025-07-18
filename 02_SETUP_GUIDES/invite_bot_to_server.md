# Fix "Unknown Integration" Error - Bot Invitation Guide

## 🚨 Current Issue
Your bot is showing "Unknown Integration" which means it needs proper permissions and slash command access.

## 🔧 Solution: Re-invite Your Bot

### Step 1: Get Your Bot's Application ID
1. Go to https://discord.com/developers/applications
2. Click on your bot application
3. Copy the **Application ID** from the General Information page

### Step 2: Generate Proper Invitation URL
Replace `YOUR_APPLICATION_ID` with your actual Application ID in this URL:

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_APPLICATION_ID&permissions=2048&scope=bot%20applications.commands
```

**Important Permissions Included:**
- ✅ `bot` - Basic bot functionality
- ✅ `applications.commands` - Slash commands support
- ✅ `Send Messages` permission (2048)

### Step 3: Invite Bot to Your Server
1. Open the generated URL in your browser
2. Select the server where you want to add the bot
3. Click "Authorize"
4. Complete any captcha if prompted

### Step 4: Restart Your Bot
After re-inviting, restart your bot:
```bash
python deployment/discord_bot_slash.py
```

You should see:
```
✅ Logged in as YourBotName#1234
🤖 Bot is ready to chat!
✅ Synced 3 command(s)
```

### Step 5: Test Slash Commands
In Discord, type `/` and you should see:
- `/hello` - Say hello to your AI assistant
- `/chat` - Chat with your personal AI assistant  
- `/about` - Ask about Eddrin's background and skills

## 🎯 Quick Test Commands
Once working, test these:
- `/hello`
- `/chat message: What is 2+2?`
- `/chat message: What are my skills?`
- `/about`

## ⚠️ If Still Not Working
1. Make sure the bot has "Send Messages" permission in the channel
2. Check that the bot role is above other roles (if needed)
3. Verify the bot is online (green status)
4. Try in a different channel or server

## 🔍 Debug Information
Your bot will show debug info when starting:
```
🔍 Debug: HF API Key found: Yes
🔍 Debug: HF API Key starts with: hf_ampqVnM...
✅ Hugging Face client initialized successfully
```

This confirms your API key is working properly.
