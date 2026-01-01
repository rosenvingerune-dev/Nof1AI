"""
Sidebar Component - Navigation menu with active state handling
"""

from nicegui import ui

class Sidebar:
    def __init__(self, on_navigate_callback):
        self.on_navigate = on_navigate_callback
        self.buttons = {}
        self.active_id = None
        self._create_layout()

    def _create_layout(self):
        """Create the sidebar layout structure"""
        with ui.column().classes('w-64 bg-slate-900 h-full flex flex-col border-r border-slate-800'):
            # Logo Area
            with ui.row().classes('w-full items-center px-6 py-6 mb-2 gap-3'):
                ui.icon('rocket_launch', size='32px', color='blue-500')
                with ui.column().classes('gap-0'):
                    ui.label('Alpha Arena').classes('text-lg font-bold text-white tracking-wide leading-none')
                    ui.label('AI Trading Bot').classes('text-xs text-gray-500 font-medium')

            # Scrollable Menu Area
            with ui.column().classes('w-full flex-grow overflow-y-auto px-0 gap-1'):
                
                self._menu_group('MAIN', [
                    ('Dashboard', 'Dashboard', 'dashboard'),
                    ('Recommendations', 'Recommendations', 'smart_toy'),
                ])
                
                self._menu_group('TRADING', [
                    ('Positions', 'Positions', 'work'),
                    ('History', 'History', 'history'),
                    ('Market', 'Market', 'candlestick_chart'),
                ])

                self._menu_group('AI INTELLIGENCE', [
                    ('Reasoning', 'Reasoning', 'psychology'),
                ])

                ui.separator().classes('my-2 opacity-10')

                self._menu_group('SYSTEM', [
                    ('Settings', 'Settings', 'settings'),
                    ('Logs', 'System Log', 'terminal'),
                ])

            # Footer
            with ui.column().classes('mt-auto w-full p-4 border-t border-slate-800 items-center opacity-60'):
                ui.label('v1.2.0').classes('text-[10px] text-gray-500 font-mono')

    def _menu_group(self, title, items):
        """Create a titled group of menu items"""
        ui.label(title).classes('px-6 py-3 text-[10px] font-bold text-gray-500 uppercase tracking-widest mt-2')
        for id, label, icon in items:
            self._create_menu_item(id, label, icon)

    def _create_menu_item(self, id, label, icon):
        """Create a single menu button"""
        # Create button container for full control over styling
        with ui.row().classes('w-full px-3 py-0.5 relative group'):
            # Active Indicator (Left Bar) - hidden by default
            indicator = ui.element('div').classes('absolute left-0 top-1 bottom-1 w-1 bg-blue-500 rounded-r opacity-0 transition-opacity duration-200')
            
            # Button
            btn = ui.button(label, on_click=lambda i=id: self.on_navigate(i)) \
                .props(f'flat icon={icon} no-caps align=left') \
                .classes('w-full rounded-lg px-4 py-2 text-sm font-medium transition-all duration-200 text-gray-400 hover:text-white hover:bg-slate-800')
            
            # Store references to update style later
            self.buttons[id] = {'btn': btn, 'indicator': indicator}

    def set_active(self, page_id):
        """Highlight the active menu item"""
        if self.active_id == page_id:
            return # Already active
            
        self.active_id = page_id
        
        for id, elements in self.buttons.items():
            btn = elements['btn']
            indicator = elements['indicator']
            
            if id == page_id:
                # Activate
                btn.props('text-color=blue-400')
                btn.classes(replace='bg-slate-800/80 text-blue-400 font-semibold')
                btn.classes(remove='text-gray-400 hover:bg-slate-800')
                indicator.classes(replace='opacity-100')
            else:
                # Deactivate
                btn.props(remove='text-color')
                btn.classes(replace='text-gray-400 hover:bg-slate-800 font-medium')
                btn.classes(remove='bg-slate-800/80 text-blue-400 font-semibold')
                indicator.classes(replace='opacity-0')
