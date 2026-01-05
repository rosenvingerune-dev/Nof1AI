import { useBotStore } from "@/stores/useBotStore";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { X, LineChart, AlertCircle } from "lucide-react";

function InfoCard({ title, value, subtext, className }: { title: string, value: string, subtext: string, className?: string }) {
    return (
        <Card className={cn("border-none shadow-md", className)}>
            <CardContent className="p-6">
                <div className="text-4xl font-bold mb-1">{value}</div>
                <div className="text-sm opacity-90 font-medium mb-4">{title}</div>
                <div className="text-xs opacity-75">{subtext}</div>
            </CardContent>
        </Card>
    )
}

export function PositionsPage() {
    const { botState, closePosition } = useBotStore();

    if (!botState) {
        return <div className="p-10 text-center">Loading positions...</div>;
    }

    const { positions } = botState;

    // Calculate Summary Stats
    const totalPositions = positions.length;
    const totalUnrealizedPnL = positions.reduce((acc, pos) => acc + pos.unrealized_pnl, 0);
    const totalExposure = positions.reduce((acc, pos) => acc + (pos.current_price * Math.abs(pos.quantity)), 0);

    const handleClosePosition = async (symbol: string) => {
        if (confirm(`Are you sure you want to close the position for ${symbol}?`)) {
            await closePosition(symbol);
        }
    };

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Active Positions</h1>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <InfoCard
                    title="Total Positions"
                    value={totalPositions.toString()}
                    subtext="Open trades"
                    className="bg-blue-600 text-white"
                />
                <InfoCard
                    title="Unrealized PnL"
                    value={`${totalUnrealizedPnL >= 0 ? "+" : ""}$${Math.abs(totalUnrealizedPnL).toFixed(2)}`}
                    subtext="Total Profit/Loss"
                    className="bg-purple-600 text-white"
                />
                <InfoCard
                    title="Total Exposure"
                    value={`$${totalExposure.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
                    subtext="Market Value"
                    className="bg-indigo-900 text-white"
                />
            </div>

            {/* Detailed Table */}
            <Card className="border shadow-sm">
                <div className="p-4 border-b bg-muted/40 font-semibold flex items-center">
                    Position Details
                </div>
                <CardContent className="p-0">
                    {positions.length === 0 ? (
                        <div className="flex flex-col items-center justify-center py-12 text-muted-foreground space-y-3">
                            <AlertCircle className="h-10 w-10 opacity-50" />
                            <p>No active positions found.</p>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm text-left">
                                <thead className="bg-[#1a1a1a] text-gray-400 uppercase text-xs">
                                    <tr>
                                        <th className="px-4 py-3 font-medium">Asset</th>
                                        <th className="px-4 py-3 font-medium">Side</th>
                                        <th className="px-4 py-3 font-medium text-right">Size</th>
                                        <th className="px-4 py-3 font-medium text-right">Entry Price</th>
                                        <th className="px-4 py-3 font-medium text-right">Current Price</th>
                                        <th className="px-4 py-3 font-medium text-right">Unrealized PnL</th>
                                        <th className="px-4 py-3 font-medium text-right">PnL %</th>
                                        <th className="px-4 py-3 font-medium text-center">Leverage</th>
                                        <th className="px-4 py-3 font-medium text-right">Liq. Price</th>
                                        <th className="px-4 py-3 font-medium text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-border/50 bg-[#0a0a0a]">
                                    {positions.map((pos) => {
                                        const pnlPercent = (pos.unrealized_pnl / (pos.entry_price * Math.abs(pos.quantity))) * 100;
                                        const side = pos.quantity >= 0 ? "LONG" : "SHORT";

                                        return (
                                            <tr key={pos.symbol} className="group hover:bg-muted/10 transition-colors">
                                                <td className="px-4 py-3 font-bold text-white">{pos.symbol}</td>
                                                <td className="px-4 py-3">
                                                    <span className={cn(
                                                        "inline-flex items-center rounded px-2 py-0.5 text-xs font-bold uppercase",
                                                        side === "LONG"
                                                            ? "bg-green-500/20 text-green-500 border border-green-500/30"
                                                            : "bg-red-500/20 text-red-500 border border-red-500/30"
                                                    )}>
                                                        {side}
                                                    </span>
                                                </td>
                                                <td className="px-4 py-3 text-right font-mono text-gray-300">{Math.abs(pos.quantity)}</td>
                                                <td className="px-4 py-3 text-right font-mono text-gray-300">${pos.entry_price.toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                                                <td className="px-4 py-3 text-right font-mono text-gray-300">${pos.current_price.toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>

                                                {/* PnL Value */}
                                                <td className={cn("px-4 py-3 text-right font-mono font-bold", pos.unrealized_pnl >= 0 ? "text-green-500" : "text-red-500")}>
                                                    {pos.unrealized_pnl >= 0 ? "+" : ""}{pos.unrealized_pnl.toFixed(2)}
                                                </td>

                                                {/* PnL % */}
                                                <td className={cn("px-4 py-3 text-right font-mono text-xs", pnlPercent >= 0 ? "text-green-500" : "text-red-500")}>
                                                    {pnlPercent >= 0 ? "+" : ""}{pnlPercent.toFixed(2)}%
                                                </td>

                                                <td className="px-4 py-3 text-center text-gray-400 font-mono">{pos.leverage || 1}</td>
                                                <td className="px-4 py-3 text-right text-gray-400 font-mono">{pos.liquidation_price ? `$${pos.liquidation_price}` : "0"}</td>

                                                <td className="px-4 py-3 text-right">
                                                    <div className="flex justify-end gap-3">
                                                        <button className="text-blue-500 hover:text-blue-400 transition-colors" title="View Chart">
                                                            <LineChart className="h-4 w-4" />
                                                        </button>
                                                        <button
                                                            className="text-red-500 hover:text-red-400 transition-colors"
                                                            onClick={() => handleClosePosition(pos.symbol)}
                                                            title="Close Position"
                                                        >
                                                            <X className="h-4 w-4" />
                                                        </button>
                                                    </div>
                                                </td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
