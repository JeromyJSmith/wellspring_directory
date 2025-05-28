// 🏗️ Dashboard Layout Component for Wellspring Dashboard

"use client";

import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { cn } from "@/lib/utils";
import {
  Menu,
  Home,
  BarChart3,
  Building2,
  Calendar,
  Settings,
  Users,
  Bell,
  Search,
  ChevronLeft,
  ChevronRight,
  LogOut,
  User,
  HelpCircle,
  Zap,
  Activity,
  MapPin,
  FileText,
  Mic,
} from "lucide-react";

// Navigation items configuration
const NAVIGATION_ITEMS = [
  {
    id: "overview",
    label: "Overview",
    icon: Home,
    href: "/dashboard/overview",
    description: "Dashboard overview",
  },
  {
    id: "projects",
    label: "Projects",
    icon: Building2,
    href: "/dashboard/projects",
    description: "All projects",
    badge: "42",
  },
  {
    id: "analytics",
    label: "Analytics",
    icon: BarChart3,
    href: "/dashboard/analytics",
    description: "Data insights",
  },
  {
    id: "calendar",
    label: "Calendar",
    icon: Calendar,
    href: "/dashboard/calendar",
    description: "Project timeline",
  },
  {
    id: "insights",
    label: "Insights",
    icon: Mic,
    href: "/dashboard/insights",
    description: "Otter.ai insights",
    badge: "New",
  },
  {
    id: "reports",
    label: "Reports",
    icon: FileText,
    href: "/dashboard/reports",
    description: "Generate reports",
  },
  {
    id: "team",
    label: "Team",
    icon: Users,
    href: "/dashboard/team",
    description: "Team management",
  },
];

// Status indicators for footer
const STATUS_INDICATORS = [
  { label: "Supabase", status: "connected", color: "bg-green-500" },
  { label: "Otter.ai", status: "connected", color: "bg-green-500" },
  { label: "MCP", status: "connected", color: "bg-green-500" },
];

interface DashboardLayoutProps {
  children: React.ReactNode;
  user?: {
    name: string;
    email: string;
    avatar?: string;
    role: string;
  };
  onNavigate?: (path: string) => void;
  currentPath?: string;
}

// Sidebar navigation component
interface SidebarProps {
  isCollapsed: boolean;
  currentPath?: string;
  onNavigate?: (path: string) => void;
  onToggleCollapse?: () => void;
  className?: string;
}

const Sidebar = ({
  isCollapsed,
  currentPath = "/dashboard/overview",
  onNavigate,
  onToggleCollapse,
  className,
}: SidebarProps) => {
  return (
    <div
      className={cn(
        "flex flex-col h-full bg-white border-r border-gray-200 transition-all duration-300",
        isCollapsed ? "w-16" : "w-64",
        className
      )}
    >
      {/* Sidebar header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        {!isCollapsed && (
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <Activity size={16} className="text-white" />
            </div>
            <div>
              <h1 className="font-bold text-gray-900">Wellspring</h1>
              <p className="text-xs text-gray-500">Project Ops</p>
            </div>
          </div>
        )}

        <Button
          variant="ghost"
          size="sm"
          onClick={onToggleCollapse}
          className="h-8 w-8 p-0"
        >
          {isCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </Button>
      </div>

      {/* Navigation items */}
      <nav className="flex-1 p-2 space-y-1 overflow-y-auto">
        {NAVIGATION_ITEMS.map((item) => {
          const IconComponent = item.icon;
          const isActive = currentPath === item.href;

          return (
            <Button
              key={item.id}
              variant={isActive ? "secondary" : "ghost"}
              size="sm"
              onClick={() => onNavigate?.(item.href)}
              className={cn(
                "w-full justify-start transition-all duration-200",
                isCollapsed ? "px-2" : "px-3",
                isActive && "bg-blue-50 text-blue-700 border-blue-200"
              )}
            >
              <IconComponent
                size={16}
                className={cn(
                  "flex-shrink-0",
                  isCollapsed ? "mx-auto" : "mr-3"
                )}
              />

              {!isCollapsed && (
                <div className="flex items-center justify-between w-full">
                  <div className="flex flex-col items-start">
                    <span className="text-sm font-medium">{item.label}</span>
                    <span className="text-xs text-gray-500">
                      {item.description}
                    </span>
                  </div>

                  {item.badge && (
                    <Badge variant="outline" className="text-xs h-5">
                      {item.badge}
                    </Badge>
                  )}
                </div>
              )}
            </Button>
          );
        })}
      </nav>

      {/* Sidebar footer */}
      <div className="p-4 border-t border-gray-200">
        {!isCollapsed && (
          <div className="space-y-2">
            <div className="text-xs text-gray-500 font-medium">
              Data Sources
            </div>
            <div className="grid grid-cols-3 gap-2">
              {STATUS_INDICATORS.map((indicator) => (
                <div
                  key={indicator.label}
                  className="flex items-center space-x-1"
                >
                  <div
                    className={cn("w-2 h-2 rounded-full", indicator.color)}
                  />
                  <span className="text-xs text-gray-600">
                    {indicator.label}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        <Button
          variant="outline"
          size="sm"
          className={cn("w-full mt-3", isCollapsed && "px-2")}
        >
          <Settings
            size={14}
            className={cn(isCollapsed ? "mx-auto" : "mr-2")}
          />
          {!isCollapsed && "Settings"}
        </Button>
      </div>
    </div>
  );
};

// Top navigation component
interface TopNavProps {
  user?: DashboardLayoutProps["user"];
  onMenuClick?: () => void;
  onUserAction?: (action: string) => void;
}

const TopNav = ({ user, onMenuClick, onUserAction }: TopNavProps) => {
  const [notifications] = useState(3); // Mock notification count

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-slate-900 text-white">
      <div className="flex h-16 items-center px-4">
        {/* Mobile menu button */}
        <Button
          variant="ghost"
          size="sm"
          onClick={onMenuClick}
          className="mr-4 md:hidden text-white hover:bg-slate-800"
        >
          <Menu size={16} />
        </Button>

        {/* Logo and title */}
        <div className="flex items-center space-x-3 mr-8">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <Activity size={16} className="text-white" />
          </div>
          <div>
            <h1 className="font-bold text-white">Wellspring Dashboard</h1>
            <p className="text-xs text-slate-300">
              Project Operations Command Center
            </p>
          </div>
        </div>

        {/* Search bar */}
        <div className="flex-1 max-w-md mr-8">
          <div className="relative">
            <Search
              size={16}
              className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400"
            />
            <input
              type="text"
              placeholder="Search projects, insights..."
              className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Right side actions */}
        <div className="flex items-center space-x-4">
          {/* Notifications */}
          <Button
            variant="ghost"
            size="sm"
            className="relative text-white hover:bg-slate-800"
          >
            <Bell size={16} />
            {notifications > 0 && (
              <Badge
                variant="destructive"
                className="absolute -top-1 -right-1 h-5 w-5 p-0 text-xs"
              >
                {notifications}
              </Badge>
            )}
          </Button>

          {/* Live status indicator */}
          <div className="flex items-center space-x-2 px-3 py-1 bg-green-900/30 rounded-full">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
            <span className="text-xs text-green-400 font-medium">Live</span>
          </div>

          {/* User menu */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="sm"
                className="flex items-center space-x-2 text-white hover:bg-slate-800"
              >
                <Avatar className="h-8 w-8">
                  <AvatarImage src={user?.avatar} alt={user?.name} />
                  <AvatarFallback className="bg-blue-600 text-white">
                    {user?.name
                      ?.split(" ")
                      .map((n) => n[0])
                      .join("") || "U"}
                  </AvatarFallback>
                </Avatar>
                <div className="text-left">
                  <div className="text-sm font-medium">
                    {user?.name || "User"}
                  </div>
                  <div className="text-xs text-slate-300">
                    {user?.role || "Admin"}
                  </div>
                </div>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuItem onClick={() => onUserAction?.("profile")}>
                <User size={14} className="mr-2" />
                Profile
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onUserAction?.("settings")}>
                <Settings size={14} className="mr-2" />
                Settings
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onUserAction?.("help")}>
                <HelpCircle size={14} className="mr-2" />
                Help & Support
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => onUserAction?.("logout")}>
                <LogOut size={14} className="mr-2" />
                Sign Out
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
};

// Main layout component
export function DashboardLayout({
  children,
  user,
  onNavigate,
  currentPath,
}: DashboardLayoutProps) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Handle responsive behavior
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 1024) {
        setSidebarCollapsed(true);
      }
    };

    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const handleUserAction = (action: string) => {
    switch (action) {
      case "logout":
        // Handle logout
        console.log("Logging out...");
        break;
      case "profile":
        onNavigate?.("/dashboard/profile");
        break;
      case "settings":
        onNavigate?.("/dashboard/settings");
        break;
      default:
        console.log(`User action: ${action}`);
    }
  };

  return (
    <div className="h-screen flex flex-col overflow-hidden bg-gray-50">
      {/* Top Navigation */}
      <TopNav
        user={user}
        onMenuClick={() => setMobileMenuOpen(true)}
        onUserAction={handleUserAction}
      />

      <div className="flex flex-1 overflow-hidden">
        {/* Desktop Sidebar */}
        <aside className="hidden md:flex flex-shrink-0">
          <Sidebar
            isCollapsed={sidebarCollapsed}
            currentPath={currentPath}
            onNavigate={onNavigate}
            onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
          />
        </aside>

        {/* Mobile Sidebar */}
        <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
          <SheetContent side="left" className="w-64 p-0">
            <Sidebar
              isCollapsed={false}
              currentPath={currentPath}
              onNavigate={(path) => {
                onNavigate?.(path);
                setMobileMenuOpen(false);
              }}
            />
          </SheetContent>
        </Sheet>

        {/* Main Content Area */}
        <main className="flex-1 overflow-auto">
          <div className="h-full p-6">{children}</div>
        </main>
      </div>

      {/* Footer Status Bar */}
      <footer className="border-t bg-white px-6 py-2">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <div className="flex items-center space-x-4">
            <span>Last sync: {new Date().toLocaleTimeString()}</span>
            <div className="flex items-center space-x-2">
              <Zap size={12} className="text-blue-500" />
              <span>Claude Code Status: Connected</span>
            </div>
          </div>

          <div className="flex items-center space-x-6">
            {STATUS_INDICATORS.map((indicator) => (
              <div
                key={indicator.label}
                className="flex items-center space-x-1"
              >
                <div className={cn("w-2 h-2 rounded-full", indicator.color)} />
                <span>{indicator.label}</span>
              </div>
            ))}
          </div>
        </div>
      </footer>
    </div>
  );
}

export default DashboardLayout;
