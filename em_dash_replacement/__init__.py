"""
Em Dash Replacement Module

Advanced typography correction system with contextual em dash replacement,
pattern recognition, and quality assurance for book production.

Components:
- scripts/: Core processing scripts and algorithms
- input/: Source documents for processing
- output/: Processed documents and results
- logs/: Processing logs and analytics
- changelog/: Version history and updates
- infographic_placeholders/: Visual content placeholders

Usage:
    from wellspring_directory.em_dash_replacement import get_scripts, get_logs
    
    # Access processing scripts
    scripts = get_scripts()
    
    # Get processing logs
    logs = get_logs()
"""

import os
from pathlib import Path
from typing import List, Dict, Any

# Module directory
MODULE_DIR = Path(__file__).parent

def get_scripts() -> List[str]:
    """Get list of available processing scripts"""
    scripts_dir = MODULE_DIR / "scripts"
    if scripts_dir.exists():
        return [f.name for f in scripts_dir.glob("*.py")]
    return []

def get_input_files() -> List[str]:
    """Get list of input files ready for processing"""
    input_dir = MODULE_DIR / "input"
    if input_dir.exists():
        return [f.name for f in input_dir.iterdir() if f.is_file()]
    return []

def get_output_files() -> List[str]:
    """Get list of processed output files"""
    output_dir = MODULE_DIR / "output"
    if output_dir.exists():
        return [f.name for f in output_dir.iterdir() if f.is_file()]
    return []

def get_logs() -> List[str]:
    """Get list of processing log files"""
    logs_dir = MODULE_DIR / "logs"
    if logs_dir.exists():
        return [f.name for f in logs_dir.glob("*.log")]
    return []

def get_changelog() -> List[str]:
    """Get changelog entries"""
    changelog_dir = MODULE_DIR / "changelog"
    if changelog_dir.exists():
        return [f.name for f in changelog_dir.iterdir() if f.is_file()]
    return []

def get_module_info() -> Dict[str, Any]:
    """Get module information and status"""
    return {
        "name": "em_dash_replacement",
        "description": "Typography correction and em dash replacement system",
        "module_dir": str(MODULE_DIR),
        "available_scripts": get_scripts(),
        "input_count": len(get_input_files()),
        "output_count": len(get_output_files()),
        "log_count": len(get_logs())
    }

__all__ = [
    'get_scripts',
    'get_input_files', 
    'get_output_files',
    'get_logs',
    'get_changelog',
    'get_module_info',
    'MODULE_DIR'
]