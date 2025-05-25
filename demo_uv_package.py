#!/usr/bin/env python3
"""
Demo: UV-Managed Wellspring Package with .cursor Access

This demo shows the complete package structure working with UV environment
management and full access to .cursor configurations and transcript data.
"""

import sys
from pathlib import Path

# Add parent directory for package import (when running from within project)
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

def demo_root_package():
    """Demo root package functionality"""
    print("🔧 Root Package Demo")
    print("=" * 40)
    
    import wellspring_directory as ws
    
    # Get project info
    info = ws.get_project_info()
    print(f"📚 Project: {info['name']} v{info['version']}")
    print(f"📁 Root directory: {info['root_dir']}")
    
    # Access MCP configuration
    mcp_servers = ws.get_mcp_servers()
    print(f"\n🔌 MCP Servers Available: {len(mcp_servers)}")
    for name in list(mcp_servers.keys())[:5]:  # Show first 5
        print(f"   - {name}")
    if len(mcp_servers) > 5:
        print(f"   ... and {len(mcp_servers) - 5} more")
    
    # Access cursor rules
    cursor_rules = ws.get_cursor_rules()
    print(f"\n📋 Cursor Rules Available: {len(cursor_rules)}")
    for rule_name in cursor_rules.keys():
        print(f"   - {rule_name}")
    
    # Access transcript data
    transcript = ws.get_transcript_data()
    if transcript:
        print(f"\n📝 Transcript loaded: {len(transcript):,} characters")
        # Show first line as sample
        first_line = transcript.split('\n')[0][:100]
        print(f"   Preview: \"{first_line}...\"")
    
    # List available agents
    agents = ws.list_available_agents()
    print(f"\n🤖 Agent Modules: {list(agents.keys())}")
    
    return True

def demo_module_access():
    """Demo accessing individual modules"""
    print("\n🧪 Module Access Demo")
    print("=" * 40)
    
    # Test em_dash_replacement
    from wellspring_directory.em_dash_replacement import get_module_info
    em_info = get_module_info()
    print(f"📝 Em Dash Module: {em_info['available_scripts']}")
    
    # Test deep_research_agent
    from wellspring_directory.deep_research_agent import get_module_info as get_research_info
    research_info = get_research_info()
    print(f"🔍 Research Module: {research_info['available_scripts']}")
    
    # Test google_adk_agents
    from wellspring_directory.google_adk_agents import get_module_info as get_adk_info, list_agent_capabilities
    adk_info = get_adk_info()
    print(f"🤖 ADK Agents: {adk_info['available_agents']}")
    
    capabilities = list_agent_capabilities()
    print("\n🎯 Agent Capabilities:")
    for agent, caps in capabilities.items():
        print(f"   {agent}: {caps}")
    
    # Test shared_utils
    from wellspring_directory.shared_utils import get_module_info as get_utils_info
    utils_info = get_utils_info()
    print(f"\n🛠️  Shared Utils: coordinator={utils_info['coordinator_available']}")
    
    return True

def demo_cursor_directory_access():
    """Demo direct access to .cursor directories"""
    print("\n📂 .cursor Directory Access Demo")
    print("=" * 40)
    
    # Test .cursor module access
    from wellspring_directory._cursor import get_mcp_config, get_all_rules
    
    mcp_config = get_mcp_config()
    print(f"🔌 MCP Config: {len(mcp_config)} top-level items")
    
    all_rules = get_all_rules()
    print(f"📋 All Rules: {len(all_rules)} rule files")
    
    # Test .cursor/rules access
    from wellspring_directory._cursor.rules import get_rule, list_available_rules, get_rule_summary
    
    available_rules = list_available_rules()
    print(f"\n📜 Available Rules: {available_rules}")
    
    # Get a specific rule
    agent_roles = get_rule('agent_roles')
    if agent_roles:
        print(f"\n👥 Agent Roles Rule: {len(agent_roles):,} characters")
        # Show first few lines
        lines = agent_roles.split('\n')[:3]
        for line in lines:
            if line.strip():
                print(f"   {line[:80]}...")
                break
    
    # Show rule summaries
    summaries = get_rule_summary()
    print(f"\n📖 Rule Summaries:")
    for rule, summary in list(summaries.items())[:3]:  # Show first 3
        print(f"   {rule}: {summary}")
    
    return True

def demo_uv_environment():
    """Demo UV environment information"""
    print("\n🌐 UV Environment Demo")
    print("=" * 40)
    
    import subprocess
    
    # Show UV version
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        print(f"📦 UV Version: {result.stdout.strip()}")
    except:
        print("📦 UV Version: Not available")
    
    # Show virtual environment info
    import os
    venv_path = os.environ.get('VIRTUAL_ENV', 'Not set')
    print(f"🔗 Virtual Environment: {venv_path}")
    
    # Show Python info
    print(f"🐍 Python Version: {sys.version.split()[0]}")
    print(f"📍 Python Path includes {len(sys.path)} directories")
    
    # Show installed package
    try:
        result = subprocess.run(['uv', 'pip', 'show', 'wellspring-book-production'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines[:3]:  # Show first 3 lines
                print(f"📋 {line}")
    except:
        print("📋 Package info not available")
    
    return True

def main():
    """Run complete demo"""
    print("🚀 Wellspring UV Package Demo")
    print("🎯 Demonstrating UV-managed package with .cursor access")
    print("=" * 60)
    
    demos = [
        demo_root_package,
        demo_module_access, 
        demo_cursor_directory_access,
        demo_uv_environment
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            return False
    
    print("\n" + "=" * 60)
    print("✨ All demos completed successfully!")
    print("🎉 Wellspring package is fully operational with UV and .cursor access!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)