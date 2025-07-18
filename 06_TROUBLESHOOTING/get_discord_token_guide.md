# How to Get Your Discord Bot Token

## 🚨 Current Issue
Your Discord bot token in the .env file is set to `your_discord_bot_token_here` which is just a placeholder. You need your actual bot token.

## 📋 Step-by-Step Instructions

### Step 1: Go to Discord Developer Portal
1. Visit: https://discord.com/developers/applications
2. Log in with your Discord account

### Step 2: Create or Select Your Bot Application
**If you don't have a bot yet:**
1. Click "New Application"
2. Give it a name (e.g., "My Personal AI Bot")
3. Click "Create"

**If you already have a bot:**
1. Click on your existing application

### Step 3: Get Your Bot Token
1. Click on "Bot" in the left sidebar
2. Under "Token" section, click "Reset Token" (if needed)
3. Click "Copy" to copy your bot token
4. **IMPORTANT**: Keep this token secret!

### Step 4: Update Your .env File
Open your `.env` file and replace this line:
```
DISCORD_BOT_TOKEN=your_discord_bot_token_here
```

With your actual token:
```
DISCORD_BOT_TOKEN=YOUR_ACTUAL_TOKEN_HERE
```

### Step 5: Invite Your Bot to a Server
1. In Discord Developer Portal, go to "OAuth2" → "URL Generator"
2. Select these scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select these bot permissions:
   - ✅ Send Messages
   - ✅ Use Slash Commands
   - ✅ Read Message History
4. Copy the generated URL and open it in your browser
5. Select a server and authorize the bot

### Step 6: Test Your Bot
After updating the .env file with your real token:
```bash
python deployment/discord_bot_slash.py
```

You should see:
```
✅ Logged in as YourBotName#1234
🤖 Bot is ready to chat!
✅ Synced 3 command(s)
```

## 🎯 Quick Test Commands
Once your bot is running, test in Discord:
- `/hello`
- `/chat message: What are my skills?`
- `/about`

## ⚠️ Security Note
- Never share your bot token publicly
- Never commit it to version control
- Keep your .env file private
