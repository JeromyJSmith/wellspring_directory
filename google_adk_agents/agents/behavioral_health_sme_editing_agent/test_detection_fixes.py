#!/usr/bin/env python3
"""
Quick test to verify detection methods are working properly
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from implementation_advanced import AdvancedBehavioralHealthSMEAgent, ProjectContext

def test_chapter_1():
    """Test specifically Chapter 1 to see if we get the expected ~64 changes."""
    print("🧪 TESTING DETECTION METHODS ON CHAPTER 1")
    print("=" * 50)
    
    # Read Chapter 1
    chapter_file = Path("input_chapters/New Wellspring-20250503-CH1.md")
    if not chapter_file.exists():
        print(f"❌ Chapter file not found: {chapter_file}")
        return
    
    with open(chapter_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📄 Chapter 1 content length: {len(content):,} characters")
    print(f"📄 Word count: {len(content.split()):,} words")
    print()
    
    # Initialize agent
    agent = AdvancedBehavioralHealthSMEAgent(
        project_context=ProjectContext(
            project_name="Wellspring Behavioral Health Development Guide",
            region="California",
            facility_types=["behavioral_health", "mental_health", "substance_abuse"],
            target_population=["vulnerable_populations", "community_members"],
            funding_source="DHCS grants and private investment",
            compliance_requirements=["DHCS", "OSHPD", "ADA", "HIPAA"]
        )
    )
    
    # Test each detection method individually
    print("🔍 TESTING INDIVIDUAL DETECTION METHODS:")
    print()
    
    # Test pillar replacements
    print("1. Testing Pillar Replacements...")
    _, pillar_edits = agent._apply_pillar_replacements(content)
    print(f"   Found: {len(pillar_edits)} pillar replacement opportunities")
    if pillar_edits:
        for edit in pillar_edits[:3]:
            print(f"   Example: '{edit.original_text}' → '{edit.edited_text}'")
    print()
    
    # Test passive voice corrections
    print("2. Testing Passive Voice Corrections...")
    _, passive_edits = agent._apply_passive_voice_corrections(content)
    print(f"   Found: {len(passive_edits)} passive voice corrections")
    if passive_edits:
        for edit in passive_edits[:3]:
            print(f"   Example: '{edit.original_text}' → '{edit.edited_text}'")
    print()
    
    # Test sentence improvements
    print("3. Testing Sentence Improvements...")
    _, sentence_edits = agent._apply_sentence_improvements(content, 35)
    print(f"   Found: {len(sentence_edits)} long sentences to improve")
    if sentence_edits:
        for edit in sentence_edits[:2]:
            print(f"   Example: '{edit.original_text[:60]}...' → '{edit.edited_text[:60]}...'")
    print()
    
    # Test vague opener corrections
    print("4. Testing Vague Opener Corrections...")
    _, vague_edits = agent._apply_vague_opener_corrections(content)
    print(f"   Found: {len(vague_edits)} vague opener corrections")
    if vague_edits:
        for edit in vague_edits[:3]:
            print(f"   Example: '{edit.original_text}' → '{edit.edited_text}'")
    print()
    
    # Test BHSME terminology
    print("5. Testing BHSME Terminology...")
    _, terminology_edits = agent._apply_bhsme_terminology(content)
    print(f"   Found: {len(terminology_edits)} terminology improvements")
    if terminology_edits:
        for edit in terminology_edits[:3]:
            print(f"   Example: '{edit.original_text}' → '{edit.edited_text}'")
    print()
    
    # Calculate totals
    total_individual = len(pillar_edits) + len(passive_edits) + len(sentence_edits) + len(vague_edits) + len(terminology_edits)
    
    print("📊 INDIVIDUAL METHOD TOTALS:")
    print(f"   Pillar Replacements: {len(pillar_edits)}")
    print(f"   Passive Voice: {len(passive_edits)}")
    print(f"   Sentence Improvements: {len(sentence_edits)}")
    print(f"   Vague Opener Corrections: {len(vague_edits)}")
    print(f"   BHSME Terminology: {len(terminology_edits)}")
    print(f"   TOTAL: {total_individual}")
    print()
    
    # Now test full agent processing
    print("🔄 TESTING FULL AGENT PROCESSING:")
    input_data = {
        'text': content,
        'chapter_title': 'Chapter 1',
        'max_sentence_length': 35,
        'focus_areas': ['pillar_replacement', 'long_sentences', 'passive_voice', 'vague_openers', 'bhsme_terminology'],
        'enable_stakeholder_validation': True
    }
    
    result = agent.process_request(input_data)
    
    print(f"   Agent edits made: {len(agent.edits_made)}")
    print(f"   Compliance score: {result.get('bhsme_compliance_score', 0.0):.1f}/10.0")
    print(f"   Validation failed: {result.get('validation_failed', False)}")
    
    if agent.edits_made:
        edit_breakdown = {}
        for edit in agent.edits_made:
            edit_type = getattr(edit, 'edit_type', 'UNKNOWN')
            edit_breakdown[edit_type] = edit_breakdown.get(edit_type, 0) + 1
        print(f"   Edit breakdown: {edit_breakdown}")
    
    print()
    print("🎯 EXPECTED vs ACTUAL:")
    print(f"   Expected: ~64 changes (from your initial analysis)")
    print(f"   Individual methods total: {total_individual}")
    print(f"   Full agent processing: {len(agent.edits_made)}")
    
    if total_individual > 40:
        print("   ✅ GOOD: Individual methods finding substantial changes")
    else:
        print("   ⚠️  WARNING: Individual methods finding fewer changes than expected")
    
    if len(agent.edits_made) > 40:
        print("   ✅ SUCCESS: Full agent processing finding substantial changes")
    else:
        print("   ❌ ISSUE: Full agent processing not finding enough changes")

if __name__ == "__main__":
    test_chapter_1() 