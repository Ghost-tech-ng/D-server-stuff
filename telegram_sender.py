"""
Telegram integration for Discord Member Tracking Bot.
Sends JSON data files to a Telegram chat before shutdown.
"""

import asyncio
import aiohttp
import os
from logger import log, log_error, log_success

class TelegramSender:
    """Handles sending files to Telegram."""
    
    def __init__(self, bot_token, chat_id):
        """
        Initialize Telegram sender.
        
        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID to send files to
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
    
    async def send_message(self, text):
        """
        Send a text message to Telegram.
        
        Args:
            text: Message text to send
        """
        url = f"{self.api_url}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        log("📱 Sent message to Telegram")
                        return True
                    else:
                        log_error(f"Failed to send Telegram message: {response.status}")
                        return False
        except Exception as e:
            log_error(f"Error sending Telegram message: {e}")
            return False
    
    async def send_file(self, file_path, caption=None):
        """
        Send a file to Telegram.
        
        Args:
            file_path: Path to the file to send
            caption: Optional caption for the file
        """
        if not os.path.exists(file_path):
            log_error(f"File not found: {file_path}")
            return False
        
        url = f"{self.api_url}/sendDocument"
        
        try:
            async with aiohttp.ClientSession() as session:
                with open(file_path, 'rb') as file:
                    form = aiohttp.FormData()
                    form.add_field('chat_id', str(self.chat_id))
                    form.add_field('document', file, filename=os.path.basename(file_path))
                    if caption:
                        form.add_field('caption', caption)
                    
                    async with session.post(url, data=form) as response:
                        if response.status == 200:
                            log_success(f"📱 Sent file to Telegram: {os.path.basename(file_path)}")
                            return True
                        else:
                            error_text = await response.text()
                            log_error(f"Failed to send file to Telegram: {response.status} - {error_text}")
                            return False
        except Exception as e:
            log_error(f"Error sending file to Telegram: {e}")
            return False
    
    async def send_all_data_files(self, data_manager):
        """
        Send all server data files to Telegram.
        
        Args:
            data_manager: MultiServerDataManager instance
        """
        # Send summary message first
        total_joins = data_manager.get_total_joins_all_servers()
        server_count = len(data_manager.servers)
        
        summary = f"🤖 *Discord Member Tracker - Final Report*\n\n"
        summary += f"📊 Total Members Tracked: *{total_joins}*\n"
        summary += f"🖥️ Servers Tracked: *{server_count}*\n\n"
        summary += f"📁 Sending {server_count} data file(s)..."
        
        await self.send_message(summary)
        
        # Send each server's data file
        for server_dm in data_manager.get_all_servers():
            joins = server_dm.get_total_joins()
            caption = f"📊 {server_dm.server_name}\n{joins} members tracked"
            
            await self.send_file(server_dm.filename, caption)
            await asyncio.sleep(0.5)  # Small delay between files
        
        # Send completion message
        completion = f"✅ All data files sent successfully!\n\n"
        completion += f"Total files: {server_count}"
        await self.send_message(completion)
