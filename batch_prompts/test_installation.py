#!/usr/bin/env python3
"""Quick test of the batch processing installation"""

import os
from pathlib import Path

def test_installation():
    print("🧪 Testing Wellspring Batch Processing Installation")
    print("=" * 50)
    
    # Test 1: Import libraries
    try:
        from openai import OpenAI
        print("✅ OpenAI SDK imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import error: {e}")
        return False
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import error: {e}")
        return False
    
    # Test 2: Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OPENAI_API_KEY is configured")
    else:
        print("⚠️  OPENAI_API_KEY not set (required for actual processing)")
    
    # Test 3: Test batch processor
    try:
        from openai_batch_processor import WellspringBatchProcessor
        print("✅ WellspringBatchProcessor imported successfully")
        
        if api_key:
            processor = WellspringBatchProcessor()
            print("✅ Batch processor initialized successfully")
        else:
            print("⚠️  Skipping processor initialization (no API key)")
            
    except Exception as e:
        print(f"❌ Batch processor error: {e}")
        return False
    
    # Test 4: Check input file
    input_file = "/Users/ojeromyo/Desktop/wellspring_directory/em_dash_replacement/changelog/visual_batch_prompts_20250526_171050.json"
    if Path(input_file).exists():
        print("✅ Visual batch prompts file found")
        
        if api_key:
            try:
                batch_data = processor.load_visual_batch_prompts(input_file)
                tasks = processor.format_prompts_for_batch_api(batch_data)
                print(f"✅ Successfully formatted {len(tasks)} batch tasks")
                print(f"   Total opportunities: {batch_data.get('total_opportunities', 0)}")
                print(f"   Sections: {len(batch_data.get('batch_prompts', {}).get('prompt_sets', []))}")
            except Exception as e:
                print(f"❌ Error processing file: {e}")
                return False
    else:
        print(f"⚠️  Input file not found: {input_file}")
    
    print("\n🎉 Installation test completed successfully!")
    print("\n📖 Next steps:")
    print("   1. Set OPENAI_API_KEY if not already set")
    print("   2. Run: python example_usage.py")
    print("   3. Or start API server: python batch_endpoint.py")
    
    return True

if __name__ == "__main__":
    test_installation()