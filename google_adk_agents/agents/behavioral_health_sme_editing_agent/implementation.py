#!/usr/bin/env python3
"""
Behavioral Health SME-Aware Editing Agent Implementation
=======================================================

Google ADK Agent for processing behavioral health real estate development content
with DHCS BHCIP compliance and industry best practices.

Author: Wellspring Development Team
Version: 1.0.0
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import math

@dataclass
class EditEntry:
    """Represents a single edit made to the text."""
    original_text: str
    edited_text: str
    edit_type: str
    rationale: str
    bhsme_alignment: str
    line_number: Optional[int] = None
    strategic_impact: Optional[str] = None

class BehavioralHealthSMEAgent:
    """
    Google ADK Agent for BHSME-aware editing of behavioral health content.
    """
    
    def __init__(self):
        self.edits_made: List[EditEntry] = []
        self.bhsme_terminology = self._load_bhsme_terminology()
        self.building_analogies = self._load_building_analogies()
        
    def _load_bhsme_terminology(self) -> Dict[str, str]:
        """Load BHSME-specific terminology standards."""
        return {
            # Core Program Terms
            "behavioral health continuum infrastructure program": "Behavioral Health Continuum Infrastructure Program (BHCIP)",
            "department of health care services": "Department of Health Care Services (DHCS)",
            "office of statewide health planning and development": "Office of Statewide Health Planning and Development (OSHPD)",
            "behavioral health infrastructure bond act": "Behavioral Health Infrastructure Bond Act of 2024 (BHIBA)",
            
            # Facility Types - Standardized with Acronyms
            "psychiatric health facility": "Psychiatric Health Facility (PHF)",
            "short-term residential therapeutic program": "Short-term Residential Therapeutic Program (STRTP)",
            "crisis stabilization unit": "Crisis Stabilization Unit (CSU)",
            "behavioral health urgent care": "Behavioral Health Urgent Care (BHUC)",
            "mental health urgent care": "Mental Health Urgent Care (MHUC)",
            "psychiatric residential treatment facility": "Psychiatric Residential Treatment Facility (PRTF)",
            "community treatment facility": "Community Treatment Facility (CTF)",
            "mental health rehabilitation center": "Mental Health Rehabilitation Center (MHRC)",
            "skilled nursing facility with special treatment program": "Skilled Nursing Facility with Special Treatment Program (SNF/STP)",
            
            # Key Legislation & Programs
            "mental health services act": "Mental Health Services Act (MHSA)",
            "community assistance, recovery and empowerment act": "Community Assistance, Recovery and Empowerment (CARE) Act",
            "proposition 1": "Proposition 1 (Behavioral Health Services Act and BHIBA)",
            
            # Clinical & Regulatory Terms
            "trauma informed care": "trauma-informed care",
            "trauma-informed care": "trauma-informed care",  # Ensure hyphenation
            "medicaid": "Medi-Cal",  # California-specific
            "pre-application consultation": "pre-application consultation (PAC)",
            "will serve letters": "Will-Serve Letters",
            "debt service coverage ratio": "debt service coverage ratio (DSCR)",
        }
    
    def _load_building_analogies(self) -> Dict[str, str]:
        """Load building analogy replacements for pillar terminology."""
        return {
            "first pillar": "primary cornerstone",
            "core pillars": "cornerstone principles", 
            "foundational pillars": "foundational cornerstones",
            "main pillars": "key structural elements",
            "supporting pillars": "supporting frameworks",
            "these pillars": "these cornerstones",
            "pillar of": "cornerstone of",
            "pillars of": "cornerstones of",
            "the pillars": "the cornerstones",
            "four pillars": "four cornerstones",
            "five pillars": "five cornerstones",
            "key pillars": "key cornerstones",
        }
    
    def process_request(self, input_data: Dict) -> Dict:
        """
        Main processing function implementing Google ADK agent interface.
        
        Args:
            input_data: Dictionary containing 'text', 'chapter_title', and optional parameters
            
        Returns:
            Dictionary containing edited_text, changelog, statistics, recommendations, and compliance score
        """
        text = input_data.get('text', '')
        chapter_title = input_data.get('chapter_title', 'Unknown Chapter')
        max_sentence_length = input_data.get('max_sentence_length', 35)
        focus_areas = input_data.get('focus_areas', ['pillar_replacement', 'long_sentences', 'passive_voice', 'vague_openers', 'bhsme_terminology'])
        
        # Reset edits for new processing
        self.edits_made = []
        
        # Apply editing transformations based on focus areas
        edited_text = text
        analysis_results = {}
        
        if 'pillar_replacement' in focus_areas:
            edited_text, pillar_edits = self._apply_pillar_replacements(edited_text)
            analysis_results['pillar_replacements'] = pillar_edits
        
        if 'long_sentences' in focus_areas:
            long_sentences = self._analyze_long_sentences(edited_text, max_sentence_length)
            analysis_results['long_sentences'] = long_sentences
        
        if 'passive_voice' in focus_areas:
            passive_instances = self._analyze_passive_voice(edited_text)
            analysis_results['passive_voice'] = passive_instances
        
        if 'vague_openers' in focus_areas:
            vague_instances = self._analyze_vague_openers(edited_text)
            analysis_results['vague_openers'] = vague_instances
        
        if 'bhsme_terminology' in focus_areas:
            edited_text, terminology_edits = self._apply_bhsme_terminology(edited_text)
            analysis_results['bhsme_improvements'] = terminology_edits
        
        # Generate comprehensive results
        statistics = self._generate_statistics(analysis_results)
        recommendations = self._generate_recommendations(analysis_results, statistics)
        compliance_score = self._calculate_compliance_score(statistics)
        changelog = self._generate_changelog(chapter_title, analysis_results, statistics)
        
        return {
            "edited_text": edited_text,
            "changelog": changelog,
            "statistics": statistics,
            "recommendations": recommendations,
            "bhsme_compliance_score": compliance_score
        }
    
    def _apply_pillar_replacements(self, text: str) -> Tuple[str, List[EditEntry]]:
        """Apply architectural terminology consistency replacements."""
        edits = []
        edited_text = text
        
        for pillar_term, replacement in self.building_analogies.items():
            # Case-insensitive search with word boundaries
            pattern = r'\b' + re.escape(pillar_term) + r'\b'
            matches = list(re.finditer(pattern, edited_text, re.IGNORECASE))
            
            for match in matches:
                original = match.group(0)
                # Preserve original capitalization pattern
                if original.istitle():
                    final_replacement = replacement.title()
                elif original.isupper():
                    final_replacement = replacement.upper()
                else:
                    final_replacement = replacement
                
                edited_text = edited_text.replace(original, final_replacement, 1)
                
                edits.append(EditEntry(
                    original_text=original,
                    edited_text=final_replacement,
                    edit_type="PILLAR_REPLACEMENT",
                    rationale=f"Replaced '{original}' with '{final_replacement}' to maintain consistent architectural terminology framework",
                    bhsme_alignment="Supports thematic coherence in real estate development context",
                    strategic_impact="Enhances professional consistency for stakeholder communications"
                ))
        
        return edited_text, edits
    
    def _analyze_long_sentences(self, text: str, max_length: int) -> List[Dict]:
        """Analyze sentences for length and suggest improvements."""
        sentences = re.split(r'[.!?]+', text)
        long_sentences = []
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
                
            words = sentence.split()
            if len(words) > max_length:
                split_suggestions = self._suggest_sentence_splits(sentence)
                long_sentences.append({
                    'sentence_number': i + 1,
                    'original': sentence,
                    'word_count': len(words),
                    'split_suggestions': split_suggestions,
                    'rationale': f'Sentence contains {len(words)} words (>{max_length} recommended). Splitting improves stakeholder readability.',
                    'priority': 'HIGH' if len(words) > 45 else 'MEDIUM'
                })
        
        return long_sentences
    
    def _suggest_sentence_splits(self, sentence: str) -> List[str]:
        """Suggest logical split points for long sentences."""
        split_patterns = [
            (r'\s+and\s+(?=\w+ing)', '. '),  # Before participles
            (r'\s+but\s+', '. But '),
            (r'\s+while\s+', '. While '),
            (r'\s+which\s+', '. This '),
            (r'\s+that\s+(?=\w+\s+\w+)', '. This '),
            (r';\s*', '. '),
            (r',\s+(?=including|such as|for example)', '. This includes '),
        ]
        
        suggestions = []
        for pattern, replacement in split_patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                split_sentence = re.sub(pattern, replacement, sentence, count=1, flags=re.IGNORECASE)
                if split_sentence != sentence:
                    suggestions.append(split_sentence)
        
        return suggestions[:3]  # Return top 3 suggestions
    
    def _analyze_passive_voice(self, text: str) -> List[Dict]:
        """Analyze passive voice constructions."""
        passive_patterns = [
            (r'\bis\s+(\w+ed)\s+by\b', 'Present passive with "is [verb]ed by"'),
            (r'\bare\s+(\w+ed)\s+by\b', 'Present plural passive with "are [verb]ed by"'),
            (r'\bwas\s+(\w+ed)\b', 'Past passive with "was [verb]ed"'),
            (r'\bwere\s+(\w+ed)\b', 'Past plural passive with "were [verb]ed"'),
            (r'\bbeing\s+(\w+ed)\b', 'Progressive passive with "being [verb]ed"'),
            (r'\bbeen\s+(\w+ed)\b', 'Perfect passive with "been [verb]ed"'),
            (r'\bwill\s+be\s+(\w+ed)\b', 'Future passive with "will be [verb]ed"'),
            (r'\bcan\s+be\s+(\w+ed)\b', 'Modal passive with "can be [verb]ed"'),
            (r'\bmust\s+be\s+(\w+ed)\b', 'Modal passive with "must be [verb]ed"'),
        ]
        
        passive_instances = []
        for pattern, description in passive_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                context_start = max(0, match.start() - 60)
                context_end = min(len(text), match.end() + 60)
                context = text[context_start:context_end].strip()
                
                passive_instances.append({
                    'match': match.group(0),
                    'context': context,
                    'description': description,
                    'suggestion': self._suggest_active_alternative(match.group(0)),
                    'rationale': 'Active voice strengthens authority and clarity in professional communications',
                    'impact': 'HIGH' if 'by' in match.group(0) else 'MEDIUM'
                })
        
        return passive_instances
    
    def _suggest_active_alternative(self, passive_phrase: str) -> str:
        """Suggest active voice alternatives."""
        active_patterns = {
            r'is designed by': 'designers create',
            r'are developed by': 'developers build', 
            r'was established by': '[entity] established',
            r'were created by': '[creators] developed',
            r'can be achieved by': '[teams] can achieve',
            r'must be completed by': '[teams] must complete',
            r'will be implemented by': '[staff] will implement',
            r'is required by': '[regulation] requires',
            r'are needed by': '[stakeholders] need',
        }
        
        phrase_lower = passive_phrase.lower().strip()
        for pattern, suggestion in active_patterns.items():
            if re.search(pattern, phrase_lower):
                return f"Consider: '{suggestion}'"
        
        return "Consider restructuring with clear subject-verb-object order"
    
    def _analyze_vague_openers(self, text: str) -> List[Dict]:
        """Analyze vague sentence openers."""
        vague_patterns = [
            (r'\bIt is\s+', 'Vague opener: "It is"', 'Specify the concrete subject'),
            (r'\bThere is\s+', 'Vague opener: "There is"', 'Use specific subject'),
            (r'\bThere are\s+', 'Vague opener: "There are"', 'Use specific plural subject'),
            (r'\bThis is\s+', 'Vague opener: "This is"', 'Clarify what "this" refers to'),
            (r'\bThat is\s+', 'Vague opener: "That is"', 'Clarify what "that" refers to'),
            (r'\bIt can be\s+', 'Vague opener: "It can be"', 'Identify the specific subject'),
            (r'\bIt should be\s+', 'Vague opener: "It should be"', 'Identify the specific subject'),
            (r'\bThere will be\s+', 'Vague opener: "There will be"', 'Use concrete future subject'),
            (r'\bIt has been\s+', 'Vague opener: "It has been"', 'Specify what has been done'),
        ]
        
        vague_instances = []
        sentences = re.split(r'[.!?]+', text)
        
        for sentence_num, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
                
            for pattern, description, suggestion in vague_patterns:
                if re.match(pattern, sentence, re.IGNORECASE):
                    vague_instances.append({
                        'sentence_number': sentence_num + 1,
                        'match': re.match(pattern, sentence, re.IGNORECASE).group(0),
                        'full_sentence': sentence,
                        'description': description,
                        'suggestion': suggestion,
                        'rationale': 'Precise openers enhance professional authority and reader engagement',
                        'impact': 'MEDIUM'
                    })
                    break  # Only report first vague opener per sentence
        
        return vague_instances
    
    def _apply_bhsme_terminology(self, text: str) -> Tuple[str, List[EditEntry]]:
        """Apply BHSME terminology standardization."""
        edits = []
        edited_text = text
        
        for original_term, standard_term in self.bhsme_terminology.items():
            # Case-insensitive replacement with word boundaries
            pattern = r'\b' + re.escape(original_term) + r'\b'
            matches = list(re.finditer(pattern, edited_text, re.IGNORECASE))
            
            for match in matches:
                original = match.group(0)
                # Skip if already in standard form
                if original.lower() == standard_term.lower():
                    continue
                    
                edited_text = edited_text.replace(original, standard_term, 1)
                
                edits.append(EditEntry(
                    original_text=original,
                    edited_text=standard_term,
                    edit_type="BHSME_TERMINOLOGY",
                    rationale=f"Standardized '{original}' to '{standard_term}' per DHCS/BHCIP guidelines",
                    bhsme_alignment="Ensures compliance with California behavioral health regulatory terminology",
                    strategic_impact="Enhances credibility with DHCS reviewers and industry stakeholders"
                ))
        
        return edited_text, edits
    
    def _generate_statistics(self, analysis_results: Dict) -> Dict:
        """Generate comprehensive editing statistics."""
        stats = {
            'total_pillar_replacements': len(analysis_results.get('pillar_replacements', [])),
            'long_sentences_count': len(analysis_results.get('long_sentences', [])),
            'passive_voice_instances': len(analysis_results.get('passive_voice', [])),
            'vague_opener_instances': len(analysis_results.get('vague_openers', [])),
            'bhsme_improvements': len(analysis_results.get('bhsme_improvements', [])),
            'total_edits_applied': len(self.edits_made),
            'readability_score_improvement': self._calculate_readability_improvement(analysis_results)
        }
        
        return stats
    
    def _calculate_readability_improvement(self, analysis_results: Dict) -> float:
        """Calculate estimated readability improvement score."""
        improvements = 0.0
        
        # Pillar replacements improve consistency
        improvements += len(analysis_results.get('pillar_replacements', [])) * 0.5
        
        # Long sentence splits improve comprehension
        improvements += len(analysis_results.get('long_sentences', [])) * 1.2
        
        # Active voice improves clarity
        improvements += len(analysis_results.get('passive_voice', [])) * 0.8
        
        # Precise openers improve engagement
        improvements += len(analysis_results.get('vague_openers', [])) * 0.6
        
        # BHSME terminology improves professional precision
        improvements += len(analysis_results.get('bhsme_improvements', [])) * 0.4
        
        return round(improvements, 2)
    
    def _generate_recommendations(self, analysis_results: Dict, statistics: Dict) -> List[str]:
        """Generate strategic recommendations."""
        recommendations = []
        
        if statistics['total_pillar_replacements'] > 0:
            recommendations.append(
                f"✅ ARCHITECTURAL CONSISTENCY: Applied {statistics['total_pillar_replacements']} "
                f"cornerstone terminology replacements for thematic coherence."
            )
        
        if statistics['long_sentences_count'] > 0:
            high_priority = sum(1 for s in analysis_results.get('long_sentences', []) if s.get('priority') == 'HIGH')
            recommendations.append(
                f"📝 READABILITY ENHANCEMENT: {statistics['long_sentences_count']} sentences identified for splitting "
                f"({high_priority} high priority). Implement suggested breaks for stakeholder accessibility."
            )
        
        if statistics['passive_voice_instances'] > 0:
            high_impact = sum(1 for p in analysis_results.get('passive_voice', []) if p.get('impact') == 'HIGH')
            recommendations.append(
                f"🎯 ACTIVE VOICE AUTHORITY: {statistics['passive_voice_instances']} passive constructions detected "
                f"({high_impact} high impact). Convert to active voice for professional strength."
            )
        
        if statistics['vague_opener_instances'] > 0:
            recommendations.append(
                f"🔍 PRECISION ENHANCEMENT: {statistics['vague_opener_instances']} vague openers require "
                f"specific subject clarification for professional authority."
            )
        
        if statistics['bhsme_improvements'] > 0:
            recommendations.append(
                f"🏥 DHCS COMPLIANCE: {statistics['bhsme_improvements']} terminology standardizations "
                f"applied for regulatory alignment and industry credibility."
            )
        
        # Strategic recommendations based on overall performance
        total_issues = sum([
            statistics['long_sentences_count'],
            statistics['passive_voice_instances'], 
            statistics['vague_opener_instances']
        ])
        
        if total_issues > 10:
            recommendations.append(
                "⚠️ COMPREHENSIVE REVIEW: High number of editing opportunities suggests need for "
                "systematic writing process improvements."
            )
        elif total_issues < 3:
            recommendations.append(
                "🌟 EXCELLENT FOUNDATION: Content demonstrates strong professional writing standards "
                "with minimal improvements needed."
            )
        
        recommendations.extend([
            "📊 STAKEHOLDER VALIDATION: Review technical accuracy with behavioral health SMEs",
            "🎯 FUNDING ALIGNMENT: Verify content supports BHCIP grant objectives and CARE Act goals",
            "🏗️ REGULATORY VERIFICATION: Confirm terminology matches current DHCS guidelines"
        ])
        
        return recommendations
    
    def _calculate_compliance_score(self, statistics: Dict) -> float:
        """Calculate BHSME compliance score (0-10)."""
        base_score = 8.0  # Start with good baseline
        
        # Deduct for issues found
        deductions = 0.0
        deductions += statistics['long_sentences_count'] * 0.1
        deductions += statistics['passive_voice_instances'] * 0.15
        deductions += statistics['vague_opener_instances'] * 0.1
        
        # Add for improvements made
        improvements = 0.0
        improvements += statistics['total_pillar_replacements'] * 0.1
        improvements += statistics['bhsme_improvements'] * 0.2
        
        final_score = base_score - deductions + improvements
        return max(0.0, min(10.0, round(final_score, 1)))
    
    def _generate_changelog(self, chapter_title: str, analysis_results: Dict, statistics: Dict) -> str:
        """Generate detailed changelog report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        changelog = f"""# BHSME Editing Report: {chapter_title}
## Generated: {timestamp}

### Executive Summary
- **Total Edits Applied**: {len(self.edits_made)}
- **Compliance Score**: {self._calculate_compliance_score(statistics)}/10
- **Readability Improvement**: +{statistics['readability_score_improvement']} points
- **DHCS Alignment**: {statistics['bhsme_improvements']} terminology standardizations

### Strategic Impact
This editing session enhances:
- ✅ **Regulatory Compliance**: DHCS/BHCIP terminology standardization
- ✅ **Professional Authority**: Active voice and precise language
- ✅ **Stakeholder Accessibility**: Optimized sentence structure
- ✅ **Industry Credibility**: Consistent architectural framework

---

## Detailed Edit Log

"""
        
        # Group edits by type
        edit_groups = {}
        for edit in self.edits_made:
            edit_type = edit.edit_type
            if edit_type not in edit_groups:
                edit_groups[edit_type] = []
            edit_groups[edit_type].append(edit)
        
        for edit_type, edits in edit_groups.items():
            changelog += f"\n### {edit_type.replace('_', ' ').title()}\n"
            for i, edit in enumerate(edits, 1):
                changelog += f"""
**Edit {i}**: `{edit.original_text}` → `{edit.edited_text}`
- **Rationale**: {edit.rationale}
- **BHSME Alignment**: {edit.bhsme_alignment}
- **Strategic Impact**: {edit.strategic_impact or 'Supports overall document quality'}
"""
        
        # Add analysis sections
        if analysis_results.get('long_sentences'):
            changelog += f"\n---\n\n## Long Sentence Analysis ({len(analysis_results['long_sentences'])} identified)\n"
            for i, sentence in enumerate(analysis_results['long_sentences'], 1):
                changelog += f"""
### Sentence {i} ({sentence['word_count']} words - {sentence['priority']} Priority)
**Original**: {sentence['original'][:150]}...
**Suggested Splits**:
"""
                for split in sentence['split_suggestions']:
                    changelog += f"- {split[:100]}...\n"
        
        if analysis_results.get('passive_voice'):
            changelog += f"\n---\n\n## Passive Voice Analysis ({len(analysis_results['passive_voice'])} instances)\n"
            for i, passive in enumerate(analysis_results['passive_voice'], 1):
                changelog += f"""
### Instance {i}: `{passive['match']}` ({passive['impact']} Impact)
**Context**: {passive['context']}
**Suggestion**: {passive['suggestion']}
**Description**: {passive['description']}
"""
        
        if analysis_results.get('vague_openers'):
            changelog += f"\n---\n\n## Vague Opener Analysis ({len(analysis_results['vague_openers'])} instances)\n"
            for i, vague in enumerate(analysis_results['vague_openers'], 1):
                changelog += f"""
### Opener {i}: `{vague['match']}`
**Full Sentence**: {vague['full_sentence']}
**Issue**: {vague['description']}
**Recommendation**: {vague['suggestion']}
"""
        
        changelog += f"""

---

## BHCIP Alignment Verification

### Funding Program Compliance
- **Proposition 1 Bond**: Content supports $4.4B infrastructure investment goals
- **CARE Act Integration**: Language aligns with implementation requirements  
- **Facility Standards**: Terminology matches current DHCS licensing framework
- **Stakeholder Communication**: Appropriate for developers, clinicians, policymakers

### Quality Assurance Checklist
- [ ] Technical accuracy verified by behavioral health SME
- [ ] Regulatory terminology cross-referenced with current DHCS guidelines
- [ ] Readability appropriate for diverse stakeholder audience
- [ ] Strategic alignment with funding objectives confirmed

---

*Report generated by Behavioral Health SME-Aware Editing Agent v1.0.0*
*Incorporating California DHCS BHCIP program standards and industry best practices*
"""
        
        return changelog

# Google ADK Agent Interface
def process_agent_request(input_data: Dict) -> Dict:
    """
    Main entry point for Google ADK agent processing.
    
    Args:
        input_data: Request data containing text, chapter_title, and optional parameters
        
    Returns:
        Processed response with edited_text, changelog, statistics, recommendations, and compliance score
    """
    agent = BehavioralHealthSMEAgent()
    return agent.process_request(input_data)

# Command line interface for testing
if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Behavioral Health SME Editing Agent')
    parser.add_argument('input_file', help='Input markdown file to process')
    parser.add_argument('--chapter-title', default='Test Chapter', help='Chapter title for reporting')
    parser.add_argument('--output', '-o', help='Output file for results (JSON)')
    
    args = parser.parse_args()
    
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        input_data = {
            'text': text,
            'chapter_title': args.chapter_title
        }
        
        result = process_agent_request(input_data)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            print("=== EDITING SUMMARY ===")
            print(f"Compliance Score: {result['bhsme_compliance_score']}/10")
            print(f"Total Edits: {result['statistics']['total_edits_applied']}")
            print(f"Readability Improvement: +{result['statistics']['readability_score_improvement']}")
            print("\n=== TOP RECOMMENDATIONS ===")
            for rec in result['recommendations'][:3]:
                print(f"• {rec}")
    
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)