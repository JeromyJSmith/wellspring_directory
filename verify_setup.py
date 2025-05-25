#!/usr/bin/env python3
"""
Wellspring Setup Verification

Quick verification script to ensure the package structure is working correctly.
"""

import sys
import os
from pathlib import Path

def main():
    print("🔍 Wellspring Package Structure Verification")
    print("=" * 45)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check for key files
    key_files = [
        "pyproject.toml",
        "__init__.py", 
        "test_package_structure.py",
        ".cursor/mcp.json"
    ]
    
    print("📋 Checking key files:")
    all_present = True
    for file_path in key_files:
        full_path = current_dir / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - MISSING")
            all_present = False
    
    if not all_present:
        print("\n⚠️  Some required files are missing!")
        return False
    
    # Check Python version
    print(f"\n🐍 Python version: {sys.version}")
    
    # Check if virtual environment is active
    venv_active = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"🌐 Virtual environment active: {'✅ Yes' if venv_active else '❌ No'}")
    
    # Try basic import with parent directory added to Python path
    print("\n🧪 Testing basic import...")
    try:
        # Add parent directory to path to import the package correctly
        parent_dir = current_dir.parent
        if str(parent_dir) not in sys.path:
            sys.path.insert(0, str(parent_dir))
            print(f"   📍 Added {parent_dir} to Python path")
        
        # First check if __init__.py exists
        init_file = current_dir / "__init__.py"
        if not init_file.exists():
            print("   ❌ __init__.py not found in root directory")
            return False
            
        # Now try the import
        import wellspring_directory
        print("   ✅ wellspring_directory imported successfully")
        
        # Test a basic function
        config = wellspring_directory.get_cursor_config()
        print(f"   ✅ get_cursor_config() returned {len(config)} items")
        
        # Test accessing modules
        from wellspring_directory import em_dash_replacement
        print("   ✅ em_dash_replacement submodule imported successfully")
        
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        import traceback
        print(f"   📝 Full traceback: {traceback.format_exc()}")
        return False
    
    print("\n🎉 Basic verification complete!")
    print("🚀 Run 'python test_package_structure.py' for comprehensive testing")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)