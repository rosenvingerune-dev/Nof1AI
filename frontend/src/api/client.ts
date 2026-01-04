import axios from 'axios';
import type { BotState, Settings, Trade } from '../types';

// Use proxy in dev (vite.config.ts)
const API_URL = '/api/v1';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const BotAPI = {
    getStatus: async (): Promise<BotState> => {
        const { data } = await api.get<BotState>('/bot/status');
        return data;
    },

    startBot: async (config: { assets: string[], interval: string }): Promise<{ status: string }> => {
        const { data } = await api.post<{ status: string }>('/bot/start', config);
        return data;
    },

    stopBot: async (): Promise<{ status: string }> => {
        const { data } = await api.post<{ status: string }>('/bot/stop');
        return data;
    },

    getPositions: async (): Promise<any[]> => {
        const { data } = await api.get('/positions/');
        return data;
    },

    closePosition: async (asset: string): Promise<{ success: boolean }> => {
        const { data } = await api.post<{ success: boolean }>(`/positions/${asset}/close`);
        return data;
    },

    getTrades: async (limit = 50, offset = 0): Promise<Trade[]> => {
        const { data } = await api.get<Trade[]>('/trades/', { params: { limit, offset } });
        return data;
    },

    getSettings: async (): Promise<Settings> => {
        const { data } = await api.get<Settings>('/settings/');
        return data;
    },

    updateSettings: async (settings: Partial<Settings>): Promise<{ success: boolean }> => {
        const { data } = await api.put<{ success: boolean }>('/settings/', settings);
        return data;
    },

    refreshMarket: async (): Promise<{ success: boolean }> => {
        const { data } = await api.post<{ success: boolean }>('/market/refresh');
        return data;
    },

    getProposals: async (): Promise<any[]> => {
        const { data } = await api.get<any[]>('/proposals/');
        return data;
    },

    approveProposal: async (id: string): Promise<{ success: boolean }> => {
        const { data } = await api.post<{ success: boolean }>(`/proposals/${id}/approve`);
        return data;
    },

    rejectProposal: async (id: string, reason: string): Promise<{ success: boolean }> => {
        const { data } = await api.post<{ success: boolean }>(`/proposals/${id}/reject`, { reason });
        return data;
    }
};
