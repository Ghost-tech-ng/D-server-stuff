"""
Configuration loader for Discord Member Tracking Bot.
Loads and validates environment variables with sensible defaults.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Bot configuration with validation."""
    
    # Required configuration
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    
    # Optional configuration with defaults
    TIMER_HOURS = float(os.getenv('TIMER_HOURS', '24'))
    OUTPUT_FILE = os.getenv('OUTPUT_FILE', 'join_logs.json')
    
    # Optional IDs (can be None)
    REPORT_CHANNEL_ID = os.getenv('REPORT_CHANNEL_ID')
    ADMIN_USER_ID = os.getenv('ADMIN_USER_ID')
    
    @classmethod
    def validate(cls):
        """Validate required configuration and return error messages if any."""
        errors = []
        
        if not cls.DISCORD_BOT_TOKEN:
            errors.append("❌ DISCORD_BOT_TOKEN is required but not set!")
            errors.append("   → Get your token from: https://discord.com/developers/applications")
            errors.append("   → Create a .env file based on .env.example")
        
        if cls.TIMER_HOURS <= 0:
            errors.append(f"❌ TIMER_HOURS must be positive (got: {cls.TIMER_HOURS})")
        
        # Convert string IDs to integers if provided
        if cls.REPORT_CHANNEL_ID:
            try:
                cls.REPORT_CHANNEL_ID = int(cls.REPORT_CHANNEL_ID)
            except ValueError:
                errors.append(f"❌ REPORT_CHANNEL_ID must be a valid number (got: {cls.REPORT_CHANNEL_ID})")
        
        if cls.ADMIN_USER_ID:
            try:
                cls.ADMIN_USER_ID = int(cls.ADMIN_USER_ID)
            except ValueError:
                errors.append(f"❌ ADMIN_USER_ID must be a valid number (got: {cls.ADMIN_USER_ID})")
        
        return errors

# Validate configuration on import
validation_errors = Config.validate()
if validation_errors:
    print("\n" + "="*60)
    print("CONFIGURATION ERROR")
    print("="*60)
    for error in validation_errors:
        print(error)
    print("="*60 + "\n")
    exit(1)
