---
description:
globs:
alwaysApply: false
---
# Global Rules for Wellspring Book Production Project

## Core Philosophy
"Agents must cooperate to deliver modular, resilient features. If data access or synchronization is required, defer to the DataLayerAgent (Roo) to define or review data hooks, query keys, and real-time subscriptions."

## Project Overview
The Wellspring Manual is an AI-assisted book production system with two main components:
1. **Em Dash Replacement Tool** - Automated typography correction
2. **Deep Research Agent** - AI-powered research and citation system

Reference configuration: [config.json](mdc:config.json)
Main project structure: [README.md](mdc:README.md)

## Agent Orchestration Rules

### 1. Context Awareness & CONTEXT7 Integration
- Always query CONTEXT7 MCP server for up-to-date docs, schemas, and code examples before generating or modifying code
- If CONTEXT7 returns no match, raise a `missing-context-error` and log the gap
- Sync CONTEXT7 search index after major agent or schema updates

### 2. Agent Orchestration & Delegation
The orchestration agent must:
- Parse the project roadmap and docs to identify deliverables
- Assign tasks to the most appropriate agent (see agent roles below)
- Pass clear, context-rich prompts and input payloads to each agent
- Track progress and update task files after each major step
- Report status and output in structured, machine-readable format (JSON or Markdown tables)

### 3. Data Layer Best Practices
- Define clear, descriptive query keys for data operations
- Use typed hooks with explicit input/output types
- Implement optimistic UI updates for mutations, with rollback on error
- Configure appropriate cache and stale time settings
- Extract database subscriptions into reusable hooks
- Handle loading, error, and empty states in every hook consumer
- Document all hooks with JSDoc and exemplary code snippets
- Keep hooks purely about data; avoid coupling UI logic

### 4. Schema & Contract Enforcement
- All agent I/O must conform to shared contracts
- Validate all schema changes before applying
- Use strict JSON for all agent communication

### 5. Documentation & Workflow
- Update [README.md](mdc:README.md), planning docs, and task files after every major change
- Comment all non-obvious code and explain intent using `# Reason:`
- Keep all files < 500 lines where possible

## File Organization Rules
- Research outputs go in `deep_research_agent/` directory
- Typography corrections use `em_dash_replacement/` directory
- Shared utilities live in `shared_utils/`
- Configuration managed through [config.json](mdc:config.json)
- Virtual environments properly isolated per component

## MCP Tool Integration
Reference MCP configuration: [.cursor/mcp.json](mdc:.cursor/mcp.json)

Available tools:
- **filesystem**: Secure file operations within project directory
- **brave-search**: Web search for research agent
- **firecrawl**: Advanced web scraping for deep research
- **puppeteer**: Browser automation for research tasks
- **sqlite**: Local database for content management
- **notion**: External documentation and collaboration
- **time**: Scheduling and temporal operations
- **sequential-thinking**: Structured problem-solving workflows
