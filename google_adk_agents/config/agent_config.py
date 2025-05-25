#!/usr/bin/env python3
"""
Google ADK Agent Configuration for Wellspring Em Dash Framework
Defines agent configurations, model settings, and tool registrations.
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class AgentConfig:
    """Configuration for a Google ADK agent."""
    name: str
    model: str
    description: str
    instructions: str
    tools: List[str]
    output_key: str
    base_agent: Optional[str] = None
    temperature: float = 0.3
    max_tokens: int = 4096
    timeout: int = 300
    retry_count: int = 3

@dataclass
class RunnerConfig:
    """Configuration for Google ADK runner."""
    app_name: str
    session_service_type: str = "InMemorySessionService"
    session_persistence: bool = True
    session_timeout: int = 3600
    max_concurrent_sessions: int = 10

class WellspringADKConfig:
    """Main configuration class for Wellspring Google ADK agents."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.db_path = self.project_root / "shared_utils" / "data" / "wellspring.db"
        self.workspace_path = self.project_root
        
        # Google AI configuration
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        # Model configurations
        self.default_model = "gemini-2.5-flash-preview-05-20"
        self.alternative_model = "gemini-1.5-pro"
        
        # Agent configurations
        self.agent_configs = self._initialize_agent_configs()
        self.runner_configs = self._initialize_runner_configs()
    
    def _initialize_agent_configs(self) -> Dict[str, AgentConfig]:
        """Initialize all agent configurations."""
        return {
            "em_dash_analyzer": AgentConfig(
                name="em_dash_analyzer",
                model=self.default_model,
                description="Specialized agent for analyzing em dash usage patterns in text",
                instructions="""You are the Em Dash Analysis Agent for the Wellspring Book Production system.
                
Your primary responsibilities:
1. Analyze text files to identify all em dash (—) occurrences
2. Determine appropriate replacement punctuation based on context
3. Assign confidence scores to replacement suggestions
4. Generate comprehensive analysis reports
5. Store analysis results in the database

Use the available tools to:
- analyze_em_dash_patterns: Scan text for em dash patterns
- suggest_replacements: Provide contextual replacement suggestions
- calculate_confidence: Determine confidence scores for replacements
- generate_analysis_report: Create detailed analysis summaries
- save_to_database: Store results in the Wellspring database

Always provide detailed reasoning for your suggestions and maintain high accuracy standards.""",
                tools=[
                    "analyze_em_dash_patterns",
                    "suggest_replacements", 
                    "calculate_confidence",
                    "generate_analysis_report",
                    "save_to_database"
                ],
                output_key="em_dash_analysis",
                temperature=0.2,  # Lower temperature for more consistent analysis
                max_tokens=2048
            ),
            
            "em_dash_processor": AgentConfig(
                name="em_dash_processor",
                model=self.default_model,
                description="Specialized agent for applying em dash replacements in text",
                instructions="""You are the Em Dash Processing Agent for the Wellspring Book Production system.

Your primary responsibilities:
1. Apply em dash replacements based on analysis results
2. Perform dry-run processing for validation
3. Execute actual replacements with backup creation
4. Monitor processing quality and statistics
5. Handle error cases and manual review items

Use the available tools to:
- load_replacement_rules: Get approved replacement patterns from database
- perform_dry_run: Preview changes before applying
- apply_replacements: Execute actual text replacements
- create_backup: Safely backup original files
- validate_results: Check processing quality
- log_session: Record processing statistics

Always prioritize data safety and create backups before making changes.""",
                tools=[
                    "load_replacement_rules",
                    "perform_dry_run",
                    "apply_replacements",
                    "create_backup",
                    "validate_results",
                    "log_session"
                ],
                output_key="em_dash_processing",
                temperature=0.1,  # Very low temperature for precise processing
                max_tokens=2048
            ),
            
            "em_dash_coordinator": AgentConfig(
                name="em_dash_coordinator",
                model=self.default_model,
                description="Orchestrates the complete em dash replacement workflow",
                instructions="""You are the Em Dash Workflow Coordinator for the Wellspring Book Production system.

Your primary responsibilities:
1. Orchestrate the complete em dash replacement workflow
2. Coordinate between analyzer and processor agents
3. Manage workflow state and progress tracking
4. Handle quality gates and approval processes
5. Generate comprehensive workflow reports

Use the available tools to:
- create_workflow: Initialize new em dash workflows
- coordinate_agents: Manage inter-agent communication
- track_progress: Monitor workflow execution status
- validate_quality_gates: Ensure quality standards are met
- generate_workflow_report: Create comprehensive reports
- manage_approvals: Handle manual review and approval processes

Always ensure high-quality outcomes and maintain clear audit trails.""",
                tools=[
                    "create_workflow",
                    "coordinate_agents",
                    "track_progress",
                    "validate_quality_gates",
                    "generate_workflow_report",
                    "manage_approvals"
                ],
                output_key="workflow_coordination",
                temperature=0.3,
                max_tokens=3072
            )
        }
    
    def _initialize_runner_configs(self) -> Dict[str, RunnerConfig]:
        """Initialize runner configurations for each agent."""
        return {
            "em_dash_analyzer": RunnerConfig(
                app_name="wellspring_em_dash_analyzer",
                session_service_type="DatabaseSessionService",
                session_persistence=True,
                session_timeout=1800,  # 30 minutes
                max_concurrent_sessions=5
            ),
            
            "em_dash_processor": RunnerConfig(
                app_name="wellspring_em_dash_processor", 
                session_service_type="DatabaseSessionService",
                session_persistence=True,
                session_timeout=3600,  # 1 hour
                max_concurrent_sessions=3
            ),
            
            "em_dash_coordinator": RunnerConfig(
                app_name="wellspring_em_dash_coordinator",
                session_service_type="DatabaseSessionService", 
                session_persistence=True,
                session_timeout=7200,  # 2 hours
                max_concurrent_sessions=2
            )
        }
    
    def get_agent_config(self, agent_name: str) -> AgentConfig:
        """Get configuration for a specific agent."""
        if agent_name not in self.agent_configs:
            raise ValueError(f"Unknown agent: {agent_name}")
        return self.agent_configs[agent_name]
    
    def get_runner_config(self, agent_name: str) -> RunnerConfig:
        """Get runner configuration for a specific agent."""
        if agent_name not in self.runner_configs:
            raise ValueError(f"Unknown agent: {agent_name}")
        return self.runner_configs[agent_name]
    
    def get_database_url(self) -> str:
        """Get database URL for session persistence."""
        return f"sqlite:///{self.db_path}"
    
    def get_tool_configurations(self) -> Dict[str, Dict[str, Any]]:
        """Get tool configurations for all agents."""
        return {
            "database_config": {
                "db_path": str(self.db_path),
                "timeout": 30,
                "retry_count": 3
            },
            "file_processing_config": {
                "workspace_path": str(self.workspace_path),
                "backup_enabled": True,
                "max_file_size": 50 * 1024 * 1024,  # 50MB
                "allowed_extensions": [".txt", ".md", ".docx"]
            },
            "analysis_config": {
                "confidence_threshold": 0.8,
                "max_context_length": 200,
                "pattern_cache_size": 1000
            },
            "processing_config": {
                "dry_run_default": True,
                "backup_retention_days": 30,
                "batch_size": 100
            }
        }

# Global configuration instance
CONFIG = WellspringADKConfig()