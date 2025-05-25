"""
Cursor Configuration Module

This module provides access to Cursor-specific configurations including
MCP server settings, agent rules, and workflow coordination patterns.

Components:
- mcp.json: MCP server configurations
- rules/: Agent behavior rules and workflow patterns

Usage:
    from wellspring_directory._cursor import get_mcp_config, get_all_rules
    
    # Get MCP configuration
    mcp_config = get_mcp_config()
    
    # Get all cursor rules
    rules = get_all_rules()
"""

import json
from pathlib import Path
from typing import Dict, Any

MODULE_DIR = Path(__file__).parent

def get_mcp_config() -> Dict[str, Any]:
    """Get the MCP server configuration from mcp.json"""
    mcp_file = MODULE_DIR / "mcp.json"
    if mcp_file.exists():
        with open(mcp_file, 'r') as f:
            return json.load(f)
    return {}

def get_mcp_servers() -> Dict[str, Dict[str, Any]]:
    """Get just the MCP servers configuration"""
    config = get_mcp_config()
    return config.get('mcpServers', {})

def get_all_rules() -> Dict[str, str]:
    """Get content of all rule files"""
    rules_dir = MODULE_DIR / "rules"
    rules = {}
    
    if rules_dir.exists():
        for rule_file in rules_dir.glob("*.md"):
            try:
                with open(rule_file, 'r', encoding='utf-8') as f:
                    rules[rule_file.stem] = f.read()
            except Exception as e:
                rules[rule_file.stem] = f"Error reading file: {e}"
    
    return rules

__all__ = [
    'get_mcp_config',
    'get_mcp_servers',
    'get_all_rules',
    'MODULE_DIR'
]