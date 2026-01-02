"""
Simple HTTP server for keeping the bot alive on Render free tier.
Responds to health checks from UptimeRobot.
"""

from aiohttp import web
import asyncio
from logger import log

class HealthServer:
    """Simple HTTP server for health checks."""
    
    def __init__(self, port=8080):
        """
        Initialize health server.
        
        Args:
            port: Port to run the server on (default: 8080)
        """
        self.port = port
        self.app = web.Application()
        self.app.router.add_get('/', self.health_check)
        self.app.router.add_get('/health', self.health_check)
        self.runner = None
    
    async def health_check(self, request):
        """Handle health check requests."""
        return web.Response(text="Bot is running! 🤖", status=200)
    
    async def start(self):
        """Start the HTTP server."""
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, '0.0.0.0', self.port)
        await site.start()
        log(f"🌐 Health server started on port {self.port}")
    
    async def stop(self):
        """Stop the HTTP server."""
        if self.runner:
            await self.runner.cleanup()
            log("🌐 Health server stopped")
