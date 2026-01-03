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

    # Import app layout and pages
    from src.gui.app import create_layout
    from src.gui.container import get_container
    from src.gui.pages import (
        dashboard_reactive as dashboard,
        positions_reactive as positions,
        history_optimized as history,
        market,
        reasoning,
        settings,
        recommendations,
        logs
    )

    # Save reference to bot_service for cleanup
    bot_service_ref = get_container().bot_service

    # --- DEFINE ROUTES (Multi-Page Architecture) ---

    @ui.page('/')
    def index():
        ui.navigate.to('/dashboard')

    @ui.page('/dashboard')
    def page_dashboard():
        create_layout(dashboard.create_dashboard, 'Dashboard')

    @ui.page('/recommendations')
    def page_recommendations():
        create_layout(recommendations.create_recommendations, 'Recommendations')
        
    @ui.page('/positions')
    def page_positions():
        create_layout(positions.create_positions, 'Positions')

    @ui.page('/history')
    def page_history():
        create_layout(history.create_history, 'History')

    @ui.page('/market')
    def page_market():
        create_layout(market.create_market, 'Market')

    @ui.page('/reasoning')
    def page_reasoning():
        create_layout(reasoning.create_reasoning, 'Reasoning')

    @ui.page('/settings')
    def page_settings():
        create_layout(settings.create_settings, 'Settings')

    @ui.page('/logs')
    def page_logs():
        create_layout(logs.create_logs, 'Logs')

    # Register shutdown handler with NiceGUI app
    async def on_app_shutdown():
        """Called when NiceGUI app is shutting down"""
        print("[INFO] NiceGUI app shutdown event triggered")
        cleanup()

    app.on_shutdown(on_app_shutdown)

    # Run in headless server mode (Docker friendly)
    ui.run(
        native=False,
        show=False,
        port=int(os.getenv('API_PORT', 8082)),
        binding_refresh_interval=0.1,  # Fast refresh for responsiveness
        reconnect_timeout=3.0,
        reload=False,
        title="AI Trading Bot",
        dark=True,
        favicon='🚀'
    )
