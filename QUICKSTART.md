# Discord Member Tracking Bot - Quick Start

## 🚀 What This Bot Does

Tracks all members who join your Discord servers and sends the data to your Telegram account.

---

## ⚡ Quick Setup (5 Minutes)

### 1. Get Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create application → Add Bot
3. Enable "SERVER MEMBERS INTENT"
4. Copy bot token

### 2. Get Telegram Bot Token
1. Open Telegram → Search **@BotFather**
2. Send `/newbot` and follow prompts
3. Copy bot token

### 3. Get Your Telegram Chat ID
1. Search **@userinfobot** on Telegram
2. Send `/start`
3. Copy your Chat ID

### 4. Configure Bot
Create `.env` file:
```env
DISCORD_BOT_TOKEN=your_discord_token
TELEGRAM_BOT_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id
TIMER_HOURS=24
```

### 5. Run Bot
```bash
pip install -r requirements.txt
python bot.py
```

### 6. Add to Discord Servers
- Copy invite link from console
- Open in browser
- Select servers to track
- Authorize

---

## 📱 What You Get

After 24 hours, bot automatically:
1. ✅ Saves all data to JSON files
2. ✅ Sends files to your Telegram
3. ✅ Shuts down gracefully

Each server gets its own file:
- `join_logs_ServerName_123456.json`

---

## 🌐 Deploy on Render (Free Hosting)

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for full guide.

**Quick steps:**
1. Push code to GitHub
2. Create Render account
3. New Background Worker → Connect repo
4. Add environment variables
5. Deploy!

---

## 📚 Documentation

- **[README.md](README.md)** - Full documentation
- **[TELEGRAM_SETUP.md](TELEGRAM_SETUP.md)** - Telegram setup guide
- **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** - Hosting guide

---

## ✨ Features

✅ Multi-server tracking  
✅ Separate files per server  
✅ Auto-disable timer  
✅ Telegram file delivery  
✅ Discord reports (optional)  
✅ Free hosting compatible  

---

**Made with Python and discord.py** 🐍
