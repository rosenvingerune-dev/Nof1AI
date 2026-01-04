import { useEffect } from "react";
import { useBotStore } from "@/stores/useBotStore";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { FileText, ArrowUpRight, ArrowDownRight } from "lucide-react";

export function TradesPage() {
    const { trades, fetchTrades } = useBotStore();

    useEffect(() => {
        fetchTrades();
    }, [fetchTrades]);

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Trade History</h1>
                <p className="text-muted-foreground">Historical record of all executed trades.</p>
            </div>

            <div className="grid gap-4 md:grid-cols-3 mb-6">
                <Card>
                    <CardHeader className="py-4">
                        <CardTitle className="text-sm font-medium text-muted-foreground">Total Trades</CardTitle>
                        <div className="text-2xl font-bold">{trades.filter(t => t.action !== 'hold').length}</div>
                    </CardHeader>
                </Card>
                <Card>
                    <CardHeader className="py-4">
                        <CardTitle className="text-sm font-medium text-muted-foreground">Buy Orders</CardTitle>
                        <div className="text-2xl font-bold text-green-600">{trades.filter(t => t.action === 'buy').length}</div>
                    </CardHeader>
                </Card>
                <Card>
                    <CardHeader className="py-4">
                        <CardTitle className="text-sm font-medium text-muted-foreground">Sell Orders</CardTitle>
                        <div className="text-2xl font-bold text-red-600">{trades.filter(t => t.action === 'sell').length}</div>
                    </CardHeader>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Execution Log</CardTitle>
                    <CardDescription>
                        Recent trading activity executed by the bot.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    {trades.length === 0 ? (
                        <div className="flex flex-col items-center justify-center py-12 text-muted-foreground space-y-3">
                            <FileText className="h-10 w-10 opacity-50" />
                            <p>No trade history available yet.</p>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm text-left">
                                <thead className="bg-muted/50 text-muted-foreground uppercase text-xs">
                                    <tr>
                                        <th className="px-4 py-3 rounded-tl-md">Time</th>
                                        <th className="px-4 py-3">Asset</th>
                                        <th className="px-4 py-3">Action</th>
                                        <th className="px-4 py-3 text-right">Amount</th>
                                        <th className="px-4 py-3 text-right">Price</th>
                                        <th className="px-4 py-3 text-right rounded-tr-md">Total Value</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y">
                                    {trades.filter(t => t.action !== 'hold').map((trade) => (
                                        <tr key={trade.id} className="hover:bg-muted/30 transition-colors">
                                            <td className="px-4 py-4 whitespace-nowrap text-muted-foreground text-xs font-mono">
                                                {new Date(trade.timestamp).toLocaleString()}
                                            </td>
                                            <td className="px-4 py-4 font-medium">{trade.asset}</td>
                                            <td className="px-4 py-4">
                                                <span className={cn(
                                                    "inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs font-medium ring-1 ring-inset",
                                                    trade.action === 'buy'
                                                        ? "bg-green-50 text-green-700 ring-green-600/20"
                                                        : (trade.action === 'sell' ? "bg-red-50 text-red-700 ring-red-600/20" : "bg-gray-50 text-gray-600 ring-gray-500/20")
                                                )}>
                                                    {trade.action === 'buy' && <ArrowUpRight className="h-3 w-3" />}
                                                    {trade.action === 'sell' && <ArrowDownRight className="h-3 w-3" />}
                                                    {trade.action.toUpperCase()}
                                                </span>
                                            </td>
                                            <td className="px-4 py-4 text-right font-mono">{trade.amount}</td>
                                            <td className="px-4 py-4 text-right font-mono">${trade.price.toLocaleString()}</td>
                                            <td className="px-4 py-4 text-right font-mono text-muted-foreground">
                                                ${(trade.amount * trade.price).toLocaleString(undefined, { maximumFractionDigits: 2 })}
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
