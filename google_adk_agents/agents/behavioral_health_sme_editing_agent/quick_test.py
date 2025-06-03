#!/usr/bin/env python3
"""
Quick Test - Show BHSME Agent transformations on DHCS content
"""

from implementation_advanced import process_agent_request

def quick_test():
    print("🌟 BHSME AGENT - QUICK TRANSFORMATION TEST")
    print("=" * 50)
    
    # Test chapters
    chapters = [
        {
            "title": "Chapter 1: Behavioral Health Transformation",
            "content": "The first pillar of behavioral health transformation was established through Proposition 1. This initiative is designed to improve accountability and increase transparency."
        },
        {
            "title": "Chapter 2: BHIBA Implementation", 
            "content": "The BHIBA portion represents a $6.38 billion general obligation bond to develop an array of behavioral health treatment facilities. These facilities will include residential care settings."
        },
        {
            "title": "Chapter 3: BHCIP Guiding Principles",
            "content": "The BHCIP program is guided by several key principles that are designed to address urgent needs. A major priority is to invest in behavioral health and community care options."
        }
    ]
    
    for i, chapter in enumerate(chapters, 1):
        print(f"\n📄 CHAPTER {i}: {chapter['title']}")
        print("-" * 60)
        
        # Process with BHCIP context
        project_context = {
            "project_name": "BHCIP Bond Round 1 Application",
            "facility_types": ["PHF", "CSU", "BHUC"],
            "funding_source": "BHCIP Bond Grant Round 1"
        }
        
        results = process_agent_request({
            "text": chapter['content'],
            "chapter_title": chapter['title'],
            "project_context": project_context,
            "focus_areas": ["pillar_replacement", "bhsme_terminology"]
        })
        
        print(f"📝 ORIGINAL: {chapter['content']}")
        print()
        print(f"✅ ENHANCED: {results['edited_text']}")
        print()
        print(f"📊 EDITS: {results['statistics']['total_edits_applied']} | " + 
              f"CONFIDENCE: {results['statistics']['avg_confidence']:.2f} | " +
              f"SCORE: {results['bhsme_compliance_score']:.1f}/10")
        
        if results['statistics']['total_edits_applied'] > 0:
            print(f"🔧 CHANGES: {results['changelog'].strip()}")

if __name__ == "__main__":
    quick_test() 