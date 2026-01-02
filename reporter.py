"""
Reporter for Discord Member Tracking Bot.
Sends periodic and final reports to a configured Discord channel.
Supports multi-server tracking.
"""

import discord
from datetime import datetime
from logger import log, log_error

class Reporter:
    """Handles sending reports to Discord channels."""
    
    def __init__(self, bot, channel_id, data_manager, start_time):
        """
        Initialize the reporter.
        
        Args:
            bot: Discord bot instance
            channel_id: Discord channel ID for reports
            data_manager: MultiServerDataManager instance
            start_time: Bot start time for calculating duration
        """
        self.bot = bot
        self.channel_id = channel_id
        self.data_manager = data_manager
        self.start_time = start_time
        self.last_report_counts = {}  # server_id -> last reported count
    
    async def get_channel(self):
        """Get the Discord channel object."""
        try:
            channel = await self.bot.fetch_channel(self.channel_id)
            return channel
        except Exception as e:
            log_error(f"Failed to fetch report channel: {e}")
            return None
    
    async def send_periodic_report(self, guild_id):
        """
        Send a periodic status report for a specific server.
        
        Args:
            guild_id: Discord guild ID
        """
        channel = await self.get_channel()
        if not channel:
            return
        
        # Get server data manager
        server_dm = self.data_manager.servers.get(str(guild_id))
        if not server_dm:
            return
        
        total_joins = server_dm.get_total_joins()
        recent_joins = server_dm.get_recent_joins(5)
        
        # Create embed
        embed = discord.Embed(
            title=f"📊 Member Join Report - {server_dm.server_name}",
            description="Periodic update on member tracking",
            color=0x3498db,  # Blue
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="Total Joins Tracked",
            value=f"**{total_joins}** members",
            inline=True
        )
        
        duration = datetime.now() - self.start_time
        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        embed.add_field(
            name="Tracking Duration",
            value=f"{hours}h {minutes}m",
            inline=True
        )
        
        # Recent joins
        if recent_joins:
            recent_text = "\n".join([
                f"• {m['username']}#{m['discriminator']}"
                for m in recent_joins
            ])
            embed.add_field(
                name="Recent Joins (Last 5)",
                value=recent_text,
                inline=False
            )
        
        try:
            await channel.send(embed=embed)
            log(f"Sent periodic report for {server_dm.server_name} to channel {self.channel_id}")
            self.last_report_counts[str(guild_id)] = total_joins
        except Exception as e:
            log_error(f"Failed to send periodic report: {e}")
    
    async def send_final_report(self, shutdown_reason):
        """
        Send final report before shutdown with stats from all servers.
        
        Args:
            shutdown_reason: Reason for shutdown
        """
        channel = await self.get_channel()
        if not channel:
            return
        
        total_joins_all = self.data_manager.get_total_joins_all_servers()
        
        # Create embed
        embed = discord.Embed(
            title="🏁 Final Member Join Report - All Servers",
            description=f"Bot shutting down: {shutdown_reason}",
            color=0xe74c3c,  # Red
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="Total Members Tracked (All Servers)",
            value=f"**{total_joins_all}** members",
            inline=True
        )
        
        duration = datetime.now() - self.start_time
        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        embed.add_field(
            name="Total Tracking Time",
            value=f"{hours}h {minutes}m",
            inline=True
        )
        
        # Per-server breakdown
        if self.data_manager.servers:
            server_stats = []
            for server_dm in self.data_manager.get_all_servers():
                joins = server_dm.get_total_joins()
                server_stats.append(f"• **{server_dm.server_name}**: {joins} joins")
                server_stats.append(f"  └ File: `{server_dm.filename}`")
            
            embed.add_field(
                name="Per-Server Statistics",
                value="\n".join(server_stats),
                inline=False
            )
        
        try:
            await channel.send(embed=embed)
            log(f"Sent final report to channel {self.channel_id}")
        except Exception as e:
            log_error(f"Failed to send final report: {e}")
    
    def should_send_periodic_report(self, guild_id):
        """
        Check if a periodic report should be sent for a specific server.
        Sends every 50 joins OR every hour (handled by timer).
        
        Args:
            guild_id: Discord guild ID
        
        Returns:
            True if report should be sent
        """
        server_dm = self.data_manager.servers.get(str(guild_id))
        if not server_dm:
            return False
        
        total_joins = server_dm.get_total_joins()
        last_count = self.last_report_counts.get(str(guild_id), 0)
        
        return (total_joins - last_count) >= 50
