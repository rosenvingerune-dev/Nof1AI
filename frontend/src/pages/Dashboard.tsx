import { useBotStore } from "@/stores/useBotStore";
import {
    Card,
    CardContent
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Play, Square, TrendingUp, DollarSign, Activity, Wallet } from "lucide-react";
import { cn } from "@/lib/utils";
import { InfoCard } from "@/components/InfoCard";

export function DashboardPage() {
    const { botState, startBot, stopBot, isLoading, error, fetchInitialState } = useBotStore();

    if (!botState) {
        if (error) {
            return (
                <div className="flex flex-col items-center justify-center p-10 space-y-4">
                    <div className="text-red-500 font-medium">Connection Error</div>
                    <p className="text-muted-foreground">{error}</p>
                    <Button onClick={fetchInitialState} disabled={isLoading}>
                        Retry Connection
                    </Button>
                </div>
            );
        }
        return <div className="p-10 text-center">Loading bot state...</div>;
    }

    const { is_running, balance, sharpe_ratio, positions } = botState;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
                    <p className="text-muted-foreground">Overview of trading performance and active bot status.</p>
                    {error && (
                        <div className="mt-2 p-3 bg-red-500/10 border border-red-500/50 rounded-md text-red-500 text-sm flex items-center">
                            <span className="font-bold mr-2">Error:</span> {error}
                        </div>
                    )}
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
                {(() => {
                    const investmentsValue = positions.reduce((acc, pos) => acc + (pos.current_price * pos.quantity), 0);
                    const calculatedTotalBalance = balance + investmentsValue;
                    const calculatedReturnPct = ((calculatedTotalBalance - 10000) / 10000) * 100;

                    return (
                        <>
                            <InfoCard
                                title="Total Value"
                                value={`$${calculatedTotalBalance.toLocaleString(undefined, { maximumFractionDigits: 2 })}`}
                                subtext={`${calculatedReturnPct.toFixed(2)}% Return (from $10k)`}
                                icon={DollarSign}
                                className="bg-indigo-900"
                            />
                            <InfoCard
                                title="Active Positions"
                                value={positions.length.toString()}
                                subtext="Open trades"
                                icon={Activity}
                                className="bg-blue-600"
                            />
                            <InfoCard
                                title="Sharpe Ratio"
                                value={sharpe_ratio?.toFixed(2) || "0.00"}
                                subtext="Risk-adjusted return"
                                icon={TrendingUp}
                                className="bg-purple-600"
                            />
                            <InfoCard
                                title="Balance (Cash)"
                                value={`$${balance.toLocaleString(undefined, { maximumFractionDigits: 2 })}`}
                                subtext="Available liquidity"
                                icon={Wallet}
                                className="bg-emerald-600"
                            />
                        </>
                    );
                })()}
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <Card className="col-span-4 border shadow-sm">
                    <div className="p-4 border-b bg-muted/40 font-semibold flex items-center">
                        Active Positions
                    </div>
                    <CardContent className="p-0">
                        {positions.length === 0 ? (
                            <div className="text-sm text-muted-foreground py-12 text-center">No active positions.</div>
                        ) : (
                            <div className="overflow-x-auto">
                                <table className="w-full text-sm text-left">
                                    <thead className="bg-[#1a1a1a] text-gray-400 uppercase text-xs">
                                        <tr>
                                            <th className="px-4 py-3 font-medium">Asset</th>
                                            <th className="px-4 py-3 font-medium text-right">Details</th>
                                            <th className="px-4 py-3 font-medium text-right">PnL</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-border/50 bg-[#0a0a0a]">
                                        {positions.map((pos) => (
                                            <tr key={pos.symbol} className="hover:bg-muted/10 transition-colors">
                                                <td className="px-4 py-3 font-bold text-white">{pos.symbol}</td>
                                                <td className="px-4 py-3 text-right text-gray-300 font-mono text-xs">
                                                    <div className="flex flex-col items-end gap-1">
                                                        <span>${Number(pos.entry_price).toLocaleString(undefined, { maximumFractionDigits: 0 })}</span>
                                                        <span className="text-muted-foreground text-xs">Qty: {Number(pos.quantity).toFixed(4)}</span>
                                                    </div>
                                                </td>
                                                <td className={cn("px-4 py-3 text-right font-mono font-bold", pos.unrealized_pnl >= 0 ? "text-green-500" : "text-red-500")}>
                                                    {pos.unrealized_pnl >= 0 ? "+" : ""}${pos.unrealized_pnl.toFixed(2)}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </CardContent>
                </Card>

                <Card className="col-span-3 border shadow-sm">
                    <div className="p-4 border-b bg-muted/40 font-semibold flex items-center">
                        System Status
                    </div>
                    <CardContent className="p-6 space-y-4">
                        <div className="flex justify-between items-center text-sm">
                            <span className="text-muted-foreground">Last Update:</span>
                            <span className="font-mono bg-muted px-2 py-1 rounded text-xs">
                                {botState.last_update ? new Date(botState.last_update).toLocaleString('nb-NO', {
                                    day: '2-digit',
                                    month: '2-digit',
                                    year: 'numeric',
                                    hour: '2-digit',
                                    minute: '2-digit'
                                }) : "Initializing..."}
                            </span>
                        </div>
                        <div className="flex justify-between items-center text-sm">
                            <span className="text-muted-foreground">Invocation Count:</span>
                            <span className="font-mono bg-muted px-2 py-1 rounded text-xs">{botState.invocation_count}</span>
                        </div>
                        {botState.error && (
                            <div className="bg-destructive/10 text-destructive text-sm p-3 rounded-md border border-destructive/20 break-all">
                                <strong>Error:</strong> {typeof botState.error === 'object' ? JSON.stringify(botState.error) : String(botState.error)}
                            </div>
                        )}
                        <div className="pt-4 border-t">
                            <div className="flex items-center text-xs text-muted-foreground">
                                <div className={cn("h-2 w-2 rounded-full mr-2", is_running ? "bg-green-500 animate-pulse" : "bg-red-500")} />
                                {is_running ? "Engine Running" : "Engine Stopped"}
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
