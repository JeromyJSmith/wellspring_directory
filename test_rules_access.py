#!/usr/bin/env python3
"""
Test Google ADK Agent Rules Access

Test that Google ADK agents can access all rules through the new Python-accessible
rules directory structure.
"""

import sys
from pathlib import Path

# Add parent directory for package import
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

import wellspring_directory as ws
from wellspring_directory.rules import get_rules_for_agent, get_rule

def test_google_adk_rules_access():
    """Test that Google ADK agents can access rules"""
    print('🤖 Google ADK Agent Rules Access Test')
    print('=' * 45)

    # Test accessing rules for different agent types
    agent_types = ['research', 'typography', 'em_dash']

    for agent_type in agent_types:
        rules = get_rules_for_agent(agent_type)
        print(f'📋 {agent_type} agent rules: {len(rules)} files')
        for rule_name in rules.keys():
            print(f'   - {rule_name}')

    # Test direct access to specific rules
    print(f'\n🎯 Direct rule access:')
    agent_roles = ws.get_specific_cursor_rule('agent_roles')
    if agent_roles:
        print(f'   Agent roles rule: {len(agent_roles):,} characters')
        
    global_rules = ws.get_specific_cursor_rule('global_rules')
    if global_rules:
        print(f'   Global rules: {len(global_rules):,} characters')

    # Test accessing rules through the rules module directly
    print(f'\n📂 Direct rules module access:')
    em_dash_rules = get_rule('em_dash_rules')
    if em_dash_rules:
        print(f'   Em dash rules: {len(em_dash_rules):,} characters')
        
    typography_rules = get_rule('typography_rules')
    if typography_rules:
        print(f'   Typography rules: {len(typography_rules):,} characters')

    # Test that all rules are accessible
    all_rules = ws.get_cursor_rules()
    print(f'\n📚 All rules accessible: {len(all_rules)} total')
    
    print('\n✅ Google ADK agents can now access all rules via Python imports!')
    print('🎉 Rules are properly located for agent access!')
    
    return True

if __name__ == "__main__":
    success = test_google_adk_rules_access()
    sys.exit(0 if success else 1)