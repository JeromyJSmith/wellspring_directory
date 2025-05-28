#!/usr/bin/env python3
"""
Wellspring OpenAI Batch Image Generator
=======================================

Uses OpenAI 4o to generate high-quality chapter images that match the 
"Setting the Vision" aesthetic with real gold flake textures and rich imagery.

NO simple icons - actual professional chapter artwork.
"""

import json
import openai
import os
from pathlib import Path
import time
from datetime import datetime
import base64
import requests

class WellspringOpenAIBatchGenerator:
    """Generate professional chapter images using OpenAI 4o batch processing"""
    
    def __init__(self):
        self.project_dir = Path("icons/wellspring_goldflake_batch_tool")
        self.batch_dir = self.project_dir / "openai_batch_processing"
        self.output_dir = self.batch_dir / "generated_images"
        self.prompts_dir = self.batch_dir / "prompts"
        self.reference_dir = self.batch_dir / "reference_images"
        
        # Create directories
        for dir_path in [self.batch_dir, self.output_dir, self.prompts_dir, self.reference_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # OpenAI setup
        self.client = openai.OpenAI()
        
        # Style guide based on actual "Setting the Vision" reference
        self.style_prompt_base = """
        Create a professional chapter cover image in the exact style of vintage leather-bound manuscripts with ornate gold details.

        ESSENTIAL STYLE ELEMENTS:
        - Dark charcoal/black leather background with rich texture (like aged book leather)
        - Ornate gold leaf decorative borders with classical flourishes and corner ornaments
        - Rich gold flake texture throughout (metallic shimmer effect)
        - Large, prominent central symbolic imagery (not tiny icons)
        - Professional serif typography in elegant gold lettering
        - Mystical/classical aesthetic with architectural elements
        - High contrast between dark background and bright gold elements
        - Vintage manuscript illumination style
        - Size: 800×1200 pixels (portrait orientation for book chapters)
        
        AVOID: Simple flat colors, modern icons, cartoonish elements, bright colors
        
        Chapter Subject: "{chapter_title}"
        
        Create imagery that captures the essence of: {subject_keywords}
        
        The central imagery should be LARGE and PROMINENT, taking up significant space in the composition.
        Use rich, detailed artistic elements that evoke the professional nature of this subject.
        """
    
    def load_chapter_names(self):
        """Load the extracted chapter names"""
        json_files = list(self.project_dir.glob("chapter_names_*.json"))
        
        if not json_files:
            print("❌ No chapter names file found!")
            return None
            
        latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
        
        with open(latest_file, 'r') as f:
            return json.load(f)
    
    def categorize_subject(self, chapter_title):
        """Determine subject keywords for better image generation"""
        title_lower = chapter_title.lower()
        
        # Healthcare & Treatment
        if any(word in title_lower for word in ['health', 'care', 'treatment', 'therapy', 'healing', 'recovery', 'wellness', 'behavioral', 'mental', 'crisis']):
            return "healthcare facilities, medical symbols, healing environments, therapeutic spaces, modern hospital architecture"
            
        # Architecture & Design  
        elif any(word in title_lower for word in ['design', 'architect', 'building', 'construction', 'infrastructure', 'layout', 'space', 'facility']):
            return "architectural blueprints, construction sites, modern buildings, design tools, structural elements, urban planning"
            
        # Leadership & Vision
        elif any(word in title_lower for word in ['vision', 'mission', 'leadership', 'strategy', 'planning', 'stakeholder', 'engagement']):
            return "leadership symbols, strategic planning, vision concepts, corporate boardrooms, organizational charts"
            
        # Financial & Legal
        elif any(word in title_lower for word in ['budget', 'cost', 'financial', 'legal', 'compliance', 'regulation', 'attorney']):
            return "financial documents, legal scales, money symbols, contract papers, accounting ledgers"
            
        # Engineering & Technology
        elif any(word in title_lower for word in ['engineer', 'technology', 'system', 'mechanical', 'electrical', 'utility']):
            return "engineering blueprints, technical diagrams, machinery, electrical systems, infrastructure networks"
            
        # Community & Environment
        elif any(word in title_lower for word in ['community', 'environment', 'sustainability', 'accessibility', 'zoning', 'landscape']):
            return "community spaces, environmental symbols, green buildings, accessible design, urban landscapes"
            
        # Quality & Management
        elif any(word in title_lower for word in ['quality', 'management', 'coordination', 'documentation', 'inspection', 'evaluation']):
            return "quality control symbols, management charts, documentation systems, inspection tools, performance metrics"
            
        else:
            return "professional business environments, organizational excellence, project management, collaborative workspaces"
    
    def create_batch_prompts(self, data):
        """Create batch prompts for OpenAI processing"""
        
        print("🎨 CREATING OPENAI BATCH PROMPTS")
        print("=" * 45)
        print("✨ Generating prompts for high-quality chapter images")
        print("")
        
        chapters = data.get('chapters', [])
        sections = data.get('sections', [])
        
        batch_requests = []
        prompt_summary = []
        
        # Process chapters
        for i, chapter in enumerate(chapters[:20], 1):  # Start with first 20 for testing
            clean_title = self.clean_chapter_name(chapter)
            if clean_title and len(clean_title) > 3:
                subject_keywords = self.categorize_subject(clean_title)
                
                prompt = self.style_prompt_base.format(
                    chapter_title=clean_title,
                    subject_keywords=subject_keywords
                )
                
                request = {
                    "custom_id": f"chapter_{i:03d}",
                    "method": "POST",
                    "url": "/v1/images/generations",
                    "body": {
                        "model": "dall-e-3",
                        "prompt": prompt,
                        "size": "1024x1792",  # Portrait orientation
                        "quality": "hd",
                        "style": "vivid"
                    }
                }
                
                batch_requests.append(request)
                prompt_summary.append({
                    "id": f"chapter_{i:03d}",
                    "title": clean_title,
                    "keywords": subject_keywords,
                    "prompt_length": len(prompt)
                })
        
        # Process key sections
        key_sections = ["Setting the Vision", "Table of Contents", "Introduction", "Conclusion"]
        for section in sections:
            if any(key in section for key in key_sections):
                i = len(batch_requests) + 1
                clean_title = self.clean_chapter_name(section)
                if clean_title:
                    subject_keywords = "manuscript elements, book organization, literary symbols, classical typography"
                    
                    prompt = self.style_prompt_base.format(
                        chapter_title=clean_title,
                        subject_keywords=subject_keywords
                    )
                    
                    request = {
                        "custom_id": f"section_{clean_title.lower().replace(' ', '_')}",
                        "method": "POST",
                        "url": "/v1/images/generations",
                        "body": {
                            "model": "dall-e-3",
                            "prompt": prompt,
                            "size": "1024x1792",
                            "quality": "hd",
                            "style": "vivid"
                        }
                    }
                    
                    batch_requests.append(request)
                    prompt_summary.append({
                        "id": f"section_{clean_title.lower().replace(' ', '_')}",
                        "title": clean_title,
                        "keywords": subject_keywords,
                        "prompt_length": len(prompt)
                    })
        
        # Save batch file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        batch_file = self.prompts_dir / f"wellspring_batch_{timestamp}.jsonl"
        
        with open(batch_file, 'w') as f:
            for request in batch_requests:
                f.write(json.dumps(request) + '\n')
        
        # Save summary
        summary_file = self.prompts_dir / f"batch_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump({
                "created_at": timestamp,
                "total_requests": len(batch_requests),
                "chapters": len([r for r in batch_requests if r["custom_id"].startswith("chapter_")]),
                "sections": len([r for r in batch_requests if r["custom_id"].startswith("section_")]),
                "requests": prompt_summary
            }, f, indent=2)
        
        print(f"✅ Created {len(batch_requests)} batch requests")
        print(f"📁 Batch file: {batch_file}")
        print(f"📋 Summary: {summary_file}")
        
        return batch_file, summary_file
    
    def clean_chapter_name(self, raw_name):
        """Clean chapter name for processing"""
        import re
        
        # Remove XML artifacts
        clean_name = re.sub(r'<[^>]+>', '', raw_name)
        clean_name = re.sub(r'&[^;]+;', '', clean_name)
        clean_name = re.sub(r'\?\?ACE \d+\?\?', '', clean_name)
        clean_name = re.sub(r'encoding="[^"]*"', '', clean_name)
        clean_name = re.sub(r'standalone="[^"]*"', '', clean_name)
        clean_name = re.sub(r'DOMVersion="[^"]*"', '', clean_name)
        
        # Clean whitespace
        clean_name = re.sub(r'\s+', ' ', clean_name)
        clean_name = clean_name.strip()
        
        # Extract meaningful title
        if ':' in clean_name:
            parts = clean_name.split(':', 1)
            if len(parts) > 1 and len(parts[1].strip()) > 3:
                clean_name = parts[1].strip()
        
        # Remove chapter prefix
        clean_name = re.sub(r'^Chapter \d+:\s*', '', clean_name)
        
        return clean_name[:100]  # Reasonable length
    
    def submit_batch(self, batch_file):
        """Submit batch to OpenAI for processing"""
        
        print(f"🚀 SUBMITTING BATCH TO OPENAI")
        print("=" * 40)
        
        try:
            # Upload batch file
            print("📤 Uploading batch file...")
            
            with open(batch_file, 'rb') as f:
                batch_input_file = self.client.files.create(
                    file=f,
                    purpose="batch"
                )
            
            print(f"✅ File uploaded: {batch_input_file.id}")
            
            # Create batch
            print("🎬 Creating batch job...")
            
            batch = self.client.batches.create(
                input_file_id=batch_input_file.id,
                endpoint="/v1/images/generations",
                completion_window="24h",
                metadata={
                    "description": "Wellspring chapter image generation",
                    "project": "wellspring_manuscript"
                }
            )
            
            print(f"✅ Batch created: {batch.id}")
            print(f"📊 Status: {batch.status}")
            print(f"⏱️  Completion window: 24 hours")
            
            # Save batch info
            batch_info = {
                "batch_id": batch.id,
                "input_file_id": batch_input_file.id,
                "status": batch.status,
                "created_at": datetime.now().isoformat(),
                "metadata": batch.metadata
            }
            
            info_file = self.batch_dir / f"batch_info_{batch.id}.json"
            with open(info_file, 'w') as f:
                json.dump(batch_info, f, indent=2)
            
            print(f"💾 Batch info saved: {info_file}")
            
            return batch.id
            
        except Exception as e:
            print(f"❌ Error submitting batch: {e}")
            return None
    
    def check_batch_status(self, batch_id=None):
        """Check status of batch processing"""
        
        if not batch_id:
            # Find most recent batch
            batch_files = list(self.batch_dir.glob("batch_info_*.json"))
            if not batch_files:
                print("❌ No batch info files found")
                return None
                
            latest_file = max(batch_files, key=lambda f: f.stat().st_mtime)
            with open(latest_file, 'r') as f:
                batch_info = json.load(f)
            batch_id = batch_info["batch_id"]
        
        print(f"🔍 CHECKING BATCH STATUS: {batch_id}")
        print("=" * 50)
        
        try:
            batch = self.client.batches.retrieve(batch_id)
            
            print(f"📊 Status: {batch.status}")
            print(f"📝 Request counts: {batch.request_counts}")
            
            if batch.status == "completed":
                print("🎉 BATCH COMPLETED!")
                return self.download_batch_results(batch)
            elif batch.status == "failed":
                print("❌ BATCH FAILED")
                if batch.errors:
                    print(f"Errors: {batch.errors}")
            elif batch.status in ["validating", "in_progress"]:
                print("⏳ Batch is still processing...")
            
            return batch.status
            
        except Exception as e:
            print(f"❌ Error checking batch: {e}")
            return None
    
    def download_batch_results(self, batch):
        """Download and save batch results"""
        
        print("📥 DOWNLOADING BATCH RESULTS")
        print("=" * 40)
        
        try:
            # Download output file
            output_file_id = batch.output_file_id
            output_file = self.client.files.content(output_file_id)
            
            # Save raw results
            results_file = self.batch_dir / f"results_{batch.id}.jsonl"
            results_file.write_bytes(output_file.content)
            
            print(f"✅ Results saved: {results_file}")
            
            # Process and download images
            successful = 0
            failed = 0
            
            with open(results_file, 'r') as f:
                for line in f:
                    result = json.loads(line)
                    
                    if result.get("error"):
                        print(f"❌ Error for {result.get('custom_id', 'unknown')}: {result['error']}")
                        failed += 1
                        continue
                    
                    try:
                        custom_id = result["custom_id"]
                        image_url = result["response"]["body"]["data"][0]["url"]
                        
                        # Download image
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            image_file = self.output_dir / f"{custom_id}.png"
                            with open(image_file, 'wb') as img_f:
                                img_f.write(response.content)
                            
                            print(f"✅ Downloaded: {custom_id}.png")
                            successful += 1
                        else:
                            print(f"❌ Failed to download: {custom_id}")
                            failed += 1
                            
                    except Exception as e:
                        print(f"❌ Error processing result: {e}")
                        failed += 1
            
            print(f"\n🎉 DOWNLOAD COMPLETE!")
            print(f"✅ Successful: {successful}")
            print(f"❌ Failed: {failed}")
            print(f"📁 Images saved to: {self.output_dir}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error downloading results: {e}")
            return False

def main():
    """Main execution"""
    
    print("🎨 WELLSPRING OPENAI BATCH IMAGE GENERATOR")
    print("=" * 50)
    print("🎯 Creating professional chapter images with OpenAI 4o")
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
    
    # Check for existing batches
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            generator.check_batch_status()
            return True
        elif sys.argv[1] == "check":
            batch_id = sys.argv[2] if len(sys.argv) > 2 else None
            generator.check_batch_status(batch_id)
            return True
    
    # Create batch prompts
    batch_file, summary_file = generator.create_batch_prompts(data)
    
    print("")
    confirm = input("🚀 Ready to submit batch to OpenAI? (y/N): ")
    
    if confirm.lower() == 'y':
        batch_id = generator.submit_batch(batch_file)
        
        if batch_id:
            print(f"\n✅ BATCH SUBMITTED SUCCESSFULLY!")
            print(f"📋 Batch ID: {batch_id}")
            print(f"⏱️  Processing time: ~15-30 minutes")
            print("")
            print("🔄 Check status with:")
            print(f"   python {__file__} status")
            print("")
            print("📥 Download results when ready with:")
            print(f"   python {__file__} check {batch_id}")
        else:
            print("❌ Failed to submit batch")
    else:
        print("📋 Batch prepared but not submitted")
        print(f"📁 Batch file ready: {batch_file}")

if __name__ == "__main__":
    main() 