#!/usr/bin/env python3
"""
Test Package Structure

Comprehensive test script to verify all packages are importable 
and functions work correctly with UV environment.

Usage:
    python test_package_structure.py
"""

import sys
from pathlib import Path

def test_root_package():
    """Test root package import and functions"""
    print("🧪 Testing root package import...")
    
    try:
        import wellspring_directory as ws
        print("✅ Root package imported successfully")
        
        # Test root functions
        print("🔧 Testing root functions...")
        
        # Test cursor config
        cursor_config = ws.get_cursor_config()
        print(f"📄 Cursor config loaded: {len(cursor_config)} items")
        
        # Test MCP servers
        mcp_servers = ws.get_mcp_servers()
        print(f"🔌 MCP servers found: {len(mcp_servers)}")
        for server_name in list(mcp_servers.keys())[:3]:  # Show first 3
            print(f"   - {server_name}")
        
        # Test cursor rules
        cursor_rules = ws.get_cursor_rules()
        print(f"📋 Cursor rules loaded: {len(cursor_rules)} files")
        for rule_name in list(cursor_rules.keys())[:3]:  # Show first 3
            print(f"   - {rule_name}")
        
        # Test transcript
        transcript = ws.get_transcript_data()
        if transcript:
            print(f"📝 Transcript loaded: {len(transcript)} characters")
        else:
            print("📝 Transcript not found")
        
        # Test project info
        project_info = ws.get_project_info()
        print(f"ℹ️  Project: {project_info['name']} v{project_info['version']}")
        
        # Test available agents
        agents = ws.list_available_agents()
        print(f"🤖 Agent modules: {list(agents.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Root package test failed: {e}")
        return False

def test_em_dash_module():
    """Test em dash replacement module"""
    print("\n🧪 Testing em_dash_replacement module...")
    
    try:
        from wellspring_directory.em_dash_replacement import get_module_info, get_scripts
        print("✅ Em dash module imported successfully")
        
        info = get_module_info()
        print(f"📊 Module info: {info['name']}")
        print(f"   Scripts: {info['available_scripts']}")
        print(f"   Input files: {info['input_count']}")
        print(f"   Output files: {info['output_count']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Em dash module test failed: {e}")
        return False

def test_research_module():
    """Test deep research agent module"""
    print("\n🧪 Testing deep_research_agent module...")
    
    try:
        from wellspring_directory.deep_research_agent import get_module_info, get_reports
        print("✅ Research module imported successfully")
        
        info = get_module_info()
        print(f"📊 Module info: {info['name']}")
        print(f"   Scripts: {info['available_scripts']}")
        print(f"   Citations: {info['citation_count']}")
        print(f"   Reports: {info['report_count']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Research module test failed: {e}")
        return False

def test_adk_module():
    """Test Google ADK agents module"""
    print("\n🧪 Testing google_adk_agents module...")
    
    try:
        from wellspring_directory.google_adk_agents import get_module_info, list_agent_capabilities
        print("✅ ADK agents module imported successfully")
        
        info = get_module_info()
        print(f"📊 Module info: {info['name']}")
        print(f"   Agents: {info['available_agents']}")
        print(f"   Tools: {info['available_tools']}")
        
        capabilities = list_agent_capabilities()
        print("🎯 Agent capabilities:")
        for agent, caps in capabilities.items():
            print(f"   - {agent}: {caps}")
        
        return True
        
    except Exception as e:
        print(f"❌ ADK agents module test failed: {e}")
        return False

def test_shared_utils_module():
    """Test shared utilities module"""
    print("\n🧪 Testing shared_utils module...")
    
    try:
        from wellspring_directory.shared_utils import get_module_info, get_database_path
        print("✅ Shared utils module imported successfully")
        
        info = get_module_info()
        print(f"📊 Module info: {info['name']}")
        print(f"   Database available: {info['database_available']}")
        print(f"   Notebooks: {info['notebook_count']}")
        print(f"   Coordinator: {info['coordinator_available']}")
        
        db_path = get_database_path()
        if db_path:
            print(f"🗄️  Database path: {db_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Shared utils module test failed: {e}")
        return False

def test_submodule_imports():
    """Test importing submodules"""
    print("\n🧪 Testing submodule imports...")
    
    submodules = [
        "wellspring_directory.em_dash_replacement.scripts",
        "wellspring_directory.deep_research_agent.scripts", 
        "wellspring_directory.google_adk_agents.agents",
        "wellspring_directory.google_adk_agents.tools",
        "wellspring_directory.shared_utils.data"
    ]
    
    success_count = 0
    for module_name in submodules:
        try:
            __import__(module_name)
            print(f"✅ {module_name}")
            success_count += 1
        except Exception as e:
            print(f"❌ {module_name}: {e}")
    
    print(f"📈 Submodule import success: {success_count}/{len(submodules)}")
    return success_count == len(submodules)

def test_absolute_imports():
    """Test absolute imports from various contexts"""
    print("\n🧪 Testing absolute imports...")
    
    try:
        # Test importing from root
        from wellspring_directory import get_cursor_config
        from wellspring_directory.em_dash_replacement import get_scripts
        from wellspring_directory.google_adk_agents import get_agents
        
        print("✅ Absolute imports successful")
        return True
        
    except Exception as e:
        print(f"❌ Absolute imports failed: {e}")
        return False

def main():
    """Run all package structure tests"""
    print("🚀 Wellspring Package Structure Test Suite")
    print("=" * 50)
    
    # We need to add the parent directory to import the package correctly
    # since we're testing from within the package directory
    project_dir = Path(__file__).parent
    parent_dir = project_dir.parent
    
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))
        print(f"📍 Added {parent_dir} to Python path for testing")
    
    # Also ensure project dir is in path for relative imports
    if str(project_dir) not in sys.path:
        sys.path.insert(0, str(project_dir))
    
    tests = [
        test_root_package,
        test_em_dash_module,
        test_research_module,
        test_adk_module,
        test_shared_utils_module,
        test_submodule_imports,
        test_absolute_imports
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test_func.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All package structure tests passed!")
        print("✨ The Wellspring package is ready for import!")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)