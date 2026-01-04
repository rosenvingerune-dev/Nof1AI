import { useBotStore } from "@/stores/useBotStore";
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    CardDescription
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Play, Square, TrendingUp, DollarSign, Activity } from "lucide-react";
import { cn } from "@/lib/utils";

// Minimal Card components for now since we manual-implemented button
function StatCard({ title, value, subtext, icon: Icon, trend }: any) {
    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                    {title}
                </CardTitle>
                <Icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">{value}</div>
                <p className={cn("text-xs", trend > 0 ? "text-green-500" : (trend < 0 ? "text-red-500" : "text-muted-foreground"))}>
                    {subtext}
                </p>
            </CardContent>
        </Card>
    )
}

export function DashboardPage() {
    const { botState, startBot, stopBot, isLoading } = useBotStore();

    if (!botState) {
        return <div className="p-10 text-center">Loading bot state...</div>;
    }

    const { is_running, balance, total_value, total_return_pct, sharpe_ratio, positions } = botState;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
                    <p className="text-muted-foreground">Overview of trading performance and active bot status.</p>
                </div>
                <div className="flex space-x-2">
                    {!is_running ? (
                        <Button
                            onClick={() => startBot()}
                            disabled={isLoading}
                            className="bg-green-600 hover:bg-green-700"
                        >
                            <Play className="mr-2 h-4 w-4" /> Start Engine
                        </Button>
                    ) : (
                        <Button
                            variant="destructive"
                            onClick={() => stopBot()}
                            disabled={isLoading}
                        >
                            <Square className="mr-2 h-4 w-4" /> Stop Engine
                        </Button>
                    )}
                </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <StatCard
                    title="Total Value"
                    value={`$${(total_value || balance).toLocaleString(undefined, { maximumFractionDigits: 2 })}`}
                    subtext={`${total_return_pct?.toFixed(2)}% Return`}
                    trend={total_return_pct}
                    icon={DollarSign}
                />
                <StatCard
                    title="Active Positions"
                    value={positions.length.toString()}
                    subtext="Open trades"
                    icon={Activity}
                    trend={0}
                />
                <StatCard
                    title="Sharpe Ratio"
                    value={sharpe_ratio?.toFixed(2) || "0.00"}
                    subtext="Risk-adjusted return"
                    icon={TrendingUp}
                    trend={sharpe_ratio} // Color green if positive
                />
                <StatCard
                    title="Balance (Cash)"
                    value={`$${balance.toLocaleString(undefined, { maximumFractionDigits: 2 })}`}
                    subtext="Available liquidity"
                    icon={DollarSign}
                    trend={0}
                />
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <Card className="col-span-4">
                    <CardHeader>
                        <CardTitle>Active Positions</CardTitle>
                        <CardDescription>Currently open market positions.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        {positions.length === 0 ? (
                            <div className="text-sm text-muted-foreground py-8 text-center">No active positions.</div>
                        ) : (
                            <div className="space-y-4">
                                {positions.map((pos) => (
                                    <div key={pos.symbol} className="flex items-center justify-between border-b pb-4 last:border-0 last:pb-0">
                                        <div className="space-y-1">
                                            <p className="font-medium">{pos.symbol}</p>
                                            <p className="text-xs text-muted-foreground">
                                                Entry: ${pos.entry_price} | Size: {pos.quantity}
                                            </p>
                                        </div>
                                        <div className={cn("text-right font-medium", pos.unrealized_pnl >= 0 ? "text-green-500" : "text-red-500")}>
                                            {pos.unrealized_pnl >= 0 ? "+" : ""}${pos.unrealized_pnl.toFixed(2)}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </CardContent>
                </Card>

                <Card className="col-span-3">
                    <CardHeader>
                        <CardTitle>System Status</CardTitle>
                        <CardDescription>Engine health and connectivity.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="text-sm">
                            <span className="text-muted-foreground">Last Update:</span> <span className="font-mono">{botState.last_update || "Never"}</span>
                        </div>
                        <div className="text-sm">
                            <span className="text-muted-foreground">Invocation Count:</span> <span className="font-mono">{botState.invocation_count}</span>
                        </div>
                        {botState.error && (
                            <div className="bg-destructive/10 text-destructive text-sm p-3 rounded-md">
                                Error: {botState.error}
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
