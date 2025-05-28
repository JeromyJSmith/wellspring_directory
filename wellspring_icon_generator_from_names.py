#!/usr/bin/env python3
"""
Wellspring Icon Generator from Names
===================================

Generates uniform, professional icons from scratch based on chapter names, following the "Setting the Vision" style guide

No processing of existing images - pure generation based on text prompts.
"""

import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path
import re
import math
import random
from datetime import datetime

class WellspringIconGenerator:
    """Generate uniform icons from chapter names using Setting the Vision style"""
    
    def __init__(self):
        self.project_dir = Path("icons/wellspring_goldflake_batch_tool")
        self.output_dir = self.project_dir / "generated_icons"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Style guide based on "Setting the Vision"
        self.style_guide = {
            'canvas_size': (400, 400),  # Square format for icons
            'background': {
                'color': '#1B1B2F',  # Dark navy/black
                'texture': True
            },
            'border': {
                'color': '#D4AF37',  # Rich gold
                'width': 8,
                'style': 'ornate'
            },
            'typography': {
                'color': '#D4AF37',
                'main_size': 24,
                'sub_size': 16,
                'font_weight': 'bold'
            },
            'symbols': {
                'color': '#D4AF37',
                'size': 60,
                'position': 'center_upper'
            }
        }
        
        # Symbol mapping based on chapter content keywords
        self.symbol_mapping = {
            # Administrative/Leadership
            'vision': '☀',
            'mission': '⭐',
            'leadership': '👑',
            'team': '👥',
            'collaboration': '🤝',
            'stakeholder': '🏛',
            'engagement': '💬',
            'planning': '📋',
            
            # Design/Architecture  
            'design': '📐',
            'architect': '🏗',
            'building': '🏢',
            'construction': '🔨',
            'infrastructure': '🏗',
            'layout': '📐',
            'space': '🏠',
            'facility': '🏥',
            
            # Healthcare/Treatment
            'health': '⚕',
            'care': '❤',
            'treatment': '🩺',
            'therapy': '🧠',
            'healing': '✨',
            'recovery': '🌱',
            'wellness': '🍃',
            'safety': '🛡',
            
            # Financial/Legal
            'budget': '💰',
            'cost': '💲',
            'financial': '📊',
            'legal': '⚖',
            'compliance': '📜',
            'regulation': '📋',
            'attorney': '👩‍💼',
            
            # Technical/Engineering
            'engineer': '⚙',
            'technology': '💻',
            'system': '🔧',
            'mechanical': '⚙',
            'electrical': '⚡',
            'utility': '🔌',
            'hvac': '🌡',
            
            # Community/Environment
            'community': '🏘',
            'environment': '🌍',
            'sustainability': '♻',
            'accessibility': '♿',
            'transportation': '🚗',
            'zoning': '🗺',
            'landscape': '🌳',
            
            # Quality/Management
            'quality': '✅',
            'management': '📈',
            'coordination': '🔄',
            'documentation': '📝',
            'inspection': '🔍',
            'evaluation': '📊',
            'performance': '📈'
        }
        
    def clean_chapter_name(self, raw_name):
        """Clean up extracted chapter name, removing XML artifacts"""
        # Remove XML tags and content
        clean_name = re.sub(r'<[^>]+>', '', raw_name)
        clean_name = re.sub(r'&[^;]+;', '', clean_name)
        
        # Remove common artifacts
        clean_name = re.sub(r'\?\?ACE \d+\?\?', '', clean_name)
        clean_name = re.sub(r'encoding="[^"]*"', '', clean_name)
        clean_name = re.sub(r'standalone="[^"]*"', '', clean_name)
        clean_name = re.sub(r'DOMVersion="[^"]*"', '', clean_name)
        
        # Clean up whitespace and formatting
        clean_name = re.sub(r'\s+', ' ', clean_name)
        clean_name = clean_name.strip()
        
        # Extract just the meaningful title part
        if ':' in clean_name:
            parts = clean_name.split(':', 1)
            if len(parts) > 1:
                title_part = parts[1].strip()
                if title_part and len(title_part) > 3:
                    clean_name = title_part
        
        # Remove chapter numbering prefix for icon titles
        clean_name = re.sub(r'^Chapter \d+:\s*', '', clean_name)
        
        return clean_name[:50]  # Limit length
    
    def determine_symbol(self, chapter_name):
        """Determine appropriate symbol based on chapter content"""
        name_lower = chapter_name.lower()
        
        # Check for keyword matches
        for keyword, symbol in self.symbol_mapping.items():
            if keyword in name_lower:
                return symbol
        
        # Default symbols based on chapter patterns
        if any(word in name_lower for word in ['chapter 1', 'vision', 'mission']):
            return '☀'  # Sun for vision/leadership
        elif any(word in name_lower for word in ['design', 'architect', 'building']):
            return '🏗'  # Architecture
        elif any(word in name_lower for word in ['health', 'care', 'treatment']):
            return '⚕'  # Medical
        elif any(word in name_lower for word in ['team', 'collaboration', 'stakeholder']):
            return '👥'  # People/team
        elif any(word in name_lower for word in ['budget', 'cost', 'financial']):
            return '💰'  # Financial
        else:
            return '⭐'  # Default star
    
    def create_base_canvas(self):
        """Create the base canvas with background and border"""
        size = self.style_guide['canvas_size']
        
        # Create base image with dark background
        img = Image.new('RGBA', size, self.style_guide['background']['color'])
        draw = ImageDraw.Draw(img)
        
        # Add subtle texture
        if self.style_guide['background']['texture']:
            self.add_texture(img)
        
        # Add ornate border
        self.add_border(img, draw)
        
        return img, draw
    
    def add_texture(self, img):
        """Add subtle texture to background"""
        width, height = img.size
        
        # Create noise overlay
        noise = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        noise_draw = ImageDraw.Draw(noise)
        
        # Add random texture points
        for _ in range(width * height // 30):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            alpha = random.randint(5, 20)
            color = random.choice([(255, 255, 255, alpha), (212, 175, 55, alpha)])
            noise_draw.point([x, y], color)
        
        # Blur for smooth texture
        noise = noise.filter(ImageFilter.GaussianBlur(radius=1))
        
        # Composite with base
        img.alpha_composite(noise)
    
    def add_border(self, img, draw):
        """Add ornate gold border"""
        width, height = img.size
        border_width = self.style_guide['border']['width']
        gold = self.style_guide['border']['color']
        
        # Main border rectangle
        for i in range(3):
            draw.rectangle([
                border_width + i,
                border_width + i,
                width - border_width - i,
                height - border_width - i
            ], outline=gold, width=1)
        
        # Corner decorations
        corner_size = 20
        corners = [
            (border_width, border_width),
            (width - border_width - corner_size, border_width),
            (border_width, height - border_width - corner_size),
            (width - border_width - corner_size, height - border_width - corner_size)
        ]
        
        for corner_x, corner_y in corners:
            # Simple corner ornament
            draw.rectangle([
                corner_x, corner_y,
                corner_x + corner_size, corner_y + corner_size
            ], outline=gold, width=2)
            
            # Corner cross decoration
            mid_x = corner_x + corner_size // 2
            mid_y = corner_y + corner_size // 2
            draw.line([corner_x + 4, mid_y, corner_x + corner_size - 4, mid_y], fill=gold, width=1)
            draw.line([mid_x, corner_y + 4, mid_x, corner_y + corner_size - 4], fill=gold, width=1)
    
    def add_symbol(self, img, draw, symbol):
        """Add symbolic element to the icon"""
        width, height = img.size
        symbol_size = self.style_guide['symbols']['size']
        gold = self.style_guide['symbols']['color']
        
        # Position in upper center
        symbol_x = width // 2
        symbol_y = height // 3
        
        try:
            # Try to load a good font for the symbol
            font_options = [
                "/System/Library/Fonts/Arial Unicode.ttc",
                "/System/Library/Fonts/Apple Color Emoji.ttc",
                "arial.ttf"
            ]
            
            symbol_font = None
            for font_path in font_options:
                try:
                    symbol_font = ImageFont.truetype(font_path, symbol_size)
                    break
                except:
                    continue
            
            if not symbol_font:
                symbol_font = ImageFont.load_default()
            
            # Get text size for centering
            bbox = draw.textbbox((0, 0), symbol, font=symbol_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Center the symbol
            x = symbol_x - text_width // 2
            y = symbol_y - text_height // 2
            
            # Draw symbol with shadow
            draw.text((x + 2, y + 2), symbol, font=symbol_font, fill='#000000AA')
            draw.text((x, y), symbol, font=symbol_font, fill=gold)
            
        except Exception as e:
            # Fallback: draw a simple geometric shape
            draw.ellipse([
                symbol_x - 25, symbol_y - 25,
                symbol_x + 25, symbol_y + 25
            ], outline=gold, width=3)
    
    def add_title(self, img, draw, title):
        """Add chapter title text"""
        width, height = img.size
        gold = self.style_guide['typography']['color']
        
        # Load font
        try:
            font_options = [
                "/System/Library/Fonts/Georgia-Bold.ttc",
                "/System/Library/Fonts/Times-Bold.ttf",
                "georgia.ttf"
            ]
            
            title_font = None
            for font_path in font_options:
                try:
                    title_font = ImageFont.truetype(font_path, self.style_guide['typography']['main_size'])
                    break
                except:
                    continue
            
            if not title_font:
                title_font = ImageFont.load_default()
                
        except:
            title_font = ImageFont.load_default()
        
        # Split title into lines if too long
        words = title.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=title_font)
            text_width = bbox[2] - bbox[0]
            
            if text_width < width - 60:  # Leave margin
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Limit to 3 lines
        lines = lines[:3]
        
        # Position in lower portion
        start_y = height - 120 - (len(lines) * 30)
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + i * 35
            
            # Draw text with shadow
            draw.text((x + 1, y + 1), line, font=title_font, fill='#000000AA')
            draw.text((x, y), line, font=title_font, fill=gold)
    
    def generate_icon(self, chapter_name, output_path):
        """Generate a single icon for a chapter"""
        # Clean the chapter name
        clean_name = self.clean_chapter_name(chapter_name)
        
        if not clean_name or len(clean_name) < 3:
            print(f"⚠️  Skipping empty/invalid name: {chapter_name}")
            return False
        
        try:
            # Create base canvas
            img, draw = self.create_base_canvas()
            
            # Determine and add symbol
            symbol = self.determine_symbol(clean_name)
            self.add_symbol(img, draw, symbol)
            
            # Add title
            self.add_title(img, draw, clean_name)
            
            # Save icon
            img.save(output_path, 'PNG', quality=95)
            print(f"✅ Generated: {clean_name[:30]}... → {output_path.name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating icon for '{clean_name}': {e}")
            return False
    
    def process_chapter_names_file(self, json_file_path):
        """Process all chapter names from the extracted JSON file"""
        
        print("🎨 WELLSPRING ICON GENERATOR")
        print("=" * 40)
        print("✨ Generating uniform icons from chapter names")
        print("🎯 Using 'Setting the Vision' style guide")
        print("")
        
        # Load the extracted names
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        chapters = data.get('chapters', [])
        sections = data.get('sections', [])
        
        print(f"📚 Processing {len(chapters)} chapters")
        print(f"📋 Processing {len(sections)} sections")
        print("")
        
        successful = 0
        failed = 0
        
        # Process chapters
        for i, chapter in enumerate(chapters, 1):
            clean_name = self.clean_chapter_name(chapter)
            if clean_name and len(clean_name) > 3:
                filename = re.sub(r'[^a-zA-Z0-9\s\-_]', '', clean_name)
                filename = re.sub(r'\s+', '_', filename)[:40].lower()
                output_path = self.output_dir / f"chapter_{i:03d}_{filename}.png"
                
                if self.generate_icon(chapter, output_path):
                    successful += 1
                else:
                    failed += 1
        
        # Process sections
        for i, section in enumerate(sections, 1):
            clean_name = self.clean_chapter_name(section)
            if clean_name and len(clean_name) > 3:
                filename = re.sub(r'[^a-zA-Z0-9\s\-_]', '', clean_name)
                filename = re.sub(r'\s+', '_', filename)[:40].lower()
                output_path = self.output_dir / f"section_{i:03d}_{filename}.png"
                
                if self.generate_icon(section, output_path):
                    successful += 1
                else:
                    failed += 1
        
        print("")
        print("🎉 ICON GENERATION COMPLETE!")
        print(f"✅ Successfully generated: {successful} icons")
        print(f"❌ Failed: {failed} icons")
        print(f"📁 Output directory: {self.output_dir}")
        
        return successful > 0

def main():
    """Main execution"""
    
    # Find the most recent chapter names file
    project_dir = Path("icons/wellspring_goldflake_batch_tool")
    json_files = list(project_dir.glob("chapter_names_*.json"))
    
    if not json_files:
        print("❌ No chapter names file found!")
        print("📋 Please run: python wellspring_chapter_name_extractor.py first")
        return False
    
    # Use the most recent file
    latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
    
    print(f"📄 Using chapter names from: {latest_file.name}")
    print("")
    
    # Generate icons
    generator = WellspringIconGenerator()
    success = generator.process_chapter_names_file(latest_file)
    
    if success:
        print("\n🚀 READY FOR REVIEW!")
        print("1. Check the generated icons in the output directory")
        print("2. Compare with your 'Setting the Vision' reference")
        print("3. All icons follow the same uniform style!")
    
    return success

if __name__ == "__main__":
    main() 