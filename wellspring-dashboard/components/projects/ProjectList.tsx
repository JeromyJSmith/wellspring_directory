// 📋 Project List Component for Wellspring Dashboard

"use client";

import React, { useState, useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  cn,
  dateUtils,
  statusUtils,
  projectUtils,
  filterUtils,
} from "@/lib/utils";
import type {
  ProjectListProps,
  Project,
  ProjectPhase,
  RiskLevel,
} from "@/types";
import {
  ChevronUp,
  ChevronDown,
  Search,
  Filter,
  Calendar,
  MapPin,
  Building2,
  AlertCircle,
  Clock,
  CheckCircle2,
  TrendingUp,
  ExternalLink,
  Refresh,
} from "lucide-react";

// Sorting configuration
type SortField =
  | "name"
  | "county"
  | "phase"
  | "estimatedCompletion"
  | "riskLevel"
  | "budget";
type SortDirection = "asc" | "desc";

interface SortConfig {
  field: SortField;
  direction: SortDirection;
}

// Risk indicator component
const RiskIndicator = ({ level }: { level: RiskLevel }) => {
  const config = {
    low: {
      color: "text-green-600 bg-green-100 border-green-200",
      icon: CheckCircle2,
      pulse: false,
    },
    medium: {
      color: "text-yellow-600 bg-yellow-100 border-yellow-200",
      icon: Clock,
      pulse: false,
    },
    high: {
      color: "text-orange-600 bg-orange-100 border-orange-200",
      icon: AlertCircle,
      pulse: true,
    },
    critical: {
      color: "text-red-600 bg-red-100 border-red-200",
      icon: AlertCircle,
      pulse: true,
    },
  };

  const { color, icon: Icon, pulse } = config[level];

  return (
    <Badge
      variant="outline"
      className={cn(
        "text-xs font-medium border",
        color,
        pulse && "animate-pulse"
      )}
    >
      <Icon size={12} className="mr-1" />
      {level.charAt(0).toUpperCase() + level.slice(1)}
    </Badge>
  );
};

// Phase indicator component
const PhaseIndicator = ({ phase }: { phase: ProjectPhase }) => {
  const config = {
    planning: { icon: TrendingUp, label: "Planning" },
    design: { icon: Building2, label: "Design" },
    permitting: { icon: Calendar, label: "Permitting" },
    construction: { icon: Building2, label: "Construction" },
    licensing: { icon: CheckCircle2, label: "Licensing" },
    operational: { icon: CheckCircle2, label: "Operational" },
    completed: { icon: CheckCircle2, label: "Completed" },
  };

  const { icon: Icon, label } = config[phase];

  return (
    <Badge
      variant="outline"
      className={cn("text-xs font-medium", statusUtils.getPhaseColor(phase))}
    >
      <Icon size={12} className="mr-1" />
      {label}
    </Badge>
  );
};

// Table header with sorting
interface SortableHeaderProps {
  children: React.ReactNode;
  field: SortField;
  sortConfig: SortConfig | null;
  onSort: (field: SortField) => void;
  className?: string;
}

const SortableHeader = ({
  children,
  field,
  sortConfig,
  onSort,
  className,
}: SortableHeaderProps) => {
  const isActive = sortConfig?.field === field;
  const direction = isActive ? sortConfig.direction : null;

  return (
    <TableHead
      className={cn(
        "cursor-pointer hover:bg-gray-50 transition-colors",
        className
      )}
    >
      <Button
        variant="ghost"
        size="sm"
        className="h-auto p-0 font-medium text-left justify-start w-full"
        onClick={() => onSort(field)}
      >
        <span>{children}</span>
        <div className="ml-2 flex flex-col">
          <ChevronUp
            size={12}
            className={cn(
              "transition-colors",
              isActive && direction === "asc"
                ? "text-blue-600"
                : "text-gray-400"
            )}
          />
          <ChevronDown
            size={12}
            className={cn(
              "transition-colors -mt-1",
              isActive && direction === "desc"
                ? "text-blue-600"
                : "text-gray-400"
            )}
          />
        </div>
      </Button>
    </TableHead>
  );
};

// Main component
export function ProjectList({
  projects,
  onProjectSelect,
  className,
}: ProjectListProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState<SortConfig | null>(null);
  const [lastUpdated, setLastUpdated] = useState(new Date());

  // Sorting function
  const handleSort = (field: SortField) => {
    setSortConfig((current) => {
      if (current?.field === field) {
        return {
          field,
          direction: current.direction === "asc" ? "desc" : "asc",
        };
      }
      return { field, direction: "asc" };
    });
  };

  // Filter and sort projects
  const processedProjects = useMemo(() => {
    let filtered = filterUtils.searchProjects(projects, searchTerm);

    if (sortConfig) {
      filtered.sort((a, b) => {
        const { field, direction } = sortConfig;
        let aValue: any = a[field];
        let bValue: any = b[field];

        // Handle different field types
        if (field === "estimatedCompletion") {
          aValue = new Date(aValue).getTime();
          bValue = new Date(bValue).getTime();
        } else if (field === "riskLevel") {
          const riskOrder = { low: 1, medium: 2, high: 3, critical: 4 };
          aValue = riskOrder[aValue as RiskLevel];
          bValue = riskOrder[bValue as RiskLevel];
        } else if (field === "phase") {
          const phaseOrder = {
            planning: 1,
            design: 2,
            permitting: 3,
            construction: 4,
            licensing: 5,
            operational: 6,
            completed: 7,
          };
          aValue = phaseOrder[aValue as ProjectPhase];
          bValue = phaseOrder[bValue as ProjectPhase];
        } else if (typeof aValue === "string") {
          aValue = aValue.toLowerCase();
          bValue = bValue.toLowerCase();
        }

        if (aValue < bValue) return direction === "asc" ? -1 : 1;
        if (aValue > bValue) return direction === "asc" ? 1 : -1;
        return 0;
      });
    }

    return filtered;
  }, [projects, searchTerm, sortConfig]);

  // Refresh data
  const handleRefresh = () => {
    setLastUpdated(new Date());
    // In real app, this would trigger data refetch
  };

  return (
    <Card className={cn("w-full", className)}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <Building2 size={20} className="text-gray-600" />
            <span>Live Project Risk Table</span>
          </CardTitle>

          <div className="flex items-center space-x-2">
            <Badge variant="outline" className="text-xs">
              {processedProjects.length} Projects
            </Badge>
            <Button
              variant="outline"
              size="sm"
              onClick={handleRefresh}
              className="text-xs"
            >
              <Refresh size={14} className="mr-1" />
              Refresh
            </Button>
          </div>
        </div>

        {/* Search and filters */}
        <div className="flex items-center space-x-4 mt-4">
          <div className="relative flex-1 max-w-md">
            <Search
              size={16}
              className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
            />
            <Input
              placeholder="Search projects..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>

          <Button variant="outline" size="sm">
            <Filter size={14} className="mr-2" />
            Filters
          </Button>
        </div>
      </CardHeader>

      <CardContent>
        <div className="rounded-lg border overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow className="bg-gray-50/50">
                <SortableHeader
                  field="name"
                  sortConfig={sortConfig}
                  onSort={handleSort}
                  className="w-[200px]"
                >
                  Project Name
                </SortableHeader>

                <SortableHeader
                  field="county"
                  sortConfig={sortConfig}
                  onSort={handleSort}
                  className="w-[120px]"
                >
                  County
                </SortableHeader>

                <TableHead className="w-[140px]">ASAM Level(s)</TableHead>

                <SortableHeader
                  field="phase"
                  sortConfig={sortConfig}
                  onSort={handleSort}
                  className="w-[140px]"
                >
                  Phase
                </SortableHeader>

                <SortableHeader
                  field="estimatedCompletion"
                  sortConfig={sortConfig}
                  onSort={handleSort}
                  className="w-[140px]"
                >
                  Est. Completion
                </SortableHeader>

                <SortableHeader
                  field="riskLevel"
                  sortConfig={sortConfig}
                  onSort={handleSort}
                  className="w-[120px]"
                >
                  Risk Level
                </SortableHeader>

                <TableHead className="w-[80px]">Actions</TableHead>
              </TableRow>
            </TableHeader>

            <TableBody>
              {processedProjects.map((project) => {
                const needsAttention = projectUtils.needsAttention(project);
                const isOverdue = dateUtils.isOverdue(
                  project.estimatedCompletion
                );
                const daysUntil = dateUtils.getDaysUntil(
                  project.estimatedCompletion
                );

                return (
                  <TableRow
                    key={project.id}
                    className={cn(
                      "cursor-pointer transition-all duration-200",
                      "hover:bg-gray-50 hover:shadow-sm",
                      needsAttention && "bg-yellow-50/30 hover:bg-yellow-50/50",
                      isOverdue && "bg-red-50/30 hover:bg-red-50/50"
                    )}
                    onClick={() => onProjectSelect?.(project)}
                  >
                    <TableCell className="font-medium">
                      <div className="flex items-center space-x-2">
                        <span className="truncate">{project.name}</span>
                        {needsAttention && (
                          <AlertCircle
                            size={14}
                            className="text-orange-500 flex-shrink-0"
                          />
                        )}
                      </div>
                    </TableCell>

                    <TableCell>
                      <div className="flex items-center space-x-1">
                        <MapPin size={12} className="text-gray-400" />
                        <span className="text-sm">{project.county}</span>
                      </div>
                    </TableCell>

                    <TableCell>
                      <div className="text-sm text-gray-600">
                        {projectUtils.formatASAMLevels(project.asamLevels)}
                      </div>
                    </TableCell>

                    <TableCell>
                      <PhaseIndicator phase={project.phase} />
                    </TableCell>

                    <TableCell>
                      <div className="space-y-1">
                        <div className="text-sm font-medium">
                          {dateUtils.formatDate(project.estimatedCompletion)}
                        </div>
                        <div
                          className={cn(
                            "text-xs",
                            isOverdue
                              ? "text-red-600"
                              : daysUntil <= 30
                              ? "text-orange-600"
                              : "text-gray-500"
                          )}
                        >
                          {isOverdue ? "Overdue" : `${daysUntil} days`}
                        </div>
                      </div>
                    </TableCell>

                    <TableCell>
                      <RiskIndicator level={project.riskLevel} />
                    </TableCell>

                    <TableCell>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="h-8 w-8 p-0"
                        onClick={(e) => {
                          e.stopPropagation();
                          onProjectSelect?.(project);
                        }}
                      >
                        <ExternalLink size={14} />
                      </Button>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>

          {/* Empty state */}
          {processedProjects.length === 0 && (
            <div className="flex items-center justify-center py-12 text-gray-500">
              <div className="text-center">
                <Building2 size={48} className="mx-auto mb-4 text-gray-400" />
                <p className="text-lg font-medium">No projects found</p>
                <p className="text-sm">
                  {searchTerm
                    ? "Try adjusting your search terms"
                    : "Start adding projects to see them here"}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Footer with live update indicator */}
        <div className="mt-4 pt-4 border-t">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <div className="flex items-center space-x-4">
              <span>
                Showing {processedProjects.length} of {projects.length} projects
              </span>
              {searchTerm && <span>Filtered by: "{searchTerm}"</span>}
            </div>

            <div className="flex items-center space-x-2">
              <span>
                Last updated: {dateUtils.getRelativeTime(lastUpdated)}
              </span>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                <span>Live</span>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default ProjectList;
