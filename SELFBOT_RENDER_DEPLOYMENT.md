# Deploying Self-Bot to Render (FREE Hosting)

> [!WARNING]
> **Self-Bot Hosting Considerations**
> 
> - Self-bots violate Discord ToS regardless of where they're hosted
> - Hosting on cloud platforms may increase detection risk
> - Your Discord account can still be banned
> - Consider running locally on a home computer/Raspberry Pi for more privacy

---

## ✅ Yes, You Can Host on Render!

Your self-bot **already has** the health server built-in, so it's ready for Render deployment with UptimeRobot.

### Why Web Service (Not Background Worker)?

- ✅ **Web Service** = FREE (750 hours/month)
- ❌ **Background Worker** = Paid ($7/month)
- ✅ **With UptimeRobot** = Stays awake 24/7 for free

---

## 🚀 Deployment Steps

### Step 1: Push to GitHub

```bash
cd "c:\Users\hp\Documents\Python scripts\discord"
git add .
git commit -m "Self-bot ready for deployment"
git push
```

### Step 2: Deploy on Render

1. **Go to Render:**
   - Visit [render.com](https://render.com)
   - Sign in with GitHub

2. **Create New Web Service:**
   - Click "New +" → Select **"Web Service"**
   - Click "Build and deploy from a Git repository"
   - Connect your `D-server-stuff` repository

3. **Configure Service:**
   - **Name:** `discord-selfbot-tracker`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`

4. **Add Environment Variables:**
   Click "Advanced" → Add these:
   
   ```
   DISCORD_USER_TOKEN = your_user_token_here
   TELEGRAM_BOT_TOKEN = your_telegram_token
   TELEGRAM_CHAT_ID = your_chat_id
   PORT = 8080
   ```

   > [!IMPORTANT]
   > Use `DISCORD_USER_TOKEN` (not `DISCORD_BOT_TOKEN`)!

5. **Select Plan:**
   - Choose **"Free"** plan
   - Click "Create Web Service"

6. **Get Your Service URL:**
   - After deployment, Render gives you a URL like:
   - `https://discord-selfbot-tracker.onrender.com`
   - **Copy this URL!** You'll need it for UptimeRobot

---

## 🔄 Step 3: Set Up UptimeRobot (Keep Bot Alive)

Render free tier sleeps after 15 minutes of inactivity. UptimeRobot pings your bot every 5 minutes to keep it awake.

### Setup UptimeRobot:

1. **Go to UptimeRobot:**
   - Visit [uptimerobot.com](https://uptimerobot.com)
   - Create free account

2. **Add New Monitor:**
   - Click "Add New Monitor"
   - **Monitor Type:** HTTP(s)
   - **Friendly Name:** Discord Self-Bot Tracker
   - **URL:** `https://discord-selfbot-tracker.onrender.com/health`
     (Use your actual Render URL)
   - **Monitoring Interval:** 5 minutes
   - Click "Create Monitor"

3. **Done!**
   - UptimeRobot will ping your bot every 5 minutes
   - Bot stays awake 24/7 on free tier! 🎉

---

## 📊 How It Works

```
UptimeRobot → Pings every 5 min → Health Server → Returns "Bot is running! 🤖"
                                        ↓
                                  Keeps Render awake
                                        ↓
                                Self-bot stays online
                                        ↓
                          Monitors all servers you're in
```

---

## ✅ Verify It's Working

### 1. Check Health Endpoint

Visit in browser: `https://your-app.onrender.com/health`

You should see: **"Bot is running! 🤖"**

### 2. Check Render Logs

Go to Render dashboard → Your service → Logs

You should see:
```
============================================================
🤖 Self-bot logged in as YourUsername#1234
============================================================
⚠️  Running in SELF-BOT mode (user account)
============================================================
📱 Telegram instant notifications enabled!
✅ Sent startup notification to Telegram
🌐 Health server started on port 8080
✅ Self-bot is ACTIVE and running
============================================================
```

### 3. Check Telegram

You should receive a startup notification:
```
🤖 Self-Bot Status: ACTIVE

👤 Logged in as: YourUsername#1234
🖥️ Monitoring X server(s)
⏰ Started at: 2026-01-17 16:45:00

✅ Bot is now monitoring for new member joins!
```

### 4. Test Ping Command

In any Discord channel, type: `!ping`

Bot should respond: "🤖 Pong! Self-bot is alive and monitoring."

### 5. Check UptimeRobot

- Should show "Up" status
- Response time should be < 1 second

---

## 🎯 Complete Environment Variables

### On Render Dashboard:

```
DISCORD_USER_TOKEN = your_actual_user_token_here
TELEGRAM_BOT_TOKEN = your_telegram_bot_token
TELEGRAM_CHAT_ID = your_telegram_chat_id
OUTPUT_FILE = join_logs
PORT = 8080
```

> [!CAUTION]
> **Never commit your user token to GitHub!**
> 
> - Only add it in Render's environment variables
> - Keep `.env` in `.gitignore`
> - If exposed, change your Discord password immediately

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

**Result:** Your self-bot runs 24/7 completely free! 🎉

---

## 🐛 Troubleshooting

### "Invalid user token!" Error

**Cause:** Token is incorrect or not set

**Solution:**
1. Verify `DISCORD_USER_TOKEN` is set in Render environment variables
2. Make sure you copied the entire token (it's very long)
3. No quotes or extra spaces

### "Application failed to respond" Error

**Cause:** Health server not starting

**Solution:**
1. Check that `PORT=8080` is set in environment variables
2. Verify `health_server.py` exists in your repo
3. Check Render logs for startup errors

### Bot Keeps Sleeping

**Cause:** UptimeRobot not pinging

**Solution:**
1. Verify UptimeRobot monitor is active
2. Check URL ends with `/health`
3. Monitoring interval should be 5 minutes

### "You are not in any servers!"

**Cause:** Your Discord account isn't in any servers

**Solution:**
- Join servers manually with your Discord account
- The bot will automatically start monitoring them

### Bot Doesn't Detect Joins

**Possible Issues:**
1. Large servers (>1000 members) may not send join events to user accounts
2. Discord may be rate-limiting or blocking self-bot activity
3. Test with smaller servers first

---

## 🔒 Security Best Practices

> [!IMPORTANT]
> **Protect Your User Token**

1. ✅ **Never commit `.env` to git** - Already in `.gitignore`
2. ✅ **Only add token in Render dashboard** - Not in code
3. ✅ **Use Telegram monitoring** - Know if bot goes down
4. ✅ **Monitor Render logs** - Watch for errors or bans
5. ✅ **Have a backup plan** - Be ready to switch to local hosting

---

## 📝 Quick Commands

```bash
# Update bot code
git add .
git commit -m "Update self-bot"
git push

# Render auto-deploys on push!

# View logs
# Go to Render dashboard → Your service → Logs tab

# Restart service
# Render dashboard → Your service → Manual Deploy → Deploy latest commit
```

---

## 🏠 Alternative: Local Hosting (More Private)

If you're concerned about detection, consider running locally:

### Option 1: Home Computer
```bash
# Run in background (Windows)
start /B python bot.py

# Or use Windows Task Scheduler for auto-start
```

### Option 2: Raspberry Pi
- More power-efficient
- Can run 24/7 for pennies
- More private than cloud hosting

### Option 3: VPS (DigitalOcean, Linode, etc.)
- More control than Render
- Can use private IP
- $5-10/month

---

## ⚠️ Detection Risk Comparison

| Hosting Method | Detection Risk | Cost | Uptime |
|----------------|---------------|------|--------|
| **Render (Cloud)** | Medium-High | Free | 99%+ |
| **Home Computer** | Low | Free | Depends on you |
| **Raspberry Pi** | Low | ~$35 one-time | 99%+ |
| **VPS** | Medium | $5-10/mo | 99.9%+ |

**Recommendation:** If you're worried about your account, start with local hosting first to test.

---

## 🎉 Summary

**What you get with Render + UptimeRobot:**
- ✅ Free 24/7 hosting
- ✅ Self-bot stays online automatically
- ✅ Instant Telegram notifications
- ✅ Multi-server tracking
- ✅ No credit card required
- ⚠️ Slightly higher detection risk than local hosting

**Total cost:** $0/month 🎊

---

## 📞 Need Help?

- **Render Docs:** [render.com/docs/web-services](https://render.com/docs/web-services)
- **UptimeRobot Docs:** [uptimerobot.com/help](https://uptimerobot.com/help)
- **Test Health Endpoint:** Visit `https://your-app.onrender.com/health`

---

**Your self-bot can now run 24/7 on Render for FREE!** 🚀

*Remember: Self-bots violate Discord ToS regardless of where they're hosted. Use at your own risk.*
