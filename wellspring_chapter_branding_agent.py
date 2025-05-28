#!/usr/bin/env python3
"""
Wellspring Chapter Branding Agent
=================================

Creates uniform, professional chapter covers matching the "Setting the Vision" aesthetic:
- Dark leather background texture
- Ornate gold decorative borders
- Classical architectural elements  
- Mystical symbols (sun, book, columns)
- Professional gold typography
- Consistent layout and spacing

This agent will analyze your perfect example and batch process chapter images
to match that exact style and quality.
"""

import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path
import sys
import re
from datetime import datetime

class WellspringChapterBrandingAgent:
    """Professional chapter cover generator matching Setting the Vision aesthetic"""
    
    def __init__(self):
        self.project_dir = Path("icons/wellspring_goldflake_batch_tool")
        self.input_dir = self.project_dir / "input_images"
        self.output_dir = self.project_dir / "processed_images" 
        self.textures_dir = self.project_dir / "textures"
        self.templates_dir = self.project_dir / "templates"
        
        # Create directories if they don't exist
        for dir_path in [self.input_dir, self.output_dir, self.textures_dir, self.templates_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # Style specifications based on "Setting the Vision"
        self.style_specs = {
            'background': {
                'base_color': '#1B1B2F',  # Dark navy/black
                'texture': 'leather_dark.png',
                'opacity': 0.95
            },
            'border': {
                'style': 'ornate_classical',
                'color': '#D4AF37',  # Rich gold
                'width': 12,
                'corner_flourishes': True
            },
            'typography': {
                'title_font': 'serif_elegant',  # Will map to available fonts
                'title_size': 48,
                'title_color': '#D4AF37',
                'title_position': 'bottom_third',
                'letter_spacing': 2
            },
            'symbols': {
                'central_symbol': 'sun_face_rays',  # The mystical sun
                'architectural': ['column_left', 'column_right'],
                'book_symbol': 'open_book_bottom',
                'symbol_color': '#D4AF37'
            },
            'layout': {
                'canvas_size': (600, 800),  # Portrait orientation
                'margin': 40,
                'symbol_spacing': 60,
                'title_margin_bottom': 80
            }
        }
    
    def analyze_reference_image(self, reference_path="setting-the-vision.png"):
        """Analyze the 'Setting the Vision' reference to extract style parameters"""
        
        print("🎨 ANALYZING REFERENCE IMAGE: Setting the Vision")
        print("=" * 55)
        
        if not Path(reference_path).exists():
            print(f"⚠️  Reference image not found: {reference_path}")
            print("📋 Using default style specifications based on description")
            return self.style_specs
            
        try:
            ref_img = Image.open(reference_path)
            width, height = ref_img.size
            
            print(f"📐 Reference dimensions: {width} × {height}")
            print(f"🎯 Aspect ratio: {width/height:.2f}")
            
            # Analyze color palette
            colors = ref_img.convert('RGB').getcolors(maxcolors=256*256*256)
            if colors:
                # Get dominant colors (simplified analysis)
                dominant = sorted(colors, key=lambda x: x[0], reverse=True)[:5]
                print(f"🎨 Dominant colors detected: {len(dominant)} color zones")
                
            # Update canvas size to match reference
            self.style_specs['layout']['canvas_size'] = (width, height)
            
            print("✅ Reference analysis complete")
            
        except Exception as e:
            print(f"❌ Error analyzing reference: {e}")
            print("📋 Using default specifications")
            
        return self.style_specs
    
    def create_base_template(self):
        """Create the base template with background, border, and architectural elements"""
        
        canvas_size = self.style_specs['layout']['canvas_size']
        img = Image.new('RGBA', canvas_size, (27, 27, 47, 255))  # Dark base
        draw = ImageDraw.Draw(img)
        
        # Add leather texture effect
        self._add_leather_texture(img)
        
        # Add ornate border
        self._add_ornate_border(img, draw)
        
        # Add architectural columns
        self._add_classical_columns(img, draw)
        
        return img
    
    def _add_leather_texture(self, img):
        """Add dark leather texture to background"""
        # Create subtle texture with noise
        width, height = img.size
        
        # Add subtle noise for leather texture
        noise = Image.new('RGBA', (width, height))
        noise_draw = ImageDraw.Draw(noise)
        
        # Simple noise pattern (in production, would use actual leather texture)
        import random
        for _ in range(width * height // 20):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            alpha = random.randint(10, 30)
            noise_draw.point([x, y], (255, 255, 255, alpha))
        
        # Blur for smoother texture
        noise = noise.filter(ImageFilter.GaussianBlur(radius=1.5))
        
        # Composite with base image
        img.alpha_composite(noise)
    
    def _add_ornate_border(self, img, draw):
        """Add ornate classical border with corner flourishes"""
        width, height = img.size
        border_width = self.style_specs['border']['width']
        gold = '#D4AF37'
        
        # Main border rectangle
        border_rect = [
            border_width,
            border_width, 
            width - border_width,
            height - border_width
        ]
        
        # Draw main border
        for i in range(3):  # Multiple lines for ornate effect
            draw.rectangle([
                border_rect[0] + i,
                border_rect[1] + i,
                border_rect[2] - i,
                border_rect[3] - i
            ], outline=gold, width=1)
        
        # Add corner flourishes (simplified)
        corner_size = 30
        for corner_x, corner_y in [(border_width, border_width), 
                                   (width-border_width-corner_size, border_width),
                                   (border_width, height-border_width-corner_size),
                                   (width-border_width-corner_size, height-border_width-corner_size)]:
            
            # Simple corner ornament (would be more elaborate in production)
            draw.rectangle([corner_x, corner_y, corner_x+corner_size, corner_y+corner_size], 
                         outline=gold, width=2)
            draw.line([corner_x+5, corner_y+5, corner_x+corner_size-5, corner_y+corner_size-5], 
                     fill=gold, width=1)
            draw.line([corner_x+corner_size-5, corner_y+5, corner_x+5, corner_y+corner_size-5], 
                     fill=gold, width=1)
    
    def _add_classical_columns(self, img, draw):
        """Add classical architectural columns on left and right"""
        width, height = img.size
        gold = '#D4AF37'
        
        # Column specifications
        column_width = 60
        column_height = height // 3
        column_top = height // 4
        
        # Left column
        left_x = width // 6
        self._draw_column(draw, left_x, column_top, column_width, column_height, gold)
        
        # Right column  
        right_x = width - width // 6 - column_width
        self._draw_column(draw, right_x, column_top, column_width, column_height, gold)
    
    def _draw_column(self, draw, x, y, width, height, color):
        """Draw a classical column with capital and base"""
        
        # Column shaft
        shaft_width = width // 2
        shaft_x = x + width // 4
        draw.rectangle([shaft_x, y + 20, shaft_x + shaft_width, y + height - 20], 
                      outline=color, width=2)
        
        # Column capital (top)
        draw.rectangle([x, y, x + width, y + 20], outline=color, width=2)
        
        # Column base (bottom)
        draw.rectangle([x, y + height - 20, x + width, y + height], outline=color, width=2)
        
        # Decorative lines on shaft
        for i in range(3):
            line_y = y + 30 + i * (height - 60) // 3
            draw.line([shaft_x + 5, line_y, shaft_x + shaft_width - 5, line_y], 
                     fill=color, width=1)
    
    def add_central_symbol(self, img, symbol_type="sun_face"):
        """Add the central mystical symbol (sun with face, radiating beams)"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Central position
        center_x = width // 2
        center_y = height // 3
        
        gold = '#D4AF37'
        
        if symbol_type == "sun_face":
            # Central circle (face)
            face_radius = 40
            draw.ellipse([
                center_x - face_radius,
                center_y - face_radius,
                center_x + face_radius,
                center_y + face_radius
            ], outline=gold, width=3)
            
            # Radiating beams
            beam_count = 16
            beam_length = 60
            import math
            
            for i in range(beam_count):
                angle = (2 * math.pi * i) / beam_count
                start_x = center_x + int((face_radius + 10) * math.cos(angle))
                start_y = center_y + int((face_radius + 10) * math.sin(angle))
                end_x = center_x + int((face_radius + beam_length) * math.cos(angle))
                end_y = center_y + int((face_radius + beam_length) * math.sin(angle))
                
                draw.line([start_x, start_y, end_x, end_y], fill=gold, width=2)
            
            # Simple face features
            eye_offset = 12
            draw.ellipse([center_x - eye_offset - 3, center_y - 8, 
                         center_x - eye_offset + 3, center_y - 2], fill=gold)
            draw.ellipse([center_x + eye_offset - 3, center_y - 8, 
                         center_x + eye_offset + 3, center_y - 2], fill=gold)
            
            # Smile
            draw.arc([center_x - 15, center_y, center_x + 15, center_y + 20], 
                    start=0, end=180, fill=gold, width=2)
    
    def add_book_symbol(self, img):
        """Add open book symbol at bottom"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        book_x = width // 2
        book_y = height - 120
        book_width = 80
        book_height = 30
        
        gold = '#D4AF37'
        
        # Open book shape
        # Left page
        draw.polygon([
            (book_x - book_width//2, book_y),
            (book_x - 5, book_y - 10),
            (book_x - 5, book_y + book_height - 10),
            (book_x - book_width//2, book_y + book_height)
        ], outline=gold, width=2)
        
        # Right page
        draw.polygon([
            (book_x + book_width//2, book_y),
            (book_x + 5, book_y - 10),
            (book_x + 5, book_y + book_height - 10),
            (book_x + book_width//2, book_y + book_height)
        ], outline=gold, width=2)
        
        # Book lines (pages)
        for i in range(3):
            y_offset = book_y + 8 + i * 6
            draw.line([book_x - book_width//2 + 8, y_offset, 
                      book_x - 8, y_offset], fill=gold, width=1)
            draw.line([book_x + 8, y_offset, 
                      book_x + book_width//2 - 8, y_offset], fill=gold, width=1)
    
    def add_chapter_title(self, img, title_text):
        """Add chapter title with professional gold typography"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Try to load a good font, fallback to default
        try:
            # Common serif fonts that might be available
            font_options = [
                "Georgia-Bold.ttf",
                "Times-Bold.ttf", 
                "TimesNewRomanPS-BoldMT.ttf",
                "/System/Library/Fonts/Times.ttc",
                "/System/Library/Fonts/Georgia.ttc"
            ]
            
            font = None
            font_size = 48
            
            for font_path in font_options:
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    break
                except:
                    continue
                    
            if not font:
                font = ImageFont.load_default()
                
        except:
            font = ImageFont.load_default()
        
        # Position title in bottom third
        title_y = height - 150
        
        # Get text dimensions for centering
        bbox = draw.textbbox((0, 0), title_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        
        gold = '#D4AF37'
        
        # Add text shadow for depth
        shadow_offset = 2
        draw.text((text_x + shadow_offset, title_y + shadow_offset), 
                 title_text, font=font, fill='#000000AA')
        
        # Main text
        draw.text((text_x, title_y), title_text, font=font, fill=gold)
    
    def process_single_chapter(self, input_path, output_path, chapter_title=None):
        """Process a single chapter image to match the Setting the Vision style"""
        
        print(f"🎨 Processing: {Path(input_path).name}")
        
        try:
            # Create base template
            base_template = self.create_base_template()
            
            # Add all decorative elements
            self.add_central_symbol(base_template, "sun_face")
            self.add_book_symbol(base_template)
            
            # Extract chapter title if not provided
            if not chapter_title:
                filename = Path(input_path).stem
                # Clean up filename to create title
                chapter_title = re.sub(r'[_-]', ' ', filename).title()
                chapter_title = re.sub(r'\d+', '', chapter_title).strip()
                
                if not chapter_title:
                    chapter_title = "Chapter Title"
            
            # Add chapter title
            self.add_chapter_title(base_template, chapter_title)
            
            # Save processed image
            base_template.save(output_path, 'PNG', quality=95)
            print(f"✅ Saved: {output_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing {input_path}: {e}")
            return False
    
    def batch_process_chapters(self):
        """Batch process all chapter images in the input directory"""
        
        print("🎨 WELLSPRING CHAPTER BRANDING BATCH PROCESSOR")
        print("=" * 55)
        print("🎯 Creating uniform chapter covers matching 'Setting the Vision' style")
        print("")
        
        # Analyze reference style
        style_specs = self.analyze_reference_image()
        
        # Find all input images
        input_files = list(self.input_dir.glob("*.png")) + list(self.input_dir.glob("*.jpg"))
        
        if not input_files:
            print(f"❌ No images found in {self.input_dir}")
            print(f"📋 Please add your chapter images to: {self.input_dir}")
            return False
            
        print(f"📁 Found {len(input_files)} images to process")
        print("")
        
        # Process each image
        successful = 0
        failed = 0
        
        for input_file in input_files:
            output_file = self.output_dir / f"branded_{input_file.name}"
            
            if self.process_single_chapter(input_file, output_file):
                successful += 1
            else:
                failed += 1
        
        print("")
        print("🎉 BATCH PROCESSING COMPLETE!")
        print(f"✅ Successfully processed: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"📁 Output directory: {self.output_dir}")
        
        return successful > 0

def main():
    """Main execution"""
    
    print("🌊 WELLSPRING CHAPTER BRANDING AGENT")
    print("=" * 40)
    print("🎨 Creating professional chapter covers")
    print("✨ Matching 'Setting the Vision' aesthetic")
    print("")
    
    agent = WellspringChapterBrandingAgent()
    
    # Check if user wants to process immediately or set up
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "analyze":
        # Just analyze the reference image
        agent.analyze_reference_image()
    elif len(sys.argv) > 1 and sys.argv[1] == "single":
        # Process single image
        if len(sys.argv) >= 4:
            input_path = sys.argv[2]
            output_path = sys.argv[3]
            title = sys.argv[4] if len(sys.argv) > 4 else None
            agent.process_single_chapter(input_path, output_path, title)
        else:
            print("Usage: python wellspring_chapter_branding_agent.py single input.png output.png 'Title'")
    else:
        # Batch process all images
        success = agent.batch_process_chapters()
        
        if success:
            print("\n🚀 READY FOR YOUR REVIEW!")
            print("1. Check the processed images in the output directory")
            print("2. Compare with your 'Setting the Vision' reference")
            print("3. Let me know what adjustments you'd like!")
        else:
            print("\n📋 SETUP REQUIRED:")
            print("1. Add your chapter images to: icons/wellspring_goldflake_batch_tool/input_images/")
            print("2. Run this script again")
            print("3. Review the generated covers")

if __name__ == "__main__":
    main() 