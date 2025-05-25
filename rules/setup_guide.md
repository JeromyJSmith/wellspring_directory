---
description:
globs:
alwaysApply: false
---
# Wellspring Setup & Initialization Guide

## Quick Start Overview
This guide helps you initialize the Wellspring book production system with all MCP tools and agents properly configured.

Reference files:
- Main configuration: [config.json](mdc:config.json)
- MCP tools: [.cursor/mcp.json](mdc:.cursor/mcp.json)
- Project overview: [README.md](mdc:README.md)

## Prerequisites

### System Requirements
- **Operating System**: macOS (darwin 24.5.0 detected)
- **Shell**: /bin/zsh (detected)
- **Node.js**: Latest LTS version for MCP server management
- **Python**: 3.13+ (virtual environments already configured)

### Environment Setup
1. **Workspace Location**: `/Users/ojeromyo/Desktop/wellspring_directory`
2. **Virtual Environments**:
   - Main project: `.venv/` (Python 3.13)
   - Shared utilities: `shared_utils/uv_env/.venv/` (Python 3.13)

## MCP Server Configuration

### Step 1: API Key Setup
Required API keys for MCP tools in [.cursor/mcp.json](mdc:.cursor/mcp.json):

```bash
# Create .env file in project root
cat > .env << 'EOF'
# Web Search & Research Tools
BRAVE_API_KEY=your_brave_search_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
EXA_API_KEY=your_exa_search_api_key

# External Integration
NOTION_TOKEN=your_notion_integration_token

# Optional: Add other service keys as needed
EOF
```

### Step 2: Install MCP Dependencies
```bash
# Ensure npm is available for MCP server management
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-brave-search
npm install -g @modelcontextprotocol/server-fetch
npm install -g @modelcontextprotocol/server-puppeteer
npm install -g @modelcontextprotocol/server-time
npm install -g @modelcontextprotocol/server-sequential-thinking
npm install -g @modelcontextprotocol/server-sqlite
npm install -g mcp-server-firecrawl
npm install -g mcp-notion
npm install -g mcp-browser-tools
npm install -g mcp-wcgw
npm install -g mcp-21st-devmagic
npm install -g mcp-exa
```

### Step 3: Database Initialization
```bash
# Create SQLite database for project data
mkdir -p shared_utils/data
sqlite3 shared_utils/data/wellspring.db "
CREATE TABLE IF NOT EXISTS research_citations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_url TEXT,
    title TEXT,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS typography_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_file TEXT,
    output_file TEXT,
    changes_made INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflow_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_type TEXT,
    status TEXT,
    agent TEXT,
    details TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
"
```

## Agent System Initialization

### Step 4: Verify Agent Rules
Ensure all agent rules are properly configured:
- [global_rules.mdc](mdc:.cursor/rules/global_rules.mdc) - Core system rules
- [agent_roles.mdc](mdc:.cursor/rules/agent_roles.mdc) - Agent definitions
- [workflow_coordination.mdc](mdc:.cursor/rules/workflow_coordination.mdc) - Coordination patterns
- [research_rules.md](mdc:.cursor/rules/research_rules.md) - Research guidelines
- [typography_rules.md](mdc:.cursor/rules/typography_rules.md) - Typography standards
- [em_dash_rules.md](mdc:.cursor/rules/em_dash_rules.md) - Em dash processing

### Step 5: Directory Structure Validation
Ensure all required directories exist:
```bash
# Verify directory structure
mkdir -p em_dash_replacement/{input,output,logs,scripts,changelog,infographic_placeholders}
mkdir -p deep_research_agent/{citations,extracted_statements,reports,logs,scripts,visual_opportunities}
mkdir -p shared_utils/{data,notebooks}
mkdir -p docs
mkdir -p icons
```

## Configuration Management

### Step 6: Update config.json
Verify [config.json](mdc:config.json) contains proper settings:
```json
{
  "project_name": "Wellspring Manual",
  "version": "1.0.0",
  "components": {
    "em_dash_replacement": {
      "enabled": true,
      "input_dir": "em_dash_replacement/input",
      "output_dir": "em_dash_replacement/output"
    },
    "deep_research_agent": {
      "enabled": true,
      "research_dir": "deep_research_agent",
      "max_sources": 50
    }
  },
  "mcp_servers": {
    "filesystem": {"enabled": true},
    "research_tools": {"enabled": true},
    "database": {"enabled": true}
  }
}
```

## Testing & Validation

### Step 7: MCP Server Testing
Test each MCP server connection:
```bash
# Test filesystem access
echo "Testing filesystem MCP server..."

# Test search capabilities
echo "Testing search MCP servers..."

# Test database connectivity
echo "Testing SQLite MCP server..."
sqlite3 shared_utils/data/wellspring.db "SELECT 'Database OK' as status;"
```

### Step 8: Agent Workflow Testing
Validate agent coordination:
1. **PlanningArchitect**: Test task breakdown and delegation
2. **DataLayerAgent (Roo)**: Test data access pattern definition
3. **DeepResearchAgent**: Test web research workflow
4. **TypographyAgent**: Test em dash replacement workflow
5. **TaskTracker**: Test progress monitoring

## Daily Workflow Initialization

### Step 9: Session Startup Checklist
Before starting work:
- [ ] Activate appropriate Python virtual environment
- [ ] Verify MCP servers are responsive
- [ ] Check database connectivity
- [ ] Confirm agent rules are loaded
- [ ] Validate file system permissions

### Step 10: Agent Handoff Protocol
When starting a new task:
1. **PlanningArchitect** receives initial requirements
2. **TaskTracker** logs new workflow session
3. **DataLayerAgent (Roo)** validates data access needs
4. Appropriate specialized agents are activated
5. Progress monitored through structured reporting

## Troubleshooting

### Common Issues
1. **MCP Server Connection Failures**:
   - Check API keys in .env file
   - Verify npm package installations
   - Test network connectivity

2. **Agent Coordination Errors**:
   - Validate agent rule files are properly formatted
   - Check file system permissions
   - Verify database schema is correct

3. **File System Access Issues**:
   - Confirm FILESYSTEM_ALLOWED_PATHS in MCP config
   - Verify directory permissions
   - Check virtual environment activation

### Support Resources
- Agent roles reference: [agent_roles.mdc](mdc:.cursor/rules/agent_roles.mdc)
- Workflow patterns: [workflow_coordination.mdc](mdc:.cursor/rules/workflow_coordination.mdc)
- Project documentation: [README.md](mdc:README.md)

## Next Steps
After successful setup:
1. Test em dash replacement workflow with sample content
2. Execute deep research workflow on a test topic
3. Validate integrated book production pipeline
4. Document any custom configurations or adjustments needed

## Maintenance
- Regularly update MCP server packages
- Monitor agent performance and adjust coordination patterns
- Keep documentation synchronized with system changes
- Backup database and critical configuration files
