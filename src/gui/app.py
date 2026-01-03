"""
Main GUI Application - Single Page App with internal navigation
"""

from nicegui import ui
from src.gui.components.header import create_header
from src.gui.components.sidebar import Sidebar

# Import pages
from src.gui.container import get_container
from src.gui.pages import dashboard_reactive as dashboard, positions_reactive as positions, history_optimized as history, market, reasoning, settings, recommendations, logs

# Initialize container
container = get_container()



def create_common_style():
    """Add global styles and fonts"""
    ui.add_head_html('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">')
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

def create_layout(content_factory, active_page: str):
    """
    Create the standard application layout for a specific page.
    This uses Multi-Page Architecture (MPA) for maximum stability.
    Each page load is a fresh context.
    
    Args:
        content_factory: Function that builds the page content
        active_page: ID of the page to highlight in sidebar
    """
    create_common_style()

    # Route handler
    def handle_navigation(page_id: str):
        # Map page IDs to routes
        routes = {
            'Dashboard': '/dashboard',
            'Recommendations': '/recommendations',
            'Positions': '/positions',
            'History': '/history',
            'Market': '/market',
            'Reasoning': '/reasoning',
            'Settings': '/settings',
            'Logs': '/logs'
        }
        route = routes.get(page_id, '/dashboard')
        ui.navigate.to(route)

    # Main layout
    with ui.column().classes('w-full h-screen p-0 gap-0 bg-slate-950'):
        create_header(container.state_manager)

        with ui.row().classes('w-full flex-grow overflow-hidden gap-0'):
            # Sidebar with direct navigation
            sidebar = Sidebar(on_navigate_callback=handle_navigation)
            sidebar.set_active(active_page)

            # Main content area
            with ui.column().classes('flex-grow h-full p-8 overflow-y-auto items-start bg-slate-950'):
                # Build content
                # Note: We pass container services here
                if active_page == 'Logs':
                    content_factory() # Logs doesn't need services
                else:
                    content_factory(container.bot_service, container.state_manager)

