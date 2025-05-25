"""
Shared Utilities Module

Common utilities, database access, and coordination functions shared
across all Wellspring book production components.

Components:
- data/: Database files and data management
- notebooks/: Jupyter notebooks for analysis and exploration  
- uv_env/: UV environment configuration
- agent_coordinator.py: Cross-module agent coordination

Usage:
    from wellspring_directory.shared_utils import get_database_path, get_notebooks
    
    # Get database path
    db_path = get_database_path()
    
    # Get available notebooks
    notebooks = get_notebooks()
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# Module directory  
MODULE_DIR = Path(__file__).parent

def get_database_path() -> Optional[str]:
    """Get path to the Wellspring database"""
    db_path = MODULE_DIR / "data" / "wellspring.db"
    if db_path.exists():
        return str(db_path)
    return None

def get_notebooks() -> List[str]:
    """Get list of available Jupyter notebooks"""
    notebooks_dir = MODULE_DIR / "notebooks"
    if notebooks_dir.exists():
        return [f.name for f in notebooks_dir.glob("*.ipynb")]
    return []

def get_data_files() -> List[str]:
    """Get list of data files"""
    data_dir = MODULE_DIR / "data"
    if data_dir.exists():
        return [f.name for f in data_dir.iterdir() if f.is_file()]
    return []

def get_coordinator_available() -> bool:
    """Check if agent coordinator is available"""
    coordinator_path = MODULE_DIR / "agent_coordinator.py"
    return coordinator_path.exists()

def get_uv_env_status() -> Dict[str, Any]:
    """Get UV environment status and configuration"""
    uv_env_dir = MODULE_DIR / "uv_env"
    status = {
        "uv_env_exists": uv_env_dir.exists(),
        "uv_env_path": str(uv_env_dir) if uv_env_dir.exists() else None
    }
    
    if uv_env_dir.exists():
        venv_dir = uv_env_dir / ".venv"
        status["venv_exists"] = venv_dir.exists()
        status["venv_path"] = str(venv_dir) if venv_dir.exists() else None
    
    return status

def get_module_info() -> Dict[str, Any]:
    """Get module information and status"""
    return {
        "name": "shared_utils",
        "description": "Common utilities and database access for Wellspring system",
        "module_dir": str(MODULE_DIR),
        "database_available": get_database_path() is not None,
        "database_path": get_database_path(),
        "notebook_count": len(get_notebooks()),
        "data_file_count": len(get_data_files()),
        "coordinator_available": get_coordinator_available(),
        "uv_env_status": get_uv_env_status()
    }

__all__ = [
    'get_database_path',
    'get_notebooks',
    'get_data_files',
    'get_coordinator_available',
    'get_uv_env_status', 
    'get_module_info',
    'MODULE_DIR'
]