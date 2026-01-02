"""
Logging utility for Discord Member Tracking Bot.
Provides consistent timestamp formatting for all console output.
"""

from datetime import datetime

def log(message, level="INFO"):
    """
    Log a message with timestamp and level.
    
    Args:
        message: The message to log
        level: Log level (INFO, WARN, ERROR)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def log_error(message):
    """Log an error message."""
    log(f"❌ ERROR: {message}", "ERROR")

def log_warning(message):
    """Log a warning message."""
    log(f"⚠️  WARNING: {message}", "WARN")

def log_success(message):
    """Log a success message."""
    log(f"✅ {message}", "INFO")
