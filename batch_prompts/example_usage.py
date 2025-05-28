#!/usr/bin/env python3
"""
Wellspring Batch Processing Usage Examples
=========================================

This script demonstrates how to use the OpenAI Batch Processing system
with the Wellspring visual batch prompts.

Author: BHSME Team
Version: 1.0.0
"""

import os
import json
import time
from pathlib import Path
import requests

# Import our batch processor
try:
    from openai_batch_processor import WellspringBatchProcessor
    PROCESSOR_AVAILABLE = True
except ImportError:
    print("❌ Batch processor not available. Run setup_batch_processing.sh first.")
    PROCESSOR_AVAILABLE = False


def example_1_direct_processing():
    """
    Example 1: Direct batch processing using the WellspringBatchProcessor class
    """
    print("🚀 Example 1: Direct Batch Processing")
    print("=" * 50)
    
    if not PROCESSOR_AVAILABLE:
        print("❌ Batch processor not available")
        return
    
    # Path to your visual batch prompts file
    input_file = "/Users/ojeromyo/Desktop/wellspring_directory/em_dash_replacement/changelog/visual_batch_prompts_20250526_171050.json"
    
    if not Path(input_file).exists():
        print(f"❌ Input file not found: {input_file}")
        return
    
    try:
        # Initialize the processor
        processor = WellspringBatchProcessor()
        
        # Load the visual batch prompts
        print("📄 Loading visual batch prompts...")
        batch_data = processor.load_visual_batch_prompts(input_file)
        print(f"✅ Loaded {batch_data.get('total_opportunities', 0)} visual opportunities")
        
        # Format prompts for batch API
        print("🔄 Formatting prompts for OpenAI Batch API...")
        tasks = processor.format_prompts_for_batch_api(batch_data)
        print(f"✅ Created {len(tasks)} batch tasks")
        
        if len(tasks) == 0:
            print("❌ No valid tasks found")
            return
        
        # Create batch file
        print("📁 Creating batch file...")
        batch_file_path = processor.create_batch_file(tasks)
        print(f"✅ Batch file created: {batch_file_path}")
        
        # Upload to OpenAI
        print("☁️  Uploading to OpenAI...")
        file_id = processor.upload_batch_file(batch_file_path)
        print(f"✅ File uploaded with ID: {file_id}")
        
        # Create batch job
        print("🚀 Creating batch job...")
        batch_job = processor.create_batch_job(file_id, "Wellspring Visual Research Example")
        print(f"✅ Batch job created: {batch_job.id}")
        print(f"   Status: {batch_job.status}")
        print(f"   Expected completion: 24 hours")
        
        print("\n📊 Batch Job Details:")
        print(f"   Job ID: {batch_job.id}")
        print(f"   Status: {batch_job.status}")
        print(f"   Endpoint: {batch_job.endpoint}")
        print(f"   Tasks: {len(tasks)}")
        
        return batch_job.id
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def example_2_monitor_job(job_id: str):
    """
    Example 2: Monitor an existing batch job
    """
    print(f"\n🔍 Example 2: Monitoring Batch Job {job_id}")
    print("=" * 50)
    
    if not PROCESSOR_AVAILABLE:
        print("❌ Batch processor not available")
        return
    
    try:
        processor = WellspringBatchProcessor()
        
        # Check current status
        print("📊 Checking job status...")
        status_info = processor.get_batch_status(job_id)
        print(f"   Status: {status_info['status']}")
        print(f"   Created: {status_info.get('created_at', 'N/A')}")
        
        if status_info['status'] == 'completed':
            print("✅ Job completed! Downloading results...")
            
            # Get the batch job object
            batch_job = processor.client.batches.retrieve(job_id)
            
            # Download and process results
            results_file_path = processor.download_results(batch_job)
            processed_results = processor.process_results(results_file_path)
            
            print(f"✅ Results processed:")
            print(f"   Total results: {processed_results['total_results']}")
            print(f"   Sections: {list(processed_results['results_by_section'].keys())}")
            
            # Show sample results
            if processed_results['results_by_section']:
                print("\n📋 Sample Results:")
                for section, prompts in list(processed_results['results_by_section'].items())[:2]:
                    print(f"\n📁 {section}:")
                    for prompt_type, result in prompts.items():
                        response = result['response'][:200] + "..." if len(result['response']) > 200 else result['response']
                        print(f"   {prompt_type}: {response}")
            
        elif status_info['status'] in ['failed', 'expired', 'cancelled']:
            print(f"❌ Job {status_info['status']}")
        else:
            print(f"⏳ Job still {status_info['status']}. Check again later.")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_3_api_usage():
    """
    Example 3: Using the REST API endpoint
    """
    print("\n🌐 Example 3: REST API Usage")
    print("=" * 50)
    
    # Check if API server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ API server not responding correctly")
            return
    except requests.exceptions.RequestException:
        print("❌ API server not running. Start it with: python batch_endpoint.py")
        return
    
    print("✅ API server is running")
    
    # Submit a batch job via API
    input_file = "/Users/ojeromyo/Desktop/wellspring_directory/em_dash_replacement/changelog/visual_batch_prompts_20250526_171050.json"
    
    if not Path(input_file).exists():
        print(f"❌ Input file not found: {input_file}")
        return
    
    try:
        print("🚀 Submitting batch job via API...")
        
        submit_data = {
            "json_file_path": input_file,
            "description": "Wellspring Visual Research API Example"
        }
        
        response = requests.post(
            "http://localhost:8000/batch/submit",
            json=submit_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Batch submitted successfully!")
            print(f"   Job ID: {result['job_id']}")
            print(f"   Status: {result['status']}")
            print(f"   Tasks: {result['task_count']}")
            
            # Start monitoring
            job_id = result['job_id']
            print(f"\n🔍 Starting background monitoring for {job_id}...")
            
            monitor_response = requests.post(f"http://localhost:8000/batch/{job_id}/monitor")
            if monitor_response.status_code == 200:
                print("✅ Monitoring started in background")
            
            return job_id
            
        else:
            print(f"❌ API error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_4_list_jobs():
    """
    Example 4: List all batch jobs
    """
    print("\n📋 Example 4: List All Batch Jobs")
    print("=" * 50)
    
    if not PROCESSOR_AVAILABLE:
        print("❌ Batch processor not available")
        return
    
    try:
        processor = WellspringBatchProcessor()
        
        jobs = processor.list_batch_jobs()
        
        print(f"📊 Found {len(jobs)} batch jobs:")
        
        for job in jobs:
            status_icon = {
                'completed': '✅',
                'failed': '❌',
                'in_progress': '⏳',
                'validating': '🔍',
                'finalizing': '🏁'
            }.get(job['status'], '📄')
            
            print(f"   {status_icon} {job['id']}: {job['status']}")
            if job.get('metadata'):
                description = job['metadata'].get('description', 'No description')
                print(f"      Description: {description}")
            print(f"      Created: {job.get('created_at', 'N/A')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_5_complete_workflow():
    """
    Example 5: Complete workflow (submit + monitor + process)
    """
    print("\n🔄 Example 5: Complete Workflow")
    print("=" * 50)
    
    if not PROCESSOR_AVAILABLE:
        print("❌ Batch processor not available")
        return
    
    input_file = "/Users/ojeromyo/Desktop/wellspring_directory/em_dash_replacement/changelog/visual_batch_prompts_20250526_171050.json"
    
    if not Path(input_file).exists():
        print(f"❌ Input file not found: {input_file}")
        return
    
    try:
        processor = WellspringBatchProcessor()
        
        print("🚀 Running complete batch workflow...")
        print("   This will submit, monitor, and process results automatically")
        print("   ⚠️  This will wait for job completion (up to 24 hours)")
        
        # Ask for confirmation
        confirm = input("\nContinue? (y/N): ").lower().strip()
        if confirm != 'y':
            print("❌ Cancelled by user")
            return
        
        # Run complete workflow
        results = processor.run_complete_batch_workflow(input_file)
        
        if "error" in results:
            print(f"❌ Workflow error: {results['error']}")
            return
        
        print("✅ Complete workflow finished successfully!")
        print(f"   Total results: {results['total_results']}")
        print(f"   Sections processed: {list(results['results_by_section'].keys())}")
        
        # Save summary
        summary_file = Path("/Users/ojeromyo/Desktop/wellspring_directory/batch_prompts/output/workflow_summary.json")
        with open(summary_file, 'w') as f:
            json.dump({
                "timestamp": results['timestamp'],
                "total_results": results['total_results'],
                "sections": list(results['results_by_section'].keys()),
                "status": "completed"
            }, f, indent=2)
        
        print(f"📄 Summary saved to: {summary_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """
    Main function to run examples
    """
    print("🎯 Wellspring OpenAI Batch Processing Examples")
    print("=" * 60)
    
    # Check environment
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set in environment variables")
        print("   Please set it in your .env file or export it:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return
    
    print("✅ Environment configured")
    
    # Show menu
    while True:
        print("\n📋 Choose an example:")
        print("1. Direct batch processing (submit job)")
        print("2. Monitor existing job (provide job ID)")
        print("3. REST API usage")
        print("4. List all batch jobs")
        print("5. Complete workflow (submit + monitor + process)")
        print("0. Exit")
        
        choice = input("\nEnter choice (0-5): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            job_id = example_1_direct_processing()
            if job_id:
                print(f"\n💡 Tip: Use choice 2 with job ID '{job_id}' to monitor this job")
        elif choice == "2":
            job_id = input("Enter job ID to monitor: ").strip()
            if job_id:
                example_2_monitor_job(job_id)
        elif choice == "3":
            job_id = example_3_api_usage()
            if job_id:
                print(f"\n💡 Tip: Use choice 2 with job ID '{job_id}' to monitor this job")
        elif choice == "4":
            example_4_list_jobs()
        elif choice == "5":
            example_5_complete_workflow()
        else:
            print("❌ Invalid choice. Please enter 0-5.")


if __name__ == "__main__":
    main()