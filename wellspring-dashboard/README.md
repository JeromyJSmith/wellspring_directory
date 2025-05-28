# 🚀 Wellspring Project Ops Command Center

A real-time operations dashboard for behavioral health capital project
directors, owner's reps, and DHCS advisors to monitor 25-100 active
multimillion-dollar behavioral health facility builds.

## 🎯 Project Context

**Name:** Wellspring Project Ops Command Center\
**Audience:** Behavioral health capital project directors, owner's reps, DHCS
advisors\
**Purpose:** Real-time status, risk, and insight tracking across active BHCIP
projects

## 🛠️ Tech Stack

- **Framework:** Next.js 15 App Router
- **Styling:** Tailwind CSS v4
- **Components:** shadcn/ui
- **Icons:** lucide-react
- **Charts:** recharts
- **Database:** Supabase with Realtime
- **Auth:** Supabase UI auth component
- **AI Pipelines:** Otter.ai → Supabase → Dashboard

## 📦 Component Architecture

```
wellspring-dashboard/
├── app/
│   ├── dashboard/
│   │   └── overview/
│   │       └── page.tsx
│   ├── layout.tsx
│   └── globals.css
├── components/
│   ├── kpi/
│   │   └── KpiCard.tsx
│   ├── charts/
│   │   └── ProjectStatusChart.tsx
│   ├── projects/
│   │   ├── ProjectList.tsx
│   │   └── ProjectListItem.tsx
│   ├── insights/
│   │   └── OtterInsightsFeed.tsx
│   └── ui/
├── layouts/
│   └── DashboardLayout.tsx
├── lib/
│   ├── supabase.ts
│   └── utils.ts
└── types/
    └── index.ts
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Setup environment variables:**
   ```bash
   cp .env.example .env.local
   # Add your Supabase keys
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Open dashboard:**
   ```
   http://localhost:3000/dashboard/overview
   ```

## 📊 Dashboard Features

### 1️⃣ KPI Cards Section

- Total Projects, On-Time Completion Rate, Average Bed Count
- Trend indicators with status coloring
- Responsive 3-4 column grid

### 2️⃣ Project Status Donut Chart

- On Track (Green), Minor Delay (Yellow), At Risk (Red), Completed (Blue)
- Interactive tooltips with percentages
- Vertical legend with counts

### 3️⃣ Live Project Risk Table

- Real-time project data with risk indicators
- Sortable columns, hover highlighting
- Live update timestamps

### 4️⃣ Otter.ai Insights Feed

- Real-time meeting insights and action items
- Decision, Risk, and Action categorization
- Filterable by project or insight type

## 🔄 Data Flow

```
Otter.ai Meetings → Supabase DB → Real-time Dashboard → Action Items
```

## 🎨 Design System

- **Colors:** Dark-blue nav, status-based coloring (green/yellow/red)
- **Layout:** Sticky top nav, collapsible sidebar, scrollable main content
- **Components:** shadcn/ui with custom project-specific modifications
- **Responsive:** Mobile-first with desktop optimization

## 📡 Real-time Features

- Live project status updates
- Automatic Otter.ai insight ingestion
- Real-time risk level changes
- Automated alert system for critical milestones

## 🛡️ Security & Compliance

- HIPAA-ready data handling
- Role-based access control
- Government security standards
- Audit logging for all actions

---

**🎯 Ready for V0.dev, Genius.design, or Claude Code deployment**
