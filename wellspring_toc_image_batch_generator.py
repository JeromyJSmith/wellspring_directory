#!/usr/bin/env python3
"""
🎨 WELLSPRING TOC IMAGE BATCH GENERATOR
=====================================
Generate all 26 Wellspring-style icons for the complete Table of Contents
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
        "future": "crystal ball and forward-pointing compass"
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

def create_toc_batch_requests():
    """Create all 26 Wellspring TOC image generation requests"""
    
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
    
    print(f"🎨 Creating {len(toc_items)} Wellspring TOC image requests...")
    print("=" * 60)
    
    batch_requests = []
    
    for i, (title, description) in enumerate(toc_items):
        prompt = create_wellspring_style_prompt(title, description)
        
        request = {
            "custom_id": f"wellspring_toc_{i+1:02d}_{title.replace(' ', '_').replace(':', '').replace(',', '')}",
            "method": "POST",
            "url": "/v1/images/generations",
            "body": {
                "model": "dall-e-3",
                "prompt": prompt,
                "size": "1024x1024",
                "quality": "hd",
                "style": "vivid"
            }
        }
        
        batch_requests.append(request)
        print(f"✅ {i+1:2d}. {title}")
    
    return batch_requests

def submit_wellspring_batch():
    """Submit the complete Wellspring TOC image generation batch"""
    
    print("🚀 WELLSPRING TOC IMAGE BATCH GENERATOR")
    print("=" * 60)
    print("🎨 Generating 26 professional Wellspring-style icons")
    print("✨ Gold flake + Classical design for complete TOC")
    print("")
    
    # Load API key
    api_key = load_env_vars()
    if not api_key:
        print("❌ ERROR: OpenAI API key not found in .env file!")
        return None
    
    print(f"✅ API Key loaded: {api_key[:20]}...{api_key[-8:]}")
    
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)
    
    # Create batch requests
    requests = create_toc_batch_requests()
    
    # Create batch directory and save requests
    batch_dir = Path("wellspring_toc_image_batch")
    batch_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    requests_file = batch_dir / f"wellspring_toc_requests_{timestamp}.jsonl"
    
    print(f"\n📁 Saving batch requests to: {requests_file}")
    
    with open(requests_file, 'w') as f:
        for request in requests:
            f.write(json.dumps(request) + '\n')
    
    print(f"✅ Created {len(requests)} image generation requests")
    
    try:
        # Upload batch file
        print("\n📤 Uploading batch file to OpenAI...")
        with open(requests_file, 'rb') as f:
            batch_file = client.files.create(
                file=f,
                purpose="batch"
            )
        
        print(f"✅ Batch file uploaded: {batch_file.id}")
        
        # Submit batch
        print("🚀 Submitting Wellspring TOC image generation batch...")
        batch = client.batches.create(
            input_file_id=batch_file.id,
            endpoint="/v1/images/generations",
            completion_window="24h",
            metadata={
                "description": f"Wellspring TOC Icons - {timestamp}",
                "project": "wellspring_manual",
                "content_type": "table_of_contents_icons",
                "style": "wellspring_gold_classical"
            }
        )
        
        print("🎉 BATCH SUBMITTED SUCCESSFULLY!")
        print("=" * 60)
        print(f"📋 Batch ID: {batch.id}")
        print(f"📊 Status: {batch.status}")
        print(f"📅 Created: {datetime.fromtimestamp(batch.created_at)}")
        print(f"📝 Description: Wellspring TOC Icons - {timestamp}")
        print(f"🎯 Total Requests: {len(requests)}")
        print("")
        print("⏳ ESTIMATED COMPLETION: 10-30 minutes")
        print("🔍 CHECK STATUS: Run wellspring_batch_status_checker.py")
        print("")
        print("🎨 GENERATING:")
        print("   • 4 Book Part icons")
        print("   • 22 Chapter icons") 
        print("   • 2 Appendix icons")
        print("   • All in Wellspring gold + classical style")
        
        # Save batch info
        batch_info = {
            "batch_id": batch.id,
            "timestamp": timestamp,
            "status": batch.status,
            "total_requests": len(requests),
            "requests_file": str(requests_file),
            "description": f"Wellspring TOC Icons - {timestamp}"
        }
        
        info_file = batch_dir / f"batch_info_{timestamp}.json"
        with open(info_file, 'w') as f:
            json.dump(batch_info, f, indent=2)
        
        print(f"📁 Batch info saved: {info_file}")
        
        return batch.id
        
    except Exception as e:
        print(f"❌ Error submitting batch: {str(e)}")
        return None

if __name__ == "__main__":
    batch_id = submit_wellspring_batch()
    
    if batch_id:
        print(f"\n🎯 NEXT STEPS:")
        print(f"1. Wait 10-30 minutes for completion")
        print(f"2. Run: uv run wellspring_batch_status_checker.py")
        print(f"3. Download your 26 Wellspring TOC icons!")
    else:
        print("\n❌ Batch submission failed. Check errors above.") 