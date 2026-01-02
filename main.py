"""
AI Trading Bot - NiceGUI Desktop Application
Entry point for the application
"""

import os 
import asyncio
import atexit
from nicegui import ui, app

# Global reference to bot_service for cleanup
bot_service_ref = None



def cleanup():
    """Cleanup function called on exit"""
    global bot_service_ref
    if bot_service_ref and bot_service_ref.is_running():
        print("[INFO] Stopping bot engine...")
        try:
            # Run the async stop in a new event loop if needed
            try:
                loop = asyncio.get_running_loop()
                # If we're here, we're in an async context
                asyncio.create_task(bot_service_ref.stop())
            except RuntimeError:
                # No running loop, create one
                asyncio.run(bot_service_ref.stop())
            print("[INFO] Bot stopped successfully")
        except Exception as e:
            print(f"[WARN] Error stopping bot: {e}")

if __name__ in {"__main__", "__mp_main__"}:


    # Register cleanup on exit
    atexit.register(cleanup)

    # Import and setup app on startup
    from src.gui.app import create_app
    from src.gui.container import get_container

    # Save reference to bot_service for cleanup
    bot_service_ref = get_container().bot_service

    # Call create_app to register all pages
    create_app()

    # Register shutdown handler with NiceGUI app
    async def on_app_shutdown():
        """Called when NiceGUI app is shutting down"""
        print("[INFO] NiceGUI app shutdown event triggered")
        cleanup()

    # Run in headless server mode (Docker friendly)

    ui.run(
        native=False,
        show=False,
        port=int(os.getenv('API_PORT', 8081)),
        binding_refresh_interval=0.5,  # Reduce refresh rate to prevent UI freezing
        reconnect_timeout=10.0,        # Allow longer reconnect time
        reload=False,
        title="AI Trading Bot (Docker)",
        dark=True
    )
