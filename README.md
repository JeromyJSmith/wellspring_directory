# The Wellspring Manual - AI-Assisted Book Production

**The definitive guide for behavioral health facility development**  
*By Brian V Jones, November 1, 2024*

This repository contains the complete AI-assisted editing and production workflow for **The Wellspring Manual**, a comprehensive 300+ page guide covering best practices for rapid delivery of behavioral health continuum infrastructure.

## 🎯 Project Status

**Current Phase**: Active editing and formatting  
**Primary Tasks**: Em dash replacement, typography standardization, content enhancement  
**InDesign Files**: Ready for processing (104MB complete manuscript)  
**AI Agents**: Configured and operational

## 🤖 AI Agent System

This project uses specialized AI agents to automate complex editorial tasks:

### 📝 Em Dash Replacement Agent
**Priority: HIGH** | **Status: Ready**
- Analyzes 300+ pages for em dash usage patterns
- Creates context-based replacement database
- Implements proper punctuation throughout manuscript
- **Location**: `em_dash_replacement/`

### 🔍 Deep Research Agent  
**Priority: MEDIUM** | **Status: Ready**
- Verifies quote relevance to chapters
- Fact-checks statistical claims and data
- Identifies visual opportunities for infographics
- **Location**: `deep_research_agent/`

### 🛠️ Shared Utilities
- UV Python environment with data science packages
- Jupyter notebooks for analysis
- Common tools and processing scripts
- **Location**: `shared_utils/`

## 📂 Repository Structure

```
wellspring_directory/
├── .cursor/                    # AI agent configurations
├── docs/                       # InDesign files & documentation
│   ├── The-Wellspring-Book.indd  # Main manuscript (104MB)
│   ├── .env                       # API keys & configuration
│   └── Wellspring Manuscript Editing Meeting_otter_ai/
├── em_dash_replacement/        # Primary editing agent
├── deep_research_agent/        # Research & verification
├── shared_utils/              # Common utilities & UV environment
├── icons/                     # Brand assets & design elements
└── config.json              # Project configuration
```

## 🚀 Quick Start

### 1. Environment Setup
The project is pre-configured with all necessary API keys in `docs/.env`:
- **Claude (Anthropic)**: Primary AI editing
- **Perplexity**: Research capabilities  
- **OpenAI**: Backup AI support
- **Supabase**: Project data management

### 2. Activate Python Environment
```bash
cd shared_utils/uv_env
source .venv/bin/activate
```

### 3. Run Primary Editing Task
Start with the most critical task - em dash replacement:
```bash
cd em_dash_replacement/scripts
# Agent scripts will be implemented here
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
