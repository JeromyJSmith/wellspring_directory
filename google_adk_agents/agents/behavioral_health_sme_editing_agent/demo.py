#!/usr/bin/env python3
"""
Demo script for Behavioral Health SME-Aware Editing Agent
========================================================

Demonstrates the agent's capabilities with sample content and provides
easy testing interface for different chapter files.
"""

from implementation import process_agent_request
import json
from pathlib import Path

def demo_basic_functionality():
    """Demonstrate basic agent functionality with sample text."""
    print("=== BEHAVIORAL HEALTH SME EDITING AGENT DEMO ===\n")
    
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
    
    print("STATISTICS:")
    for key, value in result["statistics"].items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print(f"\nCOMPLIANCE SCORE: {result['bhsme_compliance_score']}/10")
    
    print("\nTOP RECOMMENDATIONS:")
    for i, rec in enumerate(result["recommendations"][:3], 1):
        print(f"  {i}. {rec}")
    
    return result

def process_chapter_file(file_path: str, chapter_title: str = None):
    """Process a specific chapter file."""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"Error: File '{file_path}' not found.")
        return None
    
    if not chapter_title:
        chapter_title = file_path.stem.replace('-', ' ').title()
    
    print(f"\n=== PROCESSING: {chapter_title} ===\n")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    input_data = {
        "text": text,
        "chapter_title": chapter_title
    }
    
    result = process_agent_request(input_data)
    
    # Save results
    output_dir = file_path.parent / "agent_results"
    output_dir.mkdir(exist_ok=True)
    
    # Save edited text
    edited_file = output_dir / f"{file_path.stem}_edited.md"
    with open(edited_file, 'w', encoding='utf-8') as f:
        f.write(result["edited_text"])
    
    # Save changelog
    changelog_file = output_dir / f"{file_path.stem}_changelog.md"
    with open(changelog_file, 'w', encoding='utf-8') as f:
        f.write(result["changelog"])
    
    # Save full results as JSON
    results_file = output_dir / f"{file_path.stem}_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    
    print(f"✅ Results saved to: {output_dir}")
    print(f"   - Edited text: {edited_file.name}")
    print(f"   - Changelog: {changelog_file.name}")
    print(f"   - Full results: {results_file.name}")
    
    print(f"\n📊 SUMMARY:")
    print(f"   Compliance Score: {result['bhsme_compliance_score']}/10")
    print(f"   Total Edits: {result['statistics']['total_edits_applied']}")
    print(f"   Readability Improvement: +{result['statistics']['readability_score_improvement']}")
    
    print(f"\n🔍 KEY FINDINGS:")
    stats = result['statistics']
    print(f"   - Pillar Replacements: {stats['total_pillar_replacements']}")
    print(f"   - Long Sentences: {stats['long_sentences_count']}")
    print(f"   - Passive Voice: {stats['passive_voice_instances']}")
    print(f"   - Vague Openers: {stats['vague_opener_instances']}")
    print(f"   - BHSME Improvements: {stats['bhsme_improvements']}")
    
    print(f"\n💡 TOP RECOMMENDATIONS:")
    for i, rec in enumerate(result["recommendations"][:3], 1):
        print(f"   {i}. {rec}")
    
    return result

def batch_process_chapters(chapters_dir: str):
    """Process all chapters in a directory."""
    chapters_dir = Path(chapters_dir)
    
    if not chapters_dir.exists():
        print(f"Error: Directory '{chapters_dir}' not found.")
        return
    
    # Find all chapter files
    chapter_files = list(chapters_dir.glob("New Wellspring-*-CH*.md"))
    
    if not chapter_files:
        print(f"No chapter files found in '{chapters_dir}'")
        return
    
    print(f"\n🔄 BATCH PROCESSING {len(chapter_files)} CHAPTERS\n")
    
    results_summary = []
    
    for chapter_file in sorted(chapter_files):
        try:
            result = process_chapter_file(chapter_file)
            if result:
                results_summary.append({
                    'file': chapter_file.name,
                    'compliance_score': result['bhsme_compliance_score'],
                    'total_edits': result['statistics']['total_edits_applied'],
                    'readability_improvement': result['statistics']['readability_score_improvement']
                })
            print("\n" + "-"*60 + "\n")
        except Exception as e:
            print(f"❌ Error processing {chapter_file.name}: {e}")
    
    # Print summary
    print("\n📈 BATCH PROCESSING SUMMARY:")
    print(f"{'File':<40} {'Score':<8} {'Edits':<8} {'Readability':<12}")
    print("-" * 70)
    
    for summary in results_summary:
        print(f"{summary['file']:<40} {summary['compliance_score']:<8} "
              f"{summary['total_edits']:<8} +{summary['readability_improvement']:<11}")
    
    if results_summary:
        avg_score = sum(s['compliance_score'] for s in results_summary) / len(results_summary)
        total_edits = sum(s['total_edits'] for s in results_summary)
        total_improvement = sum(s['readability_improvement'] for s in results_summary)
        
        print("-" * 70)
        print(f"{'AVERAGE/TOTAL':<40} {avg_score:<8.1f} {total_edits:<8} +{total_improvement:<11.1f}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python demo.py basic                    # Run basic demo")
        print("  python demo.py file <chapter.md>        # Process single file")
        print("  python demo.py batch <chapters_dir>     # Process all chapters in directory")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "basic":
        demo_basic_functionality()
    
    elif command == "file" and len(sys.argv) >= 3:
        file_path = sys.argv[2]
        chapter_title = sys.argv[3] if len(sys.argv) > 3 else None
        process_chapter_file(file_path, chapter_title)
    
    elif command == "batch" and len(sys.argv) >= 3:
        chapters_dir = sys.argv[2]
        batch_process_chapters(chapters_dir)
    
    else:
        print("Invalid command or missing arguments.")
        sys.exit(1)