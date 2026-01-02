"""
Discord Member Tracking Bot
Automatically tracks and logs all members who join a server with timestamps.
Includes auto-disable timer feature.
"""

import discord
from discord.ext import commands
import asyncio
from datetime import datetime

# Import local modules
from config import Config
from logger import log, log_error, log_success, log_warning
from data_manager import MultiServerDataManager
from timer_manager import TimerManager
from reporter import Reporter

# Bot setup with required intents
intents = discord.Intents.default()
intents.members = True  # Privileged intent - must be enabled in Discord Developer Portal
intents.message_content = True  # For commands

bot = commands.Bot(command_prefix='!', intents=intents)

# Global instances
data_manager = None
timer_manager = None
reporter = None
start_time = None

@bot.event
async def on_ready():
    """Called when bot successfully connects to Discord."""
    global data_manager, timer_manager, reporter, start_time
    
    log("="*60)
    log_success(f"Successfully connected as {bot.user.name}#{bot.user.discriminator}")
    log(f"Bot ID: {bot.user.id}")
    log("="*60)
    
    # Generate invite link with required permissions
    # Permissions: View Channels (1024) + Send Messages (2048) + Read Message History (65536)
    permissions = discord.Permissions(permissions=68608)
    invite_url = discord.utils.oauth_url(bot.user.id, permissions=permissions)
    
    log("📎 Invite Link:")
    log(invite_url)
    log("="*60)
    
    # Initialize multi-server data manager
    base_filename = Config.OUTPUT_FILE.replace('.json', '') if Config.OUTPUT_FILE else 'join_logs'
    data_manager = MultiServerDataManager(base_filename)
    
    # Initialize tracking for all guilds the bot is in
    if bot.guilds:
        log(f"Bot is in {len(bot.guilds)} server(s):")
        for guild in bot.guilds:
            data_manager.get_or_create_server(guild)
            log(f"   • {guild.name} - {guild.member_count} total members")
    else:
        log_warning("Bot is not in any servers yet!")
        log("Use the invite link above to add the bot to a server")
    
    log("="*60)
    
    # Initialize reporter if channel ID is configured
    start_time = datetime.now()
    if Config.REPORT_CHANNEL_ID:
        reporter = Reporter(bot, Config.REPORT_CHANNEL_ID, data_manager, start_time)
        log(f"Reports will be sent to channel ID: {Config.REPORT_CHANNEL_ID}")
    
    # Initialize and start timer
    timer_manager = TimerManager(Config.TIMER_HOURS, bot, data_manager, reporter)
    
    log("="*60)
    log_success("Listening for member joins across all servers...")
    log("="*60 + "\n")
    
    # Start timer in background
    bot.loop.create_task(timer_manager.start())

@bot.event
async def on_guild_join(guild):
    """Called when bot joins a new server."""
    log_success(f"Bot joined new server: {guild.name} (ID: {guild.id})")
    
    if data_manager:
        # Create tracking for this new server
        data_manager.get_or_create_server(guild)

@bot.event
async def on_member_join(member):
    """
    Called when a new member joins the server.
    This is the core tracking functionality.
    """
    if not data_manager:
        log_error("Data manager not initialized!")
        return
    
    # Get the server-specific data manager
    server_dm = data_manager.get_or_create_server(member.guild)
    
    # Add member to tracking data for this server
    server_dm.add_member(member)
    
    # Send periodic report if configured and threshold reached
    if reporter and reporter.should_send_periodic_report(member.guild.id):
        await reporter.send_periodic_report(member.guild.id)

@bot.command(name='stopbot')
async def stop_bot(ctx):
    """
    Manual command to stop the bot.
    Only works if ADMIN_USER_ID is configured and matches the command author.
    """
    # Check if admin user is configured
    if not Config.ADMIN_USER_ID:
        await ctx.send("❌ Admin user not configured. Set ADMIN_USER_ID in .env to use this command.")
        return
    
    # Check if command author is the admin
    if ctx.author.id != Config.ADMIN_USER_ID:
        await ctx.send("❌ You don't have permission to use this command.")
        log_warning(f"Unauthorized stopbot attempt by {ctx.author.name}#{ctx.author.discriminator}")
        return
    
    # Trigger shutdown
    await ctx.send("✅ Initiating bot shutdown...")
    log(f"Manual shutdown triggered by {ctx.author.name}#{ctx.author.discriminator}")
    
    if timer_manager:
        await timer_manager.shutdown("Manual shutdown via !stopbot command")

@bot.event
async def on_error(event, *args, **kwargs):
    """Handle errors in event handlers."""
    import traceback
    log_error(f"Error in {event}:")
    traceback.print_exc()

def main():
    """Main entry point for the bot."""
    log("="*60)
    log("Discord Member Tracking Bot")
    log("="*60)
    log("Bot initializing...")
    
    # Check if Server Members Intent is enabled
    if not intents.members:
        log_error("Server Members Intent is not enabled!")
        log("Please enable it in Discord Developer Portal:")
        log("1. Go to https://discord.com/developers/applications")
        log("2. Select your bot application")
        log("3. Navigate to 'Bot' section")
        log("4. Enable 'SERVER MEMBERS INTENT' under Privileged Gateway Intents")
        return
    
    try:
        # Start the bot
        bot.run(Config.DISCORD_BOT_TOKEN)
    except discord.LoginFailure:
        log_error("Invalid bot token!")
        log("Please check your DISCORD_BOT_TOKEN in the .env file")
    except Exception as e:
        log_error(f"Failed to start bot: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
