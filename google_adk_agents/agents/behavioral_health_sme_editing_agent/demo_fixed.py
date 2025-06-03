#!/usr/bin/env python3
"""
Demo script for FIXED Behavioral Health SME-Aware Editing Agent
===============================================================

Demonstrates the ENHANCED agent's capabilities with sample content and provides
easy testing interface for different chapter files.
"""

from implementation_fixed import process_agent_request
import json
from pathlib import Path

def demo_basic_functionality():
    """Demonstrate FIXED agent functionality with sample text."""
    print("=== FIXED BEHAVIORAL HEALTH SME EDITING AGENT DEMO ===\n")
    
    sample_text = """
    The first pillar of behavioral health real estate development is needs validation. 
    It is critical that projects are designed by teams who understand the complexities 
    that are involved in this specialized field of work. There are many factors that 
    must be considered when developing psychiatric health facilities and crisis 
    stabilization units. The mental health services act provides funding that can be 
    leveraged for these important community assets.
    """
    
    print("ORIGINAL TEXT:")
    print(sample_text)
    print("\n" + "="*60 + "\n")
    
    # Process the text
    input_data = {
        "text": sample_text,
        "chapter_title": "Demo Sample",
        "max_sentence_length": 25
    }
    
    result = process_agent_request(input_data)
    
    print("EDITED TEXT:")
    print(result["edited_text"])
    print("\n" + "="*60 + "\n")
    
    print("ENHANCED STATISTICS:")
    for key, value in result["statistics"].items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print(f"\nCOMPLIANCE SCORE: {result['bhsme_compliance_score']}/10")
    
    print("\nTOP RECOMMENDATIONS:")
    for i, rec in enumerate(result["recommendations"][:3], 1):
        print(f"  {i}. {rec}")
    
    print("\nCONCRETE IMPROVEMENTS MADE:")
    print(f"  - Total Edits Applied: {result['statistics']['total_edits_applied']}")
    print(f"  - DHCS References Added: {result['statistics']['dhcs_references_added']}")
    print(f"  - Concrete Rewrites: {result['statistics']['concrete_rewrites_provided']}")
    print(f"  - Readability Improvement: +{result['statistics']['readability_score_improvement']}")
    
    return result

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python demo_fixed.py basic                    # Run basic demo with FIXED agent")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "basic":
        demo_basic_functionality()
    else:
        print("Invalid command. Use 'basic' for demonstration.")
        sys.exit(1)