"""
Timer and shutdown manager for Discord Member Tracking Bot.
Handles auto-disable timer and graceful shutdown sequence.
"""

import asyncio
from datetime import datetime, timedelta
from logger import log, log_success, log_warning

class TimerManager:
    """Manages the auto-disable timer and shutdown sequence."""
    
    def __init__(self, hours, bot, data_manager, reporter=None):
        """
        Initialize the timer manager.
        
        Args:
            hours: Number of hours until auto-shutdown
            bot: Discord bot instance
            data_manager: DataManager instance
            reporter: Optional Reporter instance for final report
        """
        self.hours = hours
        self.bot = bot
        self.data_manager = data_manager
        self.reporter = reporter
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(hours=hours)
        self.shutdown_triggered = False
    
    def get_remaining_time(self):
        """Get remaining time as a formatted string."""
        remaining = self.end_time - datetime.now()
        if remaining.total_seconds() <= 0:
            return "0h 0m"
        
        hours = int(remaining.total_seconds() // 3600)
        minutes = int((remaining.total_seconds() % 3600) // 60)
        return f"{hours}h {minutes}m"
    
    async def start(self):
        """Start the timer and monitor for expiration."""
        log(f"Timer set: Bot will auto-disable in {self.hours} hours")
        log(f"Shutdown scheduled for: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check timer every minute
        while not self.shutdown_triggered:
            await asyncio.sleep(60)  # Check every minute
            
            remaining = self.end_time - datetime.now()
            
            # Log status every hour
            if remaining.total_seconds() % 3600 < 60:
                total_joins = self.data_manager.get_total_joins_all_servers()
                log(f"Status: {total_joins} members tracked (all servers) | Time remaining: {self.get_remaining_time()}")
            
            # Check if timer expired
            if remaining.total_seconds() <= 0:
                log_warning("Timer expired - initiating shutdown")
                await self.shutdown("Timer expired")
                break
    
    async def shutdown(self, reason="Manual shutdown"):
        """
        Execute graceful shutdown sequence.
        
        Args:
            reason: Reason for shutdown
        """
        if self.shutdown_triggered:
            return  # Prevent multiple shutdowns
        
        self.shutdown_triggered = True
        
        log("="*60)
        log(f"SHUTDOWN INITIATED: {reason}")
        log("="*60)
        
        # Step 1: Save all data for all servers
        total_joins = self.data_manager.get_total_joins_all_servers()
        log(f"Final stats: {total_joins} members tracked across all servers")
        
        # Save each server's data
        for server_dm in self.data_manager.get_all_servers():
            if server_dm.save_data():
                log_success(f"[{server_dm.server_name}] Data saved to: {server_dm.filename}")
            else:
                log_warning(f"[{server_dm.server_name}] Failed to save data to file")
        
        # Step 2: Send files to Telegram if configured
        from config import Config
        if Config.TELEGRAM_BOT_TOKEN and Config.TELEGRAM_CHAT_ID:
            try:
                from telegram_sender import TelegramSender
                log("📱 Sending data files to Telegram...")
                telegram = TelegramSender(Config.TELEGRAM_BOT_TOKEN, Config.TELEGRAM_CHAT_ID)
                await telegram.send_all_data_files(self.data_manager)
                log_success("All files sent to Telegram successfully!")
            except Exception as e:
                log_warning(f"Failed to send files to Telegram: {e}")
        
        # Step 3: Send final report to Discord if reporter is configured
        if self.reporter:
            try:
                await self.reporter.send_final_report(reason)
            except Exception as e:
                log_warning(f"Failed to send final report: {e}")
        
        # Step 4: Disconnect from Discord
        log("Disconnecting from Discord...")
        await self.bot.close()
        log_success("Bot disconnected successfully")
        log("="*60)
