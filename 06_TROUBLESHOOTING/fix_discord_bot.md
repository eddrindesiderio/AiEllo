# Fix Discord Bot Not Responding to Mentions

## 🔧 Most Likely Issue: Message Content Intent

Your bot probably can't read message content because the **Message Content Intent** is not enabled.

### Step 1: Enable Message Content Intent

1. **Go to Discord Developer Portal**
   - Visit: https://discord.com/developers/applications
   - Click on your bot application

2. **Enable the Intent**
   - Go to "Bot" section (left sidebar)
   - Scroll down to "Privileged Gateway Intents"
   - ✅ **Enable "Message Content Intent"**
   - Click "Save Changes"

3. **Restart Your Bot**
   - Stop your current bot (Ctrl+C)
   - Run it again: `python deployment/discord_bot.py`

### Step 2: Alternative - Use Slash Commands (Easier)

If you don't want to deal with intents, use the slash commands bot:

```bash
python deployment/discord_bot_slash.py
```

Then use these commands in Discord:
- `/hello`
- `/chat message: What is 2+2?`
- `/about`

### Step 3: Check Your Setup

Run this to check your setup:
```bash
python test_bot_connection.py
```

**What you should see:**
```
✅ Found Discord token starting with: MTM5NTM5...
🚀 Starting Discord bot connection test...
✅ Bot connected successfully!
   Logged in as: YourBotName#1234
   Bot ID: 123456789
   Connected to 1 server(s):
   - Your Server Name (ID: 987654321)
🤖 Bot is ready to receive messages!
```

### Step 4: Test in Discord

**For Mention Bot:**
```
@YourBotName Hello
```

**For Slash Commands Bot:**
```
/hello
```

## 🚨 Common Issues & Solutions

### Issue 1: "PrivilegedIntentsRequired" Error
**Solution:** Enable Message Content Intent (Step 1 above)

### Issue 2: "400 Bad Request - Must be 2000 or fewer in length" Error
**Solution:** ✅ **FIXED!** Both bots now automatically split long messages
- Messages over 2000 characters are automatically split into chunks
- No action needed - the bots handle this automatically

### Issue 3: "Heartbeat blocked for more than 10 seconds" Error
**Solution:** ✅ **FIXED!** Added timeout handling to prevent API blocking
- API calls now have 15-second timeouts
- Bot responds with fallback messages if AI service is slow
- Discord heartbeat stays active during long operations

### Issue 4: Bot Connects But Doesn't Respond
**Possible causes:**
- Bot doesn't have permission to send messages in the channel
- You're not mentioning the bot correctly
- Bot is not in the server

**Solutions:**
- Make sure bot has "Send Messages" permission
- Use `@BotName` (not just the name)
- Re-invite bot to server with proper permissions

### Issue 5: "API key not found" Error
**Solution:** You still need to add your Hugging Face API key:
1. Go to: https://huggingface.co/settings/tokens
2. Create a new token
3. Add it to your .env file:
   ```
   HUGGINGFACE=your_actual_token_here
   ```

### Issue 6: Slash Commands Not Showing
**Solutions:**
- Wait 5-10 minutes for Discord to sync commands
- Restart the bot
- Make sure bot has "Use Slash Commands" permission

## 🎯 Quick Test Commands

Once your bot is working, test these:

**General Questions (should NOT mention personal info):**
- `@YourBot Hello`
- `@YourBot What is 2+2?`
- `@YourBot How are you?`

**Personal Questions (should mention your info):**
- `@YourBot Who is Eddrin?`
- `@YourBot What are my skills?`
- `@YourBot Tell me about myself`

## 💡 Recommended Solution

**Use the slash commands bot** - it's easier and doesn't require special permissions:

```bash
python deployment/discord_bot_slash.py
```

Then use `/chat message: your question` in Discord.
