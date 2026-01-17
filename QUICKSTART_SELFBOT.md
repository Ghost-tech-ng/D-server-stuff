# Quick Start: Self-Bot Setup

## ⚠️ WARNING
**Self-bots violate Discord ToS and can result in permanent account ban!**

---

## 🚀 Quick Setup (5 Steps)

### 1️⃣ Get Your Discord User Token

**In your web browser (NOT Discord app):**
1. Open Discord: https://discord.com/app
2. Press **F12** (Developer Tools)
3. Go to **Network** tab
4. Press **F5** (reload)
5. Click any request → Find **"Authorization"** header
6. Copy the long token string

### 2️⃣ Create `.env` File

```bash
copy .env.sample .env
```

### 3️⃣ Edit `.env` File

```env
DISCORD_USER_TOKEN=paste_your_token_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

### 4️⃣ Run the Bot

```bash
python bot.py
```

### 5️⃣ Verify It's Working

✅ Console shows: "Self-bot is ACTIVE and running"  
✅ Telegram receives startup notification  
✅ Type `!ping` in Discord → Bot responds "Pong!"

---

## 📱 Status Monitoring

**How to know the bot is working:**

1. **Console Output** - Shows all activity in real-time
2. **Telegram Notifications** - Instant alerts for:
   - Bot startup
   - New member joins
   - Server joins
3. **Ping Command** - Type `!ping` in any channel

---

## 🎯 What It Does

- ✅ Monitors ALL servers you're in
- ✅ Detects when new members join
- ✅ Sends instant Telegram notifications
- ✅ Saves data to JSON files (one per server)
- ✅ Runs continuously until you stop it

---

## 🛑 How to Stop

**Method 1:** Type `!stopbot` in Discord  
**Method 2:** Press `Ctrl+C` in terminal

Both methods save all data and send files to Telegram.

---

## 📁 Output Files

Format: `join_logs_ServerName_123456789.json`

Each server gets its own file with member join data.

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Invalid user token" | Re-extract token from browser |
| "You are not in any servers" | Join servers with your Discord account |
| No Telegram notifications | Check `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` |
| Bot doesn't detect joins | Test with smaller servers (< 1000 members) |

---

## 📚 Full Documentation

- [SELFBOT_SETUP.md](SELFBOT_SETUP.md) - Complete setup guide
- [TELEGRAM_SETUP.md](TELEGRAM_SETUP.md) - Telegram configuration
- [walkthrough.md](C:\Users\hp\.gemini\antigravity\brain\a849f641-2b93-4a81-a784-c04b76f0c986\walkthrough.md) - Implementation details

---

## ⚡ Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.sample .env

# Run the bot
python bot.py
```

---

**Remember: This violates Discord ToS. Use at your own risk!** ⚠️
