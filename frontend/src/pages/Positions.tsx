import { useBotStore } from "@/stores/useBotStore";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { TrendingUp, TrendingDown, XCircle, AlertCircle } from "lucide-react";

export function PositionsPage() {
    const { botState, closePosition } = useBotStore();

    if (!botState) {
        return <div className="p-10 text-center">Loading positions...</div>;
    }

    const { positions } = botState;

    const handleClosePosition = async (symbol: string) => {
        if (confirm(`Are you sure you want to close the position for ${symbol}?`)) {
            await closePosition(symbol);
        }
    };

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Positions</h1>
                <p className="text-muted-foreground">Manage and view detailed status of open positions.</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Active Positions</CardTitle>
                    <CardDescription>
                        Real-time overview of your current market exposure.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    {positions.length === 0 ? (
                        <div className="flex flex-col items-center justify-center py-12 text-muted-foreground space-y-3">
                            <AlertCircle className="h-10 w-10 opacity-50" />
                            <p>No active positions found.</p>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm text-left">
                                <thead className="bg-muted/50 text-muted-foreground uppercase text-xs">
                                    <tr>
                                        <th className="px-4 py-3 rounded-tl-md">Asset</th>
                                        <th className="px-4 py-3">Side</th>
                                        <th className="px-4 py-3 text-right">Size</th>
                                        <th className="px-4 py-3 text-right">Entry Price</th>
                                        <th className="px-4 py-3 text-right">Mark Price</th>
                                        <th className="px-4 py-3 text-right">Unrealized PnL</th>
                                        <th className="px-4 py-3 text-right rounded-tr-md">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y">
                                    {positions.map((pos) => (
                                        <tr key={pos.symbol} className="hover:bg-muted/30 transition-colors">
                                            <td className="px-4 py-4 font-medium">{pos.symbol}</td>
                                            <td className="px-4 py-4">
                                                <span className={cn(
                                                    "inline-flex items-center rounded-full px-2 py-1 text-xs font-medium ring-1 ring-inset",
                                                    pos.quantity > 0
                                                        ? "bg-green-50 text-green-700 ring-green-600/20"
                                                        : "bg-red-50 text-red-700 ring-red-600/20"
                                                )}>
                                                    {pos.quantity > 0 ? "LONG" : "SHORT"}
                                                </span>
                                            </td>
                                            <td className="px-4 py-4 text-right font-mono">{Math.abs(pos.quantity)}</td>
                                            <td className="px-4 py-4 text-right font-mono">${pos.entry_price.toLocaleString()}</td>
                                            <td className="px-4 py-4 text-right font-mono">${pos.current_price.toLocaleString()}</td>
                                            <td className={cn("px-4 py-4 text-right font-mono font-medium", pos.unrealized_pnl >= 0 ? "text-green-600" : "text-red-600")}>
                                                <div className="flex items-center justify-end gap-1">
                                                    {pos.unrealized_pnl >= 0 ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                                                    {pos.unrealized_pnl > 0 ? "+" : ""}{pos.unrealized_pnl.toFixed(2)}
                                                </div>
                                            </td>
                                            <td className="px-4 py-4 text-right">
                                                <Button
                                                    variant="destructive"
                                                    size="sm"
                                                    onClick={() => handleClosePosition(pos.symbol)}
                                                    className="h-8 px-2 lg:px-3"
                                                >
                                                    <XCircle className="h-3.5 w-3.5 sm:mr-2" />
                                                    <span className="hidden sm:inline">Close</span>
                                                </Button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
