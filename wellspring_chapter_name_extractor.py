#!/usr/bin/env python3
"""
Wellspring Chapter Name Extractor
=================================

Extracts chapter titles and section names from the Wellspring manuscript
to generate a complete list for icon creation.

Approaches:
1. Parse IDML file structure
2. Scan text content for chapter markers
3. Identify section headings and subsections
4. Create organized list for icon generation
"""

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import re
import json
from datetime import datetime

class WellspringChapterNameExtractor:
    """Extract chapter and section names from the manuscript"""
    
    def __init__(self, manuscript_path="docs/The-Wellspring-Book.idml"):
        self.manuscript_path = Path(manuscript_path)
        self.output_dir = Path("icons/wellspring_goldflake_batch_tool")
        self.chapters = []
        self.sections = []
        self.all_names = []
        
    def extract_from_idml(self):
        """Extract chapter and section names from IDML file"""
        
        print("📚 EXTRACTING CHAPTER NAMES FROM WELLSPRING MANUSCRIPT")
        print("=" * 60)
        
        if not self.manuscript_path.exists():
            print(f"❌ Manuscript not found: {self.manuscript_path}")
            return False
            
        try:
            with zipfile.ZipFile(self.manuscript_path, 'r') as idml_zip:
                # Get all story files
                story_files = [f for f in idml_zip.namelist() if f.startswith('Stories/')]
                
                print(f"📄 Found {len(story_files)} story files to scan")
                print("")
                
                chapter_patterns = [
                    r'Chapter\s+(\d+)[:\s]*(.+?)(?:\n|$)',
                    r'CHAPTER\s+(\d+)[:\s]*(.+?)(?:\n|$)', 
                    r'(\d+)\.\s*(.+?)(?:\n|$)',
                    r'Part\s+(\d+)[:\s]*(.+?)(?:\n|$)',
                ]
                
                section_patterns = [
                    r'^([A-Z][^.!?]*[.!?]?)\s*$',  # Lines that look like headings
                    r'Section\s+(.+?)(?:\n|$)',
                    r'[0-9]+\.[0-9]+\s+(.+?)(?:\n|$)',  # Numbered subsections
                ]
                
                found_chapters = set()
                found_sections = set()
                
                for story_file in story_files:
                    try:
                        # Read and decode story content
                        content = idml_zip.read(story_file).decode('utf-8', errors='ignore')
                        
                        # Look for chapter titles
                        for pattern in chapter_patterns:
                            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                            for match in matches:
                                if len(match.groups()) == 2:
                                    chapter_num = match.group(1)
                                    chapter_title = match.group(2).strip()
                                else:
                                    chapter_title = match.group(1).strip()
                                    chapter_num = len(found_chapters) + 1
                                
                                if chapter_title and len(chapter_title) > 3:
                                    chapter_name = f"Chapter {chapter_num}: {chapter_title}"
                                    found_chapters.add(chapter_name)
                        
                        # Look for section headings
                        lines = content.split('\n')
                        for line in lines:
                            line = line.strip()
                            
                            # Skip very short or very long lines
                            if len(line) < 5 or len(line) > 100:
                                continue
                                
                            # Look for section-like content
                            for pattern in section_patterns:
                                match = re.match(pattern, line)
                                if match:
                                    section_title = match.group(1).strip()
                                    if (section_title and 
                                        not re.search(r'\d{4}', section_title) and  # Skip years/dates
                                        not section_title.lower().startswith('page') and
                                        len(section_title.split()) <= 8):  # Reasonable length
                                        found_sections.add(section_title)
                        
                    except Exception as e:
                        print(f"⚠️  Error processing {story_file}: {e}")
                        continue
                
                # Convert to sorted lists
                self.chapters = sorted(list(found_chapters))
                self.sections = sorted(list(found_sections))
                
                print(f"✅ Found {len(self.chapters)} chapters")
                print(f"✅ Found {len(self.sections)} sections")
                
                return True
                
        except Exception as e:
            print(f"❌ Error extracting from IDML: {e}")
            return False
    
    def add_manual_entries(self):
        """Add common manuscript sections that might not be detected"""
        
        standard_sections = [
            "Table of Contents",
            "Introduction", 
            "Foreword",
            "Preface",
            "Setting the Vision",
            "Bibliography",
            "Index",
            "Acknowledgments",
            "About the Author",
            "Conclusion",
            "Summary",
            "References"
        ]
        
        print("📋 Adding standard manuscript sections...")
        
        for section in standard_sections:
            if section not in self.sections:
                self.sections.append(section)
        
        print(f"✅ Added {len(standard_sections)} standard sections")
    
    def create_icon_generation_list(self):
        """Create a comprehensive list for icon generation"""
        
        self.all_names = []
        
        # Add all chapters
        for chapter in self.chapters:
            self.all_names.append({
                'type': 'chapter',
                'name': chapter,
                'filename': self._sanitize_filename(chapter),
                'icon_style': 'chapter_cover'
            })
        
        # Add all sections  
        for section in self.sections:
            self.all_names.append({
                'type': 'section', 
                'name': section,
                'filename': self._sanitize_filename(section),
                'icon_style': 'section_header'
            })
        
        return self.all_names
    
    def _sanitize_filename(self, name):
        """Convert name to safe filename"""
        # Remove problematic characters
        safe_name = re.sub(r'[^a-zA-Z0-9\s\-_]', '', name)
        # Replace spaces with underscores
        safe_name = re.sub(r'\s+', '_', safe_name)
        # Limit length
        safe_name = safe_name[:50]
        # Ensure it's lowercase
        safe_name = safe_name.lower()
        return safe_name
    
    def save_extraction_results(self):
        """Save the extracted names to files for icon generation"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON for programmatic use
        json_file = self.output_dir / f"chapter_names_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump({
                'extracted_at': timestamp,
                'manuscript': str(self.manuscript_path),
                'chapters': self.chapters,
                'sections': self.sections,
                'icon_generation_list': self.all_names,
                'total_icons_needed': len(self.all_names)
            }, f, indent=2)
        
        # Save readable text file
        text_file = self.output_dir / f"chapter_names_{timestamp}.txt"
        with open(text_file, 'w') as f:
            f.write("WELLSPRING MANUSCRIPT - EXTRACTED NAMES\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("CHAPTERS:\n")
            f.write("-" * 20 + "\n")
            for i, chapter in enumerate(self.chapters, 1):
                f.write(f"{i:2d}. {chapter}\n")
            
            f.write("\nSECTIONS:\n") 
            f.write("-" * 20 + "\n")
            for i, section in enumerate(self.sections, 1):
                f.write(f"{i:2d}. {section}\n")
            
            f.write(f"\nTOTAL ICONS TO GENERATE: {len(self.all_names)}\n")
        
        print(f"💾 Saved extraction results:")
        print(f"   📄 JSON: {json_file}")
        print(f"   📝 Text: {text_file}")
        
        return json_file, text_file
    
    def display_results(self):
        """Display the extraction results"""
        
        print("\n📚 EXTRACTION RESULTS")
        print("=" * 40)
        
        if self.chapters:
            print(f"\n📖 CHAPTERS ({len(self.chapters)}):")
            for i, chapter in enumerate(self.chapters, 1):
                print(f"   {i:2d}. {chapter}")
        
        if self.sections:
            print(f"\n📋 SECTIONS ({len(self.sections)}):")
            for i, section in enumerate(self.sections[:10], 1):  # Show first 10
                print(f"   {i:2d}. {section}")
            
            if len(self.sections) > 10:
                print(f"   ... and {len(self.sections) - 10} more sections")
        
        print(f"\n🎨 TOTAL ICONS TO GENERATE: {len(self.all_names)}")

def main():
    """Main execution"""
    
    print("📚 WELLSPRING CHAPTER NAME EXTRACTOR")
    print("=" * 45)
    print("🎯 Extracting chapter and section names for icon generation")
    print("")
    
    extractor = WellspringChapterNameExtractor()
    
    # Extract from manuscript
    if extractor.extract_from_idml():
        # Add standard sections
        extractor.add_manual_entries()
        
        # Create icon generation list
        extractor.create_icon_generation_list()
        
        # Display results
        extractor.display_results()
        
        # Save results
        json_file, text_file = extractor.save_extraction_results()
        
        print("\n🚀 READY FOR ICON GENERATION!")
        print("📋 Next steps:")
        print("1. Review the extracted names above")
        print("2. Run the icon generator with these names")
        print("3. Generate uniform icons in 'Setting the Vision' style")
        
        return True
        
    else:
        print("❌ Failed to extract chapter names")
        print("📋 You can manually create a list of chapter/section names")
        return False

if __name__ == "__main__":
    main() 