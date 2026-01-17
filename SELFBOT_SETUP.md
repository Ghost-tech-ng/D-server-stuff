# Self-Bot Setup Guide 🤖

> [!CAUTION]
> **⚠️ CRITICAL WARNING: DISCORD TERMS OF SERVICE VIOLATION**
> 
> Self-bots (automated user accounts) **VIOLATE** Discord's Terms of Service.
> 
> **Risks:**
> - ✖️ Permanent account termination
> - ✖️ IP ban from Discord
> - ✖️ Loss of all server memberships and data
> - ✖️ No appeals or account recovery
> 
> **By proceeding, you acknowledge these risks and accept full responsibility.**

---

## What is a Self-Bot?

A self-bot is a Discord bot that runs on your **personal user account** instead of a dedicated bot account. Unlike regular bots:

- ❌ Cannot be invited via OAuth2 links
- ❌ Cannot use slash commands
- ❌ Cannot have a bot badge
- ✅ Can see all servers you're in
- ✅ Runs under your user identity
- ✅ No need to create a bot application

---

## Prerequisites

- **Python 3.8 or higher**
- **Discord account** (the one you want to monitor with)
- **Web browser** (to extract your user token)
- **Telegram account** (HIGHLY recommended for status monitoring)

---

## Step 1: Extract Your Discord User Token

Your user token is like a password - it authenticates you to Discord. **NEVER share it with anyone!**

### Method 1: Using Browser Developer Tools (Recommended)

1. **Open Discord in your web browser** (not the desktop app)
   - Go to https://discord.com/app

2. **Open Developer Tools**
   - Press `F12` (Windows/Linux) or `Cmd+Option+I` (Mac)

3. **Go to the Network tab**
   - Click on the "Network" tab in Developer Tools

4. **Reload the page**
   - Press `F5` or click the reload button

5. **Find a request**
   - Click on any request in the Network tab (look for "science" or "messages")

6. **Locate the Authorization header**
   - In the request details, look for "Request Headers"
   - Find the line that says `authorization:`
   - Copy the long string after it (this is your token)

### Method 2: Using Console (Alternative)

1. **Open Discord in your web browser**
2. **Press F12** to open Developer Tools
3. **Go to the Console tab**
4. **Paste this code and press Enter:**
   ```javascript
   (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
   ```
5. **Copy the token** that appears (without quotes)

> [!WARNING]
> **Security Alert:**
> - Your token is as sensitive as your password
> - Never share it or paste it in Discord
> - If exposed, change your password immediately (this invalidates the token)

---

## Step 2: Install Dependencies

Navigate to the bot directory and install required packages:

```bash
cd "c:\Users\hp\Documents\Python scripts\discord"
pip install -r requirements.txt
```

This installs:
- `discord.py` - Discord API library
- `python-dotenv` - Environment variable management
- `aiohttp` - Async HTTP client for Telegram

---

## Step 3: Configure Environment Variables

1. **Copy the sample environment file:**
   ```bash
   copy .env.sample .env
   ```

2. **Edit the `.env` file** and add your user token:
   ```env
   DISCORD_USER_TOKEN=your_actual_token_here
   ```

3. **Configure Telegram** (HIGHLY recommended for status monitoring):
   - See [TELEGRAM_SETUP.md](TELEGRAM_SETUP.md) for detailed instructions
   - Add your `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` to `.env`

### Example `.env` file:

```env
# Your Discord user token
DISCORD_USER_TOKEN=MTIzNDU2Nzg5MDEyMzQ1Njc4.GaBcDe.FgHiJkLmNoPqRsTuVwXyZ1234567890

# Telegram configuration (for status notifications)
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# Optional settings
OUTPUT_FILE=join_logs
PORT=8080
```

---

## Step 4: Run the Self-Bot

Start the self-bot:

```bash
python bot.py
```

### Expected Output:

```
============================================================
Discord Member Tracking Self-Bot
============================================================
⚠️  WARNING: Self-bots violate Discord ToS!
⚠️  Your account may be banned!
============================================================
Self-bot initializing...
============================================================
🤖 Self-bot logged in as YourUsername#1234
User ID: 123456789012345678
============================================================
⚠️  Running in SELF-BOT mode (user account)
⚠️  This violates Discord ToS - use at your own risk!
============================================================
Monitoring 5 server(s):
📁 Tracking server: Server Name 1 (ID: 123456789)
   Data file: join_logs_Server_Name_1_123456789.json
   • Server Name 1 - 150 total members
...
============================================================
📱 Telegram instant notifications enabled!
✅ Sent startup notification to Telegram
============================================================
✅ Monitoring for new member joins...
✅ Self-bot is ACTIVE and running
============================================================
```

### Telegram Startup Notification:

You should receive a Telegram message:

```
🤖 Self-Bot Status: ACTIVE

👤 Logged in as: YourUsername#1234
🖥️ Monitoring 5 server(s)
⏰ Started at: 2026-01-17 16:30:00

✅ Bot is now monitoring for new member joins!
```

---

## Step 5: Verify It's Working

### Test 1: Check Console Output
- The console should show "Self-bot is ACTIVE and running"
- No error messages should appear

### Test 2: Check Telegram
- You should receive a startup notification
- This confirms the bot is running and Telegram is configured correctly

### Test 3: Use the Ping Command
- In any Discord channel, type: `!ping`
- The bot should respond: "🤖 Pong! Self-bot is alive and monitoring."
- **Note:** Only you can see this response (it's from your account)

### Test 4: Monitor a Join Event
- Have a friend join one of your servers (or use a test account)
- Check console for: `[ServerName] New member: username#1234 (ID: ...)`
- Check Telegram for instant notification
- Check the JSON file for the new member data

---

## How It Works

1. **You join servers** with your Discord account (manually)
2. **The self-bot monitors** all servers you're in
3. **When someone joins** any of those servers:
   - ✅ Console logs the join event
   - ✅ Telegram sends instant notification
   - ✅ Data is saved to a JSON file (one per server)

---

## Commands

| Command | Description |
|---------|-------------|
| `!ping` | Check if self-bot is alive |
| `!stopbot` | Stop the self-bot and save all data |

**Note:** Only you can use these commands (they run from your account).

---

## Data Files

The bot creates separate JSON files for each server:

**Format:** `join_logs_ServerName_123456789.json`

**Example:**
```json
{
  "server_name": "My Discord Server",
  "server_id": "123456789012345678",
  "tracked_joins": [
    {
      "username": "john_doe",
      "user_id": "987654321098765432",
      "discriminator": "1234",
      "joined_at": "2026-01-17T15:30:00.123456+00:00",
      "account_created": "2020-05-15T08:22:00+00:00",
      "has_avatar": true
    }
  ]
}
```

---

## Troubleshooting

### "Invalid user token!" Error

**Cause:** Token is incorrect or expired

**Solution:**
1. Re-extract your token using the methods above
2. Make sure there are no extra spaces or quotes
3. If you changed your password, get a new token

### "You are not in any servers!"

**Cause:** Your Discord account isn't in any servers

**Solution:**
- Join servers manually with your Discord account
- The bot will automatically start monitoring them

### Bot doesn't detect member joins

**Possible causes:**
1. **Privileged Intent issue** - Self-bots may have limited access to member events
2. **Server size** - Large servers (>1000 members) may not send join events to user accounts
3. **Discord restrictions** - Discord may be blocking self-bot activity

**Solution:**
- Test with smaller servers first
- Check console for any error messages
- Verify Telegram notifications are working

### "Failed to send Telegram notification"

**Cause:** Telegram credentials are incorrect

**Solution:**
- Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`
- See [TELEGRAM_SETUP.md](TELEGRAM_SETUP.md) for setup instructions
- Test by sending a message directly to your bot

---

## Security Best Practices

> [!IMPORTANT]
> **Protect Your Token**

1. ✅ **Never share your user token** - It's like your password
2. ✅ **Never commit `.env` to git** - It's already in `.gitignore`
3. ✅ **Change your password if token is exposed** - This invalidates the token
4. ✅ **Use Telegram for monitoring** - Don't rely solely on console output
5. ✅ **Run on a trusted machine** - Don't run on public/shared computers

---

## Stopping the Self-Bot

### Method 1: Use the Command
In any Discord channel, type:
```
!stopbot
```

### Method 2: Press Ctrl+C
In the terminal where the bot is running, press `Ctrl+C`

Both methods will:
- ✅ Save all data to JSON files
- ✅ Send files to Telegram (if configured)
- ✅ Gracefully disconnect

---

## Differences from Regular Bot

| Feature | Regular Bot | Self-Bot |
|---------|-------------|----------|
| **Account Type** | Dedicated bot account | Your user account |
| **Invite Method** | OAuth2 link | Manual join with your account |
| **Bot Badge** | ✅ Yes | ❌ No |
| **Slash Commands** | ✅ Yes | ❌ No |
| **ToS Compliant** | ✅ Yes | ❌ **NO** |
| **Risk of Ban** | ❌ No | ✅ **YES** |
| **Setup Complexity** | Medium | Low |

---

## Final Warnings

> [!CAUTION]
> **Use at Your Own Risk**
> 
> - This self-bot violates Discord's Terms of Service
> - Your account can be permanently banned
> - There is no appeal process for ToS violations
> - You may lose access to all your servers and friends
> 
> **The developers of this bot are not responsible for any consequences.**

---

## Support

If you encounter issues:
1. Check this guide thoroughly
2. Review console output for error messages
3. Verify all configuration in `.env`
4. Test Telegram integration separately
5. Ensure you're using Python 3.8+

---

**Made with Python and discord.py** 🐍

*Remember: With great power comes great responsibility. Use wisely.*
