import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { type LucideIcon } from "lucide-react";

interface InfoCardProps {
    title: string;
    value: string;
    subtext: string;
    icon?: LucideIcon;
    className?: string;
}

export function InfoCard({ title, value, subtext, icon: Icon, className }: InfoCardProps) {
    return (
        <Card className={cn("border-none shadow-md text-white", className)}>
            <CardContent className="p-6">
                <div className="flex justify-between items-start">
                    <div className="space-y-1">
                        <div className="text-4xl font-bold">{value}</div>
                        <div className="text-sm font-medium opacity-90">{title}</div>
                        <div className="text-xs opacity-75">{subtext}</div>
                    </div>
                    {Icon && <Icon className="h-8 w-8 opacity-20" />}
                </div>
            </CardContent>
        </Card>
    )
}
