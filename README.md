# README.md

# Wellspring Project Repository

Welcome to the Wellspring Project! This repository is the central hub for all
code, documentation, and automation scripts related to our dual-platform
initiative: the Wellspring Educational Platform and the Real Estate Project
Management Tool. At the heart of this project lies the Wellspring Manual, a
definitive source of truth for all instructional, procedural, and visual
standards.

## Project Overview

The Wellspring Project is composed of three primary components:

1. **Wellspring Manual**
   - A formatted print and layout project that serves as the source of truth for
     branding, typography, layout standards, and instructional content.
2. **Educational Platform**
   - A subscription-based online portal offering structured courses, community
     engagement, and expert advisory for behavioral health facility developers.
3. **Project Management Tool**
   - A cloud-based toolset that integrates FreshBooks, Google Workspace, and AI
     agent workflows to manage compliance, scheduling, billing, and document
     tracking for client projects.

## Repository Structure

```
.wellspring_repository/
├── .cursor/
│   ├── rules/
│   ├── tasks/
│   └── agents/
├── docs/
│   ├── .env
│   └── setup.md
├── icons/
├── config.json
└── README.md
```

## Setup Instructions

### Step 1: Initialize MCP Servers

- **Context7** : Install and activate using:

```bash
npx -y @upstash/context7-mcp
```

Then add** **`'use context7'` in relevant scripts.

- **gitmcp** : Transform your GitHub repo by prepending its URL with:

```text
https://gitmcp.io/your-username/your-repo
```

### Step 2: Update** **`config.json`

```json
{
    "mcpServers": {
        "context7": {
            "activation": "use context7"
        },
        "gitmcp": {
            "url": "https://gitmcp.io/your-username/your-repo"
        }
    }
}
```

### Step 3: Create** **`.cursor` Directory Structure

- `rules/`: Define logic and constraints for agents.
- `tasks/`: Detail workflows and responsibilities.
- `agents/`: Host agent personality and behavior configs.

### Step 4: Establish Icon Style Directory

- `icons/`: Contains SVG and PNG assets.
  - Base style: Dark royal blue background.
  - Transformable variants: Gold, dark blue, black.
  - Used for chapters, headers, and visual callouts.

### Step 5: Add** **`.env` to** **`docs/`

- This stores environment secrets (e.g., Supabase keys, Notion tokens).
- Required for syncing content with Supabase and Notion.

---

# setup.md

## Wellspring Setup Guide

This file provides a step-by-step technical onboarding for contributors, AI
agents, and automation tools.

### 🔧 System Initialization

1. **Run Context7 Installer** :

```bash
npx -y @upstash/context7-mcp
```

1. **Activate MCP Server** :

- Add** **`use context7` to any script intended to interact with Codex or
  agents.

1. **Set up GitMCP** :

- Format GitHub URL:** **`https://gitmcp.io/your-username/your-repo`
- Use this format in all AI tool configuration references.

### 🗂️ Folder Setup

```bash
mkdir -p .cursor/rules .cursor/tasks .cursor/agents
mkdir -p docs icons
```

### 🧠 Populate** **`config.json`

Ensure Codex/agents access MCP servers:

```json
{
    "mcpServers": {
        "context7": { "activation": "use context7" },
        "gitmcp": { "url": "https://gitmcp.io/your-username/your-repo" }
    }
}
```

### 🎨 Icon Directory Guidelines

- **Location** :** **`/icons`
- **Primary Style** : Dark royal blue background
- **Variants** : Export styles in gold, dark blue, or black
- **Tools** : OpenAI’s DALL-E, Google image tooling APIs
- **Purpose** : Chapter badges, UI buttons, PDF callouts

### 🔐** **`.env` Secrets (Located in** **`docs/`)

```env
SUPABASE_URL=https://xyz.supabase.co
SUPABASE_KEY=public-anon-key
NOTION_API_KEY=secret_notion_key
```

### ✅ Final Checklist

- [ ] `README.md` finalized
- [ ] `.cursor/` folders in place
- [ ] `config.json` contains MCP definitions
- [ ] `.env` present in** **`docs/`
- [ ] Icons follow the style guide
- [ ] Project successfully tested and verified

> For any help, reference** **`README.md`, or ask your agent 🧠

---

This dual-document structure ensures both human and AI collaborators are aligned
with the Wellspring project's objectives, file structure, automation protocols,
and visual identity.
