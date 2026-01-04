import { NavLink } from 'react-router-dom';
import {
    LayoutDashboard,
    LineChart,
    History,
    Settings,
    Activity,
    Zap
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useBotStore } from '@/stores/useBotStore';

export function Sidebar() {
    const { botState, isConnected } = useBotStore();
    const isRunning = botState?.is_running;

    const links = [
        { to: "/", label: "Dashboard", icon: LayoutDashboard },
        { to: "/positions", label: "Positions", icon: Activity },
        { to: "/trades", label: "Trade History", icon: History },
        { to: "/market", label: "Market Data", icon: LineChart },
        { to: "/settings", label: "Settings", icon: Settings },
    ];

    return (
        <div className="flex w-64 flex-col bg-card border-r border-border h-screen">
            <div className="flex h-16 items-center px-6 border-b border-border">
                <Zap className="h-6 w-6 text-primary mr-2" />
                <span className="text-lg font-bold">NOF1 Trading</span>
            </div>

            <div className="flex flex-col flex-1 py-4">
                <nav className="space-y-1 px-3">
                    {links.map((link) => (
                        <NavLink
                            key={link.to}
                            to={link.to}
                            className={({ isActive }) =>
                                cn(
                                    "flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
                                    isActive
                                        ? "bg-primary/10 text-primary"
                                        : "text-muted-foreground hover:bg-muted hover:text-foreground"
                                )
                            }
                        >
                            <link.icon className="mr-3 h-5 w-5 flex-shrink-0" />
                            {link.label}
                        </NavLink>
                    ))}
                </nav>
            </div>

            <div className="p-4 border-t border-border bg-card/50">
                <div className="flex items-center justify-between text-xs text-muted-foreground mb-2">
                    <span>Status</span>
                    <span className={cn("inline-block h-2 w-2 rounded-full", isConnected ? "bg-green-500" : "bg-red-500")} title={isConnected ? "WS Connected" : "WS Disconnected"} />
                </div>
                <div className="flex items-center space-x-2">
                    <div className={cn("h-3 w-3 rounded-full animate-pulse", isRunning ? "bg-green-500" : "bg-yellow-500")}></div>
                    <span className="font-medium text-sm">
                        {isRunning ? "Engine Running" : "Engine Stopped"}
                    </span>
                </div>
            </div>
        </div>
    );
}
