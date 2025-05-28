// 🎯 KPI Card Component for Wellspring Dashboard

"use client";

import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn, kpiUtils, statusUtils } from "@/lib/utils";
import type { KpiCardProps } from "@/types";
import {
  TrendingUp,
  TrendingDown,
  Minus,
  ArrowUpRight,
  ArrowDownRight,
  ArrowRight,
} from "lucide-react";

export function KpiCard({ kpi, className }: KpiCardProps) {
  const { title, value, trend, format, status } = kpi;

  // Format the KPI value based on its type
  const formattedValue = kpiUtils.formatKPIValue(value, format);

  // Get trend icon component
  const getTrendIcon = () => {
    const iconProps = {
      size: 16,
      className: cn(
        "transition-colors duration-200",
        statusUtils.getTrendColor(trend.direction, status)
      ),
    };

    switch (trend.direction) {
      case "up":
        return <ArrowUpRight {...iconProps} />;
      case "down":
        return <ArrowDownRight {...iconProps} />;
      default:
        return <ArrowRight {...iconProps} />;
    }
  };

  // Get main trend icon for display
  const getMainTrendIcon = () => {
    const iconProps = {
      size: 20,
      className: cn(
        "transition-all duration-300",
        statusUtils.getTrendColor(trend.direction, status)
      ),
    };

    switch (trend.direction) {
      case "up":
        return <TrendingUp {...iconProps} />;
      case "down":
        return <TrendingDown {...iconProps} />;
      default:
        return <Minus {...iconProps} />;
    }
  };

  // Get card border color based on status
  const getCardBorderColor = () => {
    switch (status) {
      case "positive":
        return "border-green-200 hover:border-green-300";
      case "negative":
        return "border-red-200 hover:border-red-300";
      default:
        return "border-gray-200 hover:border-gray-300";
    }
  };

  // Get status indicator dot
  const getStatusDot = () => {
    const dotColor = {
      positive: "bg-green-500",
      negative: "bg-red-500",
      neutral: "bg-gray-400",
    };

    return (
      <div
        className={cn(
          "w-2 h-2 rounded-full transition-all duration-300",
          dotColor[status]
        )}
      />
    );
  };

  return (
    <Card
      className={cn(
        "relative overflow-hidden transition-all duration-300 hover:shadow-lg",
        "border-2 bg-white/50 backdrop-blur-sm",
        getCardBorderColor(),
        "group cursor-pointer",
        className
      )}
    >
      {/* Status indicator line */}
      <div
        className={cn(
          "absolute top-0 left-0 w-full h-1 transition-all duration-300",
          status === "positive" && "bg-green-500",
          status === "negative" && "bg-red-500",
          status === "neutral" && "bg-gray-400",
          "group-hover:h-2"
        )}
      />

      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-gray-600 group-hover:text-gray-800 transition-colors">
          {title}
        </CardTitle>

        {/* Status dot */}
        <div className="flex items-center space-x-1">{getStatusDot()}</div>
      </CardHeader>

      <CardContent className="space-y-3">
        {/* Main value display */}
        <div className="flex items-end justify-between">
          <div className="space-y-1">
            <div className="text-2xl font-bold text-gray-900 group-hover:text-gray-800 transition-all duration-300">
              {formattedValue}
            </div>

            {/* Trend indicator */}
            <div className="flex items-center space-x-2">
              {getMainTrendIcon()}

              <Badge
                variant="outline"
                className={cn(
                  "px-2 py-1 text-xs font-medium transition-all duration-300",
                  "border border-current",
                  statusUtils.getTrendColor(trend.direction, status),
                  trend.direction === "up" &&
                    status === "positive" &&
                    "bg-green-50",
                  trend.direction === "down" &&
                    status === "negative" &&
                    "bg-red-50",
                  trend.direction === "up" &&
                    status === "negative" &&
                    "bg-red-50",
                  trend.direction === "down" &&
                    status === "positive" &&
                    "bg-green-50",
                  "group-hover:shadow-sm"
                )}
              >
                <span className="flex items-center space-x-1">
                  {getTrendIcon()}
                  <span>
                    {trend.percentage > 0
                      ? `${trend.percentage}%`
                      : "No change"}
                  </span>
                </span>
              </Badge>
            </div>
          </div>

          {/* Large trend icon background */}
          <div className="opacity-10 group-hover:opacity-20 transition-opacity duration-300">
            {getMainTrendIcon()}
          </div>
        </div>

        {/* Hover state additional info */}
        <div className="opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-y-2 group-hover:translate-y-0">
          <div className="text-xs text-gray-500 border-t pt-2">
            <div className="flex justify-between items-center">
              <span>Trend</span>
              <span className="font-medium">
                {trend.direction === "up"
                  ? "Increasing"
                  : trend.direction === "down"
                  ? "Decreasing"
                  : "Stable"}
              </span>
            </div>
          </div>
        </div>
      </CardContent>

      {/* Subtle background pattern */}
      <div className="absolute inset-0 opacity-5 pointer-events-none">
        <div className="w-full h-full bg-gradient-to-br from-gray-100 to-transparent" />
      </div>
    </Card>
  );
}

// 📊 KPI Cards Grid Component
interface KpiCardsGridProps {
  kpis: import("@/types").KPICard[];
  className?: string;
}

export function KpiCardsGrid({ kpis, className }: KpiCardsGridProps) {
  return (
    <div
      className={cn(
        "grid gap-4",
        "grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4",
        className
      )}
    >
      {kpis.map((kpi) => (
        <KpiCard
          key={kpi.id}
          kpi={kpi}
          className="animate-in fade-in-50 duration-500"
        />
      ))}
    </div>
  );
}

// 🎯 Quick KPI Card (Simplified version)
interface QuickKpiProps {
  title: string;
  value: string | number;
  change?: number;
  format?: "number" | "percentage" | "currency";
  status?: "positive" | "negative" | "neutral";
  className?: string;
}

export function QuickKpiCard({
  title,
  value,
  change = 0,
  format = "number",
  status = "neutral",
  className,
}: QuickKpiProps) {
  const trend = {
    direction:
      change > 0
        ? ("up" as const)
        : change < 0
        ? ("down" as const)
        : ("neutral" as const),
    percentage: Math.abs(change),
  };

  const kpi: import("@/types").KPICard = {
    id: `quick-${title.toLowerCase().replace(/\s+/g, "-")}`,
    title,
    value,
    trend,
    format,
    status,
  };

  return <KpiCard kpi={kpi} className={className} />;
}

export default KpiCard;
