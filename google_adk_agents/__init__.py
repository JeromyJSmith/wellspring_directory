"""
Google ADK Agents Module

Advanced agent framework based on Google ADK documentation for 
specialized text processing, coordination, and workflow management.

Components:
- agents/: Core agent implementations (analyzer, processor, coordinator)
- tools/: Specialized tools and utilities for each agent
- config/: Configuration management and settings
- sessions/: Session persistence and state management

Available Agents:
- EmDashAnalyzer: Pattern recognition and context analysis
- EmDashProcessor: Replacement application and quality assurance  
- EmDashCoordinator: Workflow orchestration and coordination

Usage:
    from wellspring_directory.google_adk_agents import get_agents, get_tools
    
    # Get available agents
    agents = get_agents()
    
    # Get agent tools
    tools = get_tools()
"""

import os
from pathlib import Path
from typing import List, Dict, Any

# Module directory
MODULE_DIR = Path(__file__).parent

def get_agents() -> List[str]:
    """Get list of available ADK agents"""
    agents_dir = MODULE_DIR / "agents"
    if agents_dir.exists():
        return [f.stem for f in agents_dir.glob("*.py") if not f.name.startswith("__")]
    return []

def get_tools() -> List[str]:
    """Get list of available agent tools"""
    tools_dir = MODULE_DIR / "tools"
    if tools_dir.exists():
        return [f.stem for f in tools_dir.glob("*.py") if not f.name.startswith("__")]
    return []

def get_configs() -> List[str]:
    """Get list of configuration files"""
    config_dir = MODULE_DIR / "config"
    if config_dir.exists():
        return [f.name for f in config_dir.iterdir() if f.is_file()]
    return []

def get_sessions() -> List[str]:
    """Get list of session files"""
    sessions_dir = MODULE_DIR / "sessions"
    if sessions_dir.exists():
        return [f.name for f in sessions_dir.iterdir() if f.is_file()]
    return []

def get_main_scripts() -> List[str]:
    """Get main execution scripts"""
    scripts = []
    for script in ["main.py", "demo_adk_system.py"]:
        script_path = MODULE_DIR / script
        if script_path.exists():
            scripts.append(script)
    return scripts

def get_module_info() -> Dict[str, Any]:
    """Get module information and status"""
    return {
        "name": "google_adk_agents",
        "description": "Google ADK-based agent framework for text processing",
        "module_dir": str(MODULE_DIR),
        "available_agents": get_agents(),
        "available_tools": get_tools(),
        "config_count": len(get_configs()),
        "session_count": len(get_sessions()),
        "main_scripts": get_main_scripts()
    }

def list_agent_capabilities() -> Dict[str, str]:
    """List capabilities of each agent"""
    return {
        "em_dash_analyzer": "Pattern recognition, context analysis, confidence scoring",
        "em_dash_processor": "Text replacement, quality gates, validation",
        "em_dash_coordinator": "Workflow orchestration, session management, reporting"
    }

__all__ = [
    'get_agents',
    'get_tools',
    'get_configs',
    'get_sessions', 
    'get_main_scripts',
    'get_module_info',
    'list_agent_capabilities',
    'MODULE_DIR'
]