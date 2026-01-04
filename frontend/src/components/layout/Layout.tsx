import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { useWebSocket } from '@/hooks/useWebSocket';
import { useBotStore } from '@/stores/useBotStore';
import { useEffect } from 'react';

export function Layout() {
    // Init WebSocket hook globally
    useWebSocket();

    // Init initial fetch
    const fetchInitialState = useBotStore(state => state.fetchInitialState);

    useEffect(() => {
        fetchInitialState();
    }, [fetchInitialState]);

    return (
        <div className="flex h-screen bg-background text-foreground overflow-hidden">
            <Sidebar />
            <main className="flex-1 overflow-auto p-6 md:p-8">
                <div className="mx-auto max-w-7xl animate-in fade-in duration-500">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}
