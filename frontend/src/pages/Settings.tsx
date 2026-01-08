import { useEffect, useState } from "react";
import { useBotStore } from "@/stores/useBotStore";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { cn } from "@/lib/utils";
import { Save, AlertCircle, RefreshCw } from "lucide-react";
import type { Settings } from "@/types";

export function SettingsPage() {
    const { settings, fetchSettings, updateSettings, isLoading } = useBotStore();
    const [formData, setFormData] = useState<Settings | null>(null);
    const [isSaving, setIsSaving] = useState(false);
    const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

    useEffect(() => {
        fetchSettings();
    }, [fetchSettings]);

    useEffect(() => {
        if (settings) {
            setFormData(settings);
        }
    }, [settings]);

    const handleSave = async () => {
        if (!formData) return;
        setIsSaving(true);
        setMessage(null);
        try {
            await updateSettings(formData);
            setMessage({ type: 'success', text: "Settings saved successfully." });
        } catch (err: any) {
            setMessage({ type: 'error', text: "Failed to save settings." });
        } finally {
            setIsSaving(false);
        }
    };

    if (!formData && isLoading) {
        return <div className="p-10 text-center">Loading settings...</div>;
    }

    if (!formData) {
        // Fallback if load failed or empty, though fetchSettings should prevent this ideally or show error state in store
        return (
            <div className="p-10 text-center space-y-4">
                <p>Failed to load settings or no settings available.</p>
                <Button onClick={() => fetchSettings()}>Retry</Button>
            </div>
        )
    }

    return (
        <div className="space-y-6 max-w-3xl">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
                <p className="text-muted-foreground">Configure bot parameters and preferences.</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Trading Configuration</CardTitle>
                    <CardDescription>
                        Adjust how the bot interacts with the market.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    {/* Assets */}
                    <div className="space-y-2">
                        <Label htmlFor="assets">Trading Assets</Label>
                        <Input
                            id="assets"
                            value={formData.assets.join(", ")}
                            onChange={(e) => setFormData({ ...formData, assets: e.target.value.split(",").map(s => s.trim()).filter(Boolean) })}
                            placeholder="BTC, ETH, SOL"
                        />
                        <p className="text-sm text-muted-foreground">Comma-separated list of symbols to trade (e.g. BTC, ETH).</p>
                    </div>

                    {/* Interval */}
                    <div className="space-y-2">
                        <Label htmlFor="interval">Time Interval</Label>
                        <select
                            id="interval"
                            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                            value={formData.interval}
                            onChange={(e) => setFormData({ ...formData, interval: e.target.value })}
                        >
                            <option value="1m">1 Minute</option>
                            <option value="5m">5 Minutes</option>
                            <option value="15m">15 Minutes</option>
                            <option value="1h">1 Hour</option>
                            <option value="4h">4 Hours</option>
                            <option value="1d">1 Day</option>
                        </select>
                        <p className="text-sm text-muted-foreground">Candlestick interval for analysis.</p>
                    </div>

                    {/* Max Position Size - Optional */}
                    <div className="space-y-2">
                        <Label htmlFor="max_size">Max Position Size ($)</Label>
                        <Input
                            id="max_size"
                            type="number"
                            value={formData.max_position_size || ""}
                            onChange={(e) => setFormData({ ...formData, max_position_size: parseFloat(e.target.value) || 0 })}
                            placeholder="1000"
                        />
                        <p className="text-sm text-muted-foreground">Maximum capital allocated per position (0 for no limit).</p>
                    </div>

                    {/* Target Leverage */}
                    <div className="space-y-2">
                        <Label htmlFor="leverage">Target Leverage (x)</Label>
                        <Input
                            id="leverage"
                            type="number"
                            min="1"
                            max="20"
                            value={formData.leverage || 1}
                            onChange={(e) => setFormData({ ...formData, leverage: parseInt(e.target.value) || 1 })}
                            placeholder="1"
                        />
                        <p className="text-sm text-muted-foreground">Leverage multiplier (e.g., 5 for 5x). Be careful!</p>
                    </div>

                    {/* Operation Mode - Unified Control */}
                    <div className="space-y-3 pt-2">
                        <Label>Operation Mode</Label>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {/* Manual Mode */}
                            <div
                                className={cn(
                                    "cursor-pointer rounded-lg border-2 p-4 transition-all hover:bg-muted/50",
                                    formData.trading_mode === 'manual' ? "border-primary bg-primary/5" : "border-muted"
                                )}
                                onClick={() => setFormData({ ...formData, trading_mode: 'manual', auto_trade_enabled: false })}
                            >
                                <div className="font-semibold text-foreground">Manual</div>
                                <div className="text-xs text-muted-foreground mt-1">Bot is disabled. You trade manually.</div>
                            </div>

                            {/* Assistant / Semi-Auto */}
                            <div
                                className={cn(
                                    "cursor-pointer rounded-lg border-2 p-4 transition-all hover:bg-muted/50",
                                    (formData.trading_mode === 'auto' && !formData.auto_trade_enabled) ? "border-primary bg-primary/5" : "border-muted"
                                )}
                                onClick={() => setFormData({ ...formData, trading_mode: 'auto', auto_trade_enabled: false })}
                            >
                                <div className="font-semibold text-foreground">Assistant</div>
                                <div className="text-xs text-muted-foreground mt-1">Bot suggests trades. You approve execution.</div>
                            </div>

                            {/* Fully Autonomous */}
                            <div
                                className={cn(
                                    "cursor-pointer rounded-lg border-2 p-4 transition-all hover:bg-muted/50",
                                    (formData.trading_mode === 'auto' && formData.auto_trade_enabled) ? "border-primary bg-primary/5" : "border-muted"
                                )}
                                onClick={() => setFormData({ ...formData, trading_mode: 'auto', auto_trade_enabled: true })}
                            >
                                <div className="font-semibold text-foreground">Autonomous</div>
                                <div className="text-xs text-muted-foreground mt-1">Bot trades automatically 24/7.</div>
                            </div>
                        </div>
                    </div>

                    {/* Auto Trade Confidence Threshold */}
                    <div className="space-y-2">
                        <Label htmlFor="threshold">Auto-Trade Confidence Threshold (%)</Label>
                        <Input
                            id="threshold"
                            type="number"
                            min="0"
                            max="100"
                            value={formData.auto_trade_threshold || 80}
                            onChange={(e) => setFormData({ ...formData, auto_trade_threshold: parseFloat(e.target.value) || 80 })}
                            placeholder="80"
                        />
                        <p className="text-sm text-muted-foreground">Minimum AI confidence required to automatically execute a trade (Default: 80%).</p>
                    </div>

                    {message && (
                        <div className={cn(
                            "flex items-center p-3 rounded-md text-sm",
                            message.type === 'success' ? "bg-green-500/15 text-green-600" : "bg-red-500/15 text-red-600"
                        )}>
                            {message.type === 'error' && <AlertCircle className="w-4 h-4 mr-2" />}
                            {message.text}
                        </div>
                    )}

                </CardContent>
                <CardFooter className="flex justify-between border-t p-6">
                    <Button variant="ghost" onClick={() => fetchSettings()}>
                        <RefreshCw className="mr-2 h-4 w-4" /> Reset
                    </Button>
                    <Button onClick={handleClose} disabled={isSaving} className="bg-primary">
                        {isSaving ? "Saving..." : <><Save className="mr-2 h-4 w-4" /> Save Changes</>}
                    </Button>
                </CardFooter>
            </Card>
        </div >
    );

    // Helper to wire up the Save button correctly passed as callback
    function handleClose() {
        handleSave();
    }
}
