"""
Agent Rules Module

Operational rules and guidelines for all Wellspring agents including
Google ADK agents, research agents, and typography agents.

This module contains the authoritative rules that agents must follow
for consistent behavior across the Wellspring book production system.

Available Rules:
- agent_roles: Agent definitions and responsibilities
- global_rules: Core system rules and philosophy
- workflow_coordination: Inter-agent coordination patterns
- research_rules: Research and citation guidelines
- typography_rules: Typography and design standards
- em_dash_rules: Em dash replacement guidelines
- setup_guide: System initialization and setup

Usage:
    from wellspring_directory.rules import get_rule, list_available_rules
    
    # Get a specific rule
    agent_rules = get_rule('agent_roles')
    
    # List all available rules
    available = list_available_rules()
"""

from pathlib import Path
from typing import Dict, List, Optional

MODULE_DIR = Path(__file__).parent

def get_rule(rule_name: str) -> Optional[str]:
    """Get content of a specific rule file"""
    rule_file = MODULE_DIR / f"{rule_name}.md"
    if rule_file.exists():
        try:
            with open(rule_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading {rule_name}: {e}"
    return None

def list_available_rules() -> List[str]:
    """List all available rule file names (without .md extension)"""
    return [f.stem for f in MODULE_DIR.glob("*.md")]

def get_all_rules() -> Dict[str, str]:
    """Get content of all rule files"""
    rules = {}
    for rule_name in list_available_rules():
        content = get_rule(rule_name)
        if content:
            rules[rule_name] = content
    return rules

def get_rule_summary() -> Dict[str, str]:
    """Get a summary of what each rule file contains"""
    return {
        "agent_roles": "Agent definitions and responsibilities",
        "global_rules": "Core system rules and philosophy", 
        "workflow_coordination": "Inter-agent coordination patterns",
        "research_rules": "Research and citation guidelines",
        "typography_rules": "Typography and design standards",
        "em_dash_rules": "Em dash replacement guidelines",
        "setup_guide": "System initialization and setup"
    }

def get_rules_for_agent(agent_type: str) -> Dict[str, str]:
    """Get relevant rules for a specific agent type"""
    agent_rules = {}
    all_rules = get_all_rules()
    
    # Core rules all agents need
    core_rules = ['global_rules', 'agent_roles', 'workflow_coordination']
    for rule in core_rules:
        if rule in all_rules:
            agent_rules[rule] = all_rules[rule]
    
    # Add specific rules based on agent type
    if agent_type.lower() in ['research', 'deep_research_agent']:
        if 'research_rules' in all_rules:
            agent_rules['research_rules'] = all_rules['research_rules']
    
    elif agent_type.lower() in ['typography', 'em_dash', 'text_processing']:
        if 'typography_rules' in all_rules:
            agent_rules['typography_rules'] = all_rules['typography_rules']
        if 'em_dash_rules' in all_rules:
            agent_rules['em_dash_rules'] = all_rules['em_dash_rules']
    
    return agent_rules

__all__ = [
    'get_rule',
    'list_available_rules',
    'get_all_rules',
    'get_rule_summary',
    'get_rules_for_agent',
    'MODULE_DIR'
]