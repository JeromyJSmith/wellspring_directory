# Wellspring Book Project Setup Guide

## 🎯 Project Overview

This repository contains the AI-assisted editing and production system for **The Wellspring Manual** - a comprehensive guide for behavioral health facility development. The project uses specialized AI agents to automate complex editing tasks identified in the manuscript editing meeting.

## 📁 Repository Structure

```
wellspring_directory/
├── .cursor/                    # AI agent configurations
│   ├── rules/                  # Agent behavior rules
│   ├── tasks/                  # Task definitions
│   └── agents/                 # Agent configurations
├── docs/                       # Project documentation and InDesign files
│   ├── .env                    # Environment variables
│   ├── setup.md               # This file
│   ├── The Wellspring.indd    # Main InDesign file (1.4MB)
│   ├── The-Wellspring-Book.indd # Complete book file (104MB)
│   └── Wellspring Manuscript Editing Meeting_otter_ai/
│       ├── Wellspring Manuscript Editing Meeting.mp3
│       └── Wellspring Manuscript Editing Meeting.txt
├── em_dash_replacement/        # Primary editing agent
│   ├── input/                  # Source text for processing
│   ├── output/                 # Processed text
│   ├── scripts/                # Processing scripts
│   ├── logs/                   # Operation logs
│   ├── infographic_placeholders/
│   └── changelog/              # Change tracking
├── deep_research_agent/        # Research and verification agent
│   ├── extracted_statements/   # Fact extraction
│   ├── citations/              # Citation verification
│   ├── visual_opportunities/   # Infographic suggestions
│   ├── scripts/               # Research scripts
│   ├── logs/                  # Operation logs
│   └── reports/               # Research reports
├── shared_utils/              # Common utilities
│   ├── uv_env/                # UV Python environment
│   ├── notebooks/             # Jupyter notebooks
│   └── data/                  # Shared data
├── icons/                     # Brand icons and design elements
├── config.json               # Project configuration
└── README.md                 # Project documentation
```

## 🚀 Setup Instructions

### 1. Environment Setup

The `.env` file is already configured with all necessary API keys:
- **Claude (Anthropic)**: Primary AI model for editing
- **Perplexity**: Research and fact-checking
- **OpenAI**: Backup AI capabilities  
- **Supabase**: Database for project management
- **GitHub**: Version control integration
- **Firecrawl**: Web scraping for research

### 2. Python Environment

Activate the UV environment:
```bash
cd shared_utils/uv_env
source .venv/bin/activate
```

Required packages are already installed:
- pandas, jupyter, rich, openpyxl, numpy, matplotlib

### 3. MCP Server Setup (Optional)

Install Context7 for enhanced AI capabilities:
```bash
npx -y @upstash/context7-mcp
```

### 4. Agent Configuration

Create initial agent rules in `.cursor/rules/`:
- `em_dash_rules.md` - Em dash replacement patterns
- `typography_rules.md` - Typography standards
- `research_rules.md` - Fact-checking protocols

## 📝 Primary Tasks

Based on the editing meeting transcript, the main objectives are:

### 🎯 Priority 1: Em Dash Replacement
- **Location**: `em_dash_replacement/` agent
- **Task**: Replace all em dashes throughout 300+ pages with contextually appropriate punctuation
- **Process**: Analysis → Database → Dry run → Full implementation
- **Output**: Clean manuscript with proper punctuation

### 🎨 Priority 2: Typography & Layout
- Fix title page subtitle
- Reduce table of contents spacing
- Implement blue/gold header color scheme  
- Add architectural corner design elements
- Standardize margins (increase by 3 points)

### 📊 Priority 3: Content Enhancement
- Add infographics for statistical data
- Create visual aids for complex concepts
- Convert sections to actionable checklists
- Verify quote relevance to chapters
- Implement blank page layout system

### 🔍 Priority 4: Research & Verification
- **Location**: `deep_research_agent/` agent
- Verify all quotes for chapter relevance
- Fact-check statistical claims
- Research visual opportunities for data presentation

## 🛠️ Usage

1. **Start with em_dash_replacement**: This is the most critical and frequently mentioned task
2. **Process InDesign files**: Located in `docs/` directory  
3. **Follow editing transcript**: Detailed instructions in `Wellspring Manuscript Editing Meeting.txt`
4. **Track changes**: Use changelog system in each agent directory

## 🎨 Design Standards

- **Color scheme**: Dark royal blue background with gold accents
- **Typography**: Blue/gold headers, consistent spacing
- **Layout**: Blank left pages before sections for artwork
- **Icons**: Chapter badges, UI elements, PDF callouts
- **Style**: Professional manual/textbook format

## 📞 Contact

For questions about project requirements, contact Brian V Jones and team at BHSME (Behavioral Health Subject Matter Experts).

---

*This setup guide reflects the actual working structure of the Wellspring book editing project as of November 2024.*