#!/usr/bin/env python3
"""
Em Dash Processor for Wellspring Book Production
Applies contextual em dash replacements based on analysis database.
"""

import re
import json
import sqlite3
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ReplacementRule:
    """Represents a replacement rule from the database."""
    id: int
    original_text: str
    context_before: str
    context_after: str
    replacement_text: str
    replacement_type: str
    confidence_score: float
    chapter_location: str

@dataclass
class ProcessingSession:
    """Represents a processing session."""
    session_name: str
    input_file: Path
    output_file: Path
    dry_run: bool = True
    confidence_threshold: float = 0.8
    
class EmDashProcessor:
    """Processes files to replace em dashes with appropriate punctuation."""
    
    def __init__(self, db_path: str = None):
        """Initialize the processor with database connection."""
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "shared_utils" / "data" / "wellspring.db"
        
        self.db_path = Path(db_path)
        self.replacement_stats = {
            'total_found': 0,
            'total_replaced': 0,
            'by_type': {},
            'skipped_low_confidence': 0,
            'manual_review_needed': []
        }
    
    def load_replacement_rules(self, chapter_location: str = None, confidence_threshold: float = 0.8) -> List[ReplacementRule]:
        """Load replacement rules from database."""
        if not self.db_path.exists():
            logger.error(f"Database not found: {self.db_path}")
            return []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
                SELECT id, original_text, context_before, context_after, replacement_text, 
                       replacement_type, confidence_score, chapter_location
                FROM em_dash_patterns
                WHERE confidence_score >= ?
            """
            params = [confidence_threshold]
            
            if chapter_location:
                query += " AND chapter_location = ?"
                params.append(chapter_location)
            
            query += " ORDER BY confidence_score DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            rules = []
            for row in rows:
                rule = ReplacementRule(
                    id=row[0],
                    original_text=row[1],
                    context_before=row[2],
                    context_after=row[3],
                    replacement_text=row[4],
                    replacement_type=row[5],
                    confidence_score=row[6],
                    chapter_location=row[7]
                )
                rules.append(rule)
            
            conn.close()
            logger.info(f"Loaded {len(rules)} replacement rules from database")
            return rules
            
        except Exception as e:
            logger.error(f"Error loading replacement rules: {e}")
            return []
    
    def process_file(self, session: ProcessingSession) -> Dict:
        """Process a file with em dash replacements."""
        logger.info(f"Processing file: {session.input_file}")
        logger.info(f"Dry run: {session.dry_run}")
        
        if not session.input_file.exists():
            logger.error(f"Input file not found: {session.input_file}")
            return {'success': False, 'error': 'Input file not found'}
        
        try:
            # Read input file
            with open(session.input_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Process content
            processed_content, processing_stats = self._process_content(original_content, session)
            
            # Save results
            if not session.dry_run:
                # Create output directory if it doesn't exist
                session.output_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Create backup of original file
                backup_path = session.output_file.parent / f"{session.input_file.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                shutil.copy2(session.input_file, backup_path)
                logger.info(f"Backup created: {backup_path}")
                
                # Write processed content
                with open(session.output_file, 'w', encoding='utf-8') as f:
                    f.write(processed_content)
                
                logger.info(f"Processed file saved: {session.output_file}")
            
            # Log session to database
            self._log_processing_session(session, processing_stats)
            
            return {
                'success': True,
                'stats': processing_stats,
                'output_file': str(session.output_file) if not session.dry_run else None,
                'processed_content': processed_content if session.dry_run else None
            }
            
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return {'success': False, 'error': str(e)}
    
    def _process_content(self, content: str, session: ProcessingSession) -> Tuple[str, Dict]:
        """Process content for em dash replacements."""
        lines = content.split('\n')
        processed_lines = []
        stats = {
            'total_em_dashes': 0,
            'replacements_made': 0,
            'by_type': {},
            'skipped_low_confidence': 0,
            'manual_review_needed': []
        }
        
        # Load replacement rules
        rules = self.load_replacement_rules(confidence_threshold=session.confidence_threshold)
        
        for line_num, line in enumerate(lines, 1):
            processed_line = line
            em_dash_count = line.count('—')
            stats['total_em_dashes'] += em_dash_count
            
            if em_dash_count > 0:
                processed_line = self._process_line(line, line_num, rules, stats)
            
            processed_lines.append(processed_line)
        
        processed_content = '\n'.join(processed_lines)
        return processed_content, stats
    
    def _process_line(self, line: str, line_num: int, rules: List[ReplacementRule], stats: Dict) -> str:
        """Process a single line for em dash replacements."""
        processed_line = line
        
        # Find all em dash positions
        em_dash_positions = [match.start() for match in re.finditer('—', line)]
        
        # Process from right to left to maintain position indices
        for position in reversed(em_dash_positions):
            context_before = line[:position].strip()
            context_after = line[position+1:].strip()
            
            # Find best matching rule
            best_rule = self._find_best_rule(context_before, context_after, rules)
            
            if best_rule:
                # Apply replacement
                replacement = self._determine_replacement_character(best_rule.replacement_type)
                processed_line = processed_line[:position] + replacement + processed_line[position+1:]
                
                # Update statistics
                stats['replacements_made'] += 1
                stats['by_type'][best_rule.replacement_type] = stats['by_type'].get(best_rule.replacement_type, 0) + 1
                
                logger.debug(f"Line {line_num}: Replaced em dash with '{replacement}' (type: {best_rule.replacement_type}, confidence: {best_rule.confidence_score})")
            else:
                # No rule found - add to manual review
                stats['skipped_low_confidence'] += 1
                stats['manual_review_needed'].append({
                    'line_number': line_num,
                    'context_before': context_before[-30:] if len(context_before) > 30 else context_before,
                    'context_after': context_after[:30] if len(context_after) > 30 else context_after,
                    'reason': 'No matching rule found'
                })
                
                logger.warning(f"Line {line_num}: Em dash needs manual review - no matching rule")
        
        return processed_line
    
    def _find_best_rule(self, context_before: str, context_after: str, rules: List[ReplacementRule]) -> Optional[ReplacementRule]:
        """Find the best matching rule for the given context."""
        best_rule = None
        best_score = 0
        
        for rule in rules:
            # Calculate similarity score
            score = self._calculate_context_similarity(context_before, context_after, rule)
            
            if score > best_score and score > 0.5:  # Minimum similarity threshold
                best_score = score
                best_rule = rule
        
        return best_rule
    
    def _calculate_context_similarity(self, context_before: str, context_after: str, rule: ReplacementRule) -> float:
        """Calculate similarity between current context and rule context."""
        # Simple similarity based on word overlap and length similarity
        before_words = set(context_before.lower().split())
        after_words = set(context_after.lower().split())
        
        rule_before_words = set(rule.context_before.lower().split())
        rule_after_words = set(rule.context_after.lower().split())
        
        # Calculate word overlap
        before_overlap = len(before_words & rule_before_words) / max(len(before_words | rule_before_words), 1)
        after_overlap = len(after_words & rule_after_words) / max(len(after_words | rule_after_words), 1)
        
        # Calculate length similarity
        before_len_sim = 1 - abs(len(context_before) - len(rule.context_before)) / max(len(context_before) + len(rule.context_before), 1)
        after_len_sim = 1 - abs(len(context_after) - len(rule.context_after)) / max(len(context_after) + len(rule.context_after), 1)
        
        # Combined similarity score
        similarity = (before_overlap + after_overlap + before_len_sim + after_len_sim) / 4
        
        # Boost score by rule confidence
        return similarity * rule.confidence_score
    
    def _determine_replacement_character(self, replacement_type: str) -> str:
        """Determine the replacement character based on type."""
        replacement_map = {
            'comma': ',',
            'period': '.',
            'semicolon': ';',
            'colon': ':',
            'parentheses': ' (',  # Note: This would need more complex handling for closing parenthesis
            'space': ' ',
            'nothing': ''
        }
        
        return replacement_map.get(replacement_type, ',')  # Default to comma
    
    def _log_processing_session(self, session: ProcessingSession, stats: Dict) -> bool:
        """Log processing session to database."""
        if not self.db_path.exists():
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO typography_sessions 
                (session_name, input_file_path, output_file_path, em_dashes_found, 
                 em_dashes_replaced, replacement_patterns, processing_status, started_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_name,
                str(session.input_file),
                str(session.output_file) if not session.dry_run else None,
                stats['total_em_dashes'],
                stats['replacements_made'],
                json.dumps(stats['by_type']),
                'dry_run' if session.dry_run else 'completed',
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            logger.info("Processing session logged to database")
            return True
            
        except Exception as e:
            logger.error(f"Error logging session: {e}")
            return False
    
    def generate_processing_report(self, stats: Dict) -> str:
        """Generate a comprehensive processing report."""
        report = []
        report.append("=" * 60)
        report.append("📊 EM DASH PROCESSING REPORT")
        report.append("=" * 60)
        report.append(f"Total em dashes found: {stats['total_em_dashes']}")
        report.append(f"Replacements made: {stats['replacements_made']}")
        report.append(f"Success rate: {(stats['replacements_made'] / max(stats['total_em_dashes'], 1)) * 100:.1f}%")
        report.append(f"Skipped (low confidence): {stats['skipped_low_confidence']}")
        
        if stats['by_type']:
            report.append("\n📋 Replacements by Type:")
            for rep_type, count in stats['by_type'].items():
                report.append(f"  • {rep_type}: {count}")
        
        if stats['manual_review_needed']:
            report.append(f"\n⚠️  Manual Review Needed ({len(stats['manual_review_needed'])} cases):")
            for i, item in enumerate(stats['manual_review_needed'][:5], 1):  # Show first 5
                report.append(f"  {i}. Line {item['line_number']}: ...{item['context_before']} — {item['context_after']}...")
            
            if len(stats['manual_review_needed']) > 5:
                report.append(f"  ... and {len(stats['manual_review_needed']) - 5} more cases")
        
        report.append("=" * 60)
        
        return '\n'.join(report)

def main():
    """Main function to run em dash processing."""
    print("🔧 Em Dash Processor for Wellspring Book")
    print("=" * 50)
    
    # Initialize processor
    processor = EmDashProcessor()
    
    # Create sample input file for testing
    sample_input = Path("em_dash_replacement/input/sample_chapter.txt")
    sample_input.parent.mkdir(parents=True, exist_ok=True)
    
    sample_content = """Chapter 1: Setting the Vision

This chapter covers the fundamentals—planning and vision development.

The manual provides best practices—rapid delivery methods for behavioral health facilities.

There are several key phases: planning, permitting—and construction oversight.

Behavioral health facilities—complex projects by nature—require specialized expertise and careful coordination.

The development process includes these components—site selection, design development, and regulatory compliance.

Each phase has specific requirements—detailed documentation and stakeholder coordination are essential.
"""
    
    with open(sample_input, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    print(f"📝 Created sample input file: {sample_input}")
    
    # Create processing session
    session = ProcessingSession(
        session_name="sample_chapter_dry_run",
        input_file=sample_input,
        output_file=Path("em_dash_replacement/output/sample_chapter_processed.txt"),
        dry_run=True,  # Start with dry run
        confidence_threshold=0.5  # Lower threshold for testing
    )
    
    # Process file
    result = processor.process_file(session)
    
    if result['success']:
        print("\n✅ Processing completed successfully!")
        
        # Display processed content (dry run)
        if session.dry_run and result['processed_content']:
            print("\n📄 Processed Content Preview:")
            print("-" * 40)
            print(result['processed_content'][:500] + "..." if len(result['processed_content']) > 500 else result['processed_content'])
            print("-" * 40)
        
        # Display report
        report = processor.generate_processing_report(result['stats'])
        print(f"\n{report}")
        
        # Suggest next steps
        if result['stats']['manual_review_needed']:
            print(f"\n💡 Next Steps:")
            print(f"  1. Review {len(result['stats']['manual_review_needed'])} cases manually")
            print(f"  2. Add specific rules to improve accuracy")
            print(f"  3. Re-run with higher confidence threshold")
        else:
            print(f"\n💡 Ready for production processing!")
            print(f"  Run with dry_run=False to apply changes")
    else:
        print(f"\n❌ Processing failed: {result['error']}")

if __name__ == "__main__":
    main()