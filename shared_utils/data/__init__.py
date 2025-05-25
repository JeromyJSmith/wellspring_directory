"""
Shared Data Module

Database initialization and data management utilities.

Available Scripts:
- init_database.py: Database initialization and schema setup
"""

from pathlib import Path

MODULE_DIR = Path(__file__).parent

__all__ = ['MODULE_DIR']