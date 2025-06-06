#!/usr/bin/env python3
"""
TTS Chapter Processor for Behavioral Health Chapters

This script processes the enhanced chapters for text-to-speech conversion by:
1. Removing markdown formatting
2. Expanding abbreviations
3. Cleaning up text for better audio pronunciation
4. Creating properly formatted text files ready for TTS

Usage:
    python tts_chapter_processor.py
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TTSChapterProcessor:
    def __init__(self):
        # Define abbreviation expansions for first-time use
        self.abbreviations = {
            'DBIA': 'Design-Build Institute of America',
            'AIA': 'American Institute of Architects',
            'DHCS': 'Department of Health Care Services',
            'OSHPD': 'Office of Statewide Health Planning and Development',
            'HCAI': 'Health Care Access and Information',
            'POE': 'Post-Occupancy Evaluation',
            'RFI': 'Request for Information',
            'GMP': 'Guaranteed Maximum Price',
            'DSM': 'Diagnostic and Statistical Manual',
            'HIPAA': 'Health Insurance Portability and Accountability Act',
            'CMS': 'Centers for Medicare and Medicaid Services',
            'EPA': 'Environmental Protection Agency',
            'OSHA': 'Occupational Safety and Health Administration',
            'ADA': 'Americans with Disabilities Act',
            'HVAC': 'Heating, Ventilation, and Air Conditioning',
            'LED': 'Light Emitting Diode',
            'LEED': 'Leadership in Energy and Environmental Design',
            'ROI': 'Return on Investment',
            'QA': 'Quality Assurance',
            'QC': 'Quality Control',
            'FFE': 'Furniture, Fixtures, and Equipment',
            'MEP': 'Mechanical, Electrical, and Plumbing',
            'BIM': 'Building Information Modeling',
            'VE': 'Value Engineering',
            'CM': 'Construction Manager',
            'GC': 'General Contractor',
            'SOW': 'Scope of Work',
            'ITB': 'Invitation to Bid',
            'RFP': 'Request for Proposal',
            'NDA': 'Non-Disclosure Agreement',
            'LOI': 'Letter of Intent',
            'CO': 'Change Order',
            'TCO': 'Temporary Certificate of Occupancy',
            'CCO': 'Certificate of Completion and Occupancy',
        }
        
        # Track which abbreviations have been expanded in each chapter
        self.expanded_abbreviations = set()
        
        # Chapter titles for proper naming
        self.chapter_titles = {
            'CH1': 'Foundations',
            'CH2': 'Strategic_Planning',
            'CH3': 'Team_Assembly',
            'CH4': 'Site_Selection',
            'CH5': 'Stakeholder_Support',
            'CH6': 'Community_Engagement',
            'CH7': 'Financial_Planning',
            'CH8': 'Design_Process',
            'CH9': 'Design_Best_Practices',
            'CH10': 'Construction_Management',
            'CH11': 'Best_Practices',
            'CH12': 'Operations_Planning',
            'CH13': 'Quality_Metrics',
            'CH14': 'Technology_Integration',
            'CH15': 'Sustainability',
            'CH16': 'Risk_Management',
            'CH17': 'Case_Studies',
            'CH18': 'Implementation',
            'CH19': 'Call_to_Action'
        }
    
    def clean_markdown_formatting(self, text: str) -> str:
        """Remove markdown formatting for TTS conversion"""
        # Remove markdown headers but preserve text
        text = re.sub(r'^#{1,6}\s+(.+)$', r'\1', text, flags=re.MULTILINE)
        
        # Remove bold/italic formatting
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
        
        # Convert bullet points to flowing text
        text = re.sub(r'^\s*[-•*]\s+(.+)$', r'\1.', text, flags=re.MULTILINE)
        
        # Remove numbered list formatting but preserve content
        text = re.sub(r'^\s*\d+\.\s+(.+)$', r'\1.', text, flags=re.MULTILINE)
        
        # Remove code blocks and inline code
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        # Remove links but preserve text
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        
        # Remove table formatting (convert to narrative if needed)
        text = re.sub(r'\|[^|\n]*\|', '', text)
        text = re.sub(r'^[-|:\s]+$', '', text, flags=re.MULTILINE)
        
        return text
    
    def expand_abbreviations(self, text: str) -> str:
        """Expand abbreviations on first use in chapter"""
        for abbrev, expansion in self.abbreviations.items():
            if abbrev in text and abbrev not in self.expanded_abbreviations:
                # Replace first occurrence with expansion + abbreviation
                pattern = r'\b' + re.escape(abbrev) + r'\b'
                replacement = f'{expansion} ({abbrev})'
                text = re.sub(pattern, replacement, text, count=1)
                self.expanded_abbreviations.add(abbrev)
        
        return text
    
    def improve_pronunciation(self, text: str) -> str:
        """Improve text for better TTS pronunciation"""
        # Add pauses for better pacing
        text = re.sub(r'([.!?])\s+([A-Z])', r'\1\n\n\2', text)
        
        # Handle numbers and percentages
        text = re.sub(r'\$(\d+)', r'\1 dollars', text)
        text = re.sub(r'(\d+)%', r'\1 percent', text)
        text = re.sub(r'(\d+)-(\d+)', r'\1 to \2', text)
        
        # Handle common terms that might be mispronounced
        pronunciation_fixes = {
            'e.g.': 'for example',
            'i.e.': 'that is',
            'etc.': 'and so on',
            'vs.': 'versus',
            'w/': 'with',
            '&': 'and',
            '@': 'at',
            '#': 'number',
        }
        
        for term, replacement in pronunciation_fixes.items():
            text = text.replace(term, replacement)
        
        return text
    
    def clean_whitespace(self, text: str) -> str:
        """Clean up excessive whitespace"""
        # Remove multiple consecutive blank lines
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        
        # Remove trailing whitespace
        text = '\n'.join(line.rstrip() for line in text.split('\n'))
        
        # Remove leading/trailing whitespace from entire text
        text = text.strip()
        
        return text
    
    def add_chapter_intro(self, chapter_num: str, content: str) -> str:
        """Add a spoken introduction to each chapter"""
        title = self.chapter_titles.get(chapter_num, f'Chapter {chapter_num}')
        title_spoken = title.replace('_', ' ')
        
        intro = f"Chapter {chapter_num.replace('CH', '')}: {title_spoken}\n\n"
        return intro + content
    
    def process_chapter(self, chapter_path: Path) -> str:
        """Process a single chapter for TTS"""
        logger.info(f"Processing {chapter_path.name}")
        
        # Reset abbreviation tracking for each chapter
        self.expanded_abbreviations.clear()
        
        # Read the chapter content
        with open(chapter_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract chapter number from filename
        chapter_match = re.search(r'Chapter_(CH\d+)_', chapter_path.name)
        chapter_num = chapter_match.group(1) if chapter_match else 'Unknown'
        
        # Apply processing steps
        content = self.clean_markdown_formatting(content)
        content = self.expand_abbreviations(content)
        content = self.improve_pronunciation(content)
        content = self.clean_whitespace(content)
        content = self.add_chapter_intro(chapter_num, content)
        
        return content
    
    def process_all_chapters(self, input_dir: str, output_dir: str):
        """Process all chapters in the input directory"""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        # Create output directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find all chapter files
        chapter_files = list(input_path.glob('Chapter_CH*_Enhanced.md'))
        chapter_files.sort()  # Sort for consistent processing order
        
        if not chapter_files:
            logger.error(f"No chapter files found in {input_dir}")
            return
        
        logger.info(f"Found {len(chapter_files)} chapters to process")
        
        # Process each chapter
        for chapter_file in chapter_files:
            try:
                processed_content = self.process_chapter(chapter_file)
                
                # Create output filename
                chapter_match = re.search(r'Chapter_(CH\d+)_', chapter_file.name)
                if chapter_match:
                    chapter_num = chapter_match.group(1)
                    title = self.chapter_titles.get(chapter_num, chapter_num)
                    output_filename = f"Chapter_{chapter_num.replace('CH', '').zfill(2)}_{title}.txt"
                else:
                    output_filename = chapter_file.stem + '_processed.txt'
                
                output_file = output_path / output_filename
                
                # Write processed content
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(processed_content)
                
                logger.info(f"Processed {chapter_file.name} -> {output_filename}")
                
            except Exception as e:
                logger.error(f"Error processing {chapter_file.name}: {e}")
        
        logger.info(f"Processing complete. Output files saved to {output_dir}")
        
        # Create a summary file
        self.create_summary_file(output_path, chapter_files)
    
    def create_summary_file(self, output_path: Path, chapter_files: List[Path]):
        """Create a summary file with processing information"""
        summary_content = [
            "# TTS Processing Summary",
            f"Processed {len(chapter_files)} chapters",
            "",
            "## Processed Files:",
        ]
        
        for chapter_file in chapter_files:
            chapter_match = re.search(r'Chapter_(CH\d+)_', chapter_file.name)
            if chapter_match:
                chapter_num = chapter_match.group(1)
                title = self.chapter_titles.get(chapter_num, chapter_num)
                summary_content.append(f"- Chapter {chapter_num.replace('CH', '')}: {title}")
        
        summary_content.extend([
            "",
            "## Processing Applied:",
            "- Removed markdown formatting",
            "- Expanded abbreviations on first use",
            "- Improved pronunciation",
            "- Added chapter introductions",
            "- Cleaned whitespace",
            "",
            "## Recommended TTS Settings:",
            "- Voice: Professional/authoritative",
            "- Speed: Slightly slower for technical content",
            "- Pauses: Natural at paragraph breaks",
            "- Format: High-quality audio (44.1kHz, 16-bit)"
        ])
        
        summary_file = output_path / "TTS_Processing_Summary.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(summary_content))

def main():
    """Main execution function"""
    processor = TTSChapterProcessor()
    
    # Define paths
    current_dir = Path(__file__).parent
    input_dir = current_dir / "google_adk_agents/agents/behavioral_health_sme_editing_agent/19_edits"
    output_dir = current_dir / "tts_prepared_chapters"
    
    if not input_dir.exists():
        logger.error(f"Input directory not found: {input_dir}")
        return
    
    logger.info("Starting TTS chapter processing...")
    processor.process_all_chapters(str(input_dir), str(output_dir))
    logger.info("TTS processing complete!")

if __name__ == "__main__":
    main()