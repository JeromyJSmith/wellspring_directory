// 📊 Project Status Chart Component for Wellspring Dashboard

"use client";

import React, { useMemo } from "react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn, chartUtils } from "@/lib/utils";
import type {
  ProjectStatusChartProps,
  ProjectStatusDistribution,
} from "@/types";
import {
  CheckCircle2,
  Clock,
  AlertTriangle,
  XCircle,
  Activity,
} from "lucide-react";

// Chart configuration
const CHART_CONFIG = {
  innerRadius: 60,
  outerRadius: 100,
  paddingAngle: 2,
  dataKey: "value",
};

// Status configuration with colors and icons
const STATUS_CONFIG = {
  onTrack: {
    label: "On Track",
    color: "#10B981", // Green
    bgColor: "bg-green-100",
    textColor: "text-green-700",
    icon: CheckCircle2,
  },
  minorDelay: {
    label: "Minor Delay",
    color: "#F59E0B", // Yellow
    bgColor: "bg-yellow-100",
    textColor: "text-yellow-700",
    icon: Clock,
  },
  atRisk: {
    label: "At Risk",
    color: "#EF4444", // Red
    bgColor: "bg-red-100",
    textColor: "text-red-700",
    icon: AlertTriangle,
  },
  completed: {
    label: "Completed",
    color: "#3B82F6", // Blue
    bgColor: "bg-blue-100",
    textColor: "text-blue-700",
    icon: CheckCircle2,
  },
};

// Custom tooltip component
const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload || !payload[0]) return null;

  const data = payload[0].payload;
  const config = STATUS_CONFIG[data.name as keyof typeof STATUS_CONFIG];

  return (
    <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
      <div className="flex items-center space-x-2 mb-1">
        <div
          className="w-3 h-3 rounded-full"
          style={{ backgroundColor: config.color }}
        />
        <span className="font-medium text-gray-900">{config.label}</span>
      </div>
      <div className="text-sm text-gray-600">
        <div>
          Count: <span className="font-medium">{data.value}</span>
        </div>
        <div>
          Percentage: <span className="font-medium">{data.percentage}%</span>
        </div>
      </div>
    </div>
  );
};

// Custom legend component
interface CustomLegendProps {
  data: Array<{
    name: keyof typeof STATUS_CONFIG;
    value: number;
    percentage: number;
    fill: string;
  }>;
  total: number;
  className?: string;
}

const CustomLegend = ({ data, total, className }: CustomLegendProps) => {
  return (
    <div className={cn("space-y-3", className)}>
      <div className="text-sm font-medium text-gray-700 mb-3">
        Project Status Distribution
      </div>

      {data.map((entry) => {
        const config = STATUS_CONFIG[entry.name];
        const IconComponent = config.icon;

        return (
          <div
            key={entry.name}
            className="flex items-center justify-between p-2 rounded-lg hover:bg-gray-50 transition-colors duration-200"
          >
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                <div
                  className="w-3 h-3 rounded-full flex-shrink-0"
                  style={{ backgroundColor: entry.fill }}
                />
                <IconComponent
                  size={16}
                  className={cn("flex-shrink-0", config.textColor)}
                />
              </div>

              <div className="flex flex-col">
                <span className="text-sm font-medium text-gray-900">
                  {config.label}
                </span>
                <span className="text-xs text-gray-500">
                  {entry.value} projects
                </span>
              </div>
            </div>

            <Badge
              variant="outline"
              className={cn(
                "text-xs font-medium",
                config.bgColor,
                config.textColor,
                "border-current"
              )}
            >
              {entry.percentage}%
            </Badge>
          </div>
        );
      })}

      {/* Total projects summary */}
      <div className="border-t pt-3 mt-3">
        <div className="flex items-center justify-between text-sm">
          <span className="font-medium text-gray-700 flex items-center space-x-2">
            <Activity size={16} className="text-gray-500" />
            <span>Total Projects</span>
          </span>
          <Badge variant="outline" className="font-bold">
            {total}
          </Badge>
        </div>
      </div>
    </div>
  );
};

// Center label component
interface CenterLabelProps {
  total: number;
  cx?: number;
  cy?: number;
}

const CenterLabel = ({ total, cx = 0, cy = 0 }: CenterLabelProps) => {
  return (
    <g>
      <text
        x={cx}
        y={cy - 8}
        textAnchor="middle"
        dominantBaseline="middle"
        className="fill-gray-900 text-2xl font-bold"
      >
        {total}
      </text>
      <text
        x={cx}
        y={cy + 12}
        textAnchor="middle"
        dominantBaseline="middle"
        className="fill-gray-500 text-sm"
      >
        Total Projects
      </text>
    </g>
  );
};

// Main component
export function ProjectStatusChart({
  data,
  className,
}: ProjectStatusChartProps) {
  // Transform data for recharts
  const chartData = useMemo(() => {
    const total = Object.values(data).reduce((sum, value) => sum + value, 0);

    if (total === 0) {
      return {
        data: [],
        total: 0,
      };
    }

    const transformedData = Object.entries(data)
      .map(([key, value]) => {
        const config = STATUS_CONFIG[key as keyof typeof STATUS_CONFIG];
        return {
          name: key as keyof typeof STATUS_CONFIG,
          value,
          percentage: Math.round((value / total) * 100),
          fill: config.color,
        };
      })
      .filter((item) => item.value > 0); // Only show non-zero values

    return {
      data: transformedData,
      total,
    };
  }, [data]);

  // Empty state
  if (chartData.total === 0) {
    return (
      <Card className={cn("w-full", className)}>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Activity size={20} className="text-gray-600" />
            <span>Project Status Distribution</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center h-64 text-gray-500">
            <div className="text-center">
              <XCircle size={48} className="mx-auto mb-4 text-gray-400" />
              <p className="text-lg font-medium">No projects found</p>
              <p className="text-sm">
                Start adding projects to see the distribution
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={cn("w-full", className)}>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Activity size={20} className="text-gray-600" />
            <span>Project Status Distribution</span>
          </div>
          <Badge variant="outline" className="text-xs">
            Live Data
          </Badge>
        </CardTitle>
      </CardHeader>

      <CardContent>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Chart section */}
          <div className="lg:col-span-2">
            <div className="relative h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={chartData.data}
                    cx="50%"
                    cy="50%"
                    innerRadius={CHART_CONFIG.innerRadius}
                    outerRadius={CHART_CONFIG.outerRadius}
                    paddingAngle={CHART_CONFIG.paddingAngle}
                    dataKey={CHART_CONFIG.dataKey}
                    animationBegin={0}
                    animationDuration={1000}
                  >
                    {chartData.data.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={entry.fill}
                        stroke="#ffffff"
                        strokeWidth={2}
                        className="hover:opacity-80 transition-opacity duration-200"
                      />
                    ))}
                  </Pie>

                  <Tooltip content={<CustomTooltip />} />

                  {/* Center label */}
                  <text
                    x="50%"
                    y="50%"
                    textAnchor="middle"
                    dominantBaseline="middle"
                    className="fill-gray-900 text-2xl font-bold"
                  >
                    {chartData.total}
                  </text>
                  <text
                    x="50%"
                    y="50%"
                    dy={20}
                    textAnchor="middle"
                    dominantBaseline="middle"
                    className="fill-gray-500 text-sm"
                  >
                    Total Projects
                  </text>
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Legend section */}
          <div className="lg:col-span-1">
            <CustomLegend
              data={chartData.data}
              total={chartData.total}
              className="h-full flex flex-col justify-center"
            />
          </div>
        </div>

        {/* Last updated indicator */}
        <div className="mt-4 pt-4 border-t">
          <div className="text-xs text-gray-500 flex items-center justify-between">
            <span>Last updated: {new Date().toLocaleTimeString()}</span>
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span>Live</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default ProjectStatusChart;
