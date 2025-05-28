#!/usr/bin/env python3
"""
Auto-submit Wellspring OpenAI Batch
===================================
Automatically submits the batch without user confirmation
"""

import sys
sys.path.append('.')

from wellspring_openai_image_batch_generator import WellspringOpenAIBatchGenerator

def auto_submit():
    print("🎨 WELLSPRING OPENAI BATCH - AUTO SUBMIT")
    print("=" * 50)
    print("🎯 Creating and submitting professional chapter images")
    print("✨ Using real gold flake textures and rich imagery")
    print("")
    
    generator = WellspringOpenAIBatchGenerator()
    
    # Load chapter data
    data = generator.load_chapter_names()
    if not data:
        print("❌ Failed to load chapter names")
        return False
    
    print(f"📚 Loaded {len(data.get('chapters', []))} chapters")
    print(f"📋 Loaded {len(data.get('sections', []))} sections")
    print("")
    
    # Create batch prompts
    batch_file, summary_file = generator.create_batch_prompts(data)
    
    print("")
    print("🚀 AUTO-SUBMITTING BATCH TO OPENAI...")
    print("")
    
    # Submit automatically
    batch_id = generator.submit_batch(batch_file)
    
    if batch_id:
        print(f"\n🎉 BATCH SUBMITTED SUCCESSFULLY!")
        print(f"📋 Batch ID: {batch_id}")
        print(f"⏱️  Processing time: ~15-30 minutes")
        print("")
        print("🔄 Check status with:")
        print(f"   python wellspring_openai_image_batch_generator.py status")
        print("")
        print("📥 Download results when ready with:")
        print(f"   python wellspring_openai_image_batch_generator.py check {batch_id}")
        
        return True
    else:
        print("❌ Failed to submit batch")
        return False

if __name__ == "__main__":
    auto_submit() 