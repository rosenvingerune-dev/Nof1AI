import { useEffect } from "react";
import { useBotStore } from "@/stores/useBotStore";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Info, Check, X, TrendingUp, TrendingDown, Brain, Pause } from "lucide-react";
import { cn } from "@/lib/utils";

export function RecommendationsPage() {
    const {
        proposals,
        botState,
        fetchProposals,
        approveProposal,
        rejectProposal,
    } = useBotStore();

    // Auto-refresh proposals periodically
    useEffect(() => {
        fetchProposals();
        const interval = setInterval(fetchProposals, 5000);
        return () => clearInterval(interval);
    }, [fetchProposals]);

    const handleApprove = async (id: string) => {
        await approveProposal(id);
    };

    const handleReject = async (id: string) => {
        await rejectProposal(id, "Manually rejected via UI");
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">AI Recommendations</h1>
                    <p className="text-muted-foreground">Review and approve AI-generated trade proposals.</p>
                </div>
                <div className="flex items-center space-x-2">
                    <span className={cn(
                        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
                        botState?.is_running
                            ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
                            : "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300"
                    )}>
                        {botState?.is_running ? "Bot Active" : "Bot Stopped"}
                    </span>
                </div>
            </div>

            {/* Info Banner */}
            <div className="bg-blue-50/50 dark:bg-blue-900/20 border-l-4 border-blue-500 p-4 rounded-r-md">
                <div className="flex">
                    <div className="flex-shrink-0">
                        <Info className="h-5 w-5 text-blue-400" aria-hidden="true" />
                    </div>
                    <div className="ml-3">
                        <h3 className="text-sm font-medium text-blue-800 dark:text-blue-200">Manual Approval Required</h3>
                        <div className="mt-2 text-sm text-blue-700 dark:text-blue-300">
                            <p>
                                The bot is currently in semi-autonomous mode. It will analyze the market and generate trade proposals,
                                but will not execute them until you explicitly approve them here.
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Stats Row */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <Card className="bg-gradient-to-br from-purple-500/10 to-purple-900/10 border-purple-200/20">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Pending Proposals</CardTitle>
                        <Brain className="h-4 w-4 text-purple-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{proposals.length}</div>
                        <p className="text-xs text-muted-foreground">Waiting for review</p>
                    </CardContent>
                </Card>
            </div>

            {/* Proposals List */}
            <div className="space-y-4">
                {proposals.length === 0 ? (
                    <Card className="border-dashed">
                        <CardContent className="flex flex-col items-center justify-center py-12 text-muted-foreground space-y-3">
                            <Brain className="h-12 w-12 opacity-20" />
                            <h3 className="text-lg font-medium">No pending recommendations</h3>
                            <p className="text-center max-w-sm">
                                The AI engine is analyzing the market. New trade proposals will appear here automatically when criteria are met.
                            </p>
                        </CardContent>
                    </Card>
                ) : (
                    proposals.map((proposal) => (
                        <Card key={proposal.id} className={cn(
                            "overflow-hidden border-l-4",
                            proposal.action === 'buy' ? "border-l-green-500" : (proposal.action === 'sell' ? "border-l-red-500" : "border-l-gray-500")
                        )}>
                            <CardHeader className="bg-muted/30 pb-3">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center space-x-3">
                                        <div className={cn(
                                            "p-2 rounded-full",
                                            proposal.action === 'buy' ? "bg-green-100 text-green-600 dark:bg-green-900/30" : (proposal.action === 'sell' ? "bg-red-100 text-red-600 dark:bg-red-900/30" : "bg-gray-100 text-gray-600")
                                        )}>
                                            {proposal.action === 'buy' && <TrendingUp className="h-5 w-5" />}
                                            {proposal.action === 'sell' && <TrendingDown className="h-5 w-5" />}
                                            {proposal.action === 'hold' && <Pause className="h-5 w-5" />}
                                        </div>
                                        <div>
                                            <CardTitle className="text-xl">{proposal.asset}</CardTitle>
                                            <CardDescription className="font-mono text-xs uppercase">
                                                {proposal.action} ORDER
                                            </CardDescription>
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <div className="text-sm font-medium text-muted-foreground">Confidence</div>
                                        <div className="flex items-center space-x-2">
                                            <Progress value={(proposal.confidence > 1 ? proposal.confidence : proposal.confidence * 100)} className="w-20 h-2" />
                                            <span className="font-bold text-lg">
                                                {((proposal.confidence > 1 ? proposal.confidence : proposal.confidence * 100)).toFixed(0)}%
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </CardHeader>

                            <CardContent className="pt-6">
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                                    <div className="space-y-4">
                                        <div className="grid grid-cols-2 gap-4">
                                            <div className="p-3 bg-muted/30 rounded-lg">
                                                <div className="text-xs text-muted-foreground mb-1">Entry Price</div>
                                                <div className="text-lg font-mono font-semibold">${proposal.entry_price?.toLocaleString()}</div>
                                            </div>
                                            <div className="p-3 bg-muted/30 rounded-lg">
                                                <div className="text-xs text-muted-foreground mb-1">Size</div>
                                                <div className="text-lg font-mono font-semibold">{proposal.amount?.toFixed(4)}</div>
                                            </div>
                                        </div>

                                        <div className="grid grid-cols-2 gap-4">
                                            <div className="p-3 bg-green-500/10 rounded-lg border border-green-500/20">
                                                <div className="text-xs text-green-600 dark:text-green-400 mb-1">Take Profit</div>
                                                <div className="text-lg font-mono font-semibold text-green-700 dark:text-green-300">
                                                    ${proposal.tp_price?.toLocaleString() || "N/A"}
                                                </div>
                                            </div>
                                            <div className="p-3 bg-red-500/10 rounded-lg border border-red-500/20">
                                                <div className="text-xs text-red-600 dark:text-red-400 mb-1">Stop Loss</div>
                                                <div className="text-lg font-mono font-semibold text-red-700 dark:text-red-300">
                                                    ${proposal.sl_price?.toLocaleString() || "N/A"}
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="md:col-span-2 space-y-3">
                                        <h4 className="font-semibold flex items-center gap-2">
                                            <Brain className="h-4 w-4 text-purple-500" />
                                            AI Analysis
                                        </h4>
                                        <div className="bg-muted/30 p-4 rounded-lg text-sm leading-relaxed whitespace-pre-wrap">
                                            {proposal.rationale}
                                        </div>

                                        {proposal.timestamp && (
                                            <div className="text-xs text-muted-foreground text-right">
                                                Generated: {new Date(proposal.timestamp).toLocaleString()}
                                            </div>
                                        )}
                                    </div>
                                </div>

                                <div className="flex items-center justify-end gap-3 pt-4 border-t">
                                    <Button
                                        variant="outline"
                                        className="border-red-200 hover:bg-red-50 text-red-700 hover:text-red-800 dark:border-red-900/50 dark:hover:bg-red-950/50 dark:text-red-400"
                                        onClick={() => handleReject(proposal.id)}
                                    >
                                        <X className="w-4 h-4 mr-2" />
                                        Reject
                                    </Button>
                                    <Button
                                        className="bg-green-600 hover:bg-green-700 text-white"
                                        onClick={() => handleApprove(proposal.id)}
                                    >
                                        <Check className="w-4 h-4 mr-2" />
                                        Approve & Execute
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    ))
                )}
            </div>
        </div>
    );
}
