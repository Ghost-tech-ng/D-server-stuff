"""
Configuration loader for Discord Member Tracking Self-Bot.
Loads and validates environment variables with sensible defaults.

⚠️ WARNING: This is configured for self-bot (user account) usage.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Self-bot configuration with validation."""
    
    # Required configuration - USER TOKEN (not bot token!)
    DISCORD_USER_TOKEN = os.getenv('DISCORD_USER_TOKEN')
    
    # Optional configuration with defaults
    OUTPUT_FILE = os.getenv('OUTPUT_FILE', 'join_logs')
    
    # Optional IDs (can be None)
    REPORT_CHANNEL_ID = os.getenv('REPORT_CHANNEL_ID')
    ADMIN_USER_ID = os.getenv('ADMIN_USER_ID')
    
    # Telegram integration (required for real-time notifications)
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    
    @classmethod
    def validate(cls):
        """Validate required configuration and return error messages if any."""
        errors = []
        
        if not cls.DISCORD_USER_TOKEN:
            errors.append("❌ DISCORD_USER_TOKEN is required but not set!")
            errors.append("   ⚠️  WARNING: You need a USER token, not a bot token!")
            errors.append("   → How to get your user token:")
            errors.append("   → 1. Open Discord in your web browser")
            errors.append("   → 2. Press F12 to open Developer Tools")
            errors.append("   → 3. Go to 'Network' tab and press F5 to reload")
            errors.append("   → 4. Look for any request and check the 'Authorization' header")
            errors.append("   → 5. Copy the token and add it to your .env file")
            errors.append("   → Create a .env file based on .env.sample")
        
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

