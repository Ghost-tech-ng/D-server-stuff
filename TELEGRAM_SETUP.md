# Telegram Integration Setup Guide

Complete guide to set up Telegram integration for your Discord Member Tracking Bot.

---

## 📱 What This Does

The bot will automatically send all JSON data files to your Telegram account before shutting down. This ensures you never lose your tracking data, even on free hosting platforms like Render!

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Create a Telegram Bot

1. **Open Telegram** on your phone or computer
2. **Search for @BotFather** (official Telegram bot)
3. **Send:** `/start`
4. **Send:** `/newbot`
5. **Follow the prompts:**
   - Choose a name (e.g., "Discord Tracker")
   - Choose a username (must end in "bot", e.g., "discord_tracker_bot")
6. **Copy the bot token** - It looks like this:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
   ⚠️ **Keep this secret!**

---

### Step 2: Get Your Chat ID

1. **Search for @userinfobot** on Telegram
2. **Send:** `/start`
3. **Copy your Chat ID** - It's a number like:
   ```
   123456789
   ```

---

### Step 3: Add to Configuration

Edit your `.env` file and add:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

**That's it!** The bot will now send files to your Telegram automatically.

---

## 📊 What You'll Receive

When the bot shuts down, you'll get:

1. **Summary Message:**
   ```
   🤖 Discord Member Tracker - Final Report
   
   📊 Total Members Tracked: 342
   🖥️ Servers Tracked: 2
   
   📁 Sending 2 data file(s)...
   ```

2. **JSON Files:**
   - Each server's data file sent separately
   - With caption showing server name and member count
   - Example: `join_logs_Gaming_Community_111222333.json`

3. **Completion Message:**
   ```
   ✅ All data files sent successfully!
   
   Total files: 2
   ```

---

## 🔧 For Render Deployment

Add these environment variables in Render:

1. Go to your Render service
2. Click "Environment" tab
3. Add:
   ```
   TELEGRAM_BOT_TOKEN = your_bot_token_here
   TELEGRAM_CHAT_ID = your_chat_id_here
   ```
4. Click "Save Changes"
5. Render will auto-redeploy

---

## ✅ Testing

To test if it works:

1. Set `TIMER_HOURS=0.05` (3 minutes) in `.env`
2. Run the bot
3. Wait 3 minutes
4. Check your Telegram - you should receive the files!

---

## 🐛 Troubleshooting

### "Failed to send files to Telegram"
- Check bot token is correct
- Make sure you've started a chat with your bot (send `/start`)
- Verify chat ID is correct

### "Unauthorized" error
- Bot token is invalid
- Create a new bot with @BotFather

### Files not received
- Check you sent `/start` to your bot
- Verify chat ID matches your account
- Check bot logs for errors

---

## 💡 Pro Tips

1. **Start a chat with your bot first** - Send `/start` to ensure it can message you
2. **Test with short timer** - Use `TIMER_HOURS=0.05` for quick testing
3. **Check Telegram on mobile** - Files are easier to download on mobile
4. **Keep bot token secret** - Never share it publicly

---

## 📝 Example .env File

```env
# Discord Bot
DISCORD_BOT_TOKEN=your_discord_token_here
TIMER_HOURS=24

# Telegram Integration
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# Optional
REPORT_CHANNEL_ID=
ADMIN_USER_ID=
```

---

## 🎉 Benefits

✅ **Never lose data** - Files sent before shutdown  
✅ **Works on free hosting** - Perfect for Render/Railway  
✅ **Automatic** - No manual downloads needed  
✅ **Instant access** - Files in your Telegram immediately  
✅ **Mobile friendly** - Download files on your phone  

---

**Your tracking data is now safe in Telegram!** 🚀
