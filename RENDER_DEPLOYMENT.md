# Deploying Discord Bot to Render

Complete guide to deploy your Discord Member Tracking Bot on Render for free.

---

## 📋 Prerequisites

- ✅ Render account (free) - [render.com](https://render.com)
- ✅ GitHub account (to host your code)
- ✅ Discord bot token (from Discord Developer Portal)

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Code for Render

First, we need to add a few files that Render needs.

#### Create `render.yaml` (optional but recommended)
This tells Render how to deploy your bot:

```yaml
services:
  - type: worker
    name: discord-member-tracker
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python bot.py
    envVars:
      - key: DISCORD_BOT_TOKEN
        sync: false
      - key: TIMER_HOURS
        value: 24
```

Save this as `render.yaml` in your bot directory.

---

### Step 2: Push Code to GitHub

1. **Initialize Git** (if not already done):
   ```bash
   cd "c:\Users\hp\Documents\Python scripts\discord"
   git init
   git add .
   git commit -m "Initial commit - Discord member tracker bot"
   ```

2. **Create GitHub repository:**
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it: `discord-member-tracker`
   - **Don't** initialize with README (you already have code)
   - Click "Create repository"

3. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/discord-member-tracker.git
   git branch -M main
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` with your actual GitHub username.

---

### Step 3: Deploy on Render

1. **Go to Render:**
   - Visit [render.com](https://render.com)
   - Click "Get Started" or "Sign Up"
   - Sign up with GitHub (easiest)

2. **Create New Service:**
   - Click "New +" button (top right)
   - Select **"Background Worker"** (not Web Service!)
   - Click "Build and deploy from a Git repository"
   - Click "Next"

3. **Connect Repository:**
   - Click "Connect account" if needed
   - Find your `discord-member-tracker` repository
   - Click "Connect"

4. **Configure Service:**
   - **Name:** `discord-member-tracker` (or any name you like)
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`

5. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable"
   
   Add these:
   ```
   Key: DISCORD_BOT_TOKEN
   Value: [paste your actual bot token here]
   
   Key: TIMER_HOURS
   Value: 24
   ```

   **Optional variables** (if you want them):
   ```
   Key: REPORT_CHANNEL_ID
   Value: [your channel ID]
   
   Key: ADMIN_USER_ID
   Value: [your user ID]
   ```

6. **Select Plan:**
   - Choose **"Free"** plan
   - Click "Create Background Worker"

---

### Step 4: Monitor Deployment

1. **Watch Logs:**
   - Render will show build logs in real-time
   - Wait for "Build successful"
   - Then watch for your bot's startup logs:
     ```
     [2026-01-02 22:00:00] Bot initializing...
     [2026-01-02 22:00:01] ✅ Successfully connected as YourBot#1234
     ```

2. **Check Bot Status:**
   - Go to Discord
   - Your bot should show as **Online** (green dot)

---

## 📥 Getting Your Data Files

Since Render is ephemeral (files don't persist), you need to download data before the bot shuts down.

### Option 1: Send Files to Discord (Recommended)

Add this feature to send JSON files to a Discord channel before shutdown.

I can add this feature if you want!

### Option 2: Use Render Disk (Paid)

Render offers persistent storage but it's not free.

### Option 3: Database Integration

Store data in a free database like MongoDB Atlas or PostgreSQL.

---

## ⚠️ Important Render Limitations

### Free Tier Restrictions:

1. **Sleeps after 15 minutes of inactivity**
   - Your bot will sleep if no activity
   - **Solution:** Use a keep-alive service (see below)

2. **750 hours/month**
   - ~31 days of runtime
   - Perfect for your 24-hour bot!

3. **No persistent storage**
   - Files are lost when bot restarts
   - **Solution:** Send files to Discord or use database

---

## 🔄 Keep-Alive Solution (Prevent Sleep)

Render free tier sleeps after 15 min inactivity. To prevent this:

### Method 1: UptimeRobot (Free)

1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Create free account
3. Add "New Monitor"
4. **Monitor Type:** HTTP(s)
5. **URL:** Your Render service URL (get from Render dashboard)
6. **Monitoring Interval:** 5 minutes
7. Save

**Note:** This only works if you add a simple web endpoint to your bot.

### Method 2: Better Solution - Add Health Endpoint

I can modify your bot to include a simple HTTP server that UptimeRobot can ping. Want me to add this?

---

## 🎯 Recommended Setup for Your Use Case

Since your bot runs for 24 hours and auto-stops:

### Best Approach:

1. **Deploy on Render** (free)
2. **Add file upload feature** - Bot sends JSON files to Discord before shutdown
3. **Manual trigger** - Start bot when you need to track
4. **Let it run for 24 hours** - Then auto-stop
5. **Download files from Discord** - Get your data

**Want me to add the "send files to Discord" feature?** This way you'll never lose data!

---

## 📝 Quick Commands Reference

```bash
# Update bot code
git add .
git commit -m "Update bot"
git push

# Render auto-deploys on push!

# View logs
# Go to Render dashboard → Your service → Logs tab
```

---

## 🐛 Troubleshooting

### Bot shows "Offline" on Discord
- Check Render logs for errors
- Verify `DISCORD_BOT_TOKEN` is correct
- Make sure Server Members Intent is enabled

### "Build failed" error
- Check `requirements.txt` exists
- Verify Python syntax (no errors)
- Check Render build logs for details

### Bot keeps sleeping
- Free tier sleeps after inactivity
- Add keep-alive solution (see above)
- Or upgrade to paid plan ($7/month)

### Can't find data files
- Files don't persist on free tier
- Add Discord file upload feature
- Or use database storage

---

## 💡 Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy on Render
3. ✅ Add environment variables
4. ✅ Monitor logs
5. ⏳ **Optional:** Add file upload feature

**Want me to add automatic file uploading to Discord so you never lose your tracking data?**

---

## 📞 Need Help?

- **Render Docs:** [render.com/docs](https://render.com/docs)
- **Render Status:** [status.render.com](https://status.render.com)
- **Discord.py Docs:** [discordpy.readthedocs.io](https://discordpy.readthedocs.io)
