"""
Wellspring Book Production System - Root Package

A comprehensive AI-assisted book production system for "The Wellspring Manual"
with em dash processing, deep research agents, and Google ADK integration.

This package provides:
- Em dash replacement and typography correction
- Deep research and citation management  
- Google ADK agent framework
- MCP server integration and .cursor rules access
- Shared utilities and database management

Main Components:
- em_dash_replacement: Typography and text processing
- deep_research_agent: Research and citation tools
- google_adk_agents: Google ADK-based agent framework
- shared_utils: Common utilities and database access

Usage:
    >>> import wellspring_directory as ws
    >>> config = ws.get_cursor_config()
    >>> transcript = ws.get_transcript_data()
    >>> rules = ws.get_cursor_rules()
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

__version__ = "1.0.0"
__author__ = "Brian V Jones & BHSME Team"
__email__ = "contact@bhsme.org"

# Package root directory
ROOT_DIR = Path(__file__).parent.absolute()
CURSOR_DIR = ROOT_DIR / ".cursor"
DOCS_DIR = ROOT_DIR / "docs"
RULES_DIR = ROOT_DIR / "rules"

def get_cursor_config() -> Dict[str, Any]:
    """
    Get the complete .cursor/mcp.json configuration
    
    Returns:
        Dict containing all MCP server configurations
    """
    mcp_file = CURSOR_DIR / "mcp.json"
    if mcp_file.exists():
        with open(mcp_file, 'r') as f:
            return json.load(f)
    return {}

def get_mcp_servers() -> Dict[str, Dict[str, Any]]:
    """
    Get just the MCP servers section from .cursor/mcp.json
    
    Returns:
        Dict of MCP server configurations
    """
    config = get_cursor_config()
    return config.get('mcpServers', {})

def get_cursor_rules() -> Dict[str, str]:
    """
    Get all agent rules files content (now from rules/ directory)
    
    Returns:
        Dict mapping rule file names to their content
    """
    rules = {}
    
    if RULES_DIR.exists():
        for rule_file in RULES_DIR.glob("*.md"):
            try:
                with open(rule_file, 'r', encoding='utf-8') as f:
                    rules[rule_file.stem] = f.read()
            except Exception as e:
                rules[rule_file.stem] = f"Error reading file: {e}"
    
    return rules

def get_transcript_data() -> Optional[str]:
    """
    Get the Wellspring Manuscript Editing Meeting transcript content
    
    Returns:
        String content of the transcript or None if not found
    """
    transcript_path = DOCS_DIR / "Wellspring Manuscript Editing Meeting_otter_ai" / "Wellspring Manuscript Editing Meeting.txt"
    
    if transcript_path.exists():
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading transcript: {e}"
    
    return None

def get_project_info() -> Dict[str, Any]:
    """
    Get project information from pyproject.toml
    
    Returns:
        Dict containing project metadata
    """
    info = {
        "name": "wellspring-book-production",
        "version": "1.0.0",
        "description": "AI-assisted book production system for The Wellspring Manual",
        "root_dir": str(ROOT_DIR),
        "cursor_dir": str(CURSOR_DIR),
        "docs_dir": str(DOCS_DIR),
        "rules_dir": str(RULES_DIR)
    }
    return info

def list_available_agents() -> Dict[str, List[str]]:
    """
    List all available agents across different modules
    
    Returns:
        Dict mapping module names to lists of available agents
    """
    agents = {
        "google_adk_agents": [],
        "em_dash_replacement": [],
        "deep_research_agent": []
    }
    
    # Check google_adk_agents
    adk_agents_dir = ROOT_DIR / "google_adk_agents" / "agents"
    if adk_agents_dir.exists():
        agents["google_adk_agents"] = [f.stem for f in adk_agents_dir.glob("*.py") if not f.name.startswith("__")]
    
    # Check other agent directories
    for module in ["em_dash_replacement", "deep_research_agent"]:
        module_dir = ROOT_DIR / module / "scripts"
        if module_dir.exists():
            agents[module] = [f.stem for f in module_dir.glob("*.py") if not f.name.startswith("__")]
    
    return agents

def get_specific_cursor_rule(rule_name: str) -> Optional[str]:
    """
    Get content of a specific agent rule file
    
    Args:
        rule_name: Name of the rule file (without .md extension)
        
    Returns:
        String content of the rule file or None if not found
    """
    rule_file = RULES_DIR / f"{rule_name}.md"
    if rule_file.exists():
        try:
            with open(rule_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading {rule_name}: {e}"
    return None

def list_cursor_rules() -> List[str]:
    """
    List all available agent rule file names
    
    Returns:
        List of rule file names (without .md extension)
    """
    if RULES_DIR.exists():
        return [f.stem for f in RULES_DIR.glob("*.md")]
    return []

# Make key functions available at package level
__all__ = [
    'get_cursor_config',
    'get_mcp_servers', 
    'get_cursor_rules',
    'get_specific_cursor_rule',
    'list_cursor_rules',
    'get_transcript_data',
    'get_project_info',
    'list_available_agents',
    'ROOT_DIR',
    'CURSOR_DIR',
    'DOCS_DIR',
    'RULES_DIR'
]