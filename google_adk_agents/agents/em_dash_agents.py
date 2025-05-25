#!/usr/bin/env python3
"""
Google ADK Agent Definitions for Em Dash Processing
Defines the Google ADK agents using the configured tools and settings.
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, DatabaseSessionService
import logging

# Import configuration and tools
import sys
sys.path.append(str(Path(__file__).parent.parent))

from config.agent_config import CONFIG
from tools.em_dash_analysis_tools import (
    analyze_em_dash_patterns,
    suggest_replacements,
    calculate_confidence,
    generate_analysis_report,
    save_to_database
)
from tools.em_dash_processing_tools import (
    load_replacement_rules,
    perform_dry_run,
    apply_replacements,
    create_backup,
    validate_results,
    log_session
)
from tools.workflow_coordination_tools import (
    create_workflow,
    coordinate_agents,
    track_progress,
    validate_quality_gates,
    generate_workflow_report,
    manage_approvals
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmDashAgentFactory:
    """Factory for creating Google ADK Em Dash agents."""
    
    def __init__(self):
        """Initialize the agent factory."""
        self.config = CONFIG
        
        # Configure Google AI
        genai.configure(api_key=self.config.google_api_key)
        
        # Initialize session services
        self.session_services = self._create_session_services()
        
        logger.info("EmDashAgentFactory initialized")
    
    def _create_session_services(self) -> Dict[str, Any]:
        """Create session services for agents."""
        services = {}
        
        # Create database session service if database exists
        if self.config.db_path.exists():
            try:
                # For production, would use actual DatabaseSessionService
                # For now, using InMemorySessionService as fallback
                services['database'] = InMemorySessionService()
                logger.info("Created database session service")
            except Exception as e:
                logger.warning(f"Failed to create database session service: {e}")
                services['database'] = InMemorySessionService()
        else:
            services['database'] = InMemorySessionService()
            logger.info("Created in-memory session service")
        
        return services
    
    def create_em_dash_analyzer_agent(self) -> Agent:
        """Create the em dash analyzer agent."""
        config = self.config.get_agent_config("em_dash_analyzer")
        
        try:
            agent = Agent(
                name=config.name,
                model=config.model,
                description=config.description,
                instruction=config.instructions,
                tools=[
                    analyze_em_dash_patterns,
                    suggest_replacements,
                    calculate_confidence,
                    generate_analysis_report,
                    save_to_database
                ]
            )
            
            logger.info(f"Created em_dash_analyzer agent with model {config.model}")
            return agent
            
        except Exception as e:
            logger.error(f"Error creating em_dash_analyzer agent: {e}")
            raise
    
    def create_em_dash_processor_agent(self) -> Agent:
        """Create the em dash processor agent."""
        config = self.config.get_agent_config("em_dash_processor")
        
        try:
            agent = Agent(
                name=config.name,
                model=config.model,
                description=config.description,
                instruction=config.instructions,
                tools=[
                    load_replacement_rules,
                    perform_dry_run,
                    apply_replacements,
                    create_backup,
                    validate_results,
                    log_session
                ]
            )
            
            logger.info(f"Created em_dash_processor agent with model {config.model}")
            return agent
            
        except Exception as e:
            logger.error(f"Error creating em_dash_processor agent: {e}")
            raise
    
    def create_em_dash_coordinator_agent(self) -> Agent:
        """Create the em dash coordinator agent."""
        config = self.config.get_agent_config("em_dash_coordinator")
        
        try:
            agent = Agent(
                name=config.name,
                model=config.model,
                description=config.description,
                instruction=config.instructions,
                tools=[
                    create_workflow,
                    coordinate_agents,
                    track_progress,
                    validate_quality_gates,
                    generate_workflow_report,
                    manage_approvals
                ]
            )
            
            logger.info(f"Created em_dash_coordinator agent with model {config.model}")
            return agent
            
        except Exception as e:
            logger.error(f"Error creating em_dash_coordinator agent: {e}")
            raise
    
    def create_agent_runners(self) -> Dict[str, Runner]:
        """Create runners for all agents."""
        runners = {}
        
        try:
            # Create agents
            analyzer_agent = self.create_em_dash_analyzer_agent()
            processor_agent = self.create_em_dash_processor_agent()
            coordinator_agent = self.create_em_dash_coordinator_agent()
            
            # Create runners
            analyzer_config = self.config.get_runner_config("em_dash_analyzer")
            runners['analyzer'] = Runner(
                agent=analyzer_agent,
                app_name=analyzer_config.app_name,
                session_service=self.session_services['database']
            )
            
            processor_config = self.config.get_runner_config("em_dash_processor")
            runners['processor'] = Runner(
                agent=processor_agent,
                app_name=processor_config.app_name,
                session_service=self.session_services['database']
            )
            
            coordinator_config = self.config.get_runner_config("em_dash_coordinator")
            runners['coordinator'] = Runner(
                agent=coordinator_agent,
                app_name=coordinator_config.app_name,
                session_service=self.session_services['database']
            )
            
            logger.info("Created all agent runners")
            return runners
            
        except Exception as e:
            logger.error(f"Error creating agent runners: {e}")
            raise

class EmDashAgentOrchestrator:
    """Orchestrates the Google ADK em dash agents."""
    
    def __init__(self):
        """Initialize the orchestrator."""
        self.factory = EmDashAgentFactory()
        self.runners = self.factory.create_agent_runners()
        self.active_sessions = {}
        
        logger.info("EmDashAgentOrchestrator initialized")
    
    async def analyze_documents(
        self,
        file_paths: List[str],
        session_id: Optional[str] = None,
        configuration: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze documents for em dash patterns.
        
        Args:
            file_paths: List of document paths to analyze
            session_id: Optional session identifier
            configuration: Optional analysis configuration
            
        Returns:
            Dict containing analysis results
        """
        try:
            runner = self.runners['analyzer']
            
            # Prepare input data
            input_data = {
                'file_paths': file_paths,
                'configuration': configuration or {},
                'session_id': session_id
            }
            
            # Run analysis
            logger.info(f"Starting analysis of {len(file_paths)} document(s)")
            result = await runner.run_async(
                session_id=session_id,
                input_data=input_data
            )
            
            logger.info("Document analysis completed")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing documents: {e}")
            raise
    
    async def process_documents(
        self,
        file_paths: List[str],
        output_directory: str,
        session_id: Optional[str] = None,
        dry_run: bool = True,
        configuration: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process documents to apply em dash replacements.
        
        Args:
            file_paths: List of document paths to process
            output_directory: Directory for output files
            session_id: Optional session identifier
            dry_run: Whether to perform dry run first
            configuration: Optional processing configuration
            
        Returns:
            Dict containing processing results
        """
        try:
            runner = self.runners['processor']
            
            # Prepare input data
            input_data = {
                'file_paths': file_paths,
                'output_directory': output_directory,
                'dry_run': dry_run,
                'configuration': configuration or {},
                'session_id': session_id
            }
            
            # Run processing
            logger.info(f"Starting processing of {len(file_paths)} document(s) (dry_run: {dry_run})")
            result = await runner.run_async(
                session_id=session_id,
                input_data=input_data
            )
            
            logger.info("Document processing completed")
            return result
            
        except Exception as e:
            logger.error(f"Error processing documents: {e}")
            raise
    
    async def execute_workflow(
        self,
        workflow_name: str,
        input_files: List[str],
        output_directory: str,
        configuration: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute complete em dash workflow.
        
        Args:
            workflow_name: Name for the workflow
            input_files: List of input file paths
            output_directory: Directory for output files
            configuration: Optional workflow configuration
            
        Returns:
            Dict containing workflow results
        """
        try:
            runner = self.runners['coordinator']
            
            # Prepare input data
            input_data = {
                'workflow_name': workflow_name,
                'input_files': input_files,
                'output_directory': output_directory,
                'configuration': configuration or {}
            }
            
            # Execute workflow
            logger.info(f"Starting workflow: {workflow_name}")
            result = await runner.run_async(
                input_data=input_data
            )
            
            logger.info(f"Workflow completed: {workflow_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error executing workflow: {e}")
            raise
    
    async def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get status of a running workflow."""
        try:
            runner = self.runners['coordinator']
            
            result = await runner.run_async(
                input_data={
                    'action': 'get_status',
                    'workflow_id': workflow_id
                }
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting workflow status: {e}")
            raise
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        try:
            status = {
                'timestamp': CONFIG.get_tool_configurations()['database_config']['timeout'],
                'agents': {
                    'analyzer': {
                        'status': 'ready',
                        'model': CONFIG.get_agent_config('em_dash_analyzer').model,
                        'capabilities': ['analyze_patterns', 'suggest_replacements', 'generate_reports']
                    },
                    'processor': {
                        'status': 'ready',
                        'model': CONFIG.get_agent_config('em_dash_processor').model,
                        'capabilities': ['dry_run', 'apply_replacements', 'validate_results']
                    },
                    'coordinator': {
                        'status': 'ready',
                        'model': CONFIG.get_agent_config('em_dash_coordinator').model,
                        'capabilities': ['workflow_management', 'quality_gates', 'approvals']
                    }
                },
                'configuration': {
                    'database_connected': CONFIG.db_path.exists(),
                    'default_model': CONFIG.default_model,
                    'workspace_path': str(CONFIG.workspace_path)
                },
                'active_sessions': len(self.active_sessions)
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            raise

# Global orchestrator instance
ORCHESTRATOR = EmDashAgentOrchestrator()

# Convenience functions for direct use
async def analyze_file(file_path: str, **kwargs) -> Dict[str, Any]:
    """Analyze a single file for em dash patterns."""
    return await ORCHESTRATOR.analyze_documents([file_path], **kwargs)

async def process_file(
    file_path: str,
    output_directory: str,
    dry_run: bool = True,
    **kwargs
) -> Dict[str, Any]:
    """Process a single file for em dash replacements."""
    return await ORCHESTRATOR.process_documents([file_path], output_directory, dry_run=dry_run, **kwargs)

async def create_and_execute_workflow(
    workflow_name: str,
    input_files: List[str],
    output_directory: str,
    **kwargs
) -> Dict[str, Any]:
    """Create and execute a complete em dash workflow."""
    return await ORCHESTRATOR.execute_workflow(workflow_name, input_files, output_directory, **kwargs)

def get_agent_status() -> Dict[str, Any]:
    """Get status of all agents."""
    return ORCHESTRATOR.get_system_status()

if __name__ == "__main__":
    import asyncio
    
    async def demo():
        """Demonstrate the Google ADK em dash agents."""
        print("🤖 Google ADK Em Dash Agent Framework Demo")
        print("=" * 60)
        
        # Get system status
        status = get_agent_status()
        print(f"\n📊 System Status:")
        print(f"  • Database connected: {status['configuration']['database_connected']}")
        print(f"  • Default model: {status['configuration']['default_model']}")
        print(f"  • Active sessions: {status['active_sessions']}")
        
        print(f"\n🤖 Available Agents:")
        for name, info in status['agents'].items():
            print(f"  • {name}: {info['status']} ({info['model']})")
            print(f"    Capabilities: {', '.join(info['capabilities'])}")
        
        # Demo would continue with actual file processing
        print(f"\n🎉 Google ADK Em Dash Agent Framework is ready!")
    
    # Run demo
    asyncio.run(demo())