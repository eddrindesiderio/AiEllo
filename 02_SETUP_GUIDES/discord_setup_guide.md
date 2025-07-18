# How to Add Your AI to Discord Server

## Step 1: Create a Discord Bot

1. **Go to Discord Developer Portal**
   - Visit: https://discord.com/developers/applications
   - Click "New Application"
   - Give it a name (e.g., "Eddrin AI Assistant")

2. **Create the Bot**
   - Go to "Bot" section in the left sidebar
   - Click "Add Bot"
   - Copy the Bot Token (keep this secret!)

3. **Set Bot Permissions & Intents**
   - In the Bot section, scroll down to "Privileged Gateway Intents"
   - ✅ Enable "Message Content Intent" (required for mention-based bot)
   - Enable these bot permissions:
     - ✅ Send Messages
     - ✅ Read Message History
     - ✅ Use Slash Commands
     - ✅ Mention Everyone (if needed)

## Step 2: Invite Bot to Your Server

1. **Generate Invite Link**
   - Go to "OAuth2" → "URL Generator"
   - Select Scopes: ✅ `bot`
   - Select Bot Permissions:
     - ✅ Send Messages
     - ✅ Read Message History
     - ✅ Use Slash Commands

2. **Copy the Generated URL**
   - Copy the generated URL at the bottom
   - Open it in your browser
   - Select your Discord server
   - Click "Authorize"

## Step 3: Configure Your Environment

1. **Add Discord Bot Token to .env file**
   ```
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   HUGGINGFACE=your_huggingface_api_key_here
   ```

2. **Make sure you have the required packages**
   ```bash
   pip install discord.py python-dotenv huggingface_hub
   ```

## Step 4: Choose Your Bot Type

### Option A: Mention-Based Bot (Requires Message Content Intent)
1. **Make sure you enabled "Message Content Intent" in Step 1**
2. **Start the bot**
   ```bash
   python deployment/discord_bot.py
   ```

### Option B: Slash Commands Bot (No Special Permissions Needed)
1. **Start the slash command bot**
   ```bash
   python deployment/discord_bot_slash.py
   ```

2. **You should see:**
   ```
   🚀 Starting Discord bot...
   ✅ Logged in as YourBotName#1234
   🤖 Bot is ready to chat!
   ✅ Synced X command(s)
   ```

## Step 5: Test Your Bot

### For Mention-Based Bot:
1. **In your Discord server, mention the bot:**
   ```
   @YourBotName Hello
   ```

2. **Test different scenarios:**
   - `@YourBotName What is 2+2?` (should give correct math answer)
   - `@YourBotName Hello` (should respond naturally without personal info)
   - `@YourBotName Who is Eddrin?` (should use your personal information)
   - `@YourBotName What are my skills?` (should use your personal information)

### For Slash Commands Bot:
1. **Use slash commands:**
   ```
   /hello
   /chat message: What is 2+2?
   /about
   /chat message: Who is Eddrin?
   ```

2. **Available slash commands:**
   - `/hello` - Simple greeting
   - `/chat message: [your question]` - General chat
   - `/about` - Information about Eddrin

## Features of Your Discord Bot

✅ **Smart Personal Information**: Only shares your info when specifically asked
✅ **Natural Conversations**: Responds naturally to greetings and general questions
✅ **Accurate Answers**: Gives correct answers to math and factual questions
✅ **Mention-Based**: Only responds when mentioned (won't spam channels)
✅ **Error Handling**: Gracefully handles API errors

## Troubleshooting

**"PrivilegedIntentsRequired" error:**
- Go to Discord Developer Portal → Your App → Bot
- Enable "Message Content Intent" under Privileged Gateway Intents
- OR use the slash commands bot instead: `python deployment/discord_bot_slash.py`

**Bot doesn't respond:**
- Check if bot has "Send Messages" permission in the channel
- Make sure you're mentioning the bot correctly (mention-based) or using slash commands
- Check console for error messages

**"API key not found" error:**
- Make sure your .env file has both DISCORD_BOT_TOKEN and HUGGINGFACE keys
- Restart the bot after adding keys

**Slash commands not showing:**
- Wait a few minutes for Discord to sync the commands
- Try restarting the bot
- Make sure bot has "Use Slash Commands" permission

**Bot responds to everything:**
- The mention-based bot only responds to mentions
- The slash command bot only responds to slash commands

## Security Notes

🔒 **Keep your tokens secret!**
- Never share your Discord bot token
- Never commit .env file to version control
- Regenerate tokens if accidentally exposed

Your Discord bot is now ready and will behave just like the fixed Streamlit app - natural responses for general questions, and accurate personal information only when specifically asked!
