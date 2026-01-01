"""
Header Component - Top navigation bar with quick metrics
"""

from nicegui import ui
from src.gui.services.state_manager import StateManager


def create_header(state_manager: StateManager):
    """
    Create header component with logo, quick metrics, and status.

    Args:
        state_manager: Global state manager instance
    """
    with ui.header().classes(
            'row items-center justify-between p-4 bg-[#0B1120] border-b border-gray-800'
    ).style('height: 80px'):
        
        # Left: Logo & Title
        with ui.row().classes('items-center gap-4'):
            ui.icon('smart_toy').classes('text-4xl text-blue-500')
            with ui.column().classes('gap-0'):
                ui.label('AI Trading Bot v1.1.0').classes('text-xl font-bold text-white')
                ui.label('Alpha Arena').classes('text-xs text-blue-400 font-bold')

        # Right: Metrics
        with ui.row().classes('gap-8 items-center'):
            # Balance
            with ui.column().classes('text-center gap-0'):
                balance_label = ui.label('$0.00').classes('text-lg font-bold text-white')
                ui.label('Balance').classes('text-xs text-gray-400 uppercase tracking-wider')

            # 24h PnL
            with ui.column().classes('text-center gap-0'):
                pnl_label = ui.label('+0.00%').classes('text-lg font-bold text-green-500')
                ui.label('Total Return').classes('text-xs text-gray-400 uppercase tracking-wider')

            # Sharpe Ratio
            with ui.column().classes('text-center gap-0'):
                sharpe_label = ui.label('0.00').classes('text-lg font-bold text-white')
                ui.label('Sharpe').classes('text-xs text-gray-400 uppercase tracking-wider')

            # Status indicator
            with ui.column().classes('text-center gap-0 items-center justify-center border-l border-gray-700 pl-6'):
                status_label = ui.label('⚫ Stopped').classes('text-sm font-bold text-gray-400 bg-gray-900 px-3 py-1 rounded-full')
                
    # Auto-refresh metrics logic
    async def update_header():
        try:
            state = state_manager.get_state()

            # Update balance
            balance_label.text = f"${state.balance:,.2f}"

            # Update PnL with color coding
            pnl_pct = state.total_return_pct
            pnl_label.text = f"{pnl_pct:+.2f}%"
            if pnl_pct >= 0:
                pnl_label.classes(remove='text-red-500', add='text-green-500')
            else:
                pnl_label.classes(remove='text-green-500', add='text-red-500')

            # Update Sharpe
            sharpe_label.text = f"{state.sharpe_ratio:.2f}"

            # Update status
            if state.is_running:
                status_label.text = '🟢 Running'
                status_label.classes(remove='text-gray-400', add='text-green-500')
            else:
                status_label.text = '⚫ Stopped'
                status_label.classes(remove='text-green-500', add='text-gray-400')

            # Error indicator
            if state.error:
                status_label.text = '🔴 Error'
                status_label.classes(remove='text-green-500 text-gray-400', add='text-red-500')
                status_label.tooltip(str(state.error))
            else:
                status_label.tooltip('Status OK')
                
        except Exception:
            pass # Fail silently during updates

    # Refresh every second
    ui.timer(1.0, update_header)
