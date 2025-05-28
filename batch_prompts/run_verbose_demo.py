#!/usr/bin/env python3
"""
Verbose Demo of Wellspring Batch Processing - ACTUAL SUBMISSION
================================================================

This script runs a real batch submission with detailed verbose output.
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

def print_header(title):
    print("\n" + "=" * 70)
    print(f"🚀 {title}")
    print("=" * 70)

def print_step(step_num, description):
    print(f"\n📋 STEP {step_num}: {description}")
    print("-" * 50)

def main():
    print_header("WELLSPRING OPENAI BATCH PROCESSING - LIVE SUBMISSION")
    
    print("🎯 This will submit your actual visual research prompts to OpenAI")
    print("⏱️  Time: 2-3 minutes for submission + up to 24 hours for processing")
    print("💰 Cost: ~$0.135 (50% savings vs real-time API)")
    print("📊 Processing: 9 prompts across 3 research sections")
    
    # Environment check
    print_step(1, "Environment Verification")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        return False
    
    print("✅ OPENAI_API_KEY configured")
    
    try:
        from openai_batch_processor import WellspringBatchProcessor
        print("✅ WellspringBatchProcessor ready")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Initialize
    print_step(2, "Initializing Batch Processor")
    
    try:
        processor = WellspringBatchProcessor()
        print("✅ Processor initialized")
        print("   Model: gpt-4o-mini | Temperature: 0.3 | Max tokens: 2000")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Load data
    print_step(3, "Loading Visual Research Prompts")
    
    input_file = "/Users/ojeromyo/Desktop/wellspring_directory/em_dash_replacement/changelog/visual_batch_prompts_20250526_171050.json"
    
    if not Path(input_file).exists():
        print(f"❌ File not found: {input_file}")
        return False
    
    print(f"📁 Loading: {Path(input_file).name}")
    
    try:
        batch_data = processor.load_visual_batch_prompts(input_file)
        prompt_sets = batch_data.get('batch_prompts', {}).get('prompt_sets', [])
        
        print("✅ Prompts loaded successfully!")
        print(f"   Opportunities: {batch_data.get('total_opportunities', 0)}")
        print(f"   Research sections: {len(prompt_sets)}")
        
        # Show sections
        for i, prompt_set in enumerate(prompt_sets, 1):
            section = prompt_set.get('section', f'Section {i}')
            prompts = prompt_set.get('research_prompts', {})
            print(f"     {i}. {section} ({len(prompts)} prompts)")
            
    except Exception as e:
        print(f"❌ Error loading: {e}")
        return False
    
    # Format tasks
    print_step(4, "Formatting for OpenAI Batch API")
    
    try:
        tasks = processor.format_prompts_for_batch_api(batch_data)
        print(f"✅ Created {len(tasks)} batch tasks")
        
        # Preview first few tasks
        print("📋 Task preview:")
        for i, task in enumerate(tasks[:3], 1):
            custom_id = task.get('custom_id', f'task_{i}')
            print(f"     {i}. {custom_id}")
        if len(tasks) > 3:
            print(f"     ... and {len(tasks) - 3} more tasks")
            
    except Exception as e:
        print(f"❌ Error formatting: {e}")
        return False
    
    # Create batch file
    print_step(5, "Creating Batch File")
    
    try:
        batch_file_path = processor.create_batch_file(tasks)
        file_size = Path(batch_file_path).stat().st_size
        print(f"✅ Batch file created: {Path(batch_file_path).name}")
        print(f"   Size: {file_size} bytes | Format: JSONL")
        
    except Exception as e:
        print(f"❌ Error creating file: {e}")
        return False
    
    # Upload
    print_step(6, "Uploading to OpenAI")
    
    print("☁️  Uploading file to OpenAI servers...")
    
    try:
        file_id = processor.upload_batch_file(batch_file_path)
        print(f"✅ Upload successful!")
        print(f"   File ID: {file_id}")
        
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False
    
    # Submit job
    print_step(7, "Submitting Batch Job")
    
    job_description = f"Wellspring Visual Research - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    print(f"📝 Description: {job_description}")
    print("🚀 Creating batch job...")
    
    try:
        batch_job = processor.create_batch_job(file_id, job_description)
        
        print("✅ BATCH JOB SUBMITTED SUCCESSFULLY!")
        print(f"   🆔 Job ID: {batch_job.id}")
        print(f"   📊 Status: {batch_job.status}")
        print(f"   🎯 Endpoint: {batch_job.endpoint}")
        print(f"   ⏰ Window: {batch_job.completion_window}")
        print(f"   📅 Created: {datetime.fromtimestamp(batch_job.created_at)}")
        
    except Exception as e:
        print(f"❌ Job creation error: {e}")
        return False
    
    # Save job info
    job_info = {
        "job_id": batch_job.id,
        "status": batch_job.status,
        "created_at": datetime.fromtimestamp(batch_job.created_at).isoformat(),
        "description": job_description,
        "file_id": file_id,
        "task_count": len(tasks),
        "input_file": input_file
    }
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    job_info_file = output_dir / "latest_job_info.json"
    
    with open(job_info_file, 'w') as f:
        json.dump(job_info, f, indent=2)
    
    print(f"💾 Job info saved to: {job_info_file}")
    
    # Monitoring info
    print_step(8, "Monitoring Your Job")
    
    print("🔍 Your job is now processing! Here's how to monitor:")
    print()
    print("   📊 Quick status check:")
    print(f"      python -c \"from openai_batch_processor import WellspringBatchProcessor; p=WellspringBatchProcessor(); s=p.get_batch_status('{batch_job.id}'); print(f'Status: {{s[\\\"status\\\"]}} | Created: {{s[\\\"created_at\\\"]}}'")
    print()
    print("   ⏳ Monitor until completion:")
    print(f"      python -c \"from openai_batch_processor import WellspringBatchProcessor; p=WellspringBatchProcessor(); p.monitor_batch_job('{batch_job.id}')\"")
    print()
    print("   📋 List all your jobs:")
    print("      python -c \"from openai_batch_processor import WellspringBatchProcessor; p=WellspringBatchProcessor(); [print(f'{j[\\\"id\\\"]}: {j[\\\"status\\\"]}') for j in p.list_batch_jobs()]\"")
    
    # Final summary
    print_header("JOB SUBMITTED - PROCESSING IN PROGRESS!")
    
    print("🎉 Your Wellspring visual research is now being processed by OpenAI!")
    print()
    print("📊 Job Summary:")
    print(f"   🆔 Job ID: {batch_job.id}")
    print(f"   📋 Tasks: {len(tasks)} prompts across {len(prompt_sets)} sections")
    print(f"   📊 Status: {batch_job.status}")
    print(f"   ⏱️  Expected completion: Within 24 hours")
    print(f"   💰 Cost: ~$0.135 (50% savings vs real-time)")
    print()
    print("🔔 What happens next:")
    print("   1. OpenAI will process your batch (up to 24 hours)")
    print("   2. You can check status using the commands above")
    print("   3. When complete, download results with:")
    print("      python example_usage.py (choose option 2)")
    print()
    print("📁 Results will be saved to:")
    print("   - output/batch_results_[timestamp].jsonl")
    print("   - output/processed_results_[timestamp].json")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 Batch job successfully submitted and processing!")
    else:
        print("\n❌ Submission failed. Check the output above.")