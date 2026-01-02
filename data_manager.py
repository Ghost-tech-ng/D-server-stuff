"""
Data manager for Discord Member Tracking Bot.
Handles loading, saving, and managing member join data in JSON format.
Supports multiple servers with separate files per server.
"""

import json
import os
import re
from datetime import datetime
from logger import log, log_error, log_success

class MultiServerDataManager:
    """Manages member join data storage for multiple servers."""
    
    def __init__(self, base_filename="join_logs"):
        """
        Initialize the multi-server data manager.
        
        Args:
            base_filename: Base name for data files (without extension)
        """
        self.base_filename = base_filename
        self.servers = {}  # Dictionary: server_id -> server data manager
    
    def _sanitize_filename(self, server_name):
        """
        Sanitize server name for use in filename.
        
        Args:
            server_name: Server name to sanitize
        
        Returns:
            Sanitized server name safe for filenames
        """
        # Remove or replace invalid filename characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', server_name)
        # Limit length
        sanitized = sanitized[:50]
        return sanitized
    
    def _get_filename(self, server_name, server_id):
        """
        Generate filename for a specific server.
        
        Args:
            server_name: Name of the server
            server_id: Discord server ID
        
        Returns:
            Filename in format: join_logs_ServerName_123456.json
        """
        sanitized_name = self._sanitize_filename(server_name)
        return f"{self.base_filename}_{sanitized_name}_{server_id}.json"
    
    def get_or_create_server(self, guild):
        """
        Get or create a server data manager for a guild.
        
        Args:
            guild: Discord Guild object
        
        Returns:
            ServerDataManager instance for this guild
        """
        server_id = str(guild.id)
        
        if server_id not in self.servers:
            filename = self._get_filename(guild.name, guild.id)
            self.servers[server_id] = ServerDataManager(filename, guild.name, guild.id)
            log(f"📁 Tracking server: {guild.name} (ID: {guild.id})")
            log(f"   Data file: {filename}")
        
        return self.servers[server_id]
    
    def get_all_servers(self):
        """Get all server data managers."""
        return self.servers.values()
    
    def get_total_joins_all_servers(self):
        """Get total joins across all servers."""
        return sum(server.get_total_joins() for server in self.servers.values())


class ServerDataManager:
    """Manages member join data for a single server."""
    
    def __init__(self, filename, server_name, server_id):
        """
        Initialize the server data manager.
        
        Args:
            filename: Path to the JSON file for this server
            server_name: Name of the Discord server
            server_id: Discord server ID
        """
        self.filename = filename
        self.server_name = server_name
        self.server_id = str(server_id)
        self.data = {
            "server_name": server_name,
            "server_id": str(server_id),
            "tracked_joins": []
        }
        self.load_data()
    
    def load_data(self):
        """Load existing data from file if it exists."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                log(f"   Loaded existing data: {len(self.data['tracked_joins'])} members already tracked")
            except Exception as e:
                log_error(f"Failed to load existing data from {self.filename}: {e}")
                log("   Starting with fresh data for this server")
        else:
            log(f"   No existing data file, starting fresh")
            # Save initial file
            self.save_data()
    
    def save_data(self):
        """Save current data to JSON file."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            log_error(f"Failed to save data to {self.filename}: {e}")
            return False
    
    def add_member(self, member):
        """
        Add a new member join to the tracking data.
        
        Args:
            member: Discord Member object
        """
        member_data = {
            "username": member.name,
            "user_id": str(member.id),
            "discriminator": member.discriminator,
            "joined_at": member.joined_at.isoformat() if member.joined_at else datetime.utcnow().isoformat(),
            "account_created": member.created_at.isoformat(),
            "has_avatar": member.avatar is not None
        }
        
        self.data["tracked_joins"].append(member_data)
        
        # Save to file immediately
        if self.save_data():
            log(f"[{self.server_name}] New member: {member.name}#{member.discriminator} (ID: {member.id})")
        else:
            log_error(f"[{self.server_name}] Data saved to memory but file write failed")
    
    def get_total_joins(self):
        """Get the total number of tracked joins for this server."""
        return len(self.data["tracked_joins"])
    
    def get_recent_joins(self, count=5):
        """
        Get the most recent member joins for this server.
        
        Args:
            count: Number of recent joins to return
        
        Returns:
            List of recent member join data
        """
        return self.data["tracked_joins"][-count:]
