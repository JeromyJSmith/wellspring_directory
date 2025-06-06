#!/usr/bin/env python3
"""
🔍 Wellspring TOC Batch Status Checker
=====================================
Check status of Wellspring TOC image generation batch processes using correct API key
"""

import openai
import os
import json
from datetime import datetime
from pathlib import Path

def load_env_vars():
    """Load environment variables from .env file"""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    return os.environ.get('OPENAI_API_KEY')

def check_all_batches():
    """Check all recent OpenAI batches for Wellspring TOC images"""
    
    print("🔍 WELLSPRING TOC BATCH STATUS CHECKER")
    print("=" * 60)
    print("📦 Using UV Python environment")
    print("🎨 Checking Wellspring TOC image generation batches...")
    print()
    
    # Load correct API key from .env
    api_key = load_env_vars()
    
    if not api_key:
        print("❌ ERROR: OpenAI API key not found in .env file!")
        return
    
    print(f"✅ API Key loaded: {api_key[:20]}...{api_key[-8:]}")
    print()
    
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)
    
    try:
        print("🔍 Fetching recent batch jobs...")
        batches = client.batches.list(limit=20)
        
        if not batches.data:
            print("📭 No batch jobs found!")
            print("⚠️  This means either:")
            print("   - No Wellspring TOC batch was submitted")
            print("   - The batch was submitted with a different API key")
            print("   - There was an error during submission")
            return
        
        print(f"📊 Found {len(batches.data)} recent batch job(s)")
        print("=" * 60)
        
        wellspring_batches = []
        
        for i, batch in enumerate(batches.data):
            created = datetime.fromtimestamp(batch.created_at)
            
            # Check if this might be a Wellspring batch
            description = ""
            if hasattr(batch, 'metadata') and batch.metadata:
                description = batch.metadata.get('description', 'No description')
            
            is_wellspring = any(keyword in description.lower() for keyword in 
                              ['wellspring', 'toc', 'table', 'contents', 'icon'])
            
            print(f"📋 Batch #{i+1}:")
            print(f"   🆔 ID: {batch.id}")
            print(f"   📅 Created: {created.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   📊 Status: {batch.status.upper()}")
            print(f"   📝 Description: {description}")
            
            if batch.status == 'completed':
                print(f"   ✅ Completed at: {datetime.fromtimestamp(batch.completed_at).strftime('%Y-%m-%d %H:%M:%S')}")
                if hasattr(batch, 'request_counts'):
                    print(f"   📈 Requests: {batch.request_counts.total} total, {batch.request_counts.completed} completed")
                if hasattr(batch, 'output_file_id'):
                    print(f"   📁 Output file: {batch.output_file_id}")
            elif batch.status == 'failed':
                print(f"   ❌ Failed at: {datetime.fromtimestamp(batch.failed_at).strftime('%Y-%m-%d %H:%M:%S')}")
                if hasattr(batch, 'errors'):
                    print(f"   🚨 Errors: {batch.errors}")
            elif batch.status == 'in_progress':
                print(f"   ⏳ In progress...")
                if hasattr(batch, 'request_counts'):
                    print(f"   📈 Progress: {batch.request_counts.completed}/{batch.request_counts.total}")
            
            if is_wellspring:
                wellspring_batches.append(batch)
                print("   🎨 >>> POTENTIAL WELLSPRING TOC BATCH! <<<")
            
            print()
        
        # Focus on Wellspring batches
        if wellspring_batches:
            print("🎯 WELLSPRING TOC BATCH SUMMARY:")
            print("=" * 60)
            
            for batch in wellspring_batches:
                print(f"🎨 Wellspring Batch: {batch.id}")
                print(f"   Status: {batch.status.upper()}")
                
                if batch.status == 'completed':
                    print("   ✅ BATCH COMPLETED! Ready to download results.")
                    if hasattr(batch, 'output_file_id'):
                        print(f"   📁 Output file ID: {batch.output_file_id}")
                        download_results(client, batch)
                elif batch.status == 'failed':
                    print("   ❌ BATCH FAILED! Check error details above.")
                elif batch.status == 'in_progress':
                    print("   ⏳ BATCH RUNNING! Check back in a few minutes.")
                else:
                    print(f"   📋 Current status: {batch.status}")
        else:
            print("🤔 NO WELLSPRING TOC BATCHES FOUND")
            print("This suggests the batch may not have been submitted successfully.")
    
    except Exception as e:
        print(f"❌ Error checking batches: {str(e)}")
        print("🔧 This might be due to:")
        print("   - Invalid API key")
        print("   - Network connection issues")
        print("   - OpenAI API service issues")

def download_results(client, batch):
    """Download and save batch results"""
    try:
        print(f"📥 Downloading results for batch {batch.id}...")
        
        # Create results directory
        results_dir = Path("wellspring_toc_batch_results")
        results_dir.mkdir(exist_ok=True)
        
        # Download output file
        if hasattr(batch, 'output_file_id') and batch.output_file_id:
            output_content = client.files.content(batch.output_file_id)
            
            output_file = results_dir / f"batch_{batch.id}_results.jsonl"
            with open(output_file, 'wb') as f:
                f.write(output_content.content)
            
            print(f"✅ Results saved to: {output_file}")
            
            # Parse and show summary
            show_results_summary(output_file)
        
    except Exception as e:
        print(f"❌ Error downloading results: {str(e)}")

def show_results_summary(results_file):
    """Show summary of batch results"""
    try:
        print("\n📊 BATCH RESULTS SUMMARY:")
        print("-" * 40)
        
        successful = 0
        failed = 0
        
        with open(results_file, 'r') as f:
            for line in f:
                if line.strip():
                    result = json.loads(line)
                    if 'error' in result:
                        failed += 1
                    else:
                        successful += 1
        
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"📁 Full results: {results_file}")
        
        if successful > 0:
            print("\n🎨 Your Wellspring TOC images have been generated!")
            print("Check the results file for image URLs.")
        
    except Exception as e:
        print(f"❌ Error reading results: {str(e)}")

if __name__ == "__main__":
    check_all_batches() 