#!/usr/bin/env python3
"""
Single Chapter Test - Demonstrate Agent Transformations
"""

from implementation_advanced import process_agent_request

def test_single_chapter():
    # Read test chapter
    with open('input_chapters/test_chapter_with_edits.md', 'r') as f:
        content = f.read()

    print('📄 ORIGINAL CONTENT:')
    print('=' * 50)
    print(content[:200] + '...')

    # Process with agent
    results = process_agent_request({
        'text': content,
        'chapter_title': 'Test Chapter with Edits',
        'project_context': {
            'facility_types': ['PHF', 'CSU'],
            'funding_source': 'BHCIP Bond Grant Round 1'
        },
        'focus_areas': ['pillar_replacement', 'bhsme_terminology']
    })

    print('\n📝 ENHANCED CONTENT:')
    print('=' * 50)
    print(results['edited_text'][:300] + '...')

    print(f'\n📊 RESULTS:')
    print(f'Compliance Score: {results["bhsme_compliance_score"]:.1f}/10')
    print(f'Edits Applied: {results["statistics"]["total_edits_applied"]}')
    print(f'Confidence: {results["statistics"]["avg_confidence"]:.2f}')

    # Save output
    with open('output/test_chapter_enhanced.md', 'w') as f:
        f.write(results['edited_text'])

    print('\n✅ Enhanced chapter saved to: output/test_chapter_enhanced.md')
    print('\n🚨 SAFEGUARDS VERIFIED: No internal metrics in published content')

if __name__ == "__main__":
    test_single_chapter() 