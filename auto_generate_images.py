#!/usr/bin/env python3
"""
Auto-Generate Wellspring Chapter Images
======================================
Immediately starts generating professional chapter images without confirmation
"""

import sys
sys.path.append('.')

from wellspring_openai_individual_generator import WellspringIndividualImageGenerator

def auto_generate():
    print("🎨 WELLSPRING AUTO-GENERATE CHAPTER IMAGES")
    print("=" * 50)
    print("🚀 STARTING IMMEDIATE GENERATION...")
    print("✨ Creating professional chapter images with DALL-E 3")
    print("")
    
    generator = WellspringIndividualImageGenerator()
    
    # Check for existing images
    existing_images = len(list(generator.output_dir.glob("*.png")))
    if existing_images > 0:
        print(f"📁 Found {existing_images} existing images")
        print("   (Will skip existing images)")
        print("")
    
    print("💰 COST: $2.00 for 25 images")
    print("⏱️  TIME: ~15-20 minutes")
    print("")
    print("🎬 STARTING GENERATION NOW...")
    print("")
    
    # Start generation immediately
    success = generator.generate_all_images(max_images=25)
    
    if success:
        print("")
        print("🎉 AUTO-GENERATION COMPLETED!")
        print("📁 Check images in: icons/wellspring_goldflake_batch_tool/openai_individual_images/")
    else:
        print("❌ Generation failed")
    
    return success

if __name__ == "__main__":
    auto_generate() 