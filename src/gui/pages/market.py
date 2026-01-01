"""
Market Data Page - Live market data and technical indicators
"""

import plotly.graph_objects as go
from datetime import datetime
from nicegui import ui
from src.gui.services.bot_service import BotService
from src.gui.services.state_manager import StateManager


def create_market(bot_service: BotService, state_manager: StateManager):
    """Create market data page with live prices and technical indicators"""

    ui.label('Market Data').classes('text-3xl font-bold mb-4 text-white')

    # ===== ASSET SELECTOR =====
    with ui.row().classes('w-full items-center gap-4 mb-6'):
        ui.label('Select Asset:').classes('text-lg font-semibold text-white')

        # Get assets from bot config
        state = state_manager.get_state()
        configured_assets = bot_service.get_assets() if bot_service.is_running() else ['BTC', 'ETH', 'SOL']
        available_assets = configured_assets if configured_assets else ['BTC', 'ETH', 'SOL']

        asset_select = ui.select(
            label='Asset',
            options=available_assets,
            value=available_assets[0] if available_assets else 'BTC'
        ).classes('w-48')

        interval_select = ui.select(
            label='Interval',
            options=['1m', '5m', '15m', '1h', '4h', '1d'],
            value='5m'
        ).classes('w-32')

    # ===== PRICE CARDS =====
    with ui.grid(columns=4).classes('w-full gap-4 mb-6'):
        # Current Price Card
        with ui.card().classes('metric-card'):
            current_price_label = ui.label('$0.00').classes('text-4xl font-bold text-white')
            ui.label('Current Price').classes('text-sm text-gray-200 mt-2')

        # 24h Change Card
        with ui.card().classes('metric-card'):
            change_24h_label = ui.label('+0.00%').classes('text-4xl font-bold text-green-400')
            ui.label('24h Change').classes('text-sm text-gray-200 mt-2')

        # 24h Volume Card
        with ui.card().classes('metric-card'):
            volume_24h_label = ui.label('$0.00M').classes('text-4xl font-bold text-white')
            ui.label('24h Volume').classes('text-sm text-gray-200 mt-2')

        # Open Interest Card
        with ui.card().classes('metric-card'):
            open_interest_label = ui.label('$0.00M').classes('text-4xl font-bold text-white')
            ui.label('Open Interest').classes('text-sm text-gray-200 mt-2')

    # ===== PRICE CHART =====
    with ui.card().classes('w-full p-4 mb-6'):
        ui.label('Price Chart').classes('text-xl font-bold text-white mb-2')

        # Candlestick chart
        price_chart = ui.plotly(go.Figure(
            data=[go.Candlestick(
                x=[],
                open=[],
                high=[],
                low=[],
                close=[],
                name='Price'
            )],
            layout=go.Layout(
                template='plotly_dark',
                height=400,
                margin=dict(l=50, r=20, t=20, b=40),
                xaxis=dict(title='Time', showgrid=True, gridcolor='#374151'),
                yaxis=dict(title='Price ($)', showgrid=True, gridcolor='#374151'),
                paper_bgcolor='#1f2937',
                plot_bgcolor='#1f2937',
                font=dict(color='#e5e7eb'),
                showlegend=True
            )
        )).classes('w-full')

    # ===== TECHNICAL INDICATORS =====
    with ui.row().classes('w-full gap-4 mb-6'):
        # Left column - Trend Indicators
        with ui.card().classes('flex-1 p-4'):
            ui.label('Trend Indicators').classes('text-xl font-bold text-white mb-4')

            with ui.column().classes('gap-3 w-full'):
                # EMA 20/50
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('EMA 20').classes('text-gray-300')
                    ema20_label = ui.label('$0.00').classes('text-white font-semibold')

                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('EMA 50').classes('text-gray-300')
                    ema50_label = ui.label('$0.00').classes('text-white font-semibold')

                ui.separator()

                # MACD
                ui.label('MACD').classes('text-lg font-bold text-white mt-2')
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('MACD Line').classes('text-gray-300')
                    macd_line_label = ui.label('0.00').classes('text-white font-semibold')

                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('Signal Line').classes('text-gray-300')
                    macd_signal_label = ui.label('0.00').classes('text-white font-semibold')

                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('Histogram').classes('text-gray-300')
                    macd_hist_label = ui.label('0.00').classes('text-green-400 font-semibold')

        # Right column - Momentum Indicators
        with ui.card().classes('flex-1 p-4'):
            ui.label('Momentum Indicators').classes('text-xl font-bold text-white mb-4')

            with ui.column().classes('gap-3 w-full'):
                # RSI
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('RSI (14)').classes('text-gray-300')
                    rsi_label = ui.label('50.00').classes('text-white font-semibold')

                # RSI Bar
                rsi_progress = ui.linear_progress(value=0.5, show_value=False).classes('w-full')

                ui.separator()

                # ATR
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('ATR (14)').classes('text-gray-300')
                    atr_label = ui.label('$0.00').classes('text-white font-semibold')

                ui.separator()

                # Stochastic
                ui.label('Stochastic').classes('text-lg font-bold text-white mt-2')
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('%K').classes('text-gray-300')
                    stoch_k_label = ui.label('50.00').classes('text-white font-semibold')

                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('%D').classes('text-gray-300')
                    stoch_d_label = ui.label('50.00').classes('text-white font-semibold')

    # ===== INDICATOR CHART =====
    with ui.card().classes('w-full p-4 mb-6'):
        ui.label('RSI & MACD').classes('text-xl font-bold text-white mb-2')

        # Create subplot for RSI and MACD
        indicator_chart = ui.plotly(go.Figure(
            data=[
                go.Scatter(x=[], y=[], mode='lines', name='RSI', line=dict(color='#f59e0b', width=2)),
                go.Scatter(x=[], y=[], mode='lines', name='MACD', line=dict(color='#3b82f6', width=2), yaxis='y2'),
            ],
            layout=go.Layout(
                template='plotly_dark',
                height=300,
                margin=dict(l=50, r=50, t=20, b=40),
                xaxis=dict(title='Time', showgrid=True, gridcolor='#374151'),
                yaxis=dict(title='RSI', showgrid=True, gridcolor='#374151', range=[0, 100]),
                yaxis2=dict(title='MACD', overlaying='y', side='right', showgrid=False),
                paper_bgcolor='#1f2937',
                plot_bgcolor='#1f2937',
                font=dict(color='#e5e7eb'),
                showlegend=True
            )
        )).classes('w-full')

    # ===== MARKET SENTIMENT =====
    with ui.card().classes('w-full p-4'):
        ui.label('Market Sentiment').classes('text-xl font-bold text-white mb-4')

        with ui.row().classes('w-full gap-6 items-center'):
            # Sentiment gauge
            with ui.column().classes('flex-1'):
                sentiment_label = ui.label('NEUTRAL').classes('text-3xl font-bold text-gray-400')
                sentiment_desc = ui.label('Waiting for clear signals').classes('text-sm text-gray-400 mt-2')

            # Signal indicators
            with ui.column().classes('flex-1'):
                with ui.row().classes('items-center gap-2 mb-2'):
                    trend_icon = ui.label('○').classes('text-2xl text-gray-400')
                    ui.label('Trend Signal').classes('text-gray-300')

                with ui.row().classes('items-center gap-2 mb-2'):
                    momentum_icon = ui.label('○').classes('text-2xl text-gray-400')
                    ui.label('Momentum Signal').classes('text-gray-300')

                with ui.row().classes('items-center gap-2'):
                    volume_icon = ui.label('○').classes('text-2xl text-gray-400')
                    ui.label('Volume Signal').classes('text-gray-300')

    # ===== AUTO-REFRESH LOGIC =====
    async def update_market_data():
        """Update market data and indicators from real bot data"""
        def to_list(val):
            return val if isinstance(val, list) else [val]

        try:
            state = state_manager.get_state()
            selected_asset = asset_select.value

            # Get market data for selected asset from bot state
            market_data = None
            if state.market_data:
                # market_data can be either dict with asset keys or list of dicts
                if isinstance(state.market_data, dict):
                    market_data = state.market_data.get(selected_asset)
                elif isinstance(state.market_data, list):
                    market_data = next((m for m in state.market_data if m.get('asset') == selected_asset), None)

            if not market_data:
                # No data available yet
                current_price_label.set_text('Waiting for data...')
                change_24h_label.set_text('--')
                return

            # Update price cards with real data
            current_price = market_data.get('price') or market_data.get('current_price', 0)
            current_price = float(current_price) if current_price is not None else 0
            current_price_label.set_text(f'${current_price:,.2f}')
            
            # 24h change
            change_pct = market_data.get('change_24h')
            if change_pct is not None:
                change_24h_label.set_text(f'{change_pct:+.2f}%')
                color = 'text-green-400' if change_pct >= 0 else 'text-red-400'
                change_24h_label.classes(replace=f'text-4xl font-bold {color}')
            else:
                change_24h_label.set_text('--')
                change_24h_label.classes(replace='text-4xl font-bold text-gray-400')
            
            # Volume and OI
            open_interest = market_data.get('open_interest', 0)
            if open_interest:
                open_interest_label.set_text(f'${float(open_interest)/1e6:.1f}M')
            else:
                open_interest_label.set_text('--')
            
            vol_24h = market_data.get('volume_24h')
            if vol_24h:
                # Format roughly (Paper Trading volume is usually small units, Hyperliquid is USD?)
                # If volume is raw units * price ~ USD volume.
                # Let's assume raw units for now. Convert to USD est?
                # Or just display raw. If PaperTradingAPI returns Binance volume, it's Base Asset volume.
                # Let's multiply by price to get approx USD volume?
                # Or just display with M/K suffix.
                # If BTC price 87k, volume 1000 BTC = 87M.
                # Let's show Base Volume for now or USD if massive.
                # Let's format as number.
                vol_usd = float(vol_24h) * current_price
                volume_24h_label.set_text(f'${vol_usd/1e6:.1f}M')
            else:
                volume_24h_label.set_text('--')
            
            # Update indicators - use 5m data from market_data
            intraday = market_data.get('intraday', {})
            long_term = market_data.get('long_term', {})
            
            # Wrapper to safely format
            def fmt(val, prefix=''):
                if val is None: return '--'
                try:
                    return f'{prefix}{float(val):,.2f}'
                except:
                    return '--'

            # EMA values
            ema20_5m = intraday.get('ema20')
            ema20_lt = long_term.get('ema20')
            
            ema20_label.set_text(fmt(ema20_5m, '$'))
            ema50_label.set_text(fmt(long_term.get('ema50'), '$'))
            
            # MACD
            macd_obj = intraday.get('macd')
            if isinstance(macd_obj, dict):
                macd_line_label.set_text(fmt(macd_obj.get('valueMACD')))
                macd_signal_label.set_text(fmt(macd_obj.get('valueMACDSignal')))
                macd_hist_label.set_text(fmt(macd_obj.get('valueMACDHist')))
            else:
                macd_line_label.set_text(fmt(macd_obj))
                macd_signal_label.set_text('--')
                macd_hist_label.set_text('--')
            
            # RSI
            rsi_value = intraday.get('rsi14')
            if rsi_value is not None:
                try:
                    rsi_val_float = float(rsi_value)
                    rsi_label.set_text(f'{rsi_val_float:.2f}')
                    rsi_progress.set_value(rsi_val_float / 100)
                    
                    rsi_label.classes(remove='text-red-400 text-green-400 text-white')
                    if rsi_val_float > 70:
                        rsi_label.classes('text-red-400')
                    elif rsi_val_float < 30:
                        rsi_label.classes('text-green-400')
                    else:
                        rsi_label.classes('text-white')
                except:
                    rsi_label.set_text('--')
            else:
                rsi_label.set_text('--')
            
            # ATR
            atr_label.set_text(fmt(long_term.get('atr14'), '$'))
            
            # Update sentiment based on indicators
            sentiment_text = 'NO DATA'
            sentiment_color = 'text-gray-500'
            sentiment_desc_text = 'Waiting for market data...'
            
            if rsi_value is not None and ema20_5m is not None and current_price:
                try:
                    rsi_val_float = float(rsi_value)
                    ema20_val_float = float(ema20_5m)
                    
                    if rsi_val_float > 60 and current_price > ema20_val_float:
                        sentiment_text = 'BULLISH'
                        sentiment_color = 'text-green-400'
                        sentiment_desc_text = 'Price above EMA20, RSI strength'
                    elif rsi_val_float < 40 and current_price < ema20_val_float:
                        sentiment_text = 'BEARISH'
                        sentiment_color = 'text-red-400'
                        sentiment_desc_text = 'Price below EMA20, RSI weakness'
                    else:
                        sentiment_text = 'NEUTRAL'
                        sentiment_color = 'text-gray-400'
                        sentiment_desc_text = 'Mixed signals'
                except:
                    pass

            sentiment_label.set_text(sentiment_text)
            sentiment_label.classes(replace=f'text-3xl font-bold {sentiment_color}')
            sentiment_desc.set_text(sentiment_desc_text)

            # ===== SIGNAL ICONS LOGIC =====
            try:
                # 1. Trend Signal (Price relative to EMA50)
                ema50_val = intraday.get('ema50') or long_term.get('ema50')
                if current_price and ema50_val:
                    ema50_f = float(to_list(ema50_val)[-1] if isinstance(ema50_val, list) else ema50_val)
                    if current_price > ema50_f:
                        trend_icon.set_text('●')
                        trend_icon.classes(replace='text-2xl text-green-400')
                    else:
                        trend_icon.set_text('●')
                        trend_icon.classes(replace='text-2xl text-red-400')
                else:
                    trend_icon.set_text('○')
                    trend_icon.classes(replace='text-2xl text-gray-400')

                # 2. Momentum Signal (RSI)
                if rsi_value:
                    rsi_f = float(rsi_value)
                    if rsi_f > 55:
                        momentum_icon.set_text('●')
                        momentum_icon.classes(replace='text-2xl text-green-400')
                    elif rsi_f < 45:
                        momentum_icon.set_text('●')
                        momentum_icon.classes(replace='text-2xl text-red-400')
                    else:
                        momentum_icon.set_text('○')
                        momentum_icon.classes(replace='text-2xl text-gray-400')
                else:
                    momentum_icon.set_text('○')
                    momentum_icon.classes(replace='text-2xl text-gray-400')

                # 3. Volume Signal (Based on 24h Change direction)
                chg_24 = market_data.get('change_24h')
                if chg_24 is not None:
                    if chg_24 > 1.0:
                        volume_icon.set_text('●')
                        volume_icon.classes(replace='text-2xl text-green-400')
                    elif chg_24 < -1.0:
                        volume_icon.set_text('●')
                        volume_icon.classes(replace='text-2xl text-red-400')
                    else:
                        volume_icon.set_text('○')
                        volume_icon.classes(replace='text-2xl text-gray-400')
                else:
                    volume_icon.set_text('○')
                    volume_icon.classes(replace='text-2xl text-gray-400')

            except Exception as e:
                # Keep defaults on error
                pass

            # ===== CHART UPDATES (New Logic) =====
            price_history = market_data.get('price_history', [])
            if price_history:
                try:
                    # Parse OHLC (Handle potential format variations)
                    # p['t'] is usually ms timestamp
                    try:
                        # Use ISO string for safer serialization
                        dates = [datetime.fromtimestamp(p['t']/1000).isoformat() for p in price_history]
                    except:
                        # Fallback if t is missing or wrong format
                        dates = [datetime.now().isoformat()] * len(price_history)
                        
                    opens = [p.get('o') for p in price_history]
                    highs = [p.get('h') for p in price_history]
                    lows = [p.get('l') for p in price_history]
                    closes = [p.get('c') for p in price_history]

                    # Update Price Chart
                    price_chart.figure.data[0].x = dates
                    price_chart.figure.data[0].open = opens
                    price_chart.figure.data[0].high = highs
                    price_chart.figure.data[0].low = lows
                    price_chart.figure.data[0].close = closes
                    price_chart.update()

                    # Update Indicator Chart (RSI & MACD)
                    series_data = intraday.get('series', {})
                    rsi_series = series_data.get('rsi14', [])
                    macd_series = series_data.get('macd', [])
                    
                    # Plot RSI (Trace 0)
                    if rsi_series:
                        # Align dates to series length (tail alignment)
                        plot_dates = dates[-len(rsi_series):] if len(dates) >= len(rsi_series) else dates
                        # Or if series is longer than dates? (Shouldn't happen if price history is shorter)
                        chart_values = rsi_series[-len(plot_dates):]
                        
                        indicator_chart.figure.data[0].x = plot_dates
                        indicator_chart.figure.data[0].y = chart_values
                    
                    # Plot MACD (Trace 1)
                    if macd_series:
                        plot_dates = dates[-len(macd_series):] if len(dates) >= len(macd_series) else dates
                        # Extract numerical values from dicts
                        chart_values = [m.get('valueMACD') if isinstance(m, dict) else m for m in macd_series]
                        # Trim to match dates
                        chart_values = chart_values[-len(plot_dates):]
                        
                        indicator_chart.figure.data[1].x = plot_dates
                        indicator_chart.figure.data[1].y = chart_values
                        
                    indicator_chart.update()

                except Exception as e:
                    print(f"Chart Update Error: {e}")

        except Exception as e:
            ui.notify(f"UI Error: {str(e)}", type='negative')
            print(f"Error updating market data: {e}")

    # Auto-refresh every 10 seconds (Optimization to prevent UI freeze)
    ui.timer(10.0, update_market_data)

    # Refresh on asset/interval change
    asset_select.on('update:model-value', lambda: update_market_data())
    interval_select.on('update:model-value', lambda: update_market_data())
