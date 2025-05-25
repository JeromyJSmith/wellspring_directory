#!/usr/bin/env python3
"""
Em Dash Analyzer for Wellspring Book Production
Analyzes all em dash usage patterns and creates contextual replacement database.
"""

import re
import json
import sqlite3
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmDashMatch:
    """Represents an em dash match with its context."""
    original_text: str
    context_before: str
    context_after: str
    full_sentence: str
    line_number: int
    position: int
    suggested_replacement: str
    replacement_type: str
    confidence: float

class EmDashAnalyzer:
    """Analyzes em dash usage patterns and suggests appropriate replacements."""
    
    def __init__(self, db_path: str = None):
        """Initialize the analyzer with database connection."""
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "shared_utils" / "data" / "wellspring.db"
        
        self.db_path = Path(db_path)
        self.patterns = self._load_replacement_patterns()
        
    def _load_replacement_patterns(self) -> Dict[str, Dict]:
        """Load em dash replacement patterns based on context."""
        return {
            'list_separator': {
                'pattern': r'(\w+)\s*—\s*(\w+)',
                'replacement': r'\1, \2',
                'type': 'comma',
                'confidence': 0.9,
                'description': 'Em dash used as list separator'
            },
            'parenthetical': {
                'pattern': r'(\w+)\s*—\s*([^—]+)\s*—\s*(\w+)',
                'replacement': r'\1 (\2) \3',
                'type': 'parentheses',
                'confidence': 0.85,
                'description': 'Em dash pair for parenthetical expression'
            },
            'definition': {
                'pattern': r'(\w+)\s*—\s*([^.!?]+[.!?])',
                'replacement': r'\1: \2',
                'type': 'colon',
                'confidence': 0.8,
                'description': 'Em dash before definition or explanation'
            },
            'sentence_break': {
                'pattern': r'([.!?])\s*—\s*([A-Z])',
                'replacement': r'\1 \2',
                'type': 'period',
                'confidence': 0.9,
                'description': 'Em dash as sentence break'
            },
            'clause_separator': {
                'pattern': r'(\w+)\s*—\s*([^—]+)$',
                'replacement': r'\1; \2',
                'type': 'semicolon',
                'confidence': 0.7,
                'description': 'Em dash separating independent clauses'
            },
            'thought_break': {
                'pattern': r'(\w+)\s*—\s*(\w+)',
                'replacement': r'\1, \2',
                'type': 'comma',
                'confidence': 0.6,
                'description': 'Em dash as thought break'
            }
        }
    
    def analyze_file(self, file_path: Path) -> List[EmDashMatch]:
        """Analyze a single file for em dash patterns."""
        logger.info(f"Analyzing file: {file_path}")
        
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return []
        
        return self._analyze_content(content, str(file_path))
    
    def _analyze_content(self, content: str, source_file: str) -> List[EmDashMatch]:
        """Analyze content for em dash patterns."""
        matches = []
        lines = content.split('\n')
        
        # Find all em dashes (—) in the content
        em_dash_pattern = r'—'
        
        for line_num, line in enumerate(lines, 1):
            for match in re.finditer(em_dash_pattern, line):
                position = match.start()
                
                # Extract context around the em dash
                context_before = line[:position].strip()
                context_after = line[position+1:].strip()
                
                # Get full sentence context
                full_sentence = self._extract_sentence_context(lines, line_num - 1, position)
                
                # Analyze and suggest replacement
                replacement_info = self._suggest_replacement(context_before, context_after, full_sentence)
                
                em_dash_match = EmDashMatch(
                    original_text="—",
                    context_before=context_before[-50:] if len(context_before) > 50 else context_before,
                    context_after=context_after[:50] if len(context_after) > 50 else context_after,
                    full_sentence=full_sentence,
                    line_number=line_num,
                    position=position,
                    suggested_replacement=replacement_info['replacement'],
                    replacement_type=replacement_info['type'],
                    confidence=replacement_info['confidence']
                )
                
                matches.append(em_dash_match)
        
        logger.info(f"Found {len(matches)} em dash instances in {source_file}")
        return matches
    
    def _extract_sentence_context(self, lines: List[str], line_index: int, position: int) -> str:
        """Extract full sentence context around the em dash."""
        # Start from current line and expand to get full sentence
        sentence_chars = []
        
        # Get text before em dash
        current_line = lines[line_index]
        before_text = current_line[:position]
        
        # Look backwards for sentence start
        for i in range(len(before_text) - 1, -1, -1):
            char = before_text[i]
            sentence_chars.insert(0, char)
            if char in '.!?':
                break
        
        # Add the em dash
        sentence_chars.append('—')
        
        # Get text after em dash
        after_text = current_line[position + 1:]
        
        # Look forward for sentence end
        for char in after_text:
            sentence_chars.append(char)
            if char in '.!?':
                break
        
        return ''.join(sentence_chars).strip()
    
    def _suggest_replacement(self, before: str, after: str, full_sentence: str) -> Dict:
        """Suggest appropriate replacement for em dash based on context."""
        context = f"{before} — {after}"
        
        # Check each pattern
        for pattern_name, pattern_info in self.patterns.items():
            if re.search(pattern_info['pattern'], context, re.IGNORECASE):
                return {
                    'replacement': pattern_info['replacement'],
                    'type': pattern_info['type'],
                    'confidence': pattern_info['confidence'],
                    'pattern': pattern_name
                }
        
        # Default fallback analysis
        if before.endswith(('and', 'or', 'but')):
            return {'replacement': ',', 'type': 'comma', 'confidence': 0.8, 'pattern': 'conjunction'}
        elif re.search(r'\b(is|are|was|were)\s*$', before, re.IGNORECASE):
            return {'replacement': ':', 'type': 'colon', 'confidence': 0.7, 'pattern': 'definition'}
        elif before.strip().endswith(','):
            return {'replacement': ';', 'type': 'semicolon', 'confidence': 0.6, 'pattern': 'clause_separator'}
        else:
            return {'replacement': ',', 'type': 'comma', 'confidence': 0.5, 'pattern': 'default'}
    
    def save_analysis_to_db(self, matches: List[EmDashMatch], chapter_location: str = None) -> bool:
        """Save analysis results to database."""
        if not self.db_path.exists():
            logger.error(f"Database not found: {self.db_path}")
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Clear existing patterns for this chapter if specified
            if chapter_location:
                cursor.execute("DELETE FROM em_dash_patterns WHERE chapter_location = ?", (chapter_location,))
            
            # Insert new patterns
            for match in matches:
                cursor.execute("""
                    INSERT INTO em_dash_patterns 
                    (original_text, context_before, context_after, replacement_text, replacement_type, 
                     confidence_score, chapter_location, page_number, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    match.original_text,
                    match.context_before,
                    match.context_after,
                    match.suggested_replacement,
                    match.replacement_type,
                    match.confidence,
                    chapter_location or 'unknown',
                    match.line_number,  # Using line number as proxy for page
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Saved {len(matches)} em dash patterns to database")
            return True
            
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            return False
    
    def generate_analysis_report(self, matches: List[EmDashMatch]) -> Dict:
        """Generate comprehensive analysis report."""
        if not matches:
            return {'total_matches': 0, 'summary': 'No em dashes found'}
        
        # Group by replacement type
        type_counts = {}
        confidence_distribution = {'high': 0, 'medium': 0, 'low': 0}
        
        for match in matches:
            # Count by type
            type_counts[match.replacement_type] = type_counts.get(match.replacement_type, 0) + 1
            
            # Confidence distribution
            if match.confidence >= 0.8:
                confidence_distribution['high'] += 1
            elif match.confidence >= 0.6:
                confidence_distribution['medium'] += 1
            else:
                confidence_distribution['low'] += 1
        
        # Calculate statistics
        avg_confidence = sum(m.confidence for m in matches) / len(matches)
        high_confidence_count = sum(1 for m in matches if m.confidence >= 0.8)
        manual_review_needed = sum(1 for m in matches if m.confidence < 0.7)
        
        report = {
            'total_matches': len(matches),
            'replacement_types': type_counts,
            'confidence_distribution': confidence_distribution,
            'average_confidence': round(avg_confidence, 3),
            'high_confidence_replacements': high_confidence_count,
            'manual_review_needed': manual_review_needed,
            'ready_for_automation': high_confidence_count,
            'processing_recommendation': self._get_processing_recommendation(matches)
        }
        
        return report
    
    def _get_processing_recommendation(self, matches: List[EmDashMatch]) -> str:
        """Get processing recommendation based on analysis."""
        if not matches:
            return "No processing needed - no em dashes found"
        
        high_confidence = sum(1 for m in matches if m.confidence >= 0.8)
        total = len(matches)
        confidence_ratio = high_confidence / total
        
        if confidence_ratio >= 0.8:
            return "Proceed with automated replacement - high confidence"
        elif confidence_ratio >= 0.6:
            return "Proceed with caution - review medium confidence cases"
        else:
            return "Manual review required - many low confidence cases"

def main():
    """Main function to run em dash analysis."""
    print("🔍 Em Dash Analysis Tool for Wellspring Book")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = EmDashAnalyzer()
    
    # Example usage - in real usage, this would process the actual book files
    sample_text = """
    This is a test—with em dashes—that need replacement.
    The manual covers best practices—rapid delivery methods.
    There are several approaches: planning, permitting—and construction.
    Behavioral health facilities—complex projects—require expertise.
    """
    
    # Analyze sample content
    matches = analyzer._analyze_content(sample_text, "sample_text")
    
    # Generate report
    report = analyzer.generate_analysis_report(matches)
    
    # Display results
    print(f"\n📊 Analysis Results:")
    print(f"  • Total em dashes found: {report['total_matches']}")
    print(f"  • Average confidence: {report['average_confidence']}")
    print(f"  • High confidence replacements: {report['high_confidence_replacements']}")
    print(f"  • Manual review needed: {report['manual_review_needed']}")
    print(f"\n📋 Replacement Types:")
    for rep_type, count in report['replacement_types'].items():
        print(f"  • {rep_type}: {count}")
    
    print(f"\n💡 Recommendation: {report['processing_recommendation']}")
    
    # Save to database (if database exists)
    if analyzer.db_path.exists():
        analyzer.save_analysis_to_db(matches, "sample_chapter")
        print(f"\n✅ Results saved to database: {analyzer.db_path}")
    else:
        print(f"\n⚠️  Database not found - run init_database.py first")

if __name__ == "__main__":
    main()