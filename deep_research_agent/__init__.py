"""
Deep Research Agent Module

Advanced research automation system with citation management, 
fact verification, and visual opportunity identification.

Components:
- scripts/: Core research and analysis scripts
- citations/: Citation database and management
- extracted_statements/: Key statements and quotes
- reports/: Generated research reports
- logs/: Research session logs and analytics
- visual_opportunities/: Identified visual content opportunities

Usage:
    from wellspring_directory.deep_research_agent import get_citations, get_reports
    
    # Access citations database
    citations = get_citations()
    
    # Get research reports
    reports = get_reports()
"""

import os
from pathlib import Path
from typing import List, Dict, Any

# Module directory
MODULE_DIR = Path(__file__).parent

def get_scripts() -> List[str]:
    """Get list of available research scripts"""
    scripts_dir = MODULE_DIR / "scripts"
    if scripts_dir.exists():
        return [f.name for f in scripts_dir.glob("*.py")]
    return []

def get_citations() -> List[str]:
    """Get list of citation files"""
    citations_dir = MODULE_DIR / "citations"
    if citations_dir.exists():
        return [f.name for f in citations_dir.iterdir() if f.is_file()]
    return []

def get_extracted_statements() -> List[str]:
    """Get list of extracted statement files"""
    statements_dir = MODULE_DIR / "extracted_statements"
    if statements_dir.exists():
        return [f.name for f in statements_dir.iterdir() if f.is_file()]
    return []

def get_reports() -> List[str]:
    """Get list of research report files"""
    reports_dir = MODULE_DIR / "reports"
    if reports_dir.exists():
        return [f.name for f in reports_dir.iterdir() if f.is_file()]
    return []

def get_logs() -> List[str]:
    """Get list of research log files"""
    logs_dir = MODULE_DIR / "logs"
    if logs_dir.exists():
        return [f.name for f in logs_dir.glob("*.log")]
    return []

def get_visual_opportunities() -> List[str]:
    """Get list of visual opportunity files"""
    visual_dir = MODULE_DIR / "visual_opportunities"
    if visual_dir.exists():
        return [f.name for f in visual_dir.iterdir() if f.is_file()]
    return []

def get_module_info() -> Dict[str, Any]:
    """Get module information and status"""
    return {
        "name": "deep_research_agent",
        "description": "Advanced research automation and citation management",
        "module_dir": str(MODULE_DIR),
        "available_scripts": get_scripts(),
        "citation_count": len(get_citations()),
        "statement_count": len(get_extracted_statements()),
        "report_count": len(get_reports()),
        "visual_opportunity_count": len(get_visual_opportunities())
    }

__all__ = [
    'get_scripts',
    'get_citations',
    'get_extracted_statements', 
    'get_reports',
    'get_logs',
    'get_visual_opportunities',
    'get_module_info',
    'MODULE_DIR'
]