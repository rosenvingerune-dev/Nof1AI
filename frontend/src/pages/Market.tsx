import { useBotStore } from "@/stores/useBotStore";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { TrendingUp, TrendingDown, Activity, Radio } from "lucide-react";

export function MarketPage() {
    const { botState } = useBotStore();

    if (!botState) {
        return <div className="p-10 text-center">Loading market data...</div>;
    }

    const { market_data } = botState;
    const assets = market_data ? Object.values(market_data) : [];

    // Helper for simple formatting (this is just illustrative, real logic might need historical avg)
    const getLevel = (value: number, type: 'volume' | 'oi') => {
        if (!value) return { label: 'LOW', color: 'text-muted-foreground' };

        // Arbitrary thresholds for demo purposes - in a real app these would be dynamic relative to asset norms
        const thresholdHigh = type === 'volume' ? 500_000_000 : 100_000_000;
        const thresholdMed = type === 'volume' ? 50_000_000 : 10_000_000;

        if (value > thresholdHigh) return { label: 'HIGH', color: 'text-green-500' };
        if (value > thresholdMed) return { label: 'MODERATE', color: 'text-yellow-500' };
        return { label: 'LOW', color: 'text-muted-foreground' };
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Market Data</h1>
                    <p className="text-muted-foreground">Real-time market analysis and technical indicators.</p>
                </div>
            </div>

            {/* Market Sentiment Summary - Moved UP as requested */}
            {assets.length > 0 && (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                    <Card className="bg-gradient-to-br from-blue-500/10 to-blue-900/10 border-blue-200/20">
                        <CardHeader className="py-4 pb-2">
                            <CardTitle className="text-sm font-medium text-muted-foreground">Market Sentiment</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">
                                {(assets.filter(a => (a.change_24h || 0) > 0).length > assets.length / 2) ? "Bullish" : "Bearish"}
                            </div>
                            <p className="text-xs text-muted-foreground">Based on 24h change</p>
                        </CardContent>
                    </Card>
                </div>
            )}

            {assets.length === 0 ? (
                <Card>
                    <CardContent className="flex flex-col items-center justify-center py-12 text-muted-foreground space-y-3">
                        <Activity className="h-10 w-10 opacity-50" />
                        <p>No market data available. Bot might be actively trading in a different mode or initializing.</p>
                    </CardContent>
                </Card>
            ) : (
                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                    {assets.map((data) => (
                        <Card key={data.asset} className="bg-card/50 backdrop-blur-sm border-muted/60">
                            <CardHeader className="pb-3">
                                <div className="flex items-center justify-between">
                                    <CardTitle className="text-xl font-bold">{data.asset}</CardTitle>
                                    <div className={cn(
                                        "flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium",
                                        (data.change_24h || 0) >= 0
                                            ? "bg-green-500/10 text-green-500"
                                            : "bg-red-500/10 text-red-500"
                                    )}>
                                        {(data.change_24h || 0) >= 0 ? <TrendingUp className="w-3 h-3 mr-1" /> : <TrendingDown className="w-3 h-3 mr-1" />}
                                        {(data.change_24h || 0).toFixed(2)}%
                                    </div>
                                </div>
                                <CardDescription className="text-2xl font-mono text-foreground font-semibold">
                                    ${data.current_price.toLocaleString()}
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="space-y-3 text-sm">
                                    <div className="flex items-center justify-between">
                                        <span className="text-muted-foreground text-xs uppercase tracking-wider">Volume (24h)</span>
                                        <div className="text-right">
                                            <div className="font-mono">${(data.volume_24h || 0).toLocaleString(undefined, { notation: "compact" })}</div>
                                            <div className={cn("text-[10px] font-bold", getLevel(data.volume_24h || 0, 'volume').color)}>
                                                {getLevel(data.volume_24h || 0, 'volume').label}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex items-center justify-between">
                                        <span className="text-muted-foreground text-xs uppercase tracking-wider">Open Interest</span>
                                        <div className="text-right">
                                            <div className="font-mono">${(data.open_interest || 0).toLocaleString(undefined, { notation: "compact" })}</div>
                                            <div className={cn("text-[10px] font-bold", getLevel(data.open_interest || 0, 'oi').color)}>
                                                {getLevel(data.open_interest || 0, 'oi').label}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex items-center justify-between">
                                        <span className="text-muted-foreground text-xs uppercase tracking-wider">Funding Rate</span>
                                        <div className="font-mono">{(data.funding_rate || 0).toFixed(6)}%</div>
                                    </div>
                                </div>

                                <div className="pt-2 border-t border-border/50">
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center space-x-2">
                                            <Radio className="w-4 h-4 text-blue-500" />
                                            <span className="text-sm font-medium">RSI (14)</span>
                                        </div>
                                        <span className={cn(
                                            "font-mono text-sm font-medium",
                                            (data.intraday?.rsi14 || 50) > 70 ? "text-red-500" : (data.intraday?.rsi14 || 50) < 30 ? "text-green-500" : "text-muted-foreground"
                                        )}>
                                            {data.intraday?.rsi14?.toFixed(1) || "N/A"}
                                        </span>
                                    </div>
                                    <div className="flex items-center justify-between mt-2">
                                        <span className="text-sm font-medium text-muted-foreground pl-6">EMA (20)</span>
                                        <span className="font-mono text-sm text-foreground">
                                            ${data.intraday?.ema20?.toFixed(2) || "N/A"}
                                        </span>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    );
}
