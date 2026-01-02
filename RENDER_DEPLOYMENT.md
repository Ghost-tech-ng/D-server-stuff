# Deploying to Render as Web Service (FREE)

Complete guide to deploy your Discord bot on Render's **free Web Service** tier using UptimeRobot to keep it alive.

---

## 🆓 Why Web Service Instead of Background Worker?

- ✅ **Background Worker** = Paid ($7/month)
- ✅ **Web Service** = FREE (750 hours/month)
- ✅ **With UptimeRobot** = Stays awake 24/7

---

## 🚀 Step-by-Step Deployment

### Step 1: Update Your Code

The bot now includes a health server that responds to HTTP requests. This is already added to your code!

**Files added:**
- `health_server.py` - HTTP server for health checks
- Updated `bot.py` - Starts health server automatically

### Step 2: Push to GitHub

```bash
git add .
git commit -m "Add health server for Render web service"
git push
```

### Step 3: Deploy on Render

1. **Go to Render:**
   - Visit [render.com](https://render.com)
   - Sign in with GitHub

2. **Create New Web Service:**
   - Click "New +" → Select **"Web Service"** (NOT Background Worker!)
   - Click "Build and deploy from a Git repository"
   - Connect your `D-server-stuff` repository

3. **Configure Service:**
   - **Name:** `discord-member-tracker`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`

4. **Add Environment Variables:**
   Click "Advanced" → Add these:
   
   ```
   DISCORD_BOT_TOKEN = your_discord_token
   TELEGRAM_BOT_TOKEN = your_telegram_token
   TELEGRAM_CHAT_ID = your_chat_id
   TIMER_HOURS = 24
   PORT = 8080
   ```

5. **Select Plan:**
   - Choose **"Free"** plan
   - Click "Create Web Service"

6. **Get Your Service URL:**
   - After deployment, Render gives you a URL like:
   - `https://discord-member-tracker.onrender.com`
   - **Copy this URL!** You'll need it for UptimeRobot

---

## 🔄 Step 4: Set Up UptimeRobot (Keep Bot Alive)

Render free tier sleeps after 15 minutes of inactivity. UptimeRobot pings your bot every 5 minutes to keep it awake.

### Setup UptimeRobot:

1. **Go to UptimeRobot:**
   - Visit [uptimerobot.com](https://uptimerobot.com)
   - Create free account

2. **Add New Monitor:**
   - Click "Add New Monitor"
   - **Monitor Type:** HTTP(s)
   - **Friendly Name:** Discord Member Tracker
   - **URL:** `https://discord-member-tracker.onrender.com/health`
     (Use your actual Render URL)
   - **Monitoring Interval:** 5 minutes
   - Click "Create Monitor"

3. **Done!**
   - UptimeRobot will ping your bot every 5 minutes
   - Bot stays awake 24/7 on free tier! 🎉

---

## 📊 How It Works

```
UptimeRobot → Pings every 5 min → Your Bot's Health Server → Returns "Bot is running! 🤖"
                                          ↓
                                    Keeps Render awake
                                          ↓
                                  Discord bot stays online
```

---

## ✅ Verify It's Working

### Check Bot Status:

1. **Visit your Render URL in browser:**
   - Go to `https://your-app.onrender.com`
   - You should see: "Bot is running! 🤖"

2. **Check Discord:**
   - Your bot should show as **Online** (green dot)

3. **Check Render Logs:**
   - Go to Render dashboard → Your service → Logs
   - You should see:
     ```
     [2026-01-02 22:00:00] ✅ Successfully connected as YourBot#1234
     [2026-01-02 22:00:01] 🌐 Health server started on port 8080
     ```

4. **Check UptimeRobot:**
   - Should show "Up" status
   - Response time should be < 1 second

---

## 🎯 Complete Configuration Example

### `.env` file:
```env
DISCORD_BOT_TOKEN=your_discord_token_here
TELEGRAM_BOT_TOKEN=your_telegram_token_here
TELEGRAM_CHAT_ID=123456789
TIMER_HOURS=24
PORT=8080
```

### Render Environment Variables:
```
DISCORD_BOT_TOKEN = your_discord_token_here
TELEGRAM_BOT_TOKEN = your_telegram_token_here
TELEGRAM_CHAT_ID = 123456789
TIMER_HOURS = 24
PORT = 8080
```

---

## 💡 Free Tier Limits

### Render Free Web Service:
- ✅ 750 hours/month (31+ days!)
- ✅ Sleeps after 15 min inactivity (UptimeRobot prevents this)
- ✅ 512 MB RAM
- ✅ Shared CPU

### UptimeRobot Free:
- ✅ 50 monitors
- ✅ 5-minute intervals
- ✅ Unlimited checks

**Result:** Your bot runs 24/7 completely free! 🎉

---

## 🐛 Troubleshooting

### Bot shows "Offline" on Discord
- Check Render logs for errors
- Verify all environment variables are set
- Make sure Server Members Intent is enabled

### "Application failed to respond" error
- Check that `PORT=8080` is set in environment variables
- Verify `health_server.py` exists in your repo
- Check Render logs for startup errors

### Bot keeps sleeping
- Verify UptimeRobot monitor is active
- Check UptimeRobot is using `/health` endpoint
- Make sure monitoring interval is 5 minutes

### UptimeRobot shows "Down"
- Wait 2-3 minutes after deployment
- Check Render service is running
- Verify URL is correct (should end with `.onrender.com`)

---

## 📝 Quick Commands

```bash
# Update bot code
git add .
git commit -m "Update bot"
git push

# Render auto-deploys on push!

# View logs
# Go to Render dashboard → Your service → Logs tab

# Restart service
# Render dashboard → Your service → Manual Deploy → Deploy latest commit
```

---

## 🎉 Summary

**What you get:**
- ✅ Free 24/7 hosting on Render
- ✅ Bot stays online with UptimeRobot
- ✅ Automatic Telegram file delivery
- ✅ Multi-server tracking
- ✅ No credit card required

**Total cost:** $0/month 🎊

---

## 📞 Need Help?

- **Render Docs:** [render.com/docs/web-services](https://render.com/docs/web-services)
- **UptimeRobot Docs:** [uptimerobot.com/help](https://uptimerobot.com/help)
- **Test Health Endpoint:** Visit `https://your-app.onrender.com/health`

---

**Your Discord bot is now running 24/7 for FREE!** 🚀
