"""
Reasoning Page - AI decision visualization with JSON editor and timeline
"""

import json
import asyncio
from datetime import datetime
from nicegui import ui
from src.gui.services.bot_service import BotService
from src.gui.services.state_manager import StateManager


def create_reasoning(bot_service: BotService, state_manager: StateManager):
    """Create AI reasoning page with JSON editor and decision timeline"""
    print("DEBUG: Entered create_reasoning")
    ui.notify("Loading Reasoning Page...", type='info')

    ui.label('AI Reasoning').classes('text-3xl font-bold mb-4 text-white')

    # ===== TIMELINE & FILTERS SECTION (TOP PRIORITY) =====
    with ui.card().classes('w-full p-4 mb-6'):
        with ui.row().classes('w-full items-center justify-between mb-4'):
            ui.label('Trade Decisions Timeline').classes('text-xl font-bold text-white')
            
            # Filters and Stats in the header
            with ui.row().classes('items-center gap-4'):
                ui.label('Filter:').classes('text-sm font-bold text-white')
                action_filter = ui.select(
                    label='',
                    value='all',
                    options={'all': 'All Actions', 'buy': 'Buy Only', 'sell': 'Sell Only', 'hold': 'Hold Only'}
                ).classes('w-32')
                
                stats_row = ui.row().classes('gap-4 items-center ml-4')

        # Timeline container
        timeline_container = ui.column().classes('w-full')

    # ===== JSON EDITOR SECTION (COLLAPSIBLE) =====
    with ui.expansion('Raw Analysis Data (JSON)', icon='code').classes('w-full mb-6 bg-slate-800'):
        with ui.card().classes('w-full p-4 bg-slate-900'):
            with ui.row().classes('w-full justify-between items-center mb-2'):
                ui.label('LLM Response').classes('text-sm font-bold text-white')
                
                with ui.row().classes('gap-2'):
                    # Copy / Export buttons
                    async def copy_json():
                        state = state_manager.get_state()
                        reasoning_data = state.last_reasoning or {}
                        json_str = json.dumps(reasoning_data, indent=2)
                        ui.clipboard.write(json_str)
                        ui.notify('JSON copied to clipboard!', type='positive')
                    
                    ui.button('📋 Copy', on_click=copy_json).props('size=sm')
                    
                    async def export_json():
                        state = state_manager.get_state()
                        reasoning_data = state.last_reasoning or {}
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f'reasoning_{timestamp}.json'
                        json_str = json.dumps(reasoning_data, indent=2)
                        ui.download(json_str, filename)
                        ui.notify(f'Exporting {filename}...', type='info')
                        
                    ui.button('⬇️ Export', on_click=export_json).props('size=sm')

            # JSON view (Safety replacement for json_editor to avoid CSP eval issues)
            # Using simple code block which is CSP safe
            json_view = ui.code('{}', language='json').classes('w-full h-96 overflow-auto bg-slate-950 p-4 rounded text-xs')

    # Historical decisions storage
    historical_decisions = []

    # ===== AUTO-REFRESH LOGIC =====
    async def update_reasoning():
        """Update JSON editor and timeline with latest reasoning data"""
        try:
            state = state_manager.get_state()
            reasoning_data = state.last_reasoning or {}

            # Update JSON view content
            json_str = json.dumps(reasoning_data, indent=2)
            if json_view.content != json_str:
                json_view.content = json_str

            # Update timeline
            timeline_container.clear()
            
            if reasoning_data and (reasoning_data.get('reasoning') or reasoning_data.get('trade_decisions')):
                with timeline_container:
                    trade_decisions = reasoning_data.get('trade_decisions', [])

                    if trade_decisions:
                        # Apply filter
                        selected_filter = action_filter.value.upper()
                        filtered_decisions = [
                            d for d in trade_decisions
                            if selected_filter == 'ALL' or d.get('action', 'HOLD').upper() == selected_filter
                        ]

                        # Update stats
                        stats_row.clear()
                        with stats_row:
                            buy_count = len([d for d in trade_decisions if d.get('action', '').upper() == 'BUY'])
                            sell_count = len([d for d in trade_decisions if d.get('action', '').upper() == 'SELL'])
                            hold_count = len([d for d in trade_decisions if d.get('action', '').upper() == 'HOLD'])

                            ui.label(f'🟢 Buys: {buy_count}').classes('text-xs text-green-400 font-bold')
                            ui.label(f'🔴 Sells: {sell_count}').classes('text-xs text-red-400 font-bold')
                            ui.label(f'⚫ Holds: {hold_count}').classes('text-xs text-gray-400 font-bold')

                        if filtered_decisions:
                            # Create timeline with enhanced entries
                            with ui.timeline(side='right').classes('w-full'):
                                for decision in filtered_decisions:
                                    asset = decision.get('asset', 'Unknown')
                                    action = decision.get('action', 'hold').upper()
                                    rationale = decision.get('rationale', 'No rationale provided')
                                    allocation = decision.get('allocation_usd', 0)
                                    tp_price = decision.get('tp_price')
                                    sl_price = decision.get('sl_price')
                                    exit_plan = decision.get('exit_plan', 'No exit plan')
                                    entry_price = decision.get('entry_price', 'N/A')
                                    confidence = decision.get('confidence', 0)

                                    # Determine color based on action
                                    if action == 'BUY':
                                        color = 'green'
                                        icon = '📈'
                                    elif action == 'SELL':
                                        color = 'red'
                                        icon = '📉'
                                    else:  # HOLD
                                        color = 'grey'
                                        icon = '⏸️'

                                    with ui.timeline_entry(
                                        f'{icon} {asset} - {action}',
                                        color=color,
                                        icon='science'
                                    ):
                                        if confidence:
                                            confidence_pct = int(confidence * 100) if confidence <= 1 else int(confidence)
                                            with ui.row().classes('items-center gap-2 mb-2'):
                                                ui.linear_progress(value=confidence).classes('flex-grow')
                                                ui.label(f'{confidence_pct}%').classes('text-xs text-gray-400 w-12')

                                        ui.label(rationale).classes('text-sm text-gray-300 mb-2')
                                        with ui.grid(columns=2).classes('gap-2 text-xs text-gray-400'):
                                            ui.label(f'Entry: {entry_price}')
                                            ui.label(f'Allocation: ${allocation:,.2f}')
                                            # Handle None values for prices
                                            tp_str = f"{tp_price}" if tp_price is not None else "N/A"
                                            sl_str = f"{sl_price}" if sl_price is not None else "N/A"
                                            ui.label(f'TP: {tp_str}')
                                            ui.label(f'SL: {sl_str}')
                                            # Exit plan text handling
                                            exit_plan_text = str(exit_plan)
                                            display_text = f'Exit Plan: {exit_plan_text[:50]}...' if len(exit_plan_text) > 50 else f'Exit Plan: {exit_plan_text}'
                                            ui.label(display_text).classes('col-span-2')
                        else:
                            ui.label(f'No {action_filter.value} decisions in current batch').classes('text-gray-400 text-center py-4')
                    else:
                        ui.label('No trade decisions produced').classes('text-gray-400 text-center py-4')
            else:
                # Empty / Waiting state
                with timeline_container:
                    with ui.column().classes('items-center py-8'):
                        ui.label('⏳').classes('text-6xl mb-4')
                        ui.label('Waiting for AI analysis...').classes('text-xl text-gray-400 mb-2')
                        ui.label('The bot is analyzing market data. This may take 30-60 seconds.').classes('text-sm text-gray-500')
                        ui.spinner('dots', size='lg').classes('text-gray-500 mt-4')
                        
                stats_row.clear()
        
        except Exception as e:
            ui.notify(f"Reasoning View Error: {e}", type='negative')
            # Fallback to simple error display
            timeline_container.clear()
            with timeline_container:
                ui.label(f"Error displaying reasoning: {str(e)}").classes('text-red-500')

    # Action filter change handler
    def on_filter_change(value):
        """Handle filter change"""
        try:
            asyncio.create_task(update_reasoning())
        except Exception:
            pass

    action_filter.on('update:model-value', on_filter_change)

    # Auto-refresh every 10 seconds
    ui.timer(10.0, update_reasoning)

    # Initial update
    # Initial update with error handling
    try:
        asyncio.create_task(update_reasoning())
    except Exception as e:
        ui.notify(f"Failed to initialize view: {e}", type='negative')
