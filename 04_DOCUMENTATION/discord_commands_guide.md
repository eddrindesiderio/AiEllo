# How to Command Your AI in Discord

## 🤖 Two Ways to Use Your AI Bot

### Method 1: Slash Commands Bot (Recommended - Easier)

**Start the slash commands bot:**
```bash
python deployment/discord_bot_slash.py
```

**Available Commands:**

1. **`/hello`** - Simple greeting
   ```
   /hello
   ```
   *AI will respond with a natural greeting*

2. **`/chat message: [your question]`** - General chat
   ```
   /chat message: What is 2+2?
   /chat message: Hello, how are you?
   /chat message: Can you help me with coding?
   ```

3. **`/about`** - Get information about Eddrin
   ```
   /about
   ```
   *AI will share your personal information and skills*

### Method 2: Mention-Based Bot (Traditional)

**Start the mention bot:**
```bash
python deployment/discord_bot.py
```

**How to use:**
- **Mention the bot** by typing `@YourBotName` followed by your message

**Examples:**
```
@YourBotName Hello
@YourBotName What is 2+2?
@YourBotName Who is Eddrin?
@YourBotName What are my skills?
@YourBotName Can you help me with web development?
```

## 📝 Step-by-Step Instructions

### Step 1: Get Your Hugging Face API Key
1. Go to: https://huggingface.co/settings/tokens
2. Click "New token"
3. Give it a name (e.g., "Discord Bot")
4. Copy the token

### Step 2: Update Your .env File
Open your `.env` file and replace the placeholder:
```
DISCORD_BOT_TOKEN=MTM5NTM5MDk0MjY1OTM0NjU1NA.GiJeEg.H_pNPQyOgWQOisYS8G01MkEjTOof29ee0EegN8
HUGGINGFACE=your_actual_huggingface_token_here
```

### Step 3: Start Your Bot
Choose one:
```bash
# Option A: Slash Commands (Easier)
python deployment/discord_bot_slash.py

# Option B: Mention-Based (Traditional)
python deployment/discord_bot.py
```

### Step 4: Test in Discord

**For Slash Commands:**
1. Type `/` in any channel
2. You'll see your bot's commands appear
3. Click on the command you want
4. Fill in any required fields
5. Press Enter

**For Mention Bot:**
1. Type `@` and start typing your bot's name
2. Select your bot from the dropdown
3. Add your message after the mention
4. Press Enter

## 🎯 Example Conversations

### Slash Commands Examples:
```
You: /hello
Bot: Hello! I'm your personal AI assistant. How can I help you today?

You: /chat message: What is 5 + 3?
Bot: 5 + 3 = 8

You: /about
Bot: I can tell you about Eddrin Desiderio! He holds a Bachelor of Science in Information Technology from STI College Tanauan, where he was recognized as the best programmer during his senior high school years...

You: /chat message: Who is Eddrin?
Bot: Eddrin Desiderio is a web developer who specializes in turning design concepts into interactive digital experiences using HTML, CSS, and JavaScript...
```

### Mention-Based Examples:
```
You: @YourBot Hello
Bot: Hello! I'm your personal AI assistant. How can I help you today?

You: @YourBot What is 5 + 3?
Bot: 5 + 3 = 8

You: @YourBot Who is Eddrin?
Bot: Eddrin Desiderio is a web developer who specializes in turning design concepts into interactive digital experiences using HTML, CSS, and JavaScript...
```

## 🔧 Troubleshooting

**Bot doesn't respond:**
- Make sure the bot is running (check your terminal)
- Check if bot has permissions in the channel
- For slash commands: Wait a few minutes for Discord to sync commands

**"API key not found" error:**
- Make sure you added your Hugging Face API key to .env file
- Restart the bot after updating .env

**Slash commands not showing:**
- Wait 5-10 minutes for Discord to sync
- Try restarting the bot
- Make sure bot has "Use Slash Commands" permission

## 💡 Pro Tips

1. **Use slash commands** - They're easier and don't require special permissions
2. **Be specific** - Ask clear questions for better responses
3. **Test different scenarios** - Try math, general questions, and personal questions
4. **Keep the bot running** - The bot only works while the Python script is running

Your AI bot will now respond naturally to general questions and only share your personal information when specifically asked!
