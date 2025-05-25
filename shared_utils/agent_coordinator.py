#!/usr/bin/env python3
"""
Agent Coordinator for Wellspring Book Production
Orchestrates all AI agents and manages workflow coordination.
"""

import json
import sqlite3
import asyncio
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any, Callable
from datetime import datetime, timedelta
from enum import Enum
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING = "waiting"

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

@dataclass
class AgentTask:
    """Represents a task assigned to an agent."""
    task_id: str
    agent_name: str
    task_type: str
    input_data: Dict[str, Any]
    priority: int = 5  # 1-10, 10 being highest
    dependencies: List[str] = None
    estimated_duration: int = 300  # seconds
    timeout: int = 900  # seconds
    retry_count: int = 0
    max_retries: int = 3
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class AgentInfo:
    """Information about an agent."""
    name: str
    agent_type: str
    capabilities: List[str]
    status: AgentStatus
    current_task: Optional[str] = None
    last_activity: Optional[datetime] = None
    performance_metrics: Dict[str, float] = None
    
    def __post_init__(self):
        if self.performance_metrics is None:
            self.performance_metrics = {}

@dataclass
class WorkflowDefinition:
    """Defines a complete workflow with multiple agents."""
    workflow_id: str
    name: str
    description: str
    tasks: List[AgentTask]
    coordination_rules: Dict[str, Any]
    success_criteria: Dict[str, Any]

class AgentCoordinator:
    """Coordinates multiple AI agents for book production workflows."""
    
    def __init__(self, db_path: str = None):
        """Initialize the agent coordinator."""
        if db_path is None:
            db_path = Path(__file__).parent / "data" / "wellspring.db"
        
        self.db_path = Path(db_path)
        self.agents: Dict[str, AgentInfo] = {}
        self.active_workflows: Dict[str, Dict] = {}
        self.task_queue: List[AgentTask] = []
        
        # Initialize default agents
        self._register_default_agents()
    
    def _register_default_agents(self):
        """Register the default Wellspring agents."""
        default_agents = [
            AgentInfo(
                name="PlanningArchitect",
                agent_type="orchestration",
                capabilities=["workflow_planning", "task_breakdown", "coordination"],
                status=AgentStatus.IDLE
            ),
            AgentInfo(
                name="DataLayerAgent",
                agent_type="data_management",
                capabilities=["database_operations", "data_validation", "synchronization"],
                status=AgentStatus.IDLE
            ),
            AgentInfo(
                name="TypographyAgent",
                agent_type="text_processing",
                capabilities=["em_dash_replacement", "typography_correction", "formatting"],
                status=AgentStatus.IDLE
            ),
            AgentInfo(
                name="DeepResearchAgent",
                agent_type="research",
                capabilities=["quote_verification", "fact_checking", "citation_management"],
                status=AgentStatus.IDLE
            ),
            AgentInfo(
                name="TaskTracker",
                agent_type="monitoring",
                capabilities=["progress_tracking", "status_reporting", "milestone_management"],
                status=AgentStatus.IDLE
            ),
            AgentInfo(
                name="RuleKeeper",
                agent_type="quality_control",
                capabilities=["rule_enforcement", "quality_validation", "compliance_checking"],
                status=AgentStatus.IDLE
            )
        ]
        
        for agent in default_agents:
            self.agents[agent.name] = agent
            logger.info(f"Registered agent: {agent.name} ({agent.agent_type})")
    
    def create_workflow(self, workflow_type: str, input_data: Dict[str, Any]) -> str:
        """Create a new workflow based on type."""
        workflow_id = f"{workflow_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if workflow_type == "em_dash_replacement":
            workflow = self._create_em_dash_workflow(workflow_id, input_data)
        elif workflow_type == "deep_research":
            workflow = self._create_research_workflow(workflow_id, input_data)
        elif workflow_type == "full_book_processing":
            workflow = self._create_full_processing_workflow(workflow_id, input_data)
        else:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        # Register workflow
        self.active_workflows[workflow_id] = {
            'definition': workflow,
            'status': WorkflowStatus.PENDING,
            'started_at': None,
            'completed_at': None,
            'progress': 0,
            'current_step': None,
            'results': {}
        }
        
        # Log to database
        self._log_workflow_creation(workflow)
        
        logger.info(f"Created workflow: {workflow_id} ({workflow_type})")
        return workflow_id
    
    def _create_em_dash_workflow(self, workflow_id: str, input_data: Dict[str, Any]) -> WorkflowDefinition:
        """Create em dash replacement workflow."""
        tasks = [
            AgentTask(
                task_id=f"{workflow_id}_plan",
                agent_name="PlanningArchitect",
                task_type="workflow_planning",
                input_data={
                    "workflow_type": "em_dash_replacement",
                    "input_files": input_data.get("input_files", []),
                    "requirements": input_data.get("requirements", {})
                },
                priority=9
            ),
            AgentTask(
                task_id=f"{workflow_id}_data_validation",
                agent_name="DataLayerAgent",
                task_type="validate_input",
                input_data=input_data,
                dependencies=[f"{workflow_id}_plan"],
                priority=8
            ),
            AgentTask(
                task_id=f"{workflow_id}_analysis",
                agent_name="TypographyAgent",
                task_type="analyze_em_dashes",
                input_data=input_data,
                dependencies=[f"{workflow_id}_data_validation"],
                priority=8
            ),
            AgentTask(
                task_id=f"{workflow_id}_dry_run",
                agent_name="TypographyAgent",
                task_type="dry_run_replacement",
                input_data={**input_data, "dry_run": True},
                dependencies=[f"{workflow_id}_analysis"],
                priority=7
            ),
            AgentTask(
                task_id=f"{workflow_id}_quality_check",
                agent_name="RuleKeeper",
                task_type="validate_replacements",
                input_data={},
                dependencies=[f"{workflow_id}_dry_run"],
                priority=7
            ),
            AgentTask(
                task_id=f"{workflow_id}_processing",
                agent_name="TypographyAgent",
                task_type="apply_replacements",
                input_data={**input_data, "dry_run": False},
                dependencies=[f"{workflow_id}_quality_check"],
                priority=8
            ),
            AgentTask(
                task_id=f"{workflow_id}_tracking",
                agent_name="TaskTracker",
                task_type="monitor_progress",
                input_data={},
                dependencies=[],  # Runs in parallel
                priority=6
            )
        ]
        
        return WorkflowDefinition(
            workflow_id=workflow_id,
            name="Em Dash Replacement Workflow",
            description="Comprehensive em dash analysis and replacement process",
            tasks=tasks,
            coordination_rules={
                "allow_parallel": True,
                "failure_handling": "pause_and_notify",
                "quality_gates": ["dry_run", "quality_check"]
            },
            success_criteria={
                "min_confidence": 0.8,
                "max_manual_review": 0.2,
                "processing_time_limit": 3600
            }
        )
    
    def _create_research_workflow(self, workflow_id: str, input_data: Dict[str, Any]) -> WorkflowDefinition:
        """Create deep research workflow."""
        tasks = [
            AgentTask(
                task_id=f"{workflow_id}_plan",
                agent_name="PlanningArchitect",
                task_type="workflow_planning",
                input_data={
                    "workflow_type": "deep_research",
                    "chapters": input_data.get("chapters", []),
                    "research_scope": input_data.get("research_scope", "full")
                },
                priority=9
            ),
            AgentTask(
                task_id=f"{workflow_id}_extract_quotes",
                agent_name="DeepResearchAgent",
                task_type="extract_quotes",
                input_data=input_data,
                dependencies=[f"{workflow_id}_plan"],
                priority=8
            ),
            AgentTask(
                task_id=f"{workflow_id}_verify_relevance",
                agent_name="DeepResearchAgent",
                task_type="verify_quote_relevance",
                input_data=input_data,
                dependencies=[f"{workflow_id}_extract_quotes"],
                priority=7
            ),
            AgentTask(
                task_id=f"{workflow_id}_fact_check",
                agent_name="DeepResearchAgent",
                task_type="fact_check_claims",
                input_data=input_data,
                dependencies=[f"{workflow_id}_plan"],
                priority=7
            ),
            AgentTask(
                task_id=f"{workflow_id}_visual_opportunities",
                agent_name="DeepResearchAgent",
                task_type="identify_visual_opportunities",
                input_data=input_data,
                dependencies=[f"{workflow_id}_plan"],
                priority=6
            ),
            AgentTask(
                task_id=f"{workflow_id}_save_results",
                agent_name="DataLayerAgent",
                task_type="save_research_results",
                input_data={},
                dependencies=[f"{workflow_id}_verify_relevance", f"{workflow_id}_fact_check", f"{workflow_id}_visual_opportunities"],
                priority=8
            )
        ]
        
        return WorkflowDefinition(
            workflow_id=workflow_id,
            name="Deep Research Workflow",
            description="Comprehensive research, verification, and citation management",
            tasks=tasks,
            coordination_rules={
                "allow_parallel": True,
                "failure_handling": "continue_with_warnings",
                "research_timeout": 1800
            },
            success_criteria={
                "min_quote_relevance": 0.7,
                "fact_check_coverage": 0.8,
                "visual_opportunities_identified": True
            }
        )
    
    def _create_full_processing_workflow(self, workflow_id: str, input_data: Dict[str, Any]) -> WorkflowDefinition:
        """Create full book processing workflow."""
        tasks = [
            # Phase 1: Planning and Analysis
            AgentTask(
                task_id=f"{workflow_id}_master_plan",
                agent_name="PlanningArchitect",
                task_type="create_master_plan",
                input_data=input_data,
                priority=10
            ),
            
            # Phase 2: Content Analysis (Parallel)
            AgentTask(
                task_id=f"{workflow_id}_em_dash_analysis",
                agent_name="TypographyAgent",
                task_type="analyze_em_dashes",
                input_data=input_data,
                dependencies=[f"{workflow_id}_master_plan"],
                priority=9
            ),
            AgentTask(
                task_id=f"{workflow_id}_research_analysis",
                agent_name="DeepResearchAgent",
                task_type="full_research_analysis",
                input_data=input_data,
                dependencies=[f"{workflow_id}_master_plan"],
                priority=9
            ),
            
            # Phase 3: Processing (Sequential)
            AgentTask(
                task_id=f"{workflow_id}_typography_processing",
                agent_name="TypographyAgent",
                task_type="apply_typography_corrections",
                input_data=input_data,
                dependencies=[f"{workflow_id}_em_dash_analysis"],
                priority=8
            ),
            
            # Phase 4: Quality Assurance
            AgentTask(
                task_id=f"{workflow_id}_quality_validation",
                agent_name="RuleKeeper",
                task_type="full_quality_check",
                input_data=input_data,
                dependencies=[f"{workflow_id}_typography_processing", f"{workflow_id}_research_analysis"],
                priority=9
            ),
            
            # Phase 5: Final Assembly
            AgentTask(
                task_id=f"{workflow_id}_final_assembly",
                agent_name="DataLayerAgent",
                task_type="assemble_final_output",
                input_data=input_data,
                dependencies=[f"{workflow_id}_quality_validation"],
                priority=10
            )
        ]
        
        return WorkflowDefinition(
            workflow_id=workflow_id,
            name="Full Book Processing Workflow",
            description="Complete end-to-end book production workflow",
            tasks=tasks,
            coordination_rules={
                "allow_parallel": True,
                "failure_handling": "pause_and_notify",
                "quality_gates": ["em_dash_analysis", "research_analysis", "quality_validation"],
                "checkpoint_frequency": 300  # seconds
            },
            success_criteria={
                "all_tasks_completed": True,
                "quality_score": 0.95,
                "processing_time_limit": 7200  # 2 hours
            }
        )
    
    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a workflow asynchronously."""
        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow not found: {workflow_id}")
        
        workflow_info = self.active_workflows[workflow_id]
        workflow_def = workflow_info['definition']
        
        logger.info(f"Starting workflow execution: {workflow_id}")
        
        # Update workflow status
        workflow_info['status'] = WorkflowStatus.RUNNING
        workflow_info['started_at'] = datetime.now()
        
        try:
            # Execute tasks based on dependencies
            completed_tasks = set()
            failed_tasks = set()
            
            while len(completed_tasks) < len(workflow_def.tasks):
                # Find ready tasks (all dependencies completed)
                ready_tasks = []
                for task in workflow_def.tasks:
                    if (task.task_id not in completed_tasks and 
                        task.task_id not in failed_tasks and
                        all(dep in completed_tasks for dep in task.dependencies)):
                        ready_tasks.append(task)
                
                if not ready_tasks:
                    if failed_tasks:
                        raise Exception(f"Workflow blocked by failed tasks: {failed_tasks}")
                    else:
                        break  # No more tasks to process
                
                # Execute ready tasks (potentially in parallel)
                if workflow_def.coordination_rules.get("allow_parallel", False):
                    results = await asyncio.gather(
                        *[self._execute_task(task) for task in ready_tasks],
                        return_exceptions=True
                    )
                    
                    for task, result in zip(ready_tasks, results):
                        if isinstance(result, Exception):
                            failed_tasks.add(task.task_id)
                            logger.error(f"Task failed: {task.task_id} - {result}")
                        else:
                            completed_tasks.add(task.task_id)
                            workflow_info['results'][task.task_id] = result
                            logger.info(f"Task completed: {task.task_id}")
                else:
                    # Execute sequentially
                    for task in ready_tasks:
                        try:
                            result = await self._execute_task(task)
                            completed_tasks.add(task.task_id)
                            workflow_info['results'][task.task_id] = result
                            logger.info(f"Task completed: {task.task_id}")
                        except Exception as e:
                            failed_tasks.add(task.task_id)
                            logger.error(f"Task failed: {task.task_id} - {e}")
                            
                            # Handle failure based on rules
                            failure_handling = workflow_def.coordination_rules.get("failure_handling", "pause_and_notify")
                            if failure_handling == "pause_and_notify":
                                raise Exception(f"Workflow paused due to task failure: {task.task_id}")
                
                # Update progress
                progress = len(completed_tasks) / len(workflow_def.tasks) * 100
                workflow_info['progress'] = progress
                
                # Log progress to database
                self._log_workflow_progress(workflow_id, progress, completed_tasks, failed_tasks)
            
            # Check success criteria
            success = self._evaluate_success_criteria(workflow_def, workflow_info['results'])
            
            if success:
                workflow_info['status'] = WorkflowStatus.COMPLETED
                logger.info(f"Workflow completed successfully: {workflow_id}")
            else:
                workflow_info['status'] = WorkflowStatus.FAILED
                logger.error(f"Workflow failed success criteria: {workflow_id}")
            
        except Exception as e:
            workflow_info['status'] = WorkflowStatus.FAILED
            logger.error(f"Workflow execution failed: {workflow_id} - {e}")
            raise
        
        finally:
            workflow_info['completed_at'] = datetime.now()
            
            # Final database log
            self._log_workflow_completion(workflow_id, workflow_info)
        
        return workflow_info
    
    async def _execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a single agent task."""
        agent = self.agents.get(task.agent_name)
        if not agent:
            raise ValueError(f"Agent not found: {task.agent_name}")
        
        # Update agent status
        agent.status = AgentStatus.RUNNING
        agent.current_task = task.task_id
        agent.last_activity = datetime.now()
        
        try:
            # Simulate task execution (in production, would call actual agent)
            logger.info(f"Executing task: {task.task_id} on agent: {task.agent_name}")
            
            # Task execution logic would go here
            await asyncio.sleep(1)  # Simulate work
            
            # Simulate task result
            result = {
                'task_id': task.task_id,
                'agent_name': task.agent_name,
                'status': 'completed',
                'execution_time': 1.0,
                'output_data': {'message': f'Task {task.task_id} completed successfully'},
                'performance_metrics': {'accuracy': 0.95, 'processing_speed': 1.0}
            }
            
            # Update agent performance metrics
            agent.performance_metrics.update(result['performance_metrics'])
            
            return result
            
        except Exception as e:
            logger.error(f"Task execution failed: {task.task_id} - {e}")
            raise
        
        finally:
            # Reset agent status
            agent.status = AgentStatus.IDLE
            agent.current_task = None
    
    def _evaluate_success_criteria(self, workflow_def: WorkflowDefinition, results: Dict[str, Any]) -> bool:
        """Evaluate if workflow meets success criteria."""
        criteria = workflow_def.success_criteria
        
        # Check if all required tasks completed
        if criteria.get("all_tasks_completed", False):
            if len(results) < len(workflow_def.tasks):
                return False
        
        # Check quality score
        min_quality = criteria.get("quality_score", 0.0)
        if min_quality > 0:
            avg_quality = sum(
                result.get('performance_metrics', {}).get('accuracy', 0.0)
                for result in results.values()
            ) / max(len(results), 1)
            
            if avg_quality < min_quality:
                return False
        
        return True
    
    def _log_workflow_creation(self, workflow: WorkflowDefinition):
        """Log workflow creation to database."""
        if not self.db_path.exists():
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO workflow_status 
                (workflow_name, workflow_type, status, input_data, started_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                workflow.name,
                workflow.workflow_id.split('_')[0],  # Extract type from ID
                WorkflowStatus.PENDING.value,
                json.dumps(asdict(workflow)),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error logging workflow creation: {e}")
    
    def _log_workflow_progress(self, workflow_id: str, progress: float, completed: set, failed: set):
        """Log workflow progress to database."""
        if not self.db_path.exists():
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE workflow_status 
                SET progress_percentage = ?, output_data = ?
                WHERE workflow_name = ?
            """, (
                int(progress),
                json.dumps({
                    'completed_tasks': list(completed),
                    'failed_tasks': list(failed),
                    'last_update': datetime.now().isoformat()
                }),
                workflow_id
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error logging workflow progress: {e}")
    
    def _log_workflow_completion(self, workflow_id: str, workflow_info: Dict):
        """Log workflow completion to database."""
        if not self.db_path.exists():
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE workflow_status 
                SET status = ?, progress_percentage = ?, completed_at = ?, output_data = ?
                WHERE workflow_name = ?
            """, (
                workflow_info['status'].value,
                workflow_info['progress'],
                workflow_info['completed_at'].isoformat() if workflow_info['completed_at'] else None,
                json.dumps(workflow_info['results']),
                workflow_id
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error logging workflow completion: {e}")
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get current workflow status."""
        if workflow_id not in self.active_workflows:
            return {'error': f'Workflow not found: {workflow_id}'}
        
        workflow_info = self.active_workflows[workflow_id]
        
        return {
            'workflow_id': workflow_id,
            'status': workflow_info['status'].value,
            'progress': workflow_info['progress'],
            'started_at': workflow_info['started_at'].isoformat() if workflow_info['started_at'] else None,
            'completed_at': workflow_info['completed_at'].isoformat() if workflow_info['completed_at'] else None,
            'current_step': workflow_info.get('current_step'),
            'agent_status': {name: agent.status.value for name, agent in self.agents.items()}
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        return {
            'timestamp': datetime.now().isoformat(),
            'agents': {
                name: {
                    'status': agent.status.value,
                    'current_task': agent.current_task,
                    'last_activity': agent.last_activity.isoformat() if agent.last_activity else None,
                    'capabilities': agent.capabilities,
                    'performance_metrics': agent.performance_metrics
                }
                for name, agent in self.agents.items()
            },
            'active_workflows': len(self.active_workflows),
            'task_queue_size': len(self.task_queue),
            'database_connected': self.db_path.exists()
        }

async def main():
    """Main function to demonstrate agent coordination."""
    print("🤖 Agent Coordinator for Wellspring Book Production")
    print("=" * 60)
    
    # Initialize coordinator
    coordinator = AgentCoordinator()
    
    # Display system status
    system_status = coordinator.get_system_status()
    print(f"\n📊 System Status:")
    print(f"  • Registered agents: {len(system_status['agents'])}")
    print(f"  • Database connected: {system_status['database_connected']}")
    
    print(f"\n🤖 Available Agents:")
    for name, info in system_status['agents'].items():
        print(f"  • {name} ({info['status']}) - {', '.join(info['capabilities'])}")
    
    # Create sample workflow
    print(f"\n🚀 Creating Em Dash Replacement Workflow...")
    workflow_id = coordinator.create_workflow("em_dash_replacement", {
        "input_files": ["sample_chapter.txt"],
        "confidence_threshold": 0.8,
        "dry_run": True
    })
    
    print(f"  • Workflow created: {workflow_id}")
    
    # Execute workflow
    print(f"\n⚡ Executing workflow...")
    try:
        result = await coordinator.execute_workflow(workflow_id)
        print(f"  • Workflow completed with status: {result['status'].value}")
        print(f"  • Progress: {result['progress']:.1f}%")
        print(f"  • Tasks completed: {len(result['results'])}")
    except Exception as e:
        print(f"  • Workflow failed: {e}")
    
    # Show final status
    final_status = coordinator.get_workflow_status(workflow_id)
    print(f"\n📋 Final Workflow Status:")
    for key, value in final_status.items():
        if key != 'agent_status':
            print(f"  • {key}: {value}")
    
    print(f"\n🎉 Agent coordination demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main())