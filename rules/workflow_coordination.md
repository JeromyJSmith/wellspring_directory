---
description:
globs:
alwaysApply: false
---
# Workflow Coordination for Book Production

## Core Workflow Philosophy
Reference: [global_rules.mdc](mdc:.cursor/rules/global_rules.mdc) and [agent_roles.mdc](mdc:.cursor/rules/agent_roles.mdc)

## Primary Workflows

### 1. Em Dash Replacement Workflow
**Orchestrating Agent**: PlanningArchitect
**Executing Agent**: TypographyAgent
**Supporting Agents**: DataLayerAgent (Roo), RuleKeeper

**Process**:
1. PlanningArchitect receives em dash replacement request
2. TypographyAgent validates input files in `em_dash_replacement/input/`
3. DataLayerAgent (Roo) defines data access patterns for file operations
4. TypographyAgent applies rules from [em_dash_rules.md](mdc:.cursor/rules/em_dash_rules.md)
5. Output processed files to `em_dash_replacement/output/`
6. RuleKeeper validates compliance with [typography_rules.md](mdc:.cursor/rules/typography_rules.md)
7. DocBot updates logs and documentation

**MCP Tools Used**: filesystem, sqlite (for tracking)

### 2. Deep Research Workflow
**Orchestrating Agent**: PlanningArchitect
**Executing Agent**: DeepResearchAgent
**Supporting Agents**: DataLayerAgent (Roo), TaskTracker

**Process**:
1. PlanningArchitect breaks down research requirements
2. DeepResearchAgent follows [research_rules.md](mdc:.cursor/rules/research_rules.md)
3. Execute web research using brave-search and firecrawl MCP tools
4. DataLayerAgent (Roo) manages citation database and extracted statements
5. Store results in `deep_research_agent/` subdirectories:
   - `citations/` - Source citations and references
   - `extracted_statements/` - Key findings and quotes
   - `reports/` - Comprehensive research reports
   - `logs/` - Process documentation
6. TaskTracker updates progress and deliverable status

**MCP Tools Used**: brave-search, firecrawl, puppeteer, sqlite, filesystem

### 3. Integrated Book Production Workflow
**Orchestrating Agent**: PlanningArchitect
**Coordination**: All agents participate

**Process**:
1. **Planning Phase**:
   - PlanningArchitect analyzes requirements from [config.json](mdc:config.json)
   - TaskTracker creates project timeline and milestones
   - DocBot ensures documentation is current

2. **Research Phase**:
   - DeepResearchAgent conducts comprehensive research
   - DataLayerAgent (Roo) structures research data for easy access
   - Results stored according to research workflow above

3. **Content Processing Phase**:
   - TypographyAgent processes text content for typography
   - Apply corrections from em dash replacement workflow
   - RuleKeeper validates all processing steps

4. **Quality Assurance Phase**:
   - RuleKeeper performs comprehensive review
   - DocBot generates final documentation
   - TaskTracker confirms all deliverables completed

## Agent Coordination Patterns

### Sequential Coordination
For tasks requiring step-by-step processing:
```
PlanningArchitect → Agent1 → Agent2 → Agent3 → TaskTracker
```
Used for: Em dash replacement, single-document processing

### Parallel Coordination
For independent tasks that can run simultaneously:
```
PlanningArchitect → [Agent1, Agent2, Agent3] → TaskTracker
```
Used for: Multi-source research, batch processing

### Hub Coordination
For complex tasks requiring central coordination:
```
PlanningArchitect ↔ DataLayerAgent (Roo) ↔ [All Other Agents]
```
Used for: Integrated workflows, data-heavy operations

## Data Flow Management

### File System Organization
- **Input Files**: Stored in appropriate component `input/` directories
- **Working Files**: Processed in component-specific directories
- **Output Files**: Final results in `output/` directories
- **Shared Data**: Centralized in `shared_utils/data/`
- **Configuration**: Managed through [config.json](mdc:config.json)

### Database Operations
**DataLayerAgent (Roo) Responsibilities**:
- Define schema for research citations, typography tracking, workflow status
- Implement query patterns for efficient data access
- Manage SQLite database via MCP sqlite tool
- Coordinate with filesystem MCP tool for file metadata

### Status Tracking
**TaskTracker Responsibilities**:
- Maintain workflow status in structured format
- Generate progress reports for stakeholders
- Coordinate milestone deliveries
- Track agent performance and bottlenecks

## Error Handling Protocols

### Agent Failure Recovery
1. **Detection**: Monitoring agent outputs for error conditions
2. **Escalation**: Failed agent reports to PlanningArchitect
3. **Delegation**: PlanningArchitect reassigns or provides alternative approach
4. **Recovery**: Rollback procedures implemented by DataLayerAgent (Roo)
5. **Documentation**: DocBot records incident and resolution

### Data Consistency
- All file operations go through filesystem MCP tool with proper validation
- Database operations coordinated by DataLayerAgent (Roo)
- Backup and versioning managed in component directories
- Conflict resolution follows agent hierarchy (Roo has final authority on data)

## Communication Standards

### Inter-Agent Messages
```json
{
  "agent_id": "sending_agent",
  "target_agent": "receiving_agent", 
  "task_type": "workflow_step",
  "payload": {
    "input_data": "...",
    "context": "...",
    "requirements": "..."
  },
  "status": "pending|in_progress|completed|failed",
  "timestamp": "ISO_8601_format"
}
```

### Progress Reporting
- **Frequency**: After each major workflow step
- **Format**: Structured JSON or Markdown tables
- **Recipients**: PlanningArchitect, TaskTracker, relevant stakeholders
- **Content**: Status, next steps, blockers, resource requirements

### Quality Gates
Before proceeding to next workflow step:
1. **Output Validation**: RuleKeeper confirms compliance
2. **Data Integrity**: DataLayerAgent (Roo) validates data consistency
3. **Documentation**: DocBot confirms updates are complete
4. **Progress Tracking**: TaskTracker updates milestone status

## MCP Tool Coordination

### Tool Usage Matrix
- **File Operations**: filesystem MCP (all agents)
- **Web Research**: brave-search, firecrawl, puppeteer (DeepResearchAgent)
- **Data Storage**: sqlite MCP (DataLayerAgent, TaskTracker)
- **External Integration**: notion MCP (DocBot, TaskTracker)
- **Complex Reasoning**: sequential-thinking MCP (PlanningArchitect)
- **Time Management**: time MCP (TaskTracker, scheduling)

### Resource Management
- **Concurrent Usage**: Coordinate MCP tool access to prevent conflicts
- **Rate Limiting**: Respect API limits for external services
- **Caching**: Use appropriate caching strategies for web research
- **Environment Variables**: Secure API key management through MCP configuration
