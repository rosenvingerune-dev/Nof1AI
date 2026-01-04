import { create } from 'zustand';
import type { BotState, Settings, Trade } from '../types';
import { BotAPI } from '../api/client';

interface BotStore {
    // State
    botState: BotState | null;
    settings: Settings | null;
    isConnected: boolean; // WebSocket connection status
    isLoading: boolean;
    error: string | null;
    trades: Trade[]; // Historical trades

    // Actions
    fetchInitialState: () => Promise<void>;
    updateBotState: (newState: Partial<BotState>) => void;
    setConnected: (connected: boolean) => void;

    // Async Actions
    startBot: () => Promise<void>;
    stopBot: () => Promise<void>;
    closePosition: (asset: string) => Promise<void>;
    fetchSettings: () => Promise<void>;
    fetchTrades: () => Promise<void>;
    refreshMarket: () => Promise<void>;
    updateSettings: (newSettings: Partial<Settings>) => Promise<void>;
}

export const useBotStore = create<BotStore>((set, get) => ({
    botState: null,
    settings: null,
    isConnected: false,
    isLoading: false,
    error: null,
    trades: [],

    fetchInitialState: async () => {
        set({ isLoading: true, error: null });
        try {
            const state = await BotAPI.getStatus();
            set({ botState: state, isLoading: false });
        } catch (err) {
            console.error("Failed to fetch bot status", err);
            // Don't set global error yet, retry silently or handle gracefully
            set({ isLoading: false });
        }
    },

    updateBotState: (newState) => {
        set((state) => ({
            botState: state.botState ? { ...state.botState, ...newState } : (newState as BotState)
        }));
    },

    setConnected: (connected) => set({ isConnected: connected }),

    startBot: async () => {
        set({ isLoading: true });
        try {
            if (get().settings) {
                // Use current settings if available
                const { assets, interval } = get().settings!;
                await BotAPI.startBot({ assets, interval });
            } else {
                // Fallback default
                await BotAPI.startBot({ assets: ["BTC", "ETH"], interval: "1h" });
            }
            // State update will come via WebSocket
        } catch (err: any) {
            set({ error: err.message || "Failed to start bot" });
        } finally {
            set({ isLoading: false });
        }
    },

    stopBot: async () => {
        set({ isLoading: true });
        try {
            await BotAPI.stopBot();
        } catch (err: any) {
            set({ error: err.message || "Failed to stop bot" });
        } finally {
            set({ isLoading: false });
        }
    },

    closePosition: async (asset) => {
        try {
            await BotAPI.closePosition(asset);
        } catch (err: any) {
            set({ error: "Failed to close position: " + err.message });
        }
    },

    fetchSettings: async () => {
        try {
            const settings = await BotAPI.getSettings();
            set({ settings });
        } catch (err) {
            console.error("Failed to load settings", err);
        }
    },

    fetchTrades: async () => {
        try {
            const trades = await BotAPI.getTrades();
            set({ trades });
        } catch (err) {
            console.error("Failed to fetch trades", err);
        }
    },

    refreshMarket: async () => {
        try {
            await BotAPI.refreshMarket();
            // Optionally fetch state again if websocket doesn't push immediately
            await get().fetchInitialState();
        } catch (err) {
            console.error("Failed to refresh market", err);
        }
    },

    updateSettings: async (newSettings) => {
        try {
            await BotAPI.updateSettings(newSettings);
            // Refresh settings
            await get().fetchSettings();
        } catch (err: any) {
            set({ error: "Failed to update settings" });
            throw err;
        }
    }
}));
