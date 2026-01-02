# Discord Member Tracking Bot 🤖

A Python Discord bot that automatically tracks and logs all members who join a server, recording their details with timestamps, and includes an auto-disable timer feature.

## ✨ Features

- ✅ **Multi-Server Support** - Track multiple Discord servers simultaneously
- ✅ **Separate Data Files** - Each server gets its own JSON file (e.g., `join_logs_ServerName_123456.json`)
- ✅ **Automatic Member Tracking** - Detects and logs every member who joins any tracked server
- ✅ **Comprehensive Data Capture** - Records username, ID, join time, account creation date, and avatar status
- ✅ **Auto-Disable Timer** - Automatically shuts down after a configurable time period (default: 24 hours)
- ✅ **JSON Data Storage** - Saves all data to persistent JSON files (one per server)
- ✅ **Discord Reports** - Optional periodic and final reports sent as Discord embeds
- ✅ **Manual Stop Command** - Admin can manually trigger shutdown with `!stopbot`
- ✅ **Real-time Console Logging** - See member joins as they happen with timestamps and server names
- ✅ **Graceful Shutdown** - Ensures all data is saved for all servers before disconnecting

## 📋 Prerequisites

- **Python 3.8 or higher**
- **Discord Bot Application** - Create one at [Discord Developer Portal](https://discord.com/developers/applications)
- **Server Members Intent** - Must be enabled (see setup instructions below)

## 🚀 Quick Start

### 1. Create Discord Bot Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** and give it a name
3. Navigate to the **"Bot"** section in the left sidebar
4. Click **"Add Bot"** and confirm
5. **Enable Privileged Gateway Intents:**
   - Scroll down to "Privileged Gateway Intents"
   - ✅ Enable **"SERVER MEMBERS INTENT"** (REQUIRED)
   - ✅ Enable **"MESSAGE CONTENT INTENT"** (for commands)
6. Click **"Reset Token"** and copy your bot token (keep this secret!)

### 2. Install Dependencies

```bash
# Navigate to the bot directory
cd "c:\Users\hp\Documents\Python scripts\discord"

# Install required packages
pip install -r requirements.txt
```

### 3. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` file and add your bot token:
   ```env
   DISCORD_BOT_TOKEN=your_bot_token_here
   TIMER_HOURS=24
   ```

### 4. Run the Bot

```bash
python bot.py
```

### 5. Invite Bot to Your Server

When the bot starts, it will display an invite link in the console:

```
📎 Invite Link:
https://discord.com/api/oauth2/authorize?client_id=...
```

1. Copy the invite link
2. Open it in your browser
3. Select the server you want to track
4. Click **"Authorize"**

The bot will now track all new members who join that server!

## ⚙️ Configuration Options

Edit your `.env` file to customize the bot:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DISCORD_BOT_TOKEN` | ✅ Yes | - | Your Discord bot token |
| `TIMER_HOURS` | No | `24` | Hours until auto-shutdown |
| `REPORT_CHANNEL_ID` | No | - | Channel ID for Discord reports |
| `ADMIN_USER_ID` | No | - | User ID who can use `!stopbot` |
| `OUTPUT_FILE` | No | `join_logs.json` | Custom output filename |

### Getting Discord IDs

To get channel or user IDs:
1. Enable **Developer Mode** in Discord:
   - User Settings → Advanced → Developer Mode (toggle on)
2. Right-click any channel or user → **Copy ID**

## 📊 Output Format

The bot creates **separate JSON files for each server** in this format:

**Filename:** `join_logs_ServerName_123456789012345678.json`

```json
{
  "server_name": "My Discord Server",
  "server_id": "123456789012345678",
  "tracked_joins": [
    {
      "username": "john_doe",
      "user_id": "987654321098765432",
      "discriminator": "1234",
      "joined_at": "2026-01-02T20:30:00.123456+00:00",
      "account_created": "2020-05-15T08:22:00+00:00",
      "has_avatar": true
    }
  ]
}
```

**Multi-Server Example:**
- Server "Gaming Community" → `join_logs_Gaming_Community_111222333.json`
- Server "Study Group" → `join_logs_Study_Group_444555666.json`
```

## 🎮 Commands

| Command | Permission | Description |
|---------|------------|-------------|
| `!stopbot` | Admin only | Manually trigger bot shutdown |

## 📝 Console Output Examples

**On Startup (Multi-Server):**
```
[2026-01-02 21:00:00] Bot initializing...
[2026-01-02 21:00:01] ✅ Successfully connected as MyBot#1234
[2026-01-02 21:00:01] 📎 Invite Link: https://discord.com/...
[2026-01-02 21:00:01] Bot is in 2 server(s):
[2026-01-02 21:00:01] 📁 Tracking server: Gaming Community (ID: 111222333)
[2026-01-02 21:00:01]    Data file: join_logs_Gaming_Community_111222333.json
[2026-01-02 21:00:01]    • Gaming Community - 150 total members
[2026-01-02 21:00:01] 📁 Tracking server: Study Group (ID: 444555666)
[2026-01-02 21:00:01]    Data file: join_logs_Study_Group_444555666.json
[2026-01-02 21:00:01]    • Study Group - 45 total members
[2026-01-02 21:00:01] Timer set: Bot will auto-disable in 24 hours
[2026-01-02 21:00:01] Shutdown scheduled for: 2026-01-03 21:00:01
[2026-01-02 21:00:01] ✅ Listening for member joins across all servers...
```

**During Operation (Multi-Server):**
```
[2026-01-02 21:05:23] [Gaming Community] New member: alice#5678 (ID: 123456789)
[2026-01-02 21:12:45] [Study Group] New member: bob#9012 (ID: 987654321)
[2026-01-02 22:00:00] Status: 47 members tracked (all servers) | Time remaining: 23h 0m
```

**On Shutdown (Multi-Server):**
```
[2026-01-03 21:00:00] ⚠️  WARNING: Timer expired - initiating shutdown
[2026-01-03 21:00:00] Final stats: 342 members tracked across all servers
[2026-01-03 21:00:00] ✅ [Gaming Community] Data saved to: join_logs_Gaming_Community_111222333.json
[2026-01-03 21:00:00] ✅ [Study Group] Data saved to: join_logs_Study_Group_444555666.json
[2026-01-03 21:00:00] ✅ Bot disconnected successfully
```

## 🔧 Troubleshooting

### "Invalid bot token" error
- Double-check your `DISCORD_BOT_TOKEN` in `.env`
- Make sure there are no extra spaces or quotes
- Generate a new token in Discord Developer Portal

### "Server Members Intent is not enabled" error
- Go to Discord Developer Portal
- Select your bot application
- Navigate to "Bot" section
- Enable "SERVER MEMBERS INTENT" under Privileged Gateway Intents
- Restart the bot

### Bot doesn't detect member joins
- Verify Server Members Intent is enabled (see above)
- Make sure the bot has permission to view the server
- Check that the bot is online (green status)

### "Failed to fetch report channel" error
- Verify `REPORT_CHANNEL_ID` is correct
- Make sure the bot has permission to view and send messages in that channel
- The channel must be in the same server as the bot

## 📁 Project Structure

```
discord/
├── bot.py              # Main bot file
├── config.py           # Configuration loader
├── logger.py           # Logging utility
├── data_manager.py     # JSON data handling
├── timer_manager.py    # Auto-disable timer
├── reporter.py         # Discord embed reports
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── .env               # Your configuration (not in git)
├── .gitignore         # Git ignore rules
└── join_logs.json     # Generated data file
```

## 🔒 Security Notes

- ⚠️ **Never share your bot token** - It's like a password
- ⚠️ **Never commit `.env` to git** - It's already in `.gitignore`
- ✅ Use environment variables for all sensitive data
- ✅ Regenerate your token if it's accidentally exposed

## 📜 License

This bot is provided as-is for educational and research purposes.

## 🤝 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Check console output for error messages
4. Ensure Discord Developer Portal settings are correct

---

**Made with Python and discord.py** 🐍
#   D - s e r v e r - s t u f f  
 