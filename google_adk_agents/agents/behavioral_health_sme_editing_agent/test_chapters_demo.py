#!/usr/bin/env python3
"""
Test Chapters Demo Script
Demonstrates the Advanced BHSME Agent on real DHCS/BHCIP content
"""

from implementation_advanced import process_agent_request
import re

def extract_chapters_from_file(filename):
    """Extract individual chapters from the test file."""
    with open(filename, 'r') as f:
        content = f.read()
    
    print(f"📖 File content length: {len(content)} characters")
    
    # Split by chapter headers
    chapters = re.split(r'\n## (Chapter \d+:[^#\n]+)', content)
    print(f"🔍 Split result: {len(chapters)} parts")
    
    # Debug: print first few parts
    for i, part in enumerate(chapters[:5]):
        print(f"   Part {i}: '{part[:50]}...'")
    
    chapter_data = []
    for i in range(1, len(chapters), 2):
        if i + 1 < len(chapters):
            title = chapters[i].strip()
            content = chapters[i + 1].strip()
            chapter_data.append({"title": title, "content": content})
            print(f"✅ Found chapter: '{title}' ({len(content)} chars)")
    
    return chapter_data

def process_chapter_with_context(chapter_title, chapter_content):
    """Process a chapter with BHCIP-specific context."""
    
    # Configure BHCIP project context
    project_context = {
        "project_name": "BHCIP Bond Round 1 Application",
        "region": "California Statewide",
        "facility_types": ["PHF", "CSU", "BHUC", "STRTP"],
        "target_population": ["adults", "youth", "veterans", "vulnerable_populations"],
        "funding_source": "BHCIP Bond Grant Round 1",
        "compliance_requirements": ["DHCS", "OSHPD", "Title 22", "BHIBA"]
    }
    
    input_data = {
        "text": chapter_content,
        "chapter_title": chapter_title,
        "project_context": project_context,
        "enable_stakeholder_validation": True,
        "focus_areas": ["pillar_replacement", "bhsme_terminology", "passive_voice", "vague_openers", "long_sentences"]
    }
    
    return process_agent_request(input_data)

def display_results(chapter_title, original_text, results):
    """Display formatted before/after results."""
    
    print(f"\n{'='*80}")
    print(f"📄 CHAPTER: {chapter_title}")
    print(f"{'='*80}")
    
    print(f"\n📝 ORIGINAL TEXT ({len(original_text.split())} words):")
    print("-" * 50)
    print(original_text)
    
    print(f"\n✅ ENHANCED TEXT ({len(results['edited_text'].split())} words):")
    print("-" * 50)
    print(results['edited_text'])
    
    print(f"\n📊 TRANSFORMATION SUMMARY:")
    print("-" * 30)
    stats = results['statistics']
    print(f"🎯 Total Edits Applied: {stats['total_edits_applied']}")
    print(f"📈 Average Confidence: {stats['avg_confidence']:.2f}")
    print(f"🏆 High Confidence Edits: {stats['high_confidence_edits']}")
    print(f"📋 DHCS References Added: {stats.get('dhcs_references_added', 0)}")
    print(f"📚 Readability Improvement: +{stats.get('readability_improvement', 0):.1f}%")
    print(f"🎖️ BHSME Compliance Score: {results['bhsme_compliance_score']:.1f}/10")
    
    if results['statistics']['total_edits_applied'] > 0:
        print(f"\n📝 DETAILED CHANGES:")
        print("-" * 20)
        changelog_lines = results['changelog'].split('\n')
        for line in changelog_lines:
            if line.strip() and ('→' in line or 'EDIT' in line):
                print(f"   {line.strip()}")
    
    print(f"\n💡 STRATEGIC RECOMMENDATIONS:")
    print("-" * 30)
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"{i}. {rec}")
    
    # Display compliance dashboard
    if 'compliance_dashboard' in results:
        print(f"\n📊 COMPLIANCE DASHBOARD:")
        print("-" * 25)
        for metric in results['compliance_dashboard']:
            status_emoji = "🟢" if metric['status'] == 'excellent' else "🟡" if metric['status'] == 'good' else "🟠"
            print(f"{status_emoji} {metric['metric_name']}: {metric['current_score']:.1f}/{metric['target_score']}")
            if metric['status'] == 'needs_improvement':
                print(f"   → Action: {metric['improvement_actions'][0]}")
    
    # Display actionable checklist
    if 'actionable_checklist' in results and results['actionable_checklist']:
        print(f"\n✅ ACTIONABLE CHECKLIST:")
        print("-" * 22)
        for item in results['actionable_checklist']:
            print(f"   □ {item}")

def main():
    """Main demo function."""
    
    print("🌟 BHSME AGENT - DHCS/BHCIP CHAPTER TESTING DEMO")
    print("=" * 60)
    print("Testing the Advanced BHSME Agent on real DHCS content")
    print("Demonstrating BHCIP-specific enhancements and compliance")
    print()
    
    # Define test chapters directly in code
    chapters = [
        {
            "title": "Chapter 1: Behavioral Health Transformation Overview",
            "content": """The first pillar of behavioral health transformation was established through Proposition 1. In March 2024, California voters passed Proposition 1, which was a two-bill package that aims to modernize the state's behavioral health care system. This initiative is designed to improve accountability and increase transparency. It also seeks to expand the capacity of behavioral health care facilities for Californians.

The initiative consists of the Behavioral Health Services Act (SB 326) and the Behavioral Health Infrastructure Bond Act of 2024 (BHIBA) (AB 531). The first component focuses on reforming behavioral health care funding to provide services to those with the most serious mental illnesses and treat substance use disorders. Additionally, it aims to expand the behavioral health workforce to reflect and connect with California's diverse population.

There is a critical need to focus on outcomes, accountability, and equity. This comprehensive approach involves funding behavioral health treatment beds, supportive housing, and community sites. The legislation also directs funding for housing for veterans with behavioral health needs, which is an important component of the overall strategy."""
        },
        {
            "title": "Chapter 2: BHIBA Implementation and DHCS Authority", 
            "content": """The BHIBA portion represents a $6.38 billion general obligation bond to develop an array of behavioral health treatment facilities. These facilities will include residential care settings and supportive housing to help provide appropriate care facilities for individuals experiencing mental health and substance use disorders.

DHCS was authorized to award up to $4.4 billion in BHIBA funds for BHCIP competitive grants. These grants are intended to expand behavioral health facility infrastructure. Of these funds, $1.5 billion will be awarded only to counties, cities, and tribal entities. Additionally, $30 million has been set aside specifically for tribal entities.

The department released a comprehensive needs assessment on January 10, 2022. This needs assessment was designed to provide data and stakeholder perspectives for DHCS as it implements major behavioral health initiatives. The assessment focuses on expanding the behavioral health infrastructure through BHCIP and is titled "Assessing the Continuum of Care for Behavioral Health Services in California." """
        },
        {
            "title": "Chapter 3: BHCIP Guiding Principles and Priority Framework",
            "content": """The BHCIP program is guided by several key principles that are designed to address urgent needs in the care continuum. These principles focus on people with mental health or substance use conditions, including unhoused people, veterans, older adults, adults with disabilities, and children and youth.

A major priority is to invest in behavioral health and community care options that advance health equity. This involves increasing options across the life span that serve as an alternative to incarceration, hospitalization, homelessness, and institutionalization.

The program seeks to meet the needs of vulnerable populations with the greatest barriers to access. This includes people experiencing unsheltered homelessness and justice involvement. It is important to ensure that care can be provided in the least restrictive settings to support community integration, choice, and autonomy.

The initiative aims to leverage county and Medi-Cal investments to support ongoing sustainability. Additionally, it leverages the historic state investments in housing and homelessness to create a comprehensive approach to behavioral health care infrastructure development."""
        }
    ]
    
    try:        
        print(f"📚 Processing {len(chapters)} test chapters")
        
        # Process each chapter
        for i, chapter in enumerate(chapters, 1):
            print(f"\n🔄 Processing Chapter {i}/{len(chapters)}...")
            
            results = process_chapter_with_context(
                chapter['title'], 
                chapter['content']
            )
            
            display_results(
                chapter['title'],
                chapter['content'], 
                results
            )
            
            # Brief pause between chapters for readability
            if i < len(chapters):
                print(f"\n⏸️  Press Enter to continue to next chapter...")
                input()
    
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()

    print(f"\n🎉 CHAPTER TESTING DEMO COMPLETED")
    print("=" * 40)
    print("Key observations:")
    print("✅ DHCS terminology standardization") 
    print("✅ Architectural language improvements")
    print("✅ Passive voice corrections")
    print("✅ Enhanced professional authority")
    print("✅ BHCIP compliance alignment")

if __name__ == "__main__":
    main() 