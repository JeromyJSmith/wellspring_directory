#!/usr/bin/env python3
"""
🎨 WELLSPRING TOC INDIVIDUAL IMAGE GENERATOR
==========================================
Generate all 27 Wellspring-style icons individually (since batch API doesn't support images)
"""

import openai
import os
import json
import requests
from datetime import datetime
from pathlib import Path
import time

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

def create_wellspring_style_prompt(title, description=""):
    """Create Wellspring-style DALL-E prompt for each TOC item"""
    
    base_style = """
🎨 Wellspring Icon Style — Professional book cover icon design:

STYLE SPECIFICATIONS:
- Deep navy blue textured background (#003366) like aged leather
- Rich luminous gold flake (#EFD45B) with metallic, antique foil-embossed appearance
- Fine double-line gold frame with ornate corner flourishes
- Centered architecturally inspired object relating to the topic
- Balanced vertical and horizontal composition - timeless and formal
- High-relief gold engravings, classical sculptural detail
- Shadows and lighting that mimic real gilded surfaces
- Celestial accents: subtle starfields, rings, or cosmological glyphs in background

FORMAT: Square icon format, professional book design quality
"""
    
    # Map topics to specific architectural/symbolic elements
    topic_elements = {
        "introduction": "elegant quill pen and scroll",
        "foundations": "classical foundation stones and compass",
        "strategic planning": "architectural blueprints and astrolabe", 
        "feasibility": "balance scales and measuring instruments",
        "market studies": "telescope and maps",
        "site selection": "surveyor's compass and grid",
        "zoning": "legal documents and seal",
        "budgeting": "ledger books and coins",
        "risk": "shield and fortress elements", 
        "due diligence": "magnifying glass and documents",
        "design": "architectural tools and geometric forms",
        "permitting": "official stamps and scrolls",
        "construction": "building tools and scaffolding",
        "workforce": "classical columns representing people",
        "quality": "precision instruments and standards",
        "operations": "clockwork and mechanical gears",
        "compliance": "scales of justice and guidelines",
        "financial": "treasure chest and accounting tools",
        "technology": "sophisticated instruments and devices",
        "leadership": "crown and scepter elements",
        "excellence": "star constellation and achievement symbols",
        "future": "crystal ball and forward-pointing compass",
        "part": "ornate book cover or title page",
        "appendix": "reference books and scrolls"
    }
    
    # Determine appropriate architectural element
    title_lower = title.lower()
    element = "classical architectural symbol"
    for keyword, suggested_element in topic_elements.items():
        if keyword in title_lower:
            element = suggested_element
            break
    
    prompt = f"""
Create a professional Wellspring-style icon for "{title}".

{base_style}

SPECIFIC ICON: Feature a {element} as the central focal point, rendered in brilliant gold relief against the deep navy background. The design should convey professionalism, expertise, and classical architectural beauty.

COMPOSITION: Perfect symmetry, museum-quality craftsmanship, suitable for a professional behavioral health development manual.

QUALITY: Ultra-high detail, print-ready quality, classical book illustration style.
"""
    
    return prompt.strip()

def download_image(url, filepath):
    """Download image from URL to filepath"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return True
    except Exception as e:
        print(f"   ❌ Download failed: {str(e)}")
        return False

def generate_wellspring_toc_images():
    """Generate all 27 Wellspring TOC images individually"""
    
    print("🚀 WELLSPRING TOC INDIVIDUAL IMAGE GENERATOR")
    print("=" * 60)
    print("🎨 Generating 27 professional Wellspring-style icons")
    print("✨ Gold flake + Classical design for complete TOC")
    print("⚡ Individual generation (batch API doesn't support images)")
    print("")
    
    # Load API key
    api_key = load_env_vars()
    if not api_key:
        print("❌ ERROR: OpenAI API key not found in .env file!")
        return False
    
    print(f"✅ API Key loaded: {api_key[:20]}...{api_key[-8:]}")
    
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)
    
    # Complete Wellspring TOC Structure
    toc_items = [
        # BOOK PARTS
        ("Part 1: Setting The Vision", "Strategic planning and vision foundation"),
        ("Part 2: From Concept Through Permitting", "Development process and regulatory approval"),
        ("Part 3: Acceleration, Talent, Excellence", "Implementation and operational excellence"),
        ("Part 4: Future-Proofing Your Investment", "Sustainability and long-term planning"),
        
        # MAIN CONTENT
        ("Introduction", "Opening overview of behavioral health real estate development"),
        ("Chapter 1: Foundations of Behavioral Health Real Estate Development", "Core principles and complexities"),
        ("Chapter 2: Strategic Planning & Feasibility Analysis", "Market analysis and strategic planning"),
        ("Chapter 3: Market Studies and Needs Assessment", "Understanding community needs and market demand"),
        ("Chapter 4: Site Selection Criteria", "Location analysis and site evaluation"),
        ("Chapter 5: Zoning and Entitlements", "Regulatory requirements and zoning compliance"),
        ("Chapter 6: Preliminary Budgeting and Pro Forma Modeling", "Financial planning and budget development"),
        ("Chapter 7: Risk Identification and Mitigation", "Risk management and mitigation strategies"),
        ("Chapter 8: Due Diligence in Behavioral Health Development", "Comprehensive project evaluation"),
        ("Chapter 9: Design and Programming", "Facility design and program development"),
        ("Chapter 10: Navigating the Permitting Process", "Regulatory approval and permitting"),
        ("Chapter 11: Construction Management", "Project execution and construction oversight"),
        ("Chapter 12: Workforce Development and Talent Acquisition", "Staffing and human resources"),
        ("Chapter 13: Quality Assurance and Continuous Improvement", "Excellence in operations and care"),
        ("Chapter 14: Operations and Service Delivery", "Operational management and service delivery"),
        ("Chapter 15: Regulatory Compliance and Oversight", "Ongoing compliance and regulatory management"),
        ("Chapter 16: Financial Management and Sustainability", "Long-term financial planning"),
        ("Chapter 17: Technology Integration", "Modern technology implementation"),
        ("Chapter 18: Leadership and Organizational Excellence", "Management and leadership development"),
        ("Chapter 19: Performance Excellence", "Achieving superior outcomes"),
        ("Chapter 20: Future-Proofing Your Investment", "Long-term sustainability planning"),
        
        # APPENDICES  
        ("Appendix A: Templates and Checklists", "Essential tools and resources"),
        ("Appendix B: Regulatory References", "Compliance guidelines and regulations")
    ]
    
    # Create output directory
    output_dir = Path("wellspring_toc_generated_images")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = output_dir / f"session_{timestamp}"
    session_dir.mkdir(exist_ok=True)
    
    print(f"📁 Output directory: {session_dir}")
    print(f"🎯 Total images to generate: {len(toc_items)}")
    print("")
    
    results = []
    successful = 0
    failed = 0
    
    for i, (title, description) in enumerate(toc_items):
        print(f"🎨 {i+1:2d}/{len(toc_items)}: {title}")
        
        try:
            # Create prompt
            prompt = create_wellspring_style_prompt(title, description)
            
            # Generate image
            print(f"   ⚡ Generating...")
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="hd",
                style="vivid",
                n=1
            )
            
            # Download image
            image_url = response.data[0].url
            safe_title = title.replace(':', '').replace(',', '').replace('/', '_')
            filename = f"{i+1:02d}_{safe_title.replace(' ', '_')}.png"
            filepath = session_dir / filename
            
            print(f"   📥 Downloading...")
            if download_image(image_url, filepath):
                print(f"   ✅ Saved: {filename}")
                successful += 1
                
                # Save result info
                result = {
                    "index": i + 1,
                    "title": title,
                    "description": description,
                    "filename": filename,
                    "filepath": str(filepath),
                    "url": image_url,
                    "prompt": prompt,
                    "status": "success"
                }
                results.append(result)
            else:
                failed += 1
                result = {
                    "index": i + 1,
                    "title": title,
                    "status": "download_failed",
                    "url": image_url
                }
                results.append(result)
            
            # Small delay to be respectful to API
            if i < len(toc_items) - 1:  # Don't delay after last item
                time.sleep(2)
                
        except Exception as e:
            print(f"   ❌ Generation failed: {str(e)}")
            failed += 1
            result = {
                "index": i + 1,
                "title": title,
                "status": "generation_failed",
                "error": str(e)
            }
            results.append(result)
            
            # Longer delay on error
            time.sleep(5)
        
        print("")
    
    # Save session results
    results_file = session_dir / "generation_results.json"
    session_info = {
        "timestamp": timestamp,
        "total_requested": len(toc_items),
        "successful": successful,
        "failed": failed,
        "results": results
    }
    
    with open(results_file, 'w') as f:
        json.dump(session_info, f, indent=2)
    
    print("🎉 WELLSPRING TOC IMAGE GENERATION COMPLETE!")
    print("=" * 60)
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Images saved to: {session_dir}")
    print(f"📄 Results log: {results_file}")
    print("")
    
    if successful > 0:
        print("🎨 YOUR WELLSPRING TOC ICONS ARE READY!")
        print("   • Professional gold + navy classical style")
        print("   • 1024x1024 HD quality")
        print("   • Print-ready for your manual")
        print("")
        print(f"📂 View images: open {session_dir}")
    
    return successful > 0

if __name__ == "__main__":
    success = generate_wellspring_toc_images()
    
    if success:
        print("🎯 NEXT STEPS:")
        print("1. Review your generated icons")
        print("2. Select favorites for your manual")
        print("3. Integrate into your book design!")
    else:
        print("❌ Generation failed. Check errors above.") 