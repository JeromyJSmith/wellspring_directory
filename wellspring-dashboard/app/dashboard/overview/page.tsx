// 🚀 Wellspring Project Ops Command Center - Main Dashboard Page

"use client";

import React, { useState, useEffect } from "react";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { KpiCardsGrid } from "@/components/kpi/KpiCard";
import { ProjectStatusChart } from "@/components/charts/ProjectStatusChart";
import { ProjectList } from "@/components/projects/ProjectList";
import { InsightsFeed } from "@/components/insights/InsightsFeed";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { cn } from "@/lib/utils";
import {
  projectService,
  insightService,
  kpiService,
  RealtimeManager,
} from "@/lib/supabase";
import type {
  Project,
  KPICard,
  OtterInsight,
  ProjectStatusDistribution,
} from "@/types";
import {
  Activity,
  RefreshCw,
  AlertTriangle,
  TrendingUp,
  Zap,
  Calendar,
  Users,
  Building2,
} from "lucide-react";

// Mock data for development/demo
const MOCK_KPI_DATA: KPICard[] = [
  {
    id: "total-projects",
    title: "Total Active Projects",
    value: 42,
    trend: { direction: "up", percentage: 12 },
    format: "number",
    status: "positive",
  },
  {
    id: "completion-rate",
    title: "On-Time Completion Rate",
    value: 87,
    trend: { direction: "up", percentage: 5 },
    format: "percentage",
    status: "positive",
  },
  {
    id: "average-beds",
    title: "Average Bed Count",
    value: 156,
    trend: { direction: "down", percentage: 3 },
    format: "number",
    status: "neutral",
  },
  {
    id: "budget-variance",
    title: "Budget Variance",
    value: 2.4,
    trend: { direction: "down", percentage: 8 },
    format: "percentage",
    status: "positive",
  },
];

const MOCK_PROJECTS: Project[] = [
  {
    id: "proj-001",
    name: "Riverside Behavioral Health Center",
    county: "Los Angeles",
    asamLevels: ["3.1", "3.5", "3.7"],
    phase: "construction",
    estimatedCompletion: new Date("2025-06-15"),
    riskLevel: "medium",
    bedCount: 120,
    budget: 45000000,
    actualSpent: 32000000,
    facilityType: "residential",
    lastUpdated: new Date(),
    coordinates: { lat: 34.0522, lng: -118.2437 },
  },
  {
    id: "proj-002",
    name: "Valley Crisis Intervention Hub",
    county: "San Bernardino",
    asamLevels: ["2.1", "3.1"],
    phase: "licensing",
    estimatedCompletion: new Date("2025-03-30"),
    riskLevel: "high",
    bedCount: 80,
    budget: 28000000,
    actualSpent: 26500000,
    facilityType: "crisis",
    lastUpdated: new Date(),
    coordinates: { lat: 34.1083, lng: -117.2898 },
  },
  {
    id: "proj-003",
    name: "Coastal Outpatient Services",
    county: "Orange",
    asamLevels: ["1.0", "2.1", "2.5"],
    phase: "operational",
    estimatedCompletion: new Date("2024-12-01"),
    riskLevel: "low",
    bedCount: 0,
    budget: 15000000,
    actualSpent: 14800000,
    facilityType: "outpatient",
    lastUpdated: new Date(),
    coordinates: { lat: 33.7175, lng: -117.8311 },
  },
  {
    id: "proj-004",
    name: "Mountain View Recovery Campus",
    county: "Riverside",
    asamLevels: ["3.3", "3.5", "3.7", "4.0"],
    phase: "permitting",
    estimatedCompletion: new Date("2025-09-20"),
    riskLevel: "critical",
    bedCount: 200,
    budget: 62000000,
    actualSpent: 18000000,
    facilityType: "mixed",
    lastUpdated: new Date(),
    coordinates: { lat: 33.8303, lng: -116.5453 },
  },
];

const MOCK_INSIGHTS: OtterInsight[] = [
  {
    id: "insight-001",
    timestamp: new Date(Date.now() - 30 * 60 * 1000), // 30 minutes ago
    type: "risk",
    summary: "Material delivery delays identified for Riverside project due to supply chain issues",
    projectId: "proj-001",
    projectName: "Riverside Behavioral Health Center",
    priority: "high",
    actionItems: ["Contact alternate suppliers", "Adjust construction timeline"],
    source: "otter_ai",
  },
  {
    id: "insight-002",
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
    type: "decision",
    summary: "Approved design modifications for Valley Crisis Hub accessibility requirements",
    projectId: "proj-002",
    projectName: "Valley Crisis Intervention Hub",
    priority: "medium",
    source: "otter_ai",
  },
  {
    id: "insight-003",
    timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 hours ago
    type: "action",
    summary: "Scheduling final licensing inspection for Coastal Outpatient Services",
    projectId: "proj-003",
    projectName: "Coastal Outpatient Services", 
    priority: "medium",
    actionItems: ["Coordinate with state inspectors", "Prepare compliance documentation"],
    source: "otter_ai",
  },
  {
    id: "insight-004",
    timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000), // 6 hours ago
    type: "milestone",
    summary: "Mountain View project environmental impact assessment completed successfully",
    projectId: "proj-004",
    projectName: "Mountain View Recovery Campus",
    priority: "low",
    source: "system",
  },
];

const MOCK_STATUS_DISTRIBUTION: ProjectStatusDistribution = {
  onTrack: 24,
  minorDelay: 12,
  atRisk: 5,
  completed: 1,
};

export default function DashboardOverviewPage() {
  const [projects, setProjects] = useState<Project[]>(MOCK_PROJECTS);
  const [kpis, setKpis] = useState<KPICard[]>(MOCK_KPI_DATA);
  const [insights, setInsights] = useState<OtterInsight[]>(MOCK_INSIGHTS);
  const [statusDistribution, setStatusDistribution] = useState<ProjectStatusDistribution>(MOCK_STATUS_DISTRIBUTION);
  const [isLoading, setIsLoading] = useState(false);
  const [lastSync, setLastSync] = useState(new Date());
  const [realtimeManager] = useState(() => new RealtimeManager());

  // Mock user data
  const mockUser = {
    name: "Sarah Rodriguez",
    email: "sarah.rodriguez@bhcip.gov",
    avatar: "/api/placeholder/32/32",
    role: "Project Director",
  };

  // Initialize data loading
  useEffect(() => {
    loadDashboardData();

    // Setup real-time subscriptions
    realtimeManager.subscribeToDashboard({
      onProjectUpdate: (project) => {
        setProjects((prev) =>
          prev.map((p) => (p.id === project.id ? project : p))
        );
        setLastSync(new Date());
      },
      onNewInsight: (insight) => {
        setInsights((prev) => [insight, ...prev]);
        setLastSync(new Date());
      },
    });

    return () => {
      realtimeManager.unsubscribeAll();
    };
  }, [realtimeManager]);

  // Load dashboard data
  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      // In production, these would be real Supabase calls
      // const [projectsData, insightsData, kpisData, statusData] = await Promise.all([
      //   projectService.getProjects(),
      //   insightService.getRecentInsights(),
      //   calculateKPIs(),
      //   kpiService.getProjectStatusDistribution(),
      // ]);

      // For now, using mock data
      await new Promise((resolve) => setTimeout(resolve, 1000)); // Simulate loading
      setLastSync(new Date());
    } catch (error) {
      console.error("Error loading dashboard data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle project selection
  const handleProjectSelect = (project: Project) => {
    console.log("Selected project:", project);
    // In real app, this would navigate to project detail page
  };

  // Handle insight click
  const handleInsightClick = (insight: OtterInsight) => {
    console.log("Selected insight:", insight);
    // In real app, this would open insight detail modal
  };

  // Handle navigation
  const handleNavigate = (path: string) => {
    console.log("Navigate to:", path);
    // In real app, this would use Next.js router
  };

  // Manual refresh
  const handleRefresh = () => {
    loadDashboardData();
  };

  return (
    <DashboardLayout
      user={mockUser}
      onNavigate={handleNavigate}
      currentPath="/dashboard/overview"
    >
      <div className="space-y-6">
        {/* Header Section */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Project Operations Dashboard
            </h1>
            <p className="text-gray-600 mt-1">
              Real-time monitoring of {projects.length} active BHCIP projects
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <Badge variant="outline" className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span>Live Data</span>
            </Badge>

            <Button
              onClick={handleRefresh}
              disabled={isLoading}
              variant="outline"
              size="sm"
            >
              <RefreshCw
                size={16}
                className={cn("mr-2", isLoading && "animate-spin")}
              />
              Refresh
            </Button>
          </div>
        </div>

        {/* Status Alert (if any critical issues) */}
        {projects.some((p) => p.riskLevel === "critical") && (
          <Alert className="border-red-200 bg-red-50">
            <AlertTriangle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-800">
              {projects.filter((p) => p.riskLevel === "critical").length} projects require immediate attention.
              <Button variant="link" className="ml-2 p-0 h-auto text-red-700">
                View Details →
              </Button>
            </AlertDescription>
          </Alert>
        )}

        {/* KPI Cards Section */}
        <section>
          <div className="flex items-center space-x-2 mb-4">
            <TrendingUp size={20} className="text-gray-600" />
            <h2 className="text-xl font-semibold text-gray-900">
              Key Performance Indicators
            </h2>
          </div>
          <KpiCardsGrid
            kpis={kpis}
            className="animate-in fade-in-50 duration-700"
          />
        </section>

        {/* Charts and Insights Grid */}
        <section className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* Project Status Chart */}
          <div className="xl:col-span-2">
            <ProjectStatusChart
              data={statusDistribution}
              className="animate-in slide-in-from-left-5 duration-700 delay-150"
            />
          </div>

          {/* Quick Stats Card */}
          <Card className="animate-in slide-in-from-right-5 duration-700 delay-150">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Activity size={18} className="text-gray-600" />
                <span>Quick Stats</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Building2 size={16} className="text-blue-600" />
                    <span className="text-sm text-gray-600">Total Facilities</span>
                  </div>
                  <Badge variant="secondary">42</Badge>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Calendar size={16} className="text-green-600" />
                    <span className="text-sm text-gray-600">Due This Quarter</span>
                  </div>
                  <Badge variant="secondary">8</Badge>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Users size={16} className="text-purple-600" />
                    <span className="text-sm text-gray-600">Team Members</span>
                  </div>
                  <Badge variant="secondary">156</Badge>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Zap size={16} className="text-orange-600" />
                    <span className="text-sm text-gray-600">Active Issues</span>
                  </div>
                  <Badge variant="destructive">7</Badge>
                </div>
              </div>

              <div className="pt-4 border-t">
                <Button size="sm" className="w-full">
                  View Detailed Analytics →
                </Button>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Projects and Insights Grid */}
        <section className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* Project List */}
          <div className="xl:col-span-2">
            <ProjectList
              projects={projects}
              onProjectSelect={handleProjectSelect}
              className="animate-in slide-in-from-left-5 duration-700 delay-300"
            />
          </div>

          {/* Insights Feed */}
          <div className="xl:col-span-1">
            <InsightsFeed
              insights={insights}
              onInsightClick={handleInsightClick}
              onLoadMore={() => console.log("Load more insights")}
              isLoading={isLoading}
              className="animate-in slide-in-from-right-5 duration-700 delay-300 h-[600px]"
            />
          </div>
        </section>

        {/* Footer Status */}
        <div className="pt-6 border-t">
          <div className="text-xs text-gray-500 text-center">
            Dashboard last updated: {lastSync.toLocaleString()} •{" "}
            <span className="text-green-600">All systems operational</span> •{" "}
            Next auto-refresh in 30 seconds
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}