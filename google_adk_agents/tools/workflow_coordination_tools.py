#!/usr/bin/env python3
"""
Google ADK Tools for Workflow Coordination
Provides specialized tools for the em_dash_coordinator agent.
"""

import json
import sqlite3
import asyncio
from pathlib import Path
from typing import List, Dict, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running" 
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskStatus(Enum):
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class WorkflowTask:
    """Individual task within a workflow."""
    task_id: str
    task_name: str
    agent_name: str
    task_type: str
    input_data: Dict[str, Any]
    dependencies: List[str]
    status: TaskStatus = TaskStatus.WAITING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3

@dataclass
class QualityGate:
    """Quality gate configuration."""
    gate_id: str
    gate_name: str
    criteria: Dict[str, Any]
    required_tasks: List[str]
    approval_required: bool = False
    auto_approve_threshold: float = 0.9

@dataclass
class EmDashWorkflow:
    """Complete em dash workflow definition."""
    workflow_id: str
    workflow_name: str
    description: str
    input_files: List[str]
    output_directory: str
    tasks: List[WorkflowTask]
    quality_gates: List[QualityGate]
    configuration: Dict[str, Any]
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress_percentage: float = 0.0
    current_step: Optional[str] = None

class WorkflowCoordinationTools:
    """Tool implementations for workflow coordination."""
    
    def __init__(self, db_path: str = None):
        """Initialize with database connection."""
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "shared_utils" / "data" / "wellspring.db"
        self.db_path = Path(db_path)

def create_workflow(
    workflow_name: str,
    input_files: List[str],
    output_directory: str,
    configuration: Optional[Dict[str, Any]] = None
) -> EmDashWorkflow:
    """
    Create a new em dash processing workflow.
    
    Args:
        workflow_name: Name for the workflow
        input_files: List of input file paths
        output_directory: Directory for output files
        configuration: Optional workflow configuration
        
    Returns:
        EmDashWorkflow: Created workflow definition
    """
    try:
        workflow_id = f"em_dash_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Default configuration
        default_config = {
            'confidence_threshold': 0.8,
            'dry_run_first': True,
            'backup_enabled': True,
            'parallel_processing': True,
            'quality_gates_enabled': True,
            'manual_approval_required': False
        }
        
        if configuration:
            default_config.update(configuration)
        
        # Create workflow tasks
        tasks = _create_workflow_tasks(workflow_id, input_files, output_directory, default_config)
        
        # Create quality gates
        quality_gates = _create_quality_gates(workflow_id, default_config)
        
        workflow = EmDashWorkflow(
            workflow_id=workflow_id,
            workflow_name=workflow_name,
            description=f"Em dash processing workflow for {len(input_files)} file(s)",
            input_files=input_files,
            output_directory=output_directory,
            tasks=tasks,
            quality_gates=quality_gates,
            configuration=default_config,
            created_at=datetime.now()
        )
        
        logger.info(f"Created workflow: {workflow_id} with {len(tasks)} tasks")
        return workflow
        
    except Exception as e:
        logger.error(f"Error creating workflow: {e}")
        raise

def coordinate_agents(
    workflow: EmDashWorkflow,
    agent_communications: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Coordinate communication between agents in the workflow.
    
    Args:
        workflow: Workflow to coordinate
        agent_communications: Optional agent communication data
        
    Returns:
        Dict containing coordination results
    """
    try:
        coordination_result = {
            'workflow_id': workflow.workflow_id,
            'coordination_timestamp': datetime.now().isoformat(),
            'agent_status': {},
            'inter_agent_messages': [],
            'coordination_actions': []
        }
        
        # Check status of each agent's tasks
        for task in workflow.tasks:
            agent_name = task.agent_name
            if agent_name not in coordination_result['agent_status']:
                coordination_result['agent_status'][agent_name] = {
                    'assigned_tasks': [],
                    'current_task': None,
                    'status': 'idle',
                    'last_activity': None
                }
            
            task_info = {
                'task_id': task.task_id,
                'status': task.status.value,
                'dependencies_met': _check_dependencies_met(task, workflow.tasks)
            }
            
            coordination_result['agent_status'][agent_name]['assigned_tasks'].append(task_info)
            
            if task.status == TaskStatus.RUNNING:
                coordination_result['agent_status'][agent_name]['current_task'] = task.task_id
                coordination_result['agent_status'][agent_name]['status'] = 'running'
                coordination_result['agent_status'][agent_name]['last_activity'] = task.started_at.isoformat() if task.started_at else None
        
        # Generate coordination actions
        coordination_actions = _generate_coordination_actions(workflow)
        coordination_result['coordination_actions'] = coordination_actions
        
        # Handle inter-agent communications
        if agent_communications:
            coordination_result['inter_agent_messages'] = _process_agent_communications(
                workflow, agent_communications
            )
        
        logger.info(f"Coordinated agents for workflow {workflow.workflow_id}")
        return coordination_result
        
    except Exception as e:
        logger.error(f"Error coordinating agents: {e}")
        raise

def track_progress(
    workflow: EmDashWorkflow,
    update_database: bool = True
) -> Dict[str, Any]:
    """
    Track progress of workflow execution.
    
    Args:
        workflow: Workflow to track
        update_database: Whether to update database with progress
        
    Returns:
        Dict containing progress information
    """
    try:
        # Calculate overall progress
        total_tasks = len(workflow.tasks)
        completed_tasks = sum(1 for task in workflow.tasks if task.status == TaskStatus.COMPLETED)
        failed_tasks = sum(1 for task in workflow.tasks if task.status == TaskStatus.FAILED)
        running_tasks = sum(1 for task in workflow.tasks if task.status == TaskStatus.RUNNING)
        
        progress_percentage = (completed_tasks / max(total_tasks, 1)) * 100
        workflow.progress_percentage = progress_percentage
        
        # Determine current step
        current_step = None
        for task in workflow.tasks:
            if task.status == TaskStatus.RUNNING:
                current_step = task.task_name
                break
        
        if not current_step and running_tasks == 0:
            if completed_tasks == total_tasks:
                current_step = "Workflow Completed"
            elif failed_tasks > 0:
                current_step = "Error Resolution Required"
            else:
                current_step = "Ready to Start"
        
        workflow.current_step = current_step
        
        # Calculate estimated completion time
        estimated_completion = _calculate_estimated_completion(workflow)
        
        progress_info = {
            'workflow_id': workflow.workflow_id,
            'status': workflow.status.value,
            'progress_percentage': progress_percentage,
            'current_step': current_step,
            'task_summary': {
                'total': total_tasks,
                'completed': completed_tasks,
                'running': running_tasks,
                'failed': failed_tasks,
                'waiting': total_tasks - completed_tasks - running_tasks - failed_tasks
            },
            'estimated_completion': estimated_completion,
            'quality_gates_status': _check_quality_gates_status(workflow),
            'last_updated': datetime.now().isoformat()
        }
        
        # Update database if requested
        if update_database:
            _update_workflow_progress_in_db(workflow, progress_info)
        
        logger.info(f"Progress tracked for workflow {workflow.workflow_id}: {progress_percentage:.1f}%")
        return progress_info
        
    except Exception as e:
        logger.error(f"Error tracking progress: {e}")
        raise

def validate_quality_gates(
    workflow: EmDashWorkflow,
    gate_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate quality gates for the workflow.
    
    Args:
        workflow: Workflow to validate
        gate_id: Optional specific gate to validate
        
    Returns:
        Dict containing validation results
    """
    try:
        validation_results = {
            'workflow_id': workflow.workflow_id,
            'validation_timestamp': datetime.now().isoformat(),
            'gates_passed': [],
            'gates_failed': [],
            'overall_status': 'pending',
            'approval_required': []
        }
        
        gates_to_check = [gate for gate in workflow.quality_gates if gate_id is None or gate.gate_id == gate_id]
        
        for gate in gates_to_check:
            gate_result = _validate_single_quality_gate(gate, workflow)
            
            if gate_result['passed']:
                validation_results['gates_passed'].append({
                    'gate_id': gate.gate_id,
                    'gate_name': gate.gate_name,
                    'score': gate_result['score'],
                    'details': gate_result['details']
                })
            else:
                validation_results['gates_failed'].append({
                    'gate_id': gate.gate_id,
                    'gate_name': gate.gate_name,
                    'score': gate_result['score'],
                    'issues': gate_result['issues'],
                    'recommendations': gate_result['recommendations']
                })
            
            # Check if manual approval is required
            if gate.approval_required and gate_result['score'] < gate.auto_approve_threshold:
                validation_results['approval_required'].append({
                    'gate_id': gate.gate_id,
                    'gate_name': gate.gate_name,
                    'reason': 'Score below auto-approval threshold',
                    'score': gate_result['score'],
                    'threshold': gate.auto_approve_threshold
                })
        
        # Determine overall status
        if validation_results['gates_failed']:
            validation_results['overall_status'] = 'failed'
        elif validation_results['approval_required']:
            validation_results['overall_status'] = 'approval_required'
        else:
            validation_results['overall_status'] = 'passed'
        
        logger.info(f"Quality gates validated for workflow {workflow.workflow_id}: {validation_results['overall_status']}")
        return validation_results
        
    except Exception as e:
        logger.error(f"Error validating quality gates: {e}")
        raise

def generate_workflow_report(
    workflow: EmDashWorkflow,
    include_detailed_results: bool = True
) -> Dict[str, Any]:
    """
    Generate comprehensive workflow report.
    
    Args:
        workflow: Workflow to report on
        include_detailed_results: Whether to include detailed task results
        
    Returns:
        Dict containing comprehensive report
    """
    try:
        # Calculate execution metrics
        total_duration = None
        if workflow.started_at and workflow.completed_at:
            total_duration = (workflow.completed_at - workflow.started_at).total_seconds()
        
        task_metrics = _calculate_task_metrics(workflow.tasks)
        quality_metrics = _calculate_quality_metrics(workflow)
        
        report = {
            'workflow_summary': {
                'workflow_id': workflow.workflow_id,
                'workflow_name': workflow.workflow_name,
                'description': workflow.description,
                'status': workflow.status.value,
                'created_at': workflow.created_at.isoformat() if workflow.created_at else None,
                'started_at': workflow.started_at.isoformat() if workflow.started_at else None,
                'completed_at': workflow.completed_at.isoformat() if workflow.completed_at else None,
                'total_duration_seconds': total_duration,
                'progress_percentage': workflow.progress_percentage
            },
            'input_output_summary': {
                'input_files': workflow.input_files,
                'input_file_count': len(workflow.input_files),
                'output_directory': workflow.output_directory,
                'configuration': workflow.configuration
            },
            'execution_metrics': task_metrics,
            'quality_metrics': quality_metrics,
            'recommendations': _generate_workflow_recommendations(workflow)
        }
        
        # Include detailed results if requested
        if include_detailed_results:
            report['detailed_task_results'] = [
                {
                    'task_id': task.task_id,
                    'task_name': task.task_name,
                    'agent_name': task.agent_name,
                    'status': task.status.value,
                    'duration_seconds': (task.completed_at - task.started_at).total_seconds() if task.started_at and task.completed_at else None,
                    'retry_count': task.retry_count,
                    'result_summary': _summarize_task_result(task.result) if task.result else None,
                    'error_message': task.error_message
                }
                for task in workflow.tasks
            ]
            
            report['quality_gate_results'] = [
                {
                    'gate_id': gate.gate_id,
                    'gate_name': gate.gate_name,
                    'criteria': gate.criteria,
                    'validation_result': validate_quality_gates(workflow, gate.gate_id)
                }
                for gate in workflow.quality_gates
            ]
        
        logger.info(f"Generated workflow report for {workflow.workflow_id}")
        return report
        
    except Exception as e:
        logger.error(f"Error generating workflow report: {e}")
        raise

def manage_approvals(
    workflow: EmDashWorkflow,
    approval_action: str,
    gate_id: Optional[str] = None,
    approver_id: Optional[str] = None,
    approval_notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Manage manual approvals for workflow quality gates.
    
    Args:
        workflow: Workflow to manage approvals for
        approval_action: 'approve', 'reject', or 'request_changes'
        gate_id: Optional specific gate to approve
        approver_id: Optional approver identifier
        approval_notes: Optional approval notes
        
    Returns:
        Dict containing approval results
    """
    try:
        approval_result = {
            'workflow_id': workflow.workflow_id,
            'approval_action': approval_action,
            'gate_id': gate_id,
            'approver_id': approver_id,
            'approval_timestamp': datetime.now().isoformat(),
            'approval_notes': approval_notes,
            'result': 'pending'
        }
        
        if approval_action == 'approve':
            # Mark workflow as approved to continue
            approval_result['result'] = 'approved'
            approval_result['next_steps'] = ['Continue workflow execution']
            
            # Update workflow status if needed
            if workflow.status == WorkflowStatus.PAUSED:
                workflow.status = WorkflowStatus.RUNNING
            
        elif approval_action == 'reject':
            # Stop workflow execution
            approval_result['result'] = 'rejected'
            approval_result['next_steps'] = ['Workflow execution stopped', 'Review required issues', 'Restart workflow after fixes']
            
            workflow.status = WorkflowStatus.FAILED
            
        elif approval_action == 'request_changes':
            # Pause workflow for changes
            approval_result['result'] = 'changes_requested'
            approval_result['next_steps'] = ['Workflow paused', 'Implement requested changes', 'Re-submit for approval']
            
            workflow.status = WorkflowStatus.PAUSED
        
        # Log approval to database
        _log_approval_to_database(workflow, approval_result)
        
        logger.info(f"Approval processed for workflow {workflow.workflow_id}: {approval_action}")
        return approval_result
        
    except Exception as e:
        logger.error(f"Error managing approvals: {e}")
        raise

# Helper functions
def _create_workflow_tasks(
    workflow_id: str,
    input_files: List[str],
    output_directory: str,
    configuration: Dict[str, Any]
) -> List[WorkflowTask]:
    """Create workflow tasks for em dash processing."""
    tasks = []
    
    # Analysis phase tasks
    for i, input_file in enumerate(input_files):
        tasks.append(WorkflowTask(
            task_id=f"{workflow_id}_analyze_{i}",
            task_name=f"Analyze Em Dashes - {Path(input_file).name}",
            agent_name="em_dash_analyzer",
            task_type="analyze_em_dash_patterns",
            input_data={
                'file_path': input_file,
                'context_length': configuration.get('context_length', 50),
                'min_confidence': configuration.get('confidence_threshold', 0.8)
            },
            dependencies=[]
        ))
    
    # Dry run phase tasks (if enabled)
    if configuration.get('dry_run_first', True):
        for i, input_file in enumerate(input_files):
            tasks.append(WorkflowTask(
                task_id=f"{workflow_id}_dry_run_{i}",
                task_name=f"Dry Run Processing - {Path(input_file).name}",
                agent_name="em_dash_processor",
                task_type="perform_dry_run",
                input_data={
                    'input_file': input_file,
                    'output_directory': output_directory,
                    'confidence_threshold': configuration.get('confidence_threshold', 0.8)
                },
                dependencies=[f"{workflow_id}_analyze_{i}"]
            ))
    
    # Processing phase tasks
    for i, input_file in enumerate(input_files):
        dependencies = [f"{workflow_id}_analyze_{i}"]
        if configuration.get('dry_run_first', True):
            dependencies.append(f"{workflow_id}_dry_run_{i}")
        
        tasks.append(WorkflowTask(
            task_id=f"{workflow_id}_process_{i}",
            task_name=f"Apply Replacements - {Path(input_file).name}",
            agent_name="em_dash_processor",
            task_type="apply_replacements",
            input_data={
                'input_file': input_file,
                'output_directory': output_directory,
                'confidence_threshold': configuration.get('confidence_threshold', 0.8),
                'create_backup': configuration.get('backup_enabled', True)
            },
            dependencies=dependencies
        ))
    
    return tasks

def _create_quality_gates(workflow_id: str, configuration: Dict[str, Any]) -> List[QualityGate]:
    """Create quality gates for the workflow."""
    gates = []
    
    if configuration.get('quality_gates_enabled', True):
        # Analysis quality gate
        gates.append(QualityGate(
            gate_id=f"{workflow_id}_analysis_gate",
            gate_name="Analysis Quality Gate",
            criteria={
                'min_confidence_average': 0.7,
                'max_manual_review_ratio': 0.3,
                'min_pattern_coverage': 0.8
            },
            required_tasks=[task_id for task_id in [f"{workflow_id}_analyze_{i}" for i in range(10)] if task_id],
            approval_required=configuration.get('manual_approval_required', False),
            auto_approve_threshold=0.85
        ))
        
        # Processing quality gate
        gates.append(QualityGate(
            gate_id=f"{workflow_id}_processing_gate",
            gate_name="Processing Quality Gate",
            criteria={
                'min_replacement_rate': 0.8,
                'max_error_rate': 0.05,
                'processing_time_limit': 300
            },
            required_tasks=[task_id for task_id in [f"{workflow_id}_process_{i}" for i in range(10)] if task_id],
            approval_required=False,
            auto_approve_threshold=0.9
        ))
    
    return gates

def _check_dependencies_met(task: WorkflowTask, all_tasks: List[WorkflowTask]) -> bool:
    """Check if task dependencies are met."""
    if not task.dependencies:
        return True
    
    task_status_map = {t.task_id: t.status for t in all_tasks}
    
    for dep_id in task.dependencies:
        if dep_id not in task_status_map or task_status_map[dep_id] != TaskStatus.COMPLETED:
            return False
    
    return True

def _generate_coordination_actions(workflow: EmDashWorkflow) -> List[Dict[str, Any]]:
    """Generate coordination actions for the workflow."""
    actions = []
    
    for task in workflow.tasks:
        if task.status == TaskStatus.WAITING and _check_dependencies_met(task, workflow.tasks):
            actions.append({
                'action_type': 'start_task',
                'task_id': task.task_id,
                'agent_name': task.agent_name,
                'priority': 'high' if 'analyze' in task.task_type else 'medium'
            })
        elif task.status == TaskStatus.FAILED and task.retry_count < task.max_retries:
            actions.append({
                'action_type': 'retry_task',
                'task_id': task.task_id,
                'agent_name': task.agent_name,
                'retry_count': task.retry_count + 1,
                'priority': 'high'
            })
    
    return actions

def _process_agent_communications(workflow: EmDashWorkflow, communications: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Process inter-agent communications."""
    messages = []
    
    # Example processing of agent communications
    for agent_name, agent_data in communications.items():
        if 'status_update' in agent_data:
            messages.append({
                'message_type': 'status_update',
                'from_agent': agent_name,
                'timestamp': datetime.now().isoformat(),
                'content': agent_data['status_update']
            })
        
        if 'results' in agent_data:
            messages.append({
                'message_type': 'task_result',
                'from_agent': agent_name,
                'timestamp': datetime.now().isoformat(),
                'content': agent_data['results']
            })
    
    return messages

def _calculate_estimated_completion(workflow: EmDashWorkflow) -> Optional[str]:
    """Calculate estimated completion time."""
    if workflow.status == WorkflowStatus.COMPLETED:
        return None
    
    running_tasks = [task for task in workflow.tasks if task.status == TaskStatus.RUNNING]
    if not running_tasks:
        return "Ready to start"
    
    # Simple estimation based on average task duration
    completed_tasks = [task for task in workflow.tasks if task.status == TaskStatus.COMPLETED and task.started_at and task.completed_at]
    
    if completed_tasks:
        avg_duration = sum((task.completed_at - task.started_at).total_seconds() for task in completed_tasks) / len(completed_tasks)
        remaining_tasks = len([task for task in workflow.tasks if task.status in [TaskStatus.WAITING, TaskStatus.RUNNING]])
        estimated_seconds = remaining_tasks * avg_duration
        
        estimated_completion = datetime.now() + timedelta(seconds=estimated_seconds)
        return estimated_completion.isoformat()
    
    return "Calculating..."

def _check_quality_gates_status(workflow: EmDashWorkflow) -> Dict[str, str]:
    """Check status of all quality gates."""
    gate_status = {}
    
    for gate in workflow.quality_gates:
        # Check if required tasks are completed
        required_task_ids = set(gate.required_tasks)
        completed_task_ids = {task.task_id for task in workflow.tasks if task.status == TaskStatus.COMPLETED}
        
        if required_task_ids.issubset(completed_task_ids):
            gate_status[gate.gate_id] = "ready_for_validation"
        else:
            gate_status[gate.gate_id] = "waiting_for_tasks"
    
    return gate_status

def _validate_single_quality_gate(gate: QualityGate, workflow: EmDashWorkflow) -> Dict[str, Any]:
    """Validate a single quality gate."""
    result = {
        'passed': False,
        'score': 0.0,
        'details': {},
        'issues': [],
        'recommendations': []
    }
    
    # Check criteria (simplified implementation)
    criteria_met = 0
    total_criteria = len(gate.criteria)
    
    for criterion, threshold in gate.criteria.items():
        # This would contain actual validation logic based on task results
        # For now, using placeholder logic
        if criterion == 'min_confidence_average':
            # Would calculate from actual task results
            actual_confidence = 0.85  # Placeholder
            if actual_confidence >= threshold:
                criteria_met += 1
            else:
                result['issues'].append(f"Average confidence {actual_confidence:.2f} below threshold {threshold}")
        
        elif criterion == 'max_manual_review_ratio':
            # Would calculate from actual task results  
            actual_ratio = 0.15  # Placeholder
            if actual_ratio <= threshold:
                criteria_met += 1
            else:
                result['issues'].append(f"Manual review ratio {actual_ratio:.2f} above threshold {threshold}")
        
        # Add more criteria validation as needed
    
    result['score'] = criteria_met / max(total_criteria, 1)
    result['passed'] = result['score'] >= 0.8  # 80% of criteria must pass
    
    if not result['passed']:
        result['recommendations'].append("Review and adjust processing parameters")
        result['recommendations'].append("Consider manual review of flagged items")
    
    return result

def _calculate_task_metrics(tasks: List[WorkflowTask]) -> Dict[str, Any]:
    """Calculate metrics for workflow tasks."""
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.status == TaskStatus.COMPLETED)
    failed_tasks = sum(1 for task in tasks if task.status == TaskStatus.FAILED)
    
    # Calculate durations for completed tasks
    task_durations = []
    for task in tasks:
        if task.started_at and task.completed_at:
            duration = (task.completed_at - task.started_at).total_seconds()
            task_durations.append(duration)
    
    avg_duration = sum(task_durations) / len(task_durations) if task_durations else 0
    
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'failed_tasks': failed_tasks,
        'success_rate': completed_tasks / max(total_tasks, 1),
        'average_task_duration_seconds': avg_duration,
        'total_retries': sum(task.retry_count for task in tasks)
    }

def _calculate_quality_metrics(workflow: EmDashWorkflow) -> Dict[str, Any]:
    """Calculate quality metrics for the workflow."""
    # This would analyze actual task results to calculate quality metrics
    # Placeholder implementation
    return {
        'overall_quality_score': 0.85,
        'confidence_distribution': {'high': 0.7, 'medium': 0.2, 'low': 0.1},
        'processing_efficiency': 0.9,
        'manual_review_required': 0.15
    }

def _generate_workflow_recommendations(workflow: EmDashWorkflow) -> List[str]:
    """Generate recommendations based on workflow results."""
    recommendations = []
    
    # Analyze workflow performance and generate recommendations
    failed_tasks = [task for task in workflow.tasks if task.status == TaskStatus.FAILED]
    if failed_tasks:
        recommendations.append(f"Review and resolve {len(failed_tasks)} failed task(s)")
    
    retried_tasks = [task for task in workflow.tasks if task.retry_count > 0]
    if retried_tasks:
        recommendations.append("Investigate causes of task failures to improve reliability")
    
    if workflow.status == WorkflowStatus.COMPLETED:
        recommendations.append("Workflow completed successfully - review results for quality")
    
    return recommendations

def _summarize_task_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Summarize task result for reporting."""
    if not result:
        return {}
    
    summary = {}
    
    # Extract key metrics from result
    if 'total_em_dashes' in result:
        summary['em_dashes_found'] = result['total_em_dashes']
    
    if 'replacements_made' in result:
        summary['replacements_made'] = result['replacements_made']
    
    if 'confidence_distribution' in result:
        summary['confidence_distribution'] = result['confidence_distribution']
    
    if 'processing_time' in result:
        summary['processing_time_seconds'] = result['processing_time']
    
    return summary

def _update_workflow_progress_in_db(workflow: EmDashWorkflow, progress_info: Dict[str, Any]):
    """Update workflow progress in database."""
    tools = WorkflowCoordinationTools()
    
    try:
        if not tools.db_path.exists():
            return
        
        conn = sqlite3.connect(tools.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE workflow_status 
            SET progress_percentage = ?, status = ?, output_data = ?
            WHERE workflow_name = ?
        """, (
            progress_info['progress_percentage'],
            workflow.status.value,
            json.dumps(progress_info),
            workflow.workflow_id
        ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error updating workflow progress in database: {e}")

def _log_approval_to_database(workflow: EmDashWorkflow, approval_result: Dict[str, Any]):
    """Log approval action to database."""
    tools = WorkflowCoordinationTools()
    
    try:
        if not tools.db_path.exists():
            return
        
        conn = sqlite3.connect(tools.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO agent_logs 
            (agent_name, task_type, input_data, output_data, status, started_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "em_dash_coordinator",
            "manage_approval",
            json.dumps({
                'workflow_id': workflow.workflow_id,
                'approval_action': approval_result['approval_action'],
                'gate_id': approval_result.get('gate_id')
            }),
            json.dumps(approval_result),
            "completed",
            approval_result['approval_timestamp'],
            approval_result['approval_timestamp']
        ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error logging approval to database: {e}")