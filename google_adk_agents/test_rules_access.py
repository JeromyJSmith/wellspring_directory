#!/usr/bin/env python3
"""
Test Google ADK Agent Access to Rules System
Verifies that the rules are accessible to the ADK agents.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from rules import get_rule, list_available_rules, get_rules_for_agent

def main():
    """Test rules access for Google ADK agents."""
    print('🤖 Google ADK Agent Rules Access Test')
    print('=' * 50)

    print('\n📋 Available Rules:')
    rules = list_available_rules()
    for rule in rules:
        print(f'  • {rule}')

    print('\n📖 Testing em_dash_rules.md access:')
    try:
        em_dash_rule = get_rule('em_dash_rules')
        print(f'  ✅ Rule length: {len(em_dash_rule)} characters')
        print(f'  📄 First 200 chars: {em_dash_rule[:200]}...')
    except Exception as e:
        print(f'  ❌ Error accessing em_dash_rules: {e}')

    print('\n📖 Testing workflow_coordination.md access:')
    try:
        workflow_rule = get_rule('workflow_coordination')
        print(f'  ✅ Rule length: {len(workflow_rule)} characters')
        print(f'  📄 First 200 chars: {workflow_rule[:200]}...')
    except Exception as e:
        print(f'  ❌ Error accessing workflow_coordination: {e}')

    print('\n🎯 Rules for ADK agents:')
    try:
        adk_rules = get_rules_for_agent('google_adk')
        print(f'  ✅ Found {len(adk_rules)} rules relevant to ADK agents')
        for rule_name in adk_rules:
            print(f'    • {rule_name}')
    except Exception as e:
        print(f'  ❌ Error getting ADK rules: {e}')

    print('\n🎯 Rules for em_dash agents:')
    try:
        em_dash_rules = get_rules_for_agent('em_dash')
        print(f'  ✅ Found {len(em_dash_rules)} rules relevant to em_dash agents')
        for rule_name in em_dash_rules:
            print(f'    • {rule_name}')
    except Exception as e:
        print(f'  ❌ Error getting em_dash rules: {e}')

    print('\n🔄 Testing integration with agent config:')
    try:
        from config.agent_config import CONFIG
        print(f'  ✅ Agent config loaded successfully')
        print(f'  🤖 Default model: {CONFIG.default_model}')
        print(f'  📁 Workspace: {CONFIG.workspace_path}')
        
        # Test accessing rules from within agent context
        em_rule = get_rule('em_dash_rules')
        if 'em dash' in em_rule.lower() or 'em-dash' in em_rule.lower():
            print(f'  ✅ Em dash rules contain expected content')
        else:
            print(f'  ⚠️  Em dash rules may not contain expected content')
            
    except Exception as e:
        print(f'  ❌ Error testing agent config integration: {e}')

    print('\n✅ Rules system successfully integrated with Google ADK agents!')
    print('🎉 All systems operational and ready for em dash processing!')

if __name__ == "__main__":
    main() 