"""
Discord Member Tracking Self-Bot
Automatically tracks and logs all members who join servers you're in.
Uses your Discord user account token.

⚠️ WARNING: Self-bots violate Discord's Terms of Service!
Using this may result in account termination.
"""

import discord
from discord.ext import commands
import asyncio
import os
from datetime import datetime

# Import local modules
from config import Config
from logger import log, log_error, log_success, log_warning
from data_manager import MultiServerDataManager
from reporter import Reporter

# Bot setup with required intents for self-bot
intents = discord.Intents.default()
intents.members = True  # Required to detect member joins
intents.message_content = True  # For commands

# Create self-bot client
bot = commands.Bot(
    command_prefix='!',
    self_bot=True,  # KEY FLAG: Enables self-bot mode
    help_command=None,
    intents=intents
)

# Global instances
data_manager = None
reporter = None
telegram_notifier = None
start_time = None

@bot.event
async def on_ready():
    """Called when self-bot successfully connects to Discord."""
    global data_manager, reporter, start_time, telegram_notifier
    
    log("="*60)
    log_success(f"🤖 Self-bot logged in as {bot.user.name}#{bot.user.discriminator}")
    log(f"User ID: {bot.user.id}")
    log("="*60)
    log_warning("⚠️  Running in SELF-BOT mode (user account)")
    log_warning("⚠️  This violates Discord ToS - use at your own risk!")
    log("="*60)
    
    # Initialize multi-server data manager
    base_filename = Config.OUTPUT_FILE.replace('.json', '') if Config.OUTPUT_FILE else 'join_logs'
    data_manager = MultiServerDataManager(base_filename)
    
    # Initialize tracking for all guilds you're in
    if bot.guilds:
        log(f"Monitoring {len(bot.guilds)} server(s):")
        for guild in bot.guilds:
            data_manager.get_or_create_server(guild)
            log(f"   • {guild.name} - {guild.member_count} total members")
    else:
        log_warning("You are not in any servers!")
        log("Join servers with your Discord account to start monitoring")
    
    log("="*60)
    
    # Initialize reporter if channel ID is configured
    start_time = datetime.now()
    if Config.REPORT_CHANNEL_ID:
        reporter = Reporter(bot, Config.REPORT_CHANNEL_ID, data_manager, start_time)
        log(f"Reports will be sent to channel ID: {Config.REPORT_CHANNEL_ID}")
    
    # Initialize Telegram notifier for instant notifications
    telegram_notifier = None
    if Config.TELEGRAM_BOT_TOKEN and Config.TELEGRAM_CHAT_ID:
        from telegram_sender import TelegramSender
        telegram_notifier = TelegramSender(Config.TELEGRAM_BOT_TOKEN, Config.TELEGRAM_CHAT_ID)
        log_success("📱 Telegram instant notifications enabled!")
        
        # Send startup notification to Telegram
        try:
            startup_msg = f"🤖 *Self-Bot Status: ACTIVE*\n\n"
            startup_msg += f"👤 Logged in as: {bot.user.name}#{bot.user.discriminator}\n"
            startup_msg += f"🖥️ Monitoring {len(bot.guilds)} server(s)\n"
            startup_msg += f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            startup_msg += f"✅ Bot is now monitoring for new member joins!"
            await telegram_notifier.send_message(startup_msg)
            log_success("✅ Sent startup notification to Telegram")
        except Exception as e:
            log_warning(f"Failed to send startup notification: {e}")
    else:
        log_warning("⚠️  Telegram not configured - no instant notifications")
    
    # Start health server for Render/UptimeRobot (if needed)
    try:
        from health_server import HealthServer
        health_server = HealthServer(port=int(os.getenv('PORT', 8080)))
        await health_server.start()
    except Exception as e:
        log_warning(f"Health server not started: {e}")
    
    log("="*60)
    log_success("✅ Monitoring for new member joins...")
    log_success("✅ Self-bot is ACTIVE and running")
    log("="*60 + "\n")

@bot.event
async def on_guild_join(guild):
    """Called when you join a new server."""
    log_success(f"You joined new server: {guild.name} (ID: {guild.id})")
    
    if data_manager:
        # Create tracking for this new server
        data_manager.get_or_create_server(guild)
    
    # Notify via Telegram
    if telegram_notifier:
        try:
            msg = f"🆕 *Joined New Server*\n\n"
            msg += f"🖥️ Server: {guild.name}\n"
            msg += f"👥 Members: {guild.member_count}\n"
            msg += f"📅 Joined at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            await telegram_notifier.send_message(msg)
        except Exception as e:
            log_warning(f"Failed to send guild join notification: {e}")

@bot.event
async def on_member_join(member):
    """
    Called when a new member joins any server you're in.
    This is the core tracking functionality.
    """
    if not data_manager:
        log_error("Data manager not initialized!")
        return
    
    # Get the server-specific data manager
    server_dm = data_manager.get_or_create_server(member.guild)
    
    # Add member to tracking data for this server
    server_dm.add_member(member)
    
    # Send instant Telegram notification if configured
    if telegram_notifier:
        try:
            await telegram_notifier.send_member_join_notification(member, member.guild.name)
        except Exception as e:
            log_warning(f"Failed to send Telegram notification: {e}")
    
    # Send periodic report if configured and threshold reached
    if reporter and reporter.should_send_periodic_report(member.guild.id):
        await reporter.send_periodic_report(member.guild.id)

@bot.command(name='ping')
async def ping(ctx):
    """Check if self-bot is alive and responding."""
    if ctx.author.id == bot.user.id:  # Only respond to yourself
        await ctx.send("🤖 Pong! Self-bot is alive and monitoring.")
        log(f"Ping command executed - bot is active")

@bot.command(name='stopbot')
async def stop_bot(ctx):
    """
    Manual command to stop the self-bot.
    Only you can use this command.
    """
    # Only allow the bot owner (you) to stop it
    if ctx.author.id != bot.user.id:
        return  # Silently ignore commands from others
    
    # Trigger shutdown
    await ctx.send("✅ Saving data and shutting down...")
    log(f"Manual shutdown triggered by {ctx.author.name}#{ctx.author.discriminator}")
    
    # Save all data
    log("="*60)
    log("SHUTDOWN INITIATED: Manual shutdown via !stopbot command")
    log("="*60)
    
    total_joins = data_manager.get_total_joins_all_servers()
    log(f"Final stats: {total_joins} members tracked across all servers")
    
    # Save each server's data
    for server_dm in data_manager.get_all_servers():
        if server_dm.save_data():
            log_success(f"[{server_dm.server_name}] Data saved to: {server_dm.filename}")
        else:
            log_warning(f"[{server_dm.server_name}] Failed to save data to file")
    
    # Send files to Telegram if configured
    if Config.TELEGRAM_BOT_TOKEN and Config.TELEGRAM_CHAT_ID:
        try:
            from telegram_sender import TelegramSender
            log("📱 Sending data files to Telegram...")
            telegram = TelegramSender(Config.TELEGRAM_BOT_TOKEN, Config.TELEGRAM_CHAT_ID)
            await telegram.send_all_data_files(data_manager)
            log_success("All files sent to Telegram successfully!")
        except Exception as e:
            log_warning(f"Failed to send files to Telegram: {e}")
    
    # Disconnect
    log("Disconnecting from Discord...")
    await bot.close()
    log_success("Bot disconnected successfully")
    log("="*60)

@bot.event
async def on_error(event, *args, **kwargs):
    """Handle errors in event handlers."""
    import traceback
    log_error(f"Error in {event}:")
    traceback.print_exc()

def main():
    """Main entry point for the self-bot."""
    log("="*60)
    log("Discord Member Tracking Self-Bot")
    log("="*60)
    log_warning("⚠️  WARNING: Self-bots violate Discord ToS!")
    log_warning("⚠️  Your account may be banned!")
    log("="*60)
    log("Self-bot initializing...")
    
    try:
        # Start the self-bot with user token
        # bot=False is CRUCIAL - tells discord.py this is a user token, not a bot token
        bot.run(Config.DISCORD_USER_TOKEN, bot=False)
    except discord.LoginFailure:
        log_error("Invalid user token!")
        log("Please check your DISCORD_USER_TOKEN in the .env file")
        log("\nHow to get your user token:")
        log("1. Open Discord in your web browser")
        log("2. Press F12 to open Developer Tools")
        log("3. Go to 'Network' tab")
        log("4. Press F5 to reload")
        log("5. Look for any request and check the 'Authorization' header")
        log("6. Copy the token (it's a long string)")
    except Exception as e:
        log_error(f"Failed to start self-bot: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
