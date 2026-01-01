"""
Main GUI Application - Single Page App with internal navigation
"""

from nicegui import ui
from src.gui.components.header import create_header
from src.gui.components.sidebar import Sidebar
from src.gui.services.bot_service import BotService
from src.gui.services.state_manager import StateManager

# Import pages
from src.gui.pages import dashboard, positions, history, market, reasoning, settings, recommendations, logs

# Global services
bot_service = BotService()
state_manager = StateManager()

# Connect services
bot_service.state_manager = state_manager


def create_app():
    """Initialize and configure the NiceGUI application as single page"""

    # Add Material Icons font
    ui.add_head_html('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">')
    
    # Add global styles
    ui.add_head_html('''
        <style>
            * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }

            .metric-card {
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 24px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }

            .positive { color: #10b981 !important; }
            .negative { color: #ef4444 !important; }

            .q-btn {
                text-transform: none !important;
            }
        </style>
    ''')

    # Main layout
    with ui.column().classes('w-full h-screen p-0 gap-0 bg-slate-950'):
        create_header(state_manager)

        with ui.row().classes('w-full flex-grow overflow-hidden gap-0'):
            # Sidebar with navigation
            global sidebar_instance
            sidebar_instance = Sidebar(on_navigate_callback=navigate)

            # Main content area (will be updated by navigation)
            global content_container
            content_container = ui.column().classes('flex-grow h-full p-8 overflow-y-auto items-start bg-slate-950')

    # Load default page
    navigate('Dashboard')


def navigate(page: str):
    """Navigate to different page by clearing and recreating content"""
    global content_container, sidebar_instance
    
    # Update active state in sidebar
    if sidebar_instance:
        sidebar_instance.set_active(page)

    content_container.clear()

    with content_container:
        if page == 'Dashboard':
            dashboard.create_dashboard(bot_service, state_manager)
        elif page == 'Recommendations':
            recommendations.create_recommendations(bot_service, state_manager)
        elif page == 'Positions':
            positions.create_positions(bot_service, state_manager)
        elif page == 'History':
            history.create_history(bot_service, state_manager)
        elif page == 'Market':
            market.create_market(bot_service, state_manager)
        elif page == 'Reasoning':
            reasoning.create_reasoning(bot_service, state_manager)
        elif page == 'Settings':
            settings.create_settings(bot_service, state_manager)
        elif page == 'Logs':
            logs.create_logs()
