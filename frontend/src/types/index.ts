// Types for the application

export interface BotState {
    is_running: boolean;
    balance: number;
    total_value: number;
    total_return_pct: number;
    sharpe_ratio: number;
    positions: Position[];
    market_data: Record<string, MarketData>; // Keyed by asset
    error?: string;
    invocation_count: number;
    last_update: string;
}

export interface Position {
    symbol: string;
    quantity: number;
    entry_price: number;
    current_price: number;
    liquidation_price?: number;
    unrealized_pnl: number;
    leverage: number;
}

export interface MarketData {
    asset: string;
    current_price: number;
    change_24h?: number;
    volume_24h?: number;
    funding_rate?: number;
    open_interest?: number;
    intraday?: {
        ema20?: number;
        rsi14?: number;
    };
}

export interface Trade {
    id: string; // generated if not present
    asset: string;
    action: 'buy' | 'sell' | 'hold';
    amount: number;
    price: number;
    timestamp: string;
}

export interface Settings {
    assets: string[];
    interval: string;
    trading_mode: 'auto' | 'manual';
    max_position_size?: number;
    auto_trade_enabled?: boolean;
    auto_trade_threshold?: number;
}
