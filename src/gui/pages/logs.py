from nicegui import ui
from pathlib import Path
import os
import asyncio

def create_logs():
    """Create the logs page content"""
    ui.label("System Logs").classes("text-3xl font-bold text-white mb-2 tracking-tight")
    ui.label("Live tail of bot.log (Async read)").classes("text-sm text-gray-500 mb-6 font-medium")

    # Main container
    with ui.card().classes('w-full flex-grow bg-slate-900 border border-slate-800 p-0 overflow-hidden flex flex-col h-[calc(100vh-200px)]'):
        
        # Toolbar
        with ui.row().classes('w-full bg-slate-800/50 p-2 border-b border-slate-800 justify-between items-center'):
            with ui.row().classes('items-center gap-2'):
                ui.icon('terminal', size='xs', color='gray-400')
                ui.label('bot.log').classes('text-xs font-mono text-gray-400')
            
            # Status indicator
            with ui.row().classes('items-center gap-2'):
                ui.element('div').classes('w-2 h-2 rounded-full bg-green-500 animate-pulse')
                ui.label('Live').classes('text-xs text-green-500 font-bold uppercase')

        # Log View
        log_view = ui.log(max_lines=5000).classes('w-full flex-grow bg-slate-950 text-green-400 font-mono text-[11px] p-4 overflow-auto leading-tight')

    # State for file reading context
    state = {'last_pos': 0, 'file_path': Path("bot.log")}

    async def read_log():
        """Read new lines from log file asynchronously"""
        if not state['file_path'].exists():
            return

        def _read_file_sync():
            """Blocking file read logic to run in thread"""
            lines_out = []
            try:
                with open(state['file_path'], "r", encoding="utf-8") as f:
                    # First run handling
                    if state['last_pos'] == 0:
                         file_size = os.path.getsize(state['file_path'])
                         read_size = 60 * 1024 # 60KB
                         
                         if file_size > read_size:
                             f.seek(file_size - read_size)
                             f.readline() # Discard partial
                         else:
                             f.seek(0)
                        
                         lines_out = [line.rstrip() for line in f.readlines()]
                         state['last_pos'] = f.tell()
                    else:
                        # Append new data
                        f.seek(state['last_pos'])
                        new_data = f.read()
                        if new_data:
                            lines_out = new_data.splitlines()
                            state['last_pos'] = f.tell()
            except Exception:
                pass
            return lines_out

        # Offload file I/O to thread
        new_lines = await asyncio.to_thread(_read_file_sync)
        
        # Update UI
        for line in new_lines:
            log_view.push(line)

    # Auto-refresh every 1.0s
    ui.timer(1.0, read_log)
