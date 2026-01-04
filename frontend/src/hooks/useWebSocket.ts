import { useEffect, useRef } from 'react';
import { useBotStore } from '../stores/useBotStore';

export const useWebSocket = () => {
    const { setConnected, updateBotState } = useBotStore();
    const wsRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        // Protocol is ws:// normally, but for vite proxy we use generic /ws path which resolves to ws://
        // However, native WebSocket constructor needs absolute URL.
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host; // includes port
        const wsUrl = `${protocol}//${host}/ws`;

        const connect = () => {
            console.log("Connecting to WebSocket:", wsUrl);
            const ws = new WebSocket(wsUrl);
            wsRef.current = ws;

            ws.onopen = () => {
                console.log("WebSocket Connected");
                setConnected(true);
            };

            ws.onclose = () => {
                console.log("WebSocket Disconnected");
                setConnected(false);
                // Reconnect after 3s
                setTimeout(connect, 3000);
            };

            ws.onerror = (err) => {
                console.error("WebSocket Error:", err);
                ws.close();
            };

            ws.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    handleMessage(message);
                } catch (e) {
                    console.error("Failed to parse WS message", e);
                }
            };
        };

        // Message handler logic
        const handleMessage = (msg: any) => {
            // Based on EventTypes in backend
            switch (msg.type) {
                case 'state_update':
                    if (msg.data) {
                        updateBotState(msg.data);
                    }
                    break;
                case 'trade_executed':
                    console.log("Trade executed:", msg.data);
                    // We might want to trigger a refresh of recent trades or show a toast
                    break;
                case 'market_data_update':
                    if (msg.data && msg.data.market_data) {
                        updateBotState({
                            market_data: msg.data.market_data,
                            last_update: msg.timestamp
                        });
                    }
                    break;
                default:
                    console.log("Unhandled WS message type:", msg.type);
            }
        };

        connect();

        return () => {
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, [setConnected, updateBotState]);
};
