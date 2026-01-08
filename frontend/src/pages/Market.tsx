import { useBotStore } from "@/stores/useBotStore";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { TrendingUp, TrendingDown, Activity, DollarSign, BarChart3, PieChart } from "lucide-react";
import { InfoCard } from "@/components/InfoCard";

export function MarketPage() {
    const { botState } = useBotStore();

    if (!botState) {
        return <div className="p-10 text-center">Loading market data...</div>;
    }

    const { market_data } = botState;
    const assets = market_data ? Object.values(market_data) : [];

    // Calculate Summary Stats
    const bullishCount = assets.filter(a => (a.change_24h || 0) > 0).length;
    const isBullish = bullishCount > assets.length / 2;
    const totalVolume = assets.reduce((acc, a) => acc + (a.volume_24h || 0), 0);

    const getRsiColor = (rsi: number) => {
        if (rsi > 70) return "text-red-500";
        if (rsi < 30) return "text-green-500";
        return "text-gray-400";
    };

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Market Data</h1>
                <p className="text-muted-foreground">Real-time market analysis and technical indicators.</p>
            </div>

            {/* Summary Cards */}
            <div className="grid gap-4 md:grid-cols-3">
                <InfoCard
                    title="Market Sentiment"
                    value={isBullish ? "Bullish" : "Bearish"}
                    subtext={`${bullishCount} of ${assets.length} assets up`}
                    icon={PieChart}
                    className={isBullish ? "bg-green-600/20 text-green-500 border-green-500/30" : "bg-red-600/20 text-red-500 border-red-500/30"}
                />
                <InfoCard
                    title="Total Volume (24h)"
                    value={`$${totalVolume.toLocaleString(undefined, { notation: "compact", maximumFractionDigits: 1 })}`}
                    subtext="Aggregate market volume"
                    icon={BarChart3}
                    className="bg-blue-600 text-white"
                />
                <InfoCard
                    title="Assets Monitored"
                    value={assets.length.toString()}
                    subtext="Active markets"
                    icon={Activity}
                    className="bg-purple-600 text-white"
                />
            </div>

            {/* Detailed Table */}
            <Card className="border shadow-sm">
                <div className="p-4 border-b bg-muted/40 font-semibold flex items-center">
                    Market Overview
                </div>
                <CardContent className="p-0">
                    {assets.length === 0 ? (
                        <div className="flex flex-col items-center justify-center py-12 text-muted-foreground space-y-3">
                            <Activity className="h-10 w-10 opacity-50" />
                            <p>No market data available.</p>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm text-left">
                                <thead className="bg-[#1a1a1a] text-gray-400 uppercase text-xs">
                                    <tr>
                                        <th className="px-4 py-3 font-medium">Asset</th>
                                        <th className="px-4 py-3 font-medium text-right">Price</th>
                                        <th className="px-4 py-3 font-medium text-right">24h Change</th>
                                        <th className="px-4 py-3 font-medium text-right">Volume</th>
                                        <th className="px-4 py-3 font-medium text-right">Open Interest</th>
                                        <th className="px-4 py-3 font-medium text-right">Funding Rate</th>
                                        <th className="px-4 py-3 font-medium text-right">RSI (14)</th>
                                        <th className="px-4 py-3 font-medium text-right">EMA (20)</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-border/50 bg-[#0a0a0a]">
                                    {assets.map((data) => (
                                        <tr key={data.asset} className="hover:bg-muted/10 transition-colors">
                                            <td className="px-4 py-3 font-bold text-white">{data.asset}</td>
                                            <td className="px-4 py-3 text-right font-mono text-gray-300">
                                                ${data.current_price.toLocaleString(undefined, { maximumFractionDigits: data.current_price > 10 ? 0 : 2 })}
                                            </td>
                                            <td className="px-4 py-3 text-right">
                                                <div className={cn(
                                                    "inline-flex items-center justify-end font-mono font-medium",
                                                    (data.change_24h || 0) >= 0 ? "text-green-500" : "text-red-500"
                                                )}>
                                                    {(data.change_24h || 0) >= 0 ? <TrendingUp className="w-3 h-3 mr-1" /> : <TrendingDown className="w-3 h-3 mr-1" />}
                                                    {Math.abs(data.change_24h || 0).toFixed(2)}%
                                                </div>
                                            </td>
                                            <td className="px-4 py-3 text-right font-mono text-gray-400">
                                                ${(data.volume_24h || 0).toLocaleString(undefined, { notation: "compact" })}
                                            </td>
                                            <td className="px-4 py-3 text-right font-mono text-gray-400">
                                                ${(data.open_interest || 0).toLocaleString(undefined, { notation: "compact" })}
                                            </td>
                                            <td className="px-4 py-3 text-right font-mono text-yellow-500/80">
                                                {(data.funding_rate || 0).toFixed(6)}%
                                            </td>
                                            <td className={cn("px-4 py-3 text-right font-mono font-bold", getRsiColor(data.intraday?.rsi14 || 50))}>
                                                {data.intraday?.rsi14?.toFixed(1) || "-"}
                                            </td>
                                            <td className="px-4 py-3 text-right font-mono text-blue-400">
                                                ${data.intraday?.ema20?.toLocaleString(undefined, { maximumFractionDigits: (data.intraday?.ema20 || 0) > 10 ? 0 : 2 }) || "-"}
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
