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
│   └── Wellspring Manuscript Editing Meeting_otter_ai/
├── em_dash_replacement/        # Primary editing agent
├── deep_research_agent/        # Research & verification
├── shared_utils/              # Common utilities & UV environment
├── icons/                     # Brand assets & design elements
└── config.json              # Project configuration
```

## 🚀 Quick Start

### 1. Environment Setup
Copy `.env.example` to `.env` and configure with your API keys:
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

### 4. Directory Structure

#### .cursor Directory
- `rules/`: Define logic and constraints for agents
- `tasks/`: Detail workflows and responsibilities
- `agents/`: Host agent personality and behavior configs

#### Icons Directory
- `icons/`: Contains SVG and PNG assets
  - Base style: Dark royal blue background
  - Transformable variants: Gold, dark blue, black
  - Used for chapters, headers, and visual callouts

---

> For any help, reference the documentation or contact the project maintainers
