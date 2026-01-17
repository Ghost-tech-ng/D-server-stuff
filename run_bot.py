import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

# Now run the bot
exec(open('bot.py', encoding='utf-8').read())
