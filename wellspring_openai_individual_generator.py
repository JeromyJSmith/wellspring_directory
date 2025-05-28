#!/usr/bin/env python3
"""
Wellspring OpenAI Individual Image Generator
===========================================

Generates high-quality chapter images one by one using OpenAI DALL-E 3
since batch processing doesn't support image generation.

Creates professional chapter artwork matching the "Setting the Vision" aesthetic.
"""

import json
import openai
import os
from pathlib import Path
import time
from datetime import datetime
import requests
from PIL import Image
import io

class WellspringIndividualImageGenerator:
    """Generate professional chapter images using OpenAI DALL-E 3"""
    
    def __init__(self):
        self.project_dir = Path("icons/wellspring_goldflake_batch_tool")
        self.output_dir = self.project_dir / "openai_individual_images"
        self.progress_dir = self.project_dir / "generation_progress"
        
        # Create directories
        for dir_path in [self.output_dir, self.progress_dir]:
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
    
    def save_progress(self, progress_data):
        """Save generation progress"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        progress_file = self.progress_dir / f"progress_{timestamp}.json"
        
        with open(progress_file, 'w') as f:
            json.dump(progress_data, f, indent=2)
    
    def generate_image(self, chapter_title, custom_id, subject_keywords):
        """Generate a single image"""
        
        prompt = self.style_prompt_base.format(
            chapter_title=chapter_title,
            subject_keywords=subject_keywords
        )
        
        try:
            print(f"🎨 Generating: {custom_id} - {chapter_title[:50]}...")
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1792",  # Portrait orientation
                quality="hd",
                style="vivid",
                n=1
            )
            
            # Download image
            image_url = response.data[0].url
            img_response = requests.get(image_url)
            
            if img_response.status_code == 200:
                # Save image
                image_file = self.output_dir / f"{custom_id}.png"
                with open(image_file, 'wb') as f:
                    f.write(img_response.content)
                
                print(f"✅ Saved: {custom_id}.png")
                return True, None
            else:
                error_msg = f"Failed to download image: HTTP {img_response.status_code}"
                print(f"❌ {error_msg}")
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Error generating image: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def generate_all_images(self, max_images=25):
        """Generate all chapter images"""
        
        print("🎨 WELLSPRING INDIVIDUAL IMAGE GENERATION")
        print("=" * 50)
        print("🎯 Creating professional chapter images with OpenAI DALL-E 3")
        print("✨ Using real gold flake textures and rich imagery")
        print("")
        
        # Load chapter data
        data = self.load_chapter_names()
        if not data:
            print("❌ Failed to load chapter names")
            return False
        
        chapters = data.get('chapters', [])
        sections = data.get('sections', [])
        
        print(f"📚 Total chapters available: {len(chapters)}")
        print(f"📋 Total sections available: {len(sections)}")
        print(f"🎯 Generating first {max_images} images")
        print("")
        
        generation_log = {
            "started_at": datetime.now().isoformat(),
            "max_images": max_images,
            "results": [],
            "successful": 0,
            "failed": 0
        }
        
        # Process chapters
        image_count = 0
        for i, chapter in enumerate(chapters, 1):
            if image_count >= max_images:
                break
                
            clean_title = self.clean_chapter_name(chapter)
            if clean_title and len(clean_title) > 3:
                subject_keywords = self.categorize_subject(clean_title)
                custom_id = f"chapter_{i:03d}"
                
                # Check if already exists
                image_file = self.output_dir / f"{custom_id}.png"
                if image_file.exists():
                    print(f"⏭️  Skipping existing: {custom_id}")
                    continue
                
                success, error = self.generate_image(clean_title, custom_id, subject_keywords)
                
                result = {
                    "id": custom_id,
                    "title": clean_title,
                    "keywords": subject_keywords,
                    "success": success,
                    "error": error,
                    "timestamp": datetime.now().isoformat()
                }
                
                generation_log["results"].append(result)
                
                if success:
                    generation_log["successful"] += 1
                else:
                    generation_log["failed"] += 1
                
                image_count += 1
                
                # Rate limiting
                if image_count % 5 == 0:
                    print("⏸️  Pausing 10 seconds to respect rate limits...")
                    time.sleep(10)
                else:
                    time.sleep(2)  # Small delay between requests
        
        # Process key sections
        key_sections = ["Setting the Vision", "Table of Contents", "Introduction", "Conclusion"]
        for section in sections:
            if image_count >= max_images:
                break
                
            if any(key in section for key in key_sections):
                clean_title = self.clean_chapter_name(section)
                if clean_title:
                    custom_id = f"section_{clean_title.lower().replace(' ', '_')}"
                    subject_keywords = "manuscript elements, book organization, literary symbols, classical typography"
                    
                    # Check if already exists
                    image_file = self.output_dir / f"{custom_id}.png"
                    if image_file.exists():
                        print(f"⏭️  Skipping existing: {custom_id}")
                        continue
                    
                    success, error = self.generate_image(clean_title, custom_id, subject_keywords)
                    
                    result = {
                        "id": custom_id,
                        "title": clean_title,
                        "keywords": subject_keywords,
                        "success": success,
                        "error": error,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    generation_log["results"].append(result)
                    
                    if success:
                        generation_log["successful"] += 1
                    else:
                        generation_log["failed"] += 1
                    
                    image_count += 1
                    time.sleep(2)
        
        # Save final log
        generation_log["completed_at"] = datetime.now().isoformat()
        self.save_progress(generation_log)
        
        print("")
        print("🎉 GENERATION COMPLETE!")
        print("=" * 30)
        print(f"✅ Successful: {generation_log['successful']}")
        print(f"❌ Failed: {generation_log['failed']}")
        print(f"📁 Images saved to: {self.output_dir}")
        print(f"📋 Log saved to: {self.progress_dir}")
        
        return True

def main():
    """Main execution"""
    
    generator = WellspringIndividualImageGenerator()
    
    print("🎨 WELLSPRING OPENAI INDIVIDUAL IMAGE GENERATOR")
    print("=" * 55)
    print("🎯 Creating professional chapter images with DALL-E 3")
    print("✨ Individual generation (batch API doesn't support images)")
    print("")
    
    # Check for existing images
    existing_images = len(list(generator.output_dir.glob("*.png")))
    if existing_images > 0:
        print(f"📁 Found {existing_images} existing images")
        print("   (Will skip existing images)")
        print("")
    
    print("💰 COST ESTIMATE:")
    print("📊 25 images × $0.080 each = $2.00")
    print("⏱️  Generation time: ~15-20 minutes")
    print("")
    
    confirm = input("🚀 Ready to start image generation? (y/N): ")
    
    if confirm.lower() == 'y':
        generator.generate_all_images(max_images=25)
    else:
        print("📋 Generation cancelled")

if __name__ == "__main__":
    main() 