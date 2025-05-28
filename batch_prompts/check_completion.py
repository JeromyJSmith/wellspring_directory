#!/usr/bin/env python3
"""
Check if your batch job is complete and process results
"""

from openai_batch_processor import WellspringBatchProcessor
from datetime import datetime
import json

def check_and_process():
    job_id = 'batch_683506cc77cc8190b47611aeff3f7024'
    
    print("🔍 Checking batch job completion...")
    print(f"Job ID: {job_id}")
    print()
    
    try:
        p = WellspringBatchProcessor()
        job = p.client.batches.retrieve(job_id)
        
        print(f"📊 Status: {job.status}")
        
        if hasattr(job, 'request_counts') and job.request_counts:
            counts = job.request_counts.__dict__
            completed = counts.get('completed', 0)
            total = counts.get('total', 0)
            failed = counts.get('failed', 0)
            progress = (completed / total * 100) if total > 0 else 0
            
            print(f"📈 Progress: {completed}/{total} ({progress:.1f}%)")
            print(f"✅ Completed: {completed}")
            print(f"❌ Failed: {failed}")
        
        if job.status == "completed":
            print()
            print("🎉 JOB COMPLETED! Processing results...")
            
            # Download and process results
            results_file = p.download_results(job)
            processed_results = p.process_results(results_file)
            
            print(f"✅ Results processed successfully!")
            print(f"📊 Total results: {processed_results['total_results']}")
            print(f"📁 Sections: {list(processed_results['results_by_section'].keys())}")
            
            # Show sample results
            print()
            print("📋 SAMPLE RESULTS:")
            for section, prompts in processed_results['results_by_section'].items():
                print(f"\n🔹 {section}:")
                for prompt_type, result in prompts.items():
                    response_preview = result['response'][:150] + "..." if len(result['response']) > 150 else result['response']
                    print(f"   • {prompt_type}: {response_preview}")
            
            print()
            print("🎯 NEXT STEPS:")
            print("   • Review full results in output/ directory")
            print("   • Use the insights for your Wellspring Manual")
            print("   • Run more batch jobs for additional research!")
            
        elif job.status in ["failed", "expired", "cancelled"]:
            print(f"❌ Job {job.status}. Check logs for details.")
            
        else:
            print(f"⏳ Job still {job.status}. Check again later.")
            print("💡 Tip: Run this script periodically to check completion")
        
    except Exception as e:
        print(f"❌ Error checking job: {e}")

if __name__ == "__main__":
    check_and_process()