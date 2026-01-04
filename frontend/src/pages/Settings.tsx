import { useEffect, useState } from "react";
import { useBotStore } from "@/stores/useBotStore";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
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

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4">
                        {/* Trading Mode */}
                        <div className="flex flex-row items-center justify-between rounded-lg border p-4">
                            <div className="space-y-0.5">
                                <Label className="text-base">Trading Mode</Label>
                                <div className="text-sm text-muted-foreground">
                                    Set to Auto for autonomous execution.
                                </div>
                            </div>
                            <div className="flex items-center space-x-2">
                                <span className={cn("text-sm", formData.trading_mode === 'manual' ? "font-bold" : "text-muted-foreground")}>Manual</span>
                                <Switch
                                    checked={formData.trading_mode === 'auto'}
                                    onCheckedChange={(checked) => setFormData({ ...formData, trading_mode: checked ? 'auto' : 'manual' })}
                                />
                                <span className={cn("text-sm", formData.trading_mode === 'auto' ? "font-bold" : "text-muted-foreground")}>Auto</span>
                            </div>
                        </div>

                        {/* Auto Trade Enabled (Master Switch) */}
                        <div className="flex flex-row items-center justify-between rounded-lg border p-4">
                            <div className="space-y-0.5">
                                <Label className="text-base">Master Switch</Label>
                                <div className="text-sm text-muted-foreground">
                                    Enable/Disable all automatic trading activities.
                                </div>
                            </div>
                            <Switch
                                checked={formData.auto_trade_enabled ?? false}
                                onCheckedChange={(checked) => setFormData({ ...formData, auto_trade_enabled: checked })}
                            />
                        </div>
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
        </div>
    );

    // Helper to wire up the Save button correctly passed as callback
    function handleClose() {
        handleSave();
    }
}
