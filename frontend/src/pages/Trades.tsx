import { useEffect } from "react";
import { useBotStore } from "@/stores/useBotStore";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { FileText, ArrowUpRight, ArrowDownRight, History, CheckCircle, XCircle } from "lucide-react";
import { InfoCard } from "@/components/InfoCard";

export function TradesPage() {
    const { trades, fetchTrades } = useBotStore();

    useEffect(() => {
        fetchTrades();
    }, [fetchTrades]);

    const totalTrades = trades.filter(t => t.action !== 'hold').length;
    const buyOrders = trades.filter(t => t.action === 'buy').length;
    const sellOrders = trades.filter(t => t.action === 'sell').length;

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Trade History</h1>
                <p className="text-muted-foreground">Historical record of all executed trades.</p>
            </div>

            <div className="grid gap-4 md:grid-cols-3 mb-6">
                <InfoCard
                    title="Total Trades"
                    value={totalTrades.toString()}
                    subtext="Executed orders"
                    icon={History}
                    className="bg-blue-600"
                />
                <InfoCard
                    title="Buy Orders"
                    value={buyOrders.toString()}
                    subtext="Long positions opened"
                    icon={CheckCircle}
                    className="bg-green-600"
                />
                <InfoCard
                    title="Sell Orders"
                    value={sellOrders.toString()}
                    subtext="Positions closed"
                    icon={XCircle}
                    className="bg-red-600"
                />
            </div>

            <Card className="border shadow-sm">
                <div className="p-4 border-b bg-muted/40 font-semibold flex items-center">
                    Execution Log
                </div>
                <CardContent className="p-0">
                    {trades.length === 0 ? (
                        <div className="flex flex-col items-center justify-center py-12 text-muted-foreground space-y-3">
                            <FileText className="h-10 w-10 opacity-50" />
                            <p>No trade history available yet.</p>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm text-left">
                                <thead className="bg-[#1a1a1a] text-gray-400 uppercase text-xs">
                                    <tr>
                                        <th className="px-4 py-3 font-medium">Time</th>
                                        <th className="px-4 py-3 font-medium">Asset</th>
                                        <th className="px-4 py-3 font-medium">Action</th>
                                        <th className="px-4 py-3 font-medium text-right">Amount</th>
                                        <th className="px-4 py-3 font-medium text-right">Price</th>
                                        <th className="px-4 py-3 font-medium text-right">Total Value</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-border/50 bg-[#0a0a0a]">
                                    {trades.filter(t => t.action !== 'hold').map((trade) => (
                                        <tr key={trade.id} className="hover:bg-muted/10 transition-colors">
                                            <td className="px-4 py-3 whitespace-nowrap text-gray-400 text-xs font-mono">
                                                {new Date(trade.timestamp).toLocaleString()}
                                            </td>
                                            <td className="px-4 py-3 font-bold text-white">{trade.asset}</td>
                                            <td className="px-4 py-3">
                                                <span className={cn(
                                                    "inline-flex items-center gap-1 rounded px-2 py-0.5 text-xs font-bold uppercase",
                                                    trade.action === 'buy'
                                                        ? "bg-green-500/20 text-green-500 border border-green-500/30"
                                                        : (trade.action === 'sell' ? "bg-red-500/20 text-red-500 border border-red-500/30" : "bg-gray-500/20 text-gray-500")
                                                )}>
                                                    {trade.action === 'buy' && <ArrowUpRight className="h-3 w-3" />}
                                                    {trade.action === 'sell' && <ArrowDownRight className="h-3 w-3" />}
                                                    {trade.action}
                                                </span>
                                            </td>
                                            <td className="px-4 py-3 text-right font-mono text-gray-300">{Number(trade.amount || 0).toFixed(4)}</td>
                                            <td className="px-4 py-3 text-right font-mono text-gray-300">
                                                ${Number(trade.price || 0).toLocaleString(undefined, { maximumFractionDigits: (trade.price || 0) > 10 ? 0 : 2 })}
                                            </td>
                                            <td className="px-4 py-3 text-right font-mono text-gray-400">
                                                ${Number((trade.amount || 0) * (trade.price || 0)).toLocaleString(undefined, { maximumFractionDigits: 2 })}
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
