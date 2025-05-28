// 🎯 Wellspring Dashboard Type Definitions

export interface Project {
  id: string;
  name: string;
  county: string;
  asamLevels: ASAMLevel[];
  phase: ProjectPhase;
  estimatedCompletion: Date;
  riskLevel: RiskLevel;
  bedCount?: number;
  budget: number;
  actualSpent: number;
  facilityType: FacilityType;
  lastUpdated: Date;
  coordinates?: {
    lat: number;
    lng: number;
  };
}

export interface KPICard {
  id: string;
  title: string;
  value: number | string;
  trend: {
    direction: "up" | "down" | "neutral";
    percentage: number;
  };
  format: "number" | "percentage" | "currency" | "text";
  status: "positive" | "negative" | "neutral";
}

export interface OtterInsight {
  id: string;
  timestamp: Date;
  type: InsightType;
  summary: string;
  projectId?: string;
  projectName?: string;
  priority: "high" | "medium" | "low";
  actionItems?: string[];
  source: "otter_ai" | "manual" | "system";
}

export interface ProjectStatusDistribution {
  onTrack: number;
  minorDelay: number;
  atRisk: number;
  completed: number;
}

// Enums and Constants
export type ProjectPhase =
  | "planning"
  | "design"
  | "permitting"
  | "construction"
  | "licensing"
  | "operational"
  | "completed";

export type RiskLevel = "low" | "medium" | "high" | "critical";

export type FacilityType =
  | "residential"
  | "outpatient"
  | "crisis"
  | "mobile_crisis"
  | "mixed";

export type ASAMLevel =
  | "1.0"
  | "2.1"
  | "2.5"
  | "3.1"
  | "3.3"
  | "3.5"
  | "3.7"
  | "4.0";

export type InsightType =
  | "decision"
  | "risk"
  | "action"
  | "milestone"
  | "budget";

// Dashboard State Management
export interface DashboardState {
  projects: Project[];
  kpis: KPICard[];
  insights: OtterInsight[];
  lastSync: Date;
  isLoading: boolean;
  filters: {
    county?: string;
    phase?: ProjectPhase;
    riskLevel?: RiskLevel;
    facilityType?: FacilityType;
  };
}

// Real-time Event Types
export interface RealtimeEvent {
  type: "project_update" | "new_insight" | "risk_change" | "milestone_reached";
  data: any;
  timestamp: Date;
}

// API Response Types
export interface APIResponse<T> {
  data: T;
  error?: string;
  timestamp: Date;
}

// Chart Data Types
export interface ChartData {
  label: string;
  value: number;
  color: string;
  percentage?: number;
}

// Geographic Data
export interface CountyData {
  name: string;
  code: string;
  projectCount: number;
  riskScore: number;
  bedCapacity: number;
  coordinates: {
    lat: number;
    lng: number;
  };
}

// User and Auth Types
export interface User {
  id: string;
  email: string;
  role: UserRole;
  name: string;
  avatar?: string;
  permissions: Permission[];
}

export type UserRole =
  | "admin"
  | "project_director"
  | "owner_rep"
  | "dhcs_advisor"
  | "viewer";

export type Permission =
  | "view_all_projects"
  | "edit_projects"
  | "manage_users"
  | "view_financial_data"
  | "export_data";

// Supabase Database Types
export interface Database {
  public: {
    Tables: {
      projects: {
        Row: Project;
        Insert: Omit<Project, "id" | "lastUpdated">;
        Update: Partial<Omit<Project, "id">>;
      };
      insights: {
        Row: OtterInsight;
        Insert: Omit<OtterInsight, "id" | "timestamp">;
        Update: Partial<Omit<OtterInsight, "id">>;
      };
      users: {
        Row: User;
        Insert: Omit<User, "id">;
        Update: Partial<Omit<User, "id">>;
      };
    };
  };
}

// Component Props Types
export interface KpiCardProps {
  kpi: KPICard;
  className?: string;
}

export interface ProjectListProps {
  projects: Project[];
  onProjectSelect?: (project: Project) => void;
  className?: string;
}

export interface ProjectStatusChartProps {
  data: ProjectStatusDistribution;
  className?: string;
}

export interface OtterInsightsFeedProps {
  insights: OtterInsight[];
  onInsightClick?: (insight: OtterInsight) => void;
  filters?: {
    type?: InsightType;
    projectId?: string;
  };
  className?: string;
}

// Utility Types
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;
export type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Status Colors and Theme
export const StatusColors = {
  positive: "text-green-600 bg-green-50",
  negative: "text-red-600 bg-red-50",
  neutral: "text-gray-600 bg-gray-50",
  warning: "text-yellow-600 bg-yellow-50",
} as const;

export const RiskColors = {
  low: "text-green-600 bg-green-100",
  medium: "text-yellow-600 bg-yellow-100",
  high: "text-orange-600 bg-orange-100",
  critical: "text-red-600 bg-red-100",
} as const;

export const PhaseColors = {
  planning: "text-blue-600 bg-blue-100",
  design: "text-purple-600 bg-purple-100",
  permitting: "text-yellow-600 bg-yellow-100",
  construction: "text-orange-600 bg-orange-100",
  licensing: "text-indigo-600 bg-indigo-100",
  operational: "text-green-600 bg-green-100",
  completed: "text-gray-600 bg-gray-100",
} as const;
