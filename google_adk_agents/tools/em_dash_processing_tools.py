#!/usr/bin/env python3
"""
Google ADK Tools for Em Dash Processing
Provides specialized tools for the em_dash_processor agent.
"""

import re
import json
import sqlite3
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ReplacementRule:
    """Represents a replacement rule from analysis."""
    id: Optional[int]
    original_text: str
    context_before: str
    context_after: str
    replacement_text: str
    replacement_type: str
    confidence_score: float
    chapter_location: str
    reasoning: str

@dataclass
class ProcessingSession:
    """Represents a processing session configuration."""
    session_id: str
    session_name: str
    input_file: Path
    output_file: Path
    dry_run: bool
    confidence_threshold: float
    backup_enabled: bool
    rules_source: str  # 'database', 'file', 'inline'

@dataclass
class ProcessingResult:
    """Results from processing operation."""
    session_id: str
    input_file: str
    output_file: Optional[str]
    total_em_dashes: int
    replacements_made: int
    skipped_low_confidence: int
    replacement_breakdown: Dict[str, int]
    manual_review_items: List[Dict[str, Any]]
    processing_time: float
    backup_file: Optional[str]
    success: bool
    error_message: Optional[str]

class EmDashProcessingTools:
    """Tool implementations for em dash processing."""
    
    def __init__(self, db_path: str = None):
        """Initialize with database connection."""
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "shared_utils" / "data" / "wellspring.db"
        self.db_path = Path(db_path)

def load_replacement_rules(
    chapter_location: Optional[str] = None,
    confidence_threshold: float = 0.8,
    rule_types: Optional[List[str]] = None
) -> List[ReplacementRule]:
    """
    Load replacement rules from the database.
    
    Args:
        chapter_location: Specific chapter/document to load rules for
        confidence_threshold: Minimum confidence score for rules
        rule_types: Specific replacement types to include
        
    Returns:
        List[ReplacementRule]: Loaded replacement rules
    """
    tools = EmDashProcessingTools()
    
    try:
        if not tools.db_path.exists():
            logger.error(f"Database not found: {tools.db_path}")
            return []
        
        conn = sqlite3.connect(tools.db_path)
        cursor = conn.cursor()
        
        # Build query
        query = """
            SELECT id, original_text, context_before, context_after, replacement_text, 
                   replacement_type, confidence_score, chapter_location, reasoning
            FROM em_dash_patterns
            WHERE confidence_score >= ?
        """
        params = [confidence_threshold]
        
        if chapter_location:
            query += " AND chapter_location = ?"
            params.append(chapter_location)
        
        if rule_types:
            placeholders = ','.join(['?' for _ in rule_types])
            query += f" AND replacement_type IN ({placeholders})"
            params.extend(rule_types)
        
        query += " ORDER BY confidence_score DESC, id"
        
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
                chapter_location=row[7],
                reasoning=row[8] if len(row) > 8 else "No reasoning provided"
            )
            rules.append(rule)
        
        conn.close()
        logger.info(f"Loaded {len(rules)} replacement rules")
        return rules
        
    except Exception as e:
        logger.error(f"Error loading replacement rules: {e}")
        return []

def perform_dry_run(
    session: ProcessingSession,
    rules: Optional[List[ReplacementRule]] = None
) -> ProcessingResult:
    """
    Perform a dry run of em dash replacement without modifying files.
    
    Args:
        session: Processing session configuration
        rules: Optional list of rules to use (loads from DB if not provided)
        
    Returns:
        ProcessingResult: Dry run results
    """
    start_time = datetime.now()
    
    try:
        if not session.input_file.exists():
            return ProcessingResult(
                session_id=session.session_id,
                input_file=str(session.input_file),
                output_file=None,
                total_em_dashes=0,
                replacements_made=0,
                skipped_low_confidence=0,
                replacement_breakdown={},
                manual_review_items=[],
                processing_time=0.0,
                backup_file=None,
                success=False,
                error_message=f"Input file not found: {session.input_file}"
            )
        
        # Load rules if not provided
        if rules is None:
            rules = load_replacement_rules(
                chapter_location=str(session.input_file),
                confidence_threshold=session.confidence_threshold
            )
        
        # Read input content
        with open(session.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Process content
        processed_content, processing_stats = _process_content_with_rules(
            content, rules, session.confidence_threshold, dry_run=True
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        result = ProcessingResult(
            session_id=session.session_id,
            input_file=str(session.input_file),
            output_file=str(session.output_file) if not session.dry_run else None,
            total_em_dashes=processing_stats['total_em_dashes'],
            replacements_made=processing_stats['replacements_made'],
            skipped_low_confidence=processing_stats['skipped_low_confidence'],
            replacement_breakdown=processing_stats['replacement_breakdown'],
            manual_review_items=processing_stats['manual_review_items'],
            processing_time=processing_time,
            backup_file=None,
            success=True,
            error_message=None
        )
        
        logger.info(f"Dry run completed: {result.replacements_made}/{result.total_em_dashes} replacements")
        return result
        
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"Error in dry run: {e}")
        return ProcessingResult(
            session_id=session.session_id,
            input_file=str(session.input_file),
            output_file=None,
            total_em_dashes=0,
            replacements_made=0,
            skipped_low_confidence=0,
            replacement_breakdown={},
            manual_review_items=[],
            processing_time=processing_time,
            backup_file=None,
            success=False,
            error_message=str(e)
        )

def apply_replacements(
    session: ProcessingSession,
    rules: Optional[List[ReplacementRule]] = None,
    create_backup: bool = True
) -> ProcessingResult:
    """
    Apply em dash replacements to the actual file.
    
    Args:
        session: Processing session configuration
        rules: Optional list of rules to use
        create_backup: Whether to create backup before processing
        
    Returns:
        ProcessingResult: Processing results
    """
    start_time = datetime.now()
    backup_file = None
    
    try:
        if not session.input_file.exists():
            return ProcessingResult(
                session_id=session.session_id,
                input_file=str(session.input_file),
                output_file=None,
                total_em_dashes=0,
                replacements_made=0,
                skipped_low_confidence=0,
                replacement_breakdown={},
                manual_review_items=[],
                processing_time=0.0,
                backup_file=None,
                success=False,
                error_message=f"Input file not found: {session.input_file}"
            )
        
        # Create backup if requested
        if create_backup and session.backup_enabled:
            backup_file = create_backup_file(session.input_file)
            logger.info(f"Created backup: {backup_file}")
        
        # Load rules if not provided
        if rules is None:
            rules = load_replacement_rules(
                chapter_location=str(session.input_file),
                confidence_threshold=session.confidence_threshold
            )
        
        # Read input content
        with open(session.input_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Process content
        processed_content, processing_stats = _process_content_with_rules(
            original_content, rules, session.confidence_threshold, dry_run=False
        )
        
        # Create output directory if needed
        session.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write processed content
        with open(session.output_file, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        result = ProcessingResult(
            session_id=session.session_id,
            input_file=str(session.input_file),
            output_file=str(session.output_file),
            total_em_dashes=processing_stats['total_em_dashes'],
            replacements_made=processing_stats['replacements_made'],
            skipped_low_confidence=processing_stats['skipped_low_confidence'],
            replacement_breakdown=processing_stats['replacement_breakdown'],
            manual_review_items=processing_stats['manual_review_items'],
            processing_time=processing_time,
            backup_file=backup_file,
            success=True,
            error_message=None
        )
        
        logger.info(f"Processing completed: {result.replacements_made}/{result.total_em_dashes} replacements applied")
        return result
        
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"Error applying replacements: {e}")
        return ProcessingResult(
            session_id=session.session_id,
            input_file=str(session.input_file),
            output_file=None,
            total_em_dashes=0,
            replacements_made=0,
            skipped_low_confidence=0,
            replacement_breakdown={},
            manual_review_items=[],
            processing_time=processing_time,
            backup_file=backup_file,
            success=False,
            error_message=str(e)
        )

def create_backup(file_path: str, backup_dir: Optional[str] = None) -> str:
    """
    Create a backup of the specified file.
    
    Args:
        file_path: Path to file to backup
        backup_dir: Optional backup directory (defaults to file's parent)
        
    Returns:
        str: Path to the created backup file
    """
    try:
        source_path = Path(file_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {file_path}")
        
        # Determine backup location
        if backup_dir:
            backup_location = Path(backup_dir)
            backup_location.mkdir(parents=True, exist_ok=True)
        else:
            backup_location = source_path.parent
        
        # Generate backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{source_path.stem}_backup_{timestamp}{source_path.suffix}"
        backup_path = backup_location / backup_name
        
        # Create backup
        shutil.copy2(source_path, backup_path)
        
        logger.info(f"Backup created: {backup_path}")
        return str(backup_path)
        
    except Exception as e:
        logger.error(f"Error creating backup: {e}")
        raise

def validate_results(
    processing_result: ProcessingResult,
    expected_replacements: Optional[int] = None,
    max_manual_review_ratio: float = 0.2
) -> Dict[str, Any]:
    """
    Validate processing results against quality criteria.
    
    Args:
        processing_result: Results to validate
        expected_replacements: Expected number of replacements (optional)
        max_manual_review_ratio: Maximum acceptable ratio of manual review items
        
    Returns:
        Dict containing validation results
    """
    try:
        validation_result = {
            'overall_success': processing_result.success,
            'validation_passed': True,
            'issues': [],
            'metrics': {},
            'recommendations': []
        }
        
        if not processing_result.success:
            validation_result['validation_passed'] = False
            validation_result['issues'].append(f"Processing failed: {processing_result.error_message}")
            return validation_result
        
        # Calculate metrics
        total_found = processing_result.total_em_dashes
        replaced = processing_result.replacements_made
        manual_review_needed = len(processing_result.manual_review_items)
        
        replacement_rate = replaced / max(total_found, 1)
        manual_review_ratio = manual_review_needed / max(total_found, 1)
        
        validation_result['metrics'] = {
            'replacement_rate': replacement_rate,
            'manual_review_ratio': manual_review_ratio,
            'processing_efficiency': replaced / max(total_found, 1),
            'accuracy_confidence': sum(1 for breakdown in processing_result.replacement_breakdown.values()) / max(len(processing_result.replacement_breakdown), 1)
        }
        
        # Validate replacement rate
        if expected_replacements and abs(replaced - expected_replacements) > expected_replacements * 0.1:
            validation_result['issues'].append(f"Replacement count deviation: expected ~{expected_replacements}, got {replaced}")
        
        # Validate manual review ratio
        if manual_review_ratio > max_manual_review_ratio:
            validation_result['validation_passed'] = False
            validation_result['issues'].append(f"Too many manual review items: {manual_review_ratio:.1%} > {max_manual_review_ratio:.1%}")
        
        # Generate recommendations
        if replacement_rate < 0.8:
            validation_result['recommendations'].append("Consider lowering confidence threshold to increase replacement rate")
        
        if manual_review_ratio > 0.1:
            validation_result['recommendations'].append("Review and improve pattern recognition rules")
        
        if processing_result.processing_time > 60:
            validation_result['recommendations'].append("Consider optimizing processing performance")
        
        logger.info(f"Validation completed: {'PASSED' if validation_result['validation_passed'] else 'FAILED'}")
        return validation_result
        
    except Exception as e:
        logger.error(f"Error validating results: {e}")
        return {
            'overall_success': False,
            'validation_passed': False,
            'issues': [f"Validation error: {e}"],
            'metrics': {},
            'recommendations': []
        }

def log_session(
    processing_result: ProcessingResult,
    validation_result: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Log processing session to the database.
    
    Args:
        processing_result: Results from processing
        validation_result: Optional validation results
        
    Returns:
        bool: True if logged successfully
    """
    tools = EmDashProcessingTools()
    
    try:
        if not tools.db_path.exists():
            logger.error(f"Database not found: {tools.db_path}")
            return False
        
        conn = sqlite3.connect(tools.db_path)
        cursor = conn.cursor()
        
        # Log to typography_sessions table
        cursor.execute("""
            INSERT INTO typography_sessions 
            (session_name, input_file_path, output_file_path, em_dashes_found, 
             em_dashes_replaced, replacement_patterns, processing_status, 
             started_at, completed_at, processing_time_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            processing_result.session_id,
            processing_result.input_file,
            processing_result.output_file,
            processing_result.total_em_dashes,
            processing_result.replacements_made,
            json.dumps(processing_result.replacement_breakdown),
            'completed' if processing_result.success else 'failed',
            datetime.now().isoformat(),
            datetime.now().isoformat(),
            processing_result.processing_time
        ))
        
        # Log to agent_logs table
        cursor.execute("""
            INSERT INTO agent_logs 
            (agent_name, task_type, input_data, output_data, status, 
             started_at, completed_at, performance_metrics)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "em_dash_processor",
            "apply_replacements",
            json.dumps({
                'input_file': processing_result.input_file,
                'session_id': processing_result.session_id,
                'total_em_dashes': processing_result.total_em_dashes
            }),
            json.dumps({
                'replacements_made': processing_result.replacements_made,
                'manual_review_items': len(processing_result.manual_review_items),
                'replacement_breakdown': processing_result.replacement_breakdown,
                'validation_result': validation_result
            }),
            'completed' if processing_result.success else 'failed',
            datetime.now().isoformat(),
            datetime.now().isoformat(),
            json.dumps({
                'processing_time': processing_result.processing_time,
                'replacement_rate': processing_result.replacements_made / max(processing_result.total_em_dashes, 1),
                'success_rate': 1.0 if processing_result.success else 0.0
            })
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Session logged to database: {processing_result.session_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error logging session: {e}")
        return False

# Helper functions
def _process_content_with_rules(
    content: str,
    rules: List[ReplacementRule],
    confidence_threshold: float,
    dry_run: bool = False
) -> Tuple[str, Dict[str, Any]]:
    """Process content using replacement rules."""
    lines = content.split('\n')
    processed_lines = []
    
    stats = {
        'total_em_dashes': 0,
        'replacements_made': 0,
        'skipped_low_confidence': 0,
        'replacement_breakdown': {},
        'manual_review_items': []
    }
    
    for line_num, line in enumerate(lines, 1):
        processed_line = line
        em_dash_count = line.count('—')
        stats['total_em_dashes'] += em_dash_count
        
        if em_dash_count > 0:
            processed_line = _process_line_with_rules(
                line, line_num, rules, confidence_threshold, stats, dry_run
            )
        
        processed_lines.append(processed_line)
    
    return '\n'.join(processed_lines), stats

def _process_line_with_rules(
    line: str,
    line_num: int,
    rules: List[ReplacementRule],
    confidence_threshold: float,
    stats: Dict[str, Any],
    dry_run: bool
) -> str:
    """Process a single line with replacement rules."""
    processed_line = line
    
    # Find all em dash positions
    em_dash_positions = [match.start() for match in re.finditer('—', line)]
    
    # Process from right to left to maintain position indices
    for position in reversed(em_dash_positions):
        context_before = line[:position].strip()
        context_after = line[position+1:].strip()
        
        # Find best matching rule
        best_rule = _find_best_matching_rule(context_before, context_after, rules)
        
        if best_rule and best_rule.confidence_score >= confidence_threshold:
            # Apply replacement
            replacement = _get_replacement_character(best_rule.replacement_type, best_rule.replacement_text)
            
            if not dry_run:
                processed_line = processed_line[:position] + replacement + processed_line[position+1:]
            
            # Update statistics
            stats['replacements_made'] += 1
            stats['replacement_breakdown'][best_rule.replacement_type] = \
                stats['replacement_breakdown'].get(best_rule.replacement_type, 0) + 1
                
        else:
            # Add to manual review
            stats['skipped_low_confidence'] += 1
            stats['manual_review_items'].append({
                'line_number': line_num,
                'context_before': context_before[-30:] if len(context_before) > 30 else context_before,
                'context_after': context_after[:30] if len(context_after) > 30 else context_after,
                'reason': 'No matching rule found' if not best_rule else f'Low confidence: {best_rule.confidence_score:.2f}'
            })
    
    return processed_line

def _find_best_matching_rule(
    context_before: str,
    context_after: str,
    rules: List[ReplacementRule]
) -> Optional[ReplacementRule]:
    """Find the best matching rule for the given context."""
    best_rule = None
    best_score = 0.0
    
    for rule in rules:
        # Calculate similarity score
        score = _calculate_context_similarity(context_before, context_after, rule)
        
        if score > best_score:
            best_score = score
            best_rule = rule
    
    return best_rule if best_score > 0.3 else None  # Minimum similarity threshold

def _calculate_context_similarity(
    context_before: str,
    context_after: str,
    rule: ReplacementRule
) -> float:
    """Calculate similarity between current context and rule context."""
    # Word-based similarity
    before_words = set(context_before.lower().split())
    after_words = set(context_after.lower().split())
    
    rule_before_words = set(rule.context_before.lower().split())
    rule_after_words = set(rule.context_after.lower().split())
    
    # Calculate overlap ratios
    before_overlap = len(before_words & rule_before_words) / max(len(before_words | rule_before_words), 1)
    after_overlap = len(after_words & rule_after_words) / max(len(after_words | rule_after_words), 1)
    
    # Length similarity
    before_len_sim = 1 - abs(len(context_before) - len(rule.context_before)) / max(len(context_before) + len(rule.context_before), 1)
    after_len_sim = 1 - abs(len(context_after) - len(rule.context_after)) / max(len(context_after) + len(rule.context_after), 1)
    
    # Combined similarity with rule confidence weighting
    similarity = (before_overlap + after_overlap + before_len_sim + after_len_sim) / 4
    return similarity * rule.confidence_score

def _get_replacement_character(replacement_type: str, replacement_text: str) -> str:
    """Get the actual replacement character(s)."""
    if replacement_text:
        return replacement_text
    
    # Fallback mapping
    type_mapping = {
        'comma': ', ',
        'period': '. ',
        'semicolon': '; ',
        'colon': ': ',
        'space': ' ',
        'nothing': ''
    }
    
    return type_mapping.get(replacement_type, ', ')

def create_backup_file(file_path: Path) -> str:
    """Create backup file with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
    backup_path = file_path.parent / backup_name
    shutil.copy2(file_path, backup_path)
    return str(backup_path)