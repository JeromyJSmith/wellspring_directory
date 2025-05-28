// 🎙️ Otter.ai Insights Feed Component for Wellspring Dashboard

"use client";

import React, { useState, useEffect, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { cn, dateUtils, notificationUtils } from "@/lib/utils";
import type { InsightsFeedProps, OtterInsight, InsightType } from "@/types";
import {
  Brain,
  AlertTriangle,
  CheckCircle,
  Filter,
  Mic,
  Clock,
  RefreshCw,
  ChevronDown,
  Zap,
  TrendingUp,
  FileText,
  Users,
} from "lucide-react";

// Insight type configuration
const INSIGHT_CONFIG = {
  decision: {
    label: "Decision",
    icon: Brain,
    color: "text-blue-600 bg-blue-100 border-blue-200",
    emoji: "🧠",
  },
  risk: {
    label: "Risk",
    icon: AlertTriangle,
    color: "text-red-600 bg-red-100 border-red-200",
    emoji: "🚩",
  },
  action: {
    label: "Action",
    icon: CheckCircle,
    color: "text-green-600 bg-green-100 border-green-200",
    emoji: "✅",
  },
  update: {
    label: "Update",
    icon: TrendingUp,
    color: "text-orange-600 bg-orange-100 border-orange-200",
    emoji: "📈",
  },
  meeting: {
    label: "Meeting",
    icon: Users,
    color: "text-purple-600 bg-purple-100 border-purple-200",
    emoji: "👥",
  },
  document: {
    label: "Document",
    icon: FileText,
    color: "text-gray-600 bg-gray-100 border-gray-200",
    emoji: "📄",
  },
};

// Filter options
const FILTER_OPTIONS = [
  { value: "all", label: "All Insights" },
  { value: "decision", label: "Decisions" },
  { value: "risk", label: "Risks" },
  { value: "action", label: "Actions" },
  { value: "update", label: "Updates" },
  { value: "meeting", label: "Meetings" },
  { value: "document", label: "Documents" },
];

// Individual insight item component
interface InsightItemProps {
  insight: OtterInsight;
  isNew?: boolean;
  onClick?: (insight: OtterInsight) => void;
}

const InsightItem = ({ insight, isNew = false, onClick }: InsightItemProps) => {
  const config = INSIGHT_CONFIG[insight.type] || INSIGHT_CONFIG.update;
  const IconComponent = config.icon;
  const priority = notificationUtils.getInsightPriority(insight);

  return (
    <div
      className={cn(
        "p-3 rounded-lg border transition-all duration-200 cursor-pointer",
        "hover:shadow-sm hover:border-gray-300",
        "bg-white",
        isNew && "ring-2 ring-blue-500/20 bg-blue-50/50",
        priority === "high" && "border-l-4 border-l-red-500",
        priority === "medium" && "border-l-4 border-l-yellow-500"
      )}
      onClick={() => onClick?.(insight)}
    >
      <div className="flex items-start space-x-3">
        {/* Timestamp and type badge */}
        <div className="flex flex-col items-center space-y-2 flex-shrink-0">
          <div className="text-xs text-gray-500 font-medium">
            {dateUtils.formatDateTime(insight.timestamp).split(" ")[1]}
          </div>
          <Badge
            variant="outline"
            className={cn("text-xs font-medium", config.color)}
          >
            <span className="mr-1">{config.emoji}</span>
            {config.label}
          </Badge>
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between mb-2">
            <div className="text-sm font-medium text-gray-900 leading-tight">
              {insight.summary}
            </div>
            {isNew && (
              <div className="flex-shrink-0 ml-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
              </div>
            )}
          </div>

          {/* Project info */}
          {insight.projectId && (
            <div className="text-xs text-gray-600 mb-2">
              Project: {insight.projectId}
            </div>
          )}

          {/* Full timestamp */}
          <div className="text-xs text-gray-500">
            {dateUtils.formatDateTime(insight.timestamp)}
          </div>

          {/* Priority indicator */}
          {priority === "high" && (
            <div className="mt-2 flex items-center space-x-1">
              <Zap size={12} className="text-red-500" />
              <span className="text-xs text-red-600 font-medium">
                High Priority
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Hover actions */}
      <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-200 mt-2 pt-2 border-t">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Click to view details</span>
          <IconComponent size={14} />
        </div>
      </div>
    </div>
  );
};

// Main insights feed component
export function InsightsFeed({
  insights,
  onInsightClick,
  onLoadMore,
  isLoading = false,
  className,
}: InsightsFeedProps) {
  const [filter, setFilter] = useState<string>("all");
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [newInsights, setNewInsights] = useState<Set<string>>(new Set());
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const [lastCount, setLastCount] = useState(insights.length);

  // Filter insights
  const filteredInsights = React.useMemo(() => {
    if (filter === "all") return insights;
    return insights.filter((insight) => insight.type === filter);
  }, [insights, filter]);

  // Detect new insights
  useEffect(() => {
    if (insights.length > lastCount) {
      const newIds = insights
        .slice(0, insights.length - lastCount)
        .map((insight) => insight.id);

      setNewInsights((prev) => new Set([...prev, ...newIds]));

      // Auto-scroll to top for new insights
      if (scrollAreaRef.current) {
        scrollAreaRef.current.scrollTo({ top: 0, behavior: "smooth" });
      }

      // Clear new status after 5 seconds
      setTimeout(() => {
        setNewInsights((prev) => {
          const updated = new Set(prev);
          newIds.forEach((id) => updated.delete(id));
          return updated;
        });
      }, 5000);
    }
    setLastCount(insights.length);
  }, [insights.length, lastCount]);

  // Auto-refresh every 30 seconds
  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(() => {
      // In real app, this would trigger a refresh
      console.log("Auto-refreshing insights...");
    }, 30000);

    return () => clearInterval(interval);
  }, [autoRefresh]);

  const handleRefresh = () => {
    // In real app, this would trigger data refetch
    onLoadMore?.();
  };

  return (
    <Card className={cn("w-full h-full flex flex-col", className)}>
      <CardHeader className="flex-shrink-0">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <Mic size={20} className="text-gray-600" />
            <span>Latest Project Insights</span>
          </CardTitle>

          <div className="flex items-center space-x-2">
            <Badge variant="outline" className="text-xs">
              {filteredInsights.length} insights
            </Badge>

            <Button
              variant="outline"
              size="sm"
              onClick={handleRefresh}
              disabled={isLoading}
              className="text-xs"
            >
              <RefreshCw
                size={14}
                className={cn("mr-1", isLoading && "animate-spin")}
              />
              Refresh
            </Button>
          </div>
        </div>

        {/* Filters */}
        <div className="flex items-center justify-between pt-2">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm" className="text-xs">
                <Filter size={14} className="mr-2" />
                {FILTER_OPTIONS.find((opt) => opt.value === filter)?.label}
                <ChevronDown size={14} className="ml-2" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start" className="w-48">
              {FILTER_OPTIONS.map((option) => (
                <DropdownMenuItem
                  key={option.value}
                  onClick={() => setFilter(option.value)}
                  className={cn(
                    "text-sm",
                    filter === option.value && "bg-blue-50 text-blue-700"
                  )}
                >
                  {option.label}
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>

          <div className="flex items-center space-x-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setAutoRefresh(!autoRefresh)}
              className={cn(
                "text-xs",
                autoRefresh ? "text-green-600" : "text-gray-500"
              )}
            >
              <div
                className={cn(
                  "w-2 h-2 rounded-full mr-2",
                  autoRefresh ? "bg-green-500 animate-pulse" : "bg-gray-400"
                )}
              />
              Auto-refresh
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="flex-1 overflow-hidden p-0">
        <ScrollArea ref={scrollAreaRef} className="h-full px-6 pb-6">
          <div className="space-y-3">
            {filteredInsights.length === 0 ? (
              <div className="flex items-center justify-center py-12 text-gray-500">
                <div className="text-center">
                  <Mic size={48} className="mx-auto mb-4 text-gray-400" />
                  <p className="text-lg font-medium">No insights found</p>
                  <p className="text-sm">
                    {filter === "all"
                      ? "Start a meeting to generate insights"
                      : `No ${filter} insights available`}
                  </p>
                </div>
              </div>
            ) : (
              filteredInsights.map((insight) => (
                <InsightItem
                  key={insight.id}
                  insight={insight}
                  isNew={newInsights.has(insight.id)}
                  onClick={onInsightClick}
                />
              ))
            )}

            {/* Load more button */}
            {filteredInsights.length > 0 && onLoadMore && (
              <div className="pt-4">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={onLoadMore}
                  disabled={isLoading}
                  className="w-full text-xs"
                >
                  {isLoading ? (
                    <RefreshCw size={14} className="mr-2 animate-spin" />
                  ) : (
                    <Clock size={14} className="mr-2" />
                  )}
                  Load More Insights
                </Button>
              </div>
            )}
          </div>
        </ScrollArea>
      </CardContent>

      {/* Footer status */}
      <div className="flex-shrink-0 border-t px-6 py-3">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <div className="flex items-center space-x-2">
            <Mic size={12} />
            <span>Otter.ai Integration</span>
          </div>

          <div className="flex items-center space-x-2">
            <span>Last sync: {new Date().toLocaleTimeString()}</span>
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span>Live</span>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}

export default InsightsFeed;
