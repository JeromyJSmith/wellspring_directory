#!/usr/bin/env python3
"""
Pilot Deployment Script for SME-Aware Editing Agent
==================================================

Systematically process diverse chapters with full safeguards and SME validation.
"""

import os
from implementation_advanced import process_agent_request

def run_pilot_deployment():
    """
    Execute pilot deployment on diverse chapter types following deployment checklist.
    """
    print("🚀 PILOT DEPLOYMENT - SME-AWARE EDITING AGENT v3.0.0")
    print("=" * 60)
    
    # Select diverse chapters for pilot testing
    chapters = [
        "sample_chapter_1.md",  # Regulatory-intensive
        "sample_chapter_2.md",  # Clinical-oriented  
        "sample_chapter_3.md"   # Community-focused
    ]
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    pilot_results = []
    
    for chapter_file in chapters:
        print(f"\n📄 PROCESSING: {chapter_file}")
        print("-" * 50)
        
        # Read input chapter
        input_path = f"input_chapters/{chapter_file}"
        if not os.path.exists(input_path):
            print(f"❌ ERROR: {input_path} not found")
            continue
            
        with open(input_path, "r") as f:
            content = f.read()
        
        # Process with enhanced agent
        results = process_agent_request({
            "text": content,
            "chapter_title": chapter_file.replace(".md", ""),
            "project_context": {
                "project_name": "Wellspring Book - Pilot Deployment",
                "facility_types": ["PHF", "CSU", "BHUC"],
                "funding_source": "BHCIP Bond Grant Round 1",
                "target_population": ["adults", "youth"],
                "region": "California"
            },
            "focus_areas": ["pillar_replacement", "bhsme_terminology", "passive_voice"]
        })
        
        # Save enhanced output
        enhanced_output_path = f"output/{chapter_file.replace('.md', '_enhanced.md')}"
        with open(enhanced_output_path, "w") as f_out:
            f_out.write(results['edited_text'])
        
        # Save processing report
        report_path = f"output/{chapter_file.replace('.md', '_report.md')}"
        with open(report_path, "w") as f_report:
            f_report.write(f"# Processing Report: {chapter_file}\n\n")
            f_report.write(f"**Compliance Score:** {results['bhsme_compliance_score']:.1f}/10\n\n")
            f_report.write(f"**Statistics:**\n")
            for key, value in results['statistics'].items():
                f_report.write(f"- {key}: {value}\n")
            f_report.write(f"\n**Changelog:**\n{results['changelog']}\n\n")
            f_report.write(f"**Recommendations:**\n")
            for rec in results['recommendations']:
                f_report.write(f"- {rec}\n")
        
        # Display results
        print(f"✅ PROCESSED: {chapter_file}")
        print(f"📊 Compliance Score: {results['bhsme_compliance_score']:.1f}/10")
        print(f"🔧 Edits Applied: {results['statistics']['total_edits_applied']}")
        print(f"🎯 Confidence: {results['statistics']['avg_confidence']:.2f}")
        
        # Check for SME review requirements
        if "SME Review Required" in results.get('changelog', ''):
            print("⚠️  SME REVIEW REQUIRED for regulatory precision")
        
        # Store pilot results
        pilot_results.append({
            "chapter": chapter_file,
            "compliance_score": results['bhsme_compliance_score'],
            "edits_applied": results['statistics']['total_edits_applied'],
            "confidence": results['statistics']['avg_confidence'],
            "output_path": enhanced_output_path,
            "report_path": report_path
        })
    
    # Generate pilot summary
    print(f"\n🎯 PILOT DEPLOYMENT SUMMARY")
    print("=" * 60)
    
    total_chapters = len(pilot_results)
    avg_compliance = sum(r['compliance_score'] for r in pilot_results) / total_chapters
    total_edits = sum(r['edits_applied'] for r in pilot_results)
    avg_confidence = sum(r['confidence'] for r in pilot_results) / total_chapters
    
    print(f"📊 Chapters Processed: {total_chapters}")
    print(f"📊 Average Compliance Score: {avg_compliance:.1f}/10")
    print(f"📊 Total Edits Applied: {total_edits}")
    print(f"📊 Average Confidence: {avg_confidence:.2f}")
    
    # Generate pilot deployment report
    summary_path = "output/pilot_deployment_summary.md"
    with open(summary_path, "w") as f_summary:
        f_summary.write("# Pilot Deployment Summary\n\n")
        f_summary.write("## Overall Results\n\n")
        f_summary.write(f"- **Chapters Processed:** {total_chapters}\n")
        f_summary.write(f"- **Average Compliance Score:** {avg_compliance:.1f}/10\n")
        f_summary.write(f"- **Total Edits Applied:** {total_edits}\n")
        f_summary.write(f"- **Average Confidence:** {avg_confidence:.2f}\n\n")
        f_summary.write("## Chapter Results\n\n")
        
        for result in pilot_results:
            f_summary.write(f"### {result['chapter']}\n")
            f_summary.write(f"- **Compliance Score:** {result['compliance_score']:.1f}/10\n")
            f_summary.write(f"- **Edits Applied:** {result['edits_applied']}\n")
            f_summary.write(f"- **Confidence:** {result['confidence']:.2f}\n")
            f_summary.write(f"- **Enhanced Output:** {result['output_path']}\n")
            f_summary.write(f"- **Processing Report:** {result['report_path']}\n\n")
        
        f_summary.write("## Next Steps\n\n")
        f_summary.write("1. **SME Review:** Conduct thorough SME validation of enhanced chapters\n")
        f_summary.write("2. **Regulatory Verification:** Confirm all edits maintain precise regulatory meanings\n")
        f_summary.write("3. **Quality Assurance:** Verify no internal metrics appear in published content\n")
        f_summary.write("4. **Full Deployment Authorization:** Proceed with full book deployment if validation successful\n")
    
    print(f"\n📋 Pilot summary saved to: {summary_path}")
    print(f"\n⚠️  CRITICAL NEXT STEP: SME VALIDATION REQUIRED")
    print(f"📝 Review all enhanced chapters and processing reports before full deployment")
    
    return pilot_results

if __name__ == "__main__":
    run_pilot_deployment() 