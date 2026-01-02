
from nicegui import ui

def skeleton_box(height: str = 'h-4', width: str = 'w-full', classes: str = ''):
    """
    Create a skeleton loading placeholder (gray pulse animation).
    """
    return ui.element('div').classes(f'{height} {width} bg-slate-700/50 rounded animate-pulse {classes}')

def skeleton_card(height: str = 'h-32'):
    """
    Create a card skeleton.
    """
    with ui.card().classes(f'w-full {height} bg-slate-800/50 border-none p-4 animate-pulse'):
        # Header pulse
        ui.element('div').classes('h-6 w-1/3 bg-slate-700 rounded mb-4')
        # Content pulse
        ui.element('div').classes('h-4 w-full bg-slate-700 rounded mb-2')
        ui.element('div').classes('h-4 w-2/3 bg-slate-700 rounded')

def skeleton_table_row(cols: int = 4):
    """
    Create a skeleton table row.
    """
    with ui.row().classes('w-full gap-4 py-2 border-b border-gray-800 animate-pulse'):
        for _ in range(cols):
            ui.element('div').classes('h-4 flex-1 bg-slate-700/50 rounded')
