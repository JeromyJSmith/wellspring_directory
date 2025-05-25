#!/usr/bin/env python3
"""
Google ADK Tools for Em Dash Analysis
Provides specialized tools for the em_dash_analyzer agent.
"""

import re
import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmDashPattern:
    """Represents an em dash pattern found in text."""
    text: str
    position: int
    line_number: int
    context_before: str
    context_after: str
    full_sentence: str
    suggested_replacement: str
    replacement_type: str
    confidence_score: float
    reasoning: str

@dataclass
class AnalysisResult:
    """Complete analysis result for a document."""
    document_path: str
    total_em_dashes: int
    patterns: List[EmDashPattern]
    replacement_summary: Dict[str, int]
    confidence_distribution: Dict[str, int]
    processing_recommendation: str
    analysis_timestamp: str

class EmDashAnalysisTools:
    """Tool implementations for em dash analysis."""
    
    def __init__(self, db_path: str = None):
        """Initialize with database connection."""
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "shared_utils" / "data" / "wellspring.db"
        self.db_path = Path(db_path)
        
        # Replacement pattern definitions
        self.replacement_patterns = {
            'list_separator': {
                'patterns': [
                    r'(\w+),?\s*—\s*(\w+)',  # word—word
                    r'([^.!?]+),?\s*—\s*([^.!?]+),?\s*—',  # item—item—
                ],
                'replacement': ',',
                'confidence_base': 0.9,
                'description': 'Em dash used as list separator'
            },
            'parenthetical': {
                'patterns': [
                    r'(\w+)\s*—\s*([^—]+)\s*—\s*(\w+)',  # word—phrase—word
                    r'([^.!?]+)\s*—\s*([^—]+)\s*—\s*([^.!?]+)',
                ],
                'replacement': ' (',
                'replacement_end': ') ',
                'confidence_base': 0.85,
                'description': 'Em dash pair for parenthetical expression'
            },
            'definition_introduction': {
                'patterns': [
                    r'(\w+)\s*—\s*([^.!?]+[.!?])',  # word—definition.
                    r'([^:]+)\s*—\s*([A-Z][^.!?]+)',  # phrase—Definition
                ],
                'replacement': ': ',
                'confidence_base': 0.8,
                'description': 'Em dash introducing definition or explanation'
            },
            'sentence_break': {
                'patterns': [
                    r'([.!?])\s*—\s*([A-Z])',  # sentence.—Next
                    r'([.!?])\s*—\s*(\w+)',
                ],
                'replacement': ' ',
                'confidence_base': 0.9,
                'description': 'Em dash as sentence break'
            },
            'clause_separator': {
                'patterns': [
                    r'([^.!?]+),?\s*—\s*([^.!?]+)$',  # clause—clause at end
                    r'([^.!?]+),?\s*—\s*([^.!?]+)\.',  # clause—clause.
                ],
                'replacement': '; ',
                'confidence_base': 0.7,
                'description': 'Em dash separating independent clauses'
            },
            'interruption_thought': {
                'patterns': [
                    r'(\w+)\s*—\s*(\w+)',  # Simple interruption
                ],
                'replacement': ', ',
                'confidence_base': 0.6,
                'description': 'Em dash as thought break or interruption'
            }
        }

def analyze_em_dash_patterns(
    file_path: str,
    context_length: int = 50,
    min_confidence: float = 0.5
) -> AnalysisResult:
    """
    Analyze em dash patterns in a text file.
    
    Args:
        file_path: Path to the text file to analyze
        context_length: Length of context to capture around each em dash
        min_confidence: Minimum confidence threshold for suggestions
        
    Returns:
        AnalysisResult: Complete analysis results
    """
    tools = EmDashAnalysisTools()
    
    try:
        # Read file content
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path_obj, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all em dash patterns
        patterns = []
        lines = content.split('\n')
        
        logger.info(f"Analyzing em dash patterns in {file_path}")
        
        for line_num, line in enumerate(lines, 1):
            # Find all em dashes in the line
            for match in re.finditer(r'—', line):
                position = match.start()
                
                # Extract context
                context_before = line[:position][-context_length:] if len(line[:position]) > context_length else line[:position]
                context_after = line[position+1:][:context_length] if len(line[position+1:]) > context_length else line[position+1:]
                
                # Get full sentence context
                full_sentence = tools._extract_sentence_context(lines, line_num - 1, position)
                
                # Analyze pattern and suggest replacement
                replacement_info = tools._analyze_pattern(context_before, context_after, full_sentence)
                
                # Only include patterns above minimum confidence
                if replacement_info['confidence'] >= min_confidence:
                    pattern = EmDashPattern(
                        text="—",
                        position=position,
                        line_number=line_num,
                        context_before=context_before.strip(),
                        context_after=context_after.strip(),
                        full_sentence=full_sentence,
                        suggested_replacement=replacement_info['replacement'],
                        replacement_type=replacement_info['type'],
                        confidence_score=replacement_info['confidence'],
                        reasoning=replacement_info['reasoning']
                    )
                    patterns.append(pattern)
        
        # Generate summary statistics
        replacement_summary = {}
        confidence_distribution = {'high': 0, 'medium': 0, 'low': 0}
        
        for pattern in patterns:
            # Count by replacement type
            replacement_summary[pattern.replacement_type] = replacement_summary.get(pattern.replacement_type, 0) + 1
            
            # Confidence distribution
            if pattern.confidence_score >= 0.8:
                confidence_distribution['high'] += 1
            elif pattern.confidence_score >= 0.6:
                confidence_distribution['medium'] += 1
            else:
                confidence_distribution['low'] += 1
        
        # Generate processing recommendation
        total_patterns = len(patterns)
        high_confidence_ratio = confidence_distribution['high'] / max(total_patterns, 1)
        
        if high_confidence_ratio >= 0.8:
            recommendation = "Proceed with automated replacement - high confidence across patterns"
        elif high_confidence_ratio >= 0.6:
            recommendation = "Proceed with caution - review medium confidence cases"
        else:
            recommendation = "Manual review required - many low confidence patterns detected"
        
        result = AnalysisResult(
            document_path=str(file_path_obj),
            total_em_dashes=total_patterns,
            patterns=patterns,
            replacement_summary=replacement_summary,
            confidence_distribution=confidence_distribution,
            processing_recommendation=recommendation,
            analysis_timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"Analysis complete: {total_patterns} em dash patterns found")
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing em dash patterns: {e}")
        raise

def suggest_replacements(
    context_before: str,
    context_after: str,
    full_sentence: str,
    pattern_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Suggest appropriate replacements for an em dash based on context.
    
    Args:
        context_before: Text before the em dash
        context_after: Text after the em dash
        full_sentence: Complete sentence containing the em dash
        pattern_type: Optional specific pattern type to check
        
    Returns:
        Dict containing replacement suggestion and metadata
    """
    tools = EmDashAnalysisTools()
    
    try:
        # Analyze the specific context
        result = tools._analyze_pattern(context_before, context_after, full_sentence, pattern_type)
        
        # Add additional context analysis
        result['context_analysis'] = {
            'before_length': len(context_before),
            'after_length': len(context_after),
            'sentence_length': len(full_sentence),
            'has_punctuation_before': bool(re.search(r'[.!?,:;]$', context_before.strip())),
            'has_punctuation_after': bool(re.search(r'^[.!?,:;]', context_after.strip())),
            'capitalized_after': context_after.strip().startswith(tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')) if context_after.strip() else False
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error suggesting replacements: {e}")
        raise

def calculate_confidence(
    pattern: EmDashPattern,
    similar_patterns: Optional[List[EmDashPattern]] = None
) -> float:
    """
    Calculate confidence score for a replacement suggestion.
    
    Args:
        pattern: The em dash pattern to evaluate
        similar_patterns: List of similar patterns for comparison
        
    Returns:
        float: Confidence score between 0.0 and 1.0
    """
    try:
        base_confidence = 0.5
        confidence_factors = []
        
        # Context clarity factor
        context_clarity = len(pattern.context_before.strip()) + len(pattern.context_after.strip())
        if context_clarity > 20:
            confidence_factors.append(0.1)
        elif context_clarity > 10:
            confidence_factors.append(0.05)
        
        # Sentence completeness factor
        if pattern.full_sentence.strip().endswith(('.', '!', '?')):
            confidence_factors.append(0.1)
        
        # Pattern specificity factor
        specific_patterns = ['parenthetical', 'definition_introduction', 'sentence_break']
        if pattern.replacement_type in specific_patterns:
            confidence_factors.append(0.15)
        
        # Consistency factor (if similar patterns provided)
        if similar_patterns:
            same_type_count = sum(1 for p in similar_patterns if p.replacement_type == pattern.replacement_type)
            consistency_ratio = same_type_count / len(similar_patterns)
            confidence_factors.append(consistency_ratio * 0.2)
        
        # Calculate final confidence
        final_confidence = min(base_confidence + sum(confidence_factors), 1.0)
        
        logger.debug(f"Calculated confidence {final_confidence:.3f} for pattern type {pattern.replacement_type}")
        return final_confidence
        
    except Exception as e:
        logger.error(f"Error calculating confidence: {e}")
        return 0.5  # Default confidence

def generate_analysis_report(analysis_result: AnalysisResult) -> Dict[str, Any]:
    """
    Generate a comprehensive analysis report.
    
    Args:
        analysis_result: Complete analysis results
        
    Returns:
        Dict containing formatted report data
    """
    try:
        report = {
            'document_info': {
                'path': analysis_result.document_path,
                'analysis_timestamp': analysis_result.analysis_timestamp,
                'total_em_dashes': analysis_result.total_em_dashes
            },
            'pattern_summary': {
                'by_type': analysis_result.replacement_summary,
                'confidence_distribution': analysis_result.confidence_distribution,
                'average_confidence': sum(p.confidence_score for p in analysis_result.patterns) / max(len(analysis_result.patterns), 1)
            },
            'processing_guidance': {
                'recommendation': analysis_result.processing_recommendation,
                'high_confidence_count': analysis_result.confidence_distribution['high'],
                'manual_review_needed': analysis_result.confidence_distribution['low'],
                'ready_for_automation': analysis_result.confidence_distribution['high'] + analysis_result.confidence_distribution['medium']
            },
            'detailed_patterns': [
                {
                    'line': p.line_number,
                    'type': p.replacement_type,
                    'suggested_replacement': p.suggested_replacement,
                    'confidence': round(p.confidence_score, 3),
                    'context': f"...{p.context_before} — {p.context_after}...",
                    'reasoning': p.reasoning
                }
                for p in analysis_result.patterns[:10]  # Show first 10 for report
            ],
            'quality_metrics': {
                'pattern_diversity': len(set(p.replacement_type for p in analysis_result.patterns)),
                'average_context_length': sum(len(p.context_before) + len(p.context_after) for p in analysis_result.patterns) / max(len(analysis_result.patterns), 1),
                'sentence_completeness_ratio': sum(1 for p in analysis_result.patterns if p.full_sentence.strip().endswith(('.', '!', '?'))) / max(len(analysis_result.patterns), 1)
            }
        }
        
        logger.info(f"Generated analysis report for {analysis_result.document_path}")
        return report
        
    except Exception as e:
        logger.error(f"Error generating analysis report: {e}")
        raise

def save_to_database(
    analysis_result: AnalysisResult,
    session_id: Optional[str] = None,
    overwrite_existing: bool = False
) -> bool:
    """
    Save analysis results to the Wellspring database.
    
    Args:
        analysis_result: Complete analysis results to save
        session_id: Optional session identifier
        overwrite_existing: Whether to overwrite existing patterns for this document
        
    Returns:
        bool: True if saved successfully
    """
    tools = EmDashAnalysisTools()
    
    try:
        if not tools.db_path.exists():
            logger.error(f"Database not found: {tools.db_path}")
            return False
        
        conn = sqlite3.connect(tools.db_path)
        cursor = conn.cursor()
        
        # Clear existing patterns if requested
        if overwrite_existing:
            cursor.execute(
                "DELETE FROM em_dash_patterns WHERE chapter_location = ?",
                (analysis_result.document_path,)
            )
            logger.info(f"Cleared existing patterns for {analysis_result.document_path}")
        
        # Insert new patterns
        for pattern in analysis_result.patterns:
            cursor.execute("""
                INSERT INTO em_dash_patterns 
                (original_text, context_before, context_after, replacement_text, replacement_type, 
                 confidence_score, chapter_location, page_number, created_at, session_id, reasoning)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pattern.text,
                pattern.context_before,
                pattern.context_after,
                pattern.suggested_replacement,
                pattern.replacement_type,
                pattern.confidence_score,
                analysis_result.document_path,
                pattern.line_number,
                analysis_result.analysis_timestamp,
                session_id,
                pattern.reasoning
            ))
        
        # Log analysis session
        cursor.execute("""
            INSERT INTO agent_logs 
            (agent_name, task_type, input_data, output_data, status, started_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "em_dash_analyzer",
            "analyze_patterns",
            json.dumps({
                'document_path': analysis_result.document_path,
                'total_patterns': analysis_result.total_em_dashes
            }),
            json.dumps({
                'patterns_found': len(analysis_result.patterns),
                'replacement_summary': analysis_result.replacement_summary,
                'confidence_distribution': analysis_result.confidence_distribution
            }),
            "completed",
            analysis_result.analysis_timestamp,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved {len(analysis_result.patterns)} patterns to database")
        return True
        
    except Exception as e:
        logger.error(f"Error saving to database: {e}")
        return False

# Additional helper methods for the EmDashAnalysisTools class
EmDashAnalysisTools._extract_sentence_context = lambda self, lines, line_index, position: self._get_sentence_context(lines, line_index, position)
EmDashAnalysisTools._analyze_pattern = lambda self, before, after, sentence, pattern_type=None: self._pattern_analysis(before, after, sentence, pattern_type)

def _get_sentence_context(self, lines: List[str], line_index: int, position: int) -> str:
    """Extract full sentence context around the em dash."""
    sentence_chars = []
    current_line = lines[line_index]
    
    # Get text before em dash
    before_text = current_line[:position]
    for i in range(len(before_text) - 1, -1, -1):
        char = before_text[i]
        sentence_chars.insert(0, char)
        if char in '.!?' and i > 0:
            break
    
    # Add the em dash
    sentence_chars.append('—')
    
    # Get text after em dash
    after_text = current_line[position + 1:]
    for char in after_text:
        sentence_chars.append(char)
        if char in '.!?':
            break
    
    return ''.join(sentence_chars).strip()

def _pattern_analysis(self, before: str, after: str, sentence: str, pattern_type: Optional[str] = None) -> Dict[str, Any]:
    """Analyze pattern and suggest replacement."""
    context = f"{before} — {after}"
    
    # Check specific pattern if requested
    if pattern_type and pattern_type in self.replacement_patterns:
        pattern_info = self.replacement_patterns[pattern_type]
        for pattern in pattern_info['patterns']:
            if re.search(pattern, context, re.IGNORECASE):
                return {
                    'replacement': pattern_info['replacement'],
                    'type': pattern_type,
                    'confidence': pattern_info['confidence_base'],
                    'reasoning': pattern_info['description']
                }
    
    # Check all patterns
    for pattern_name, pattern_info in self.replacement_patterns.items():
        for pattern in pattern_info['patterns']:
            if re.search(pattern, context, re.IGNORECASE):
                return {
                    'replacement': pattern_info['replacement'],
                    'type': pattern_name,
                    'confidence': pattern_info['confidence_base'],
                    'reasoning': pattern_info['description']
                }
    
    # Default analysis based on context
    if before.strip().endswith(('and', 'or', 'but')):
        return {
            'replacement': ', ',
            'type': 'conjunction_separator',
            'confidence': 0.7,
            'reasoning': 'Em dash follows conjunction, suggesting comma replacement'
        }
    elif re.search(r'\b(is|are|was|were)\s*$', before, re.IGNORECASE):
        return {
            'replacement': ': ',
            'type': 'definition_marker',
            'confidence': 0.6,
            'reasoning': 'Em dash follows linking verb, suggesting colon for definition'
        }
    else:
        return {
            'replacement': ', ',
            'type': 'default_separator',
            'confidence': 0.5,
            'reasoning': 'General separator context, defaulting to comma'
        }

# Bind helper methods to the class
EmDashAnalysisTools._get_sentence_context = _get_sentence_context
EmDashAnalysisTools._pattern_analysis = _pattern_analysis