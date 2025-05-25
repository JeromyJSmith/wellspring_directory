#!/usr/bin/env python3
"""
Deep Research Agent for Wellspring Book Production
Handles quote verification, fact-checking, and citation management.
"""

import re
import json
import sqlite3
import requests
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Quote:
    """Represents a quote found in the text."""
    text: str
    author: str
    context: str
    chapter_location: str
    page_number: int
    source_line: int

@dataclass
class Citation:
    """Represents a research citation."""
    quote_text: str
    source_url: Optional[str]
    author: Optional[str]
    publication_date: Optional[str]
    relevance_score: float
    verification_status: str
    notes: str

@dataclass
class FactCheckResult:
    """Represents a fact-checking result."""
    claim: str
    verification_status: str  # 'verified', 'disputed', 'unverified'
    confidence: float
    sources: List[str]
    explanation: str

@dataclass
class VisualOpportunity:
    """Represents an opportunity for visual content."""
    location: str
    content_type: str  # 'infographic', 'chart', 'checklist', 'diagram'
    data_content: str
    suggested_format: str
    priority_level: str

class DeepResearchAgent:
    """AI-powered research agent for content verification and enhancement."""
    
    def __init__(self, db_path: str = None):
        """Initialize the research agent."""
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "shared_utils" / "data" / "wellspring.db"
        
        self.db_path = Path(db_path)
        self.api_keys = self._load_api_keys()
        
    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from environment or config."""
        # In production, these would come from environment variables
        return {
            'brave_search': 'YOUR_BRAVE_API_KEY',
            'perplexity': 'YOUR_PERPLEXITY_API_KEY',
            'exa': 'YOUR_EXA_API_KEY'
        }
    
    def extract_quotes(self, content: str, chapter_name: str = "unknown") -> List[Quote]:
        """Extract quotes from text content."""
        quotes = []
        lines = content.split('\n')
        
        # Pattern to match quotes - looking for quoted text with attribution
        quote_patterns = [
            r'"([^"]{20,})"[^\w]*[-—]\s*([^.\n]{5,50})',  # "Quote" - Attribution
            r'"([^"]{20,})"[^\w]*\(([^)]{5,50})\)',        # "Quote" (Attribution)
            r'"([^"]{20,})"[^\w]*([A-Z][a-z]+ [A-Z][a-z]+)', # "Quote" FirstName LastName
            r'\"([^\"]{20,})\"[^\w]*[-—]\s*([^.\n]{5,50})', # Alternative quote marks
        ]
        
        for line_num, line in enumerate(lines, 1):
            for pattern in quote_patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    quote_text = match.group(1).strip()
                    author = match.group(2).strip()
                    
                    # Extract surrounding context
                    context_start = max(0, line_num - 3)
                    context_end = min(len(lines), line_num + 3)
                    context = '\n'.join(lines[context_start:context_end])
                    
                    quote = Quote(
                        text=quote_text,
                        author=author,
                        context=context,
                        chapter_location=chapter_name,
                        page_number=line_num // 25,  # Rough page estimation
                        source_line=line_num
                    )
                    quotes.append(quote)
        
        logger.info(f"Extracted {len(quotes)} quotes from {chapter_name}")
        return quotes
    
    def verify_quote_relevance(self, quote: Quote, chapter_content: str) -> float:
        """Verify how relevant a quote is to the chapter content."""
        # Extract key themes from chapter
        chapter_keywords = self._extract_keywords(chapter_content)
        quote_keywords = self._extract_keywords(quote.text + " " + quote.context)
        
        # Calculate keyword overlap
        common_keywords = set(chapter_keywords) & set(quote_keywords)
        relevance_score = len(common_keywords) / max(len(chapter_keywords), len(quote_keywords), 1)
        
        # Boost score if quote appears in relevant section
        if any(keyword in quote.context.lower() for keyword in ['introduction', 'conclusion', 'summary']):
            relevance_score += 0.2
        
        # Context-specific relevance for behavioral health
        behavioral_health_terms = [
            'behavioral health', 'mental health', 'healthcare', 'treatment', 'therapy',
            'clinical', 'patient', 'care', 'medical', 'health facility', 'continuum',
            'infrastructure', 'development', 'planning', 'design', 'construction'
        ]
        
        bh_terms_in_quote = sum(1 for term in behavioral_health_terms if term in quote.text.lower())
        bh_terms_in_chapter = sum(1 for term in behavioral_health_terms if term in chapter_content.lower())
        
        if bh_terms_in_quote > 0 and bh_terms_in_chapter > 0:
            relevance_score += 0.3
        
        return min(relevance_score, 1.0)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        # Simple keyword extraction - in production would use NLP libraries
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        
        # Remove common stop words
        stop_words = {
            'this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 'their',
            'said', 'each', 'which', 'what', 'there', 'would', 'could', 'should',
            'about', 'after', 'before', 'during', 'through', 'while', 'where'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Return most frequent keywords
        from collections import Counter
        counter = Counter(keywords)
        return [word for word, count in counter.most_common(20)]
    
    def research_quote_authenticity(self, quote: Quote) -> Citation:
        """Research quote authenticity and find sources."""
        logger.info(f"Researching quote by {quote.author}: '{quote.text[:50]}...'")
        
        # Simulate research process (in production would use actual APIs)
        citation = Citation(
            quote_text=quote.text,
            source_url=self._search_quote_sources(quote),
            author=quote.author,
            publication_date=None,
            relevance_score=0.0,
            verification_status='researched',
            notes=f"Research completed for quote from {quote.author}"
        )
        
        return citation
    
    def _search_quote_sources(self, quote: Quote) -> Optional[str]:
        """Search for quote sources using web search APIs."""
        # In production, this would use actual search APIs
        search_query = f'"{quote.text[:100]}" {quote.author}'
        
        # Simulate search result
        logger.info(f"Searching for: {search_query}")
        
        # Return simulated URL
        return f"https://example.com/quote-source/{quote.author.replace(' ', '-').lower()}"
    
    def fact_check_claims(self, content: str) -> List[FactCheckResult]:
        """Identify and fact-check statistical claims in content."""
        claims = []
        
        # Patterns to identify factual claims
        fact_patterns = [
            r'(\d+(?:\.\d+)?%\s+of[^.]{10,100})',  # Percentage claims
            r'(\d+(?:,\d{3})*\s+(?:people|patients|facilities|projects)[^.]{10,100})', # Numeric claims
            r'(studies show[^.]{10,100})',  # Study references
            r'(research indicates[^.]{10,100})',  # Research claims
            r'(according to[^.]{10,100})',  # Attribution claims
        ]
        
        for pattern in fact_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                claim_text = match.group(1).strip()
                
                # Simulate fact-checking process
                fact_result = FactCheckResult(
                    claim=claim_text,
                    verification_status='unverified',  # Would be actual verification
                    confidence=0.7,
                    sources=['https://example.com/source1', 'https://example.com/source2'],
                    explanation=f"Claim requires verification: {claim_text}"
                )
                claims.append(fact_result)
        
        logger.info(f"Identified {len(claims)} factual claims for verification")
        return claims
    
    def identify_visual_opportunities(self, content: str, chapter_name: str) -> List[VisualOpportunity]:
        """Identify opportunities for visual content (infographics, charts, etc.)."""
        opportunities = []
        
        # Patterns that suggest visual opportunities
        visual_patterns = [
            (r'(\d+(?:\.\d+)?%[^.]{20,100})', 'chart', 'pie_chart', 'percentage data'),
            (r'(steps?:\s*\n(?:\d+\.[^\n]+\n?){3,})', 'checklist', 'numbered_list', 'process steps'),
            (r'(phases?[^.]{20,100})', 'diagram', 'flowchart', 'phase description'),
            (r'(components?[^.]{20,100})', 'infographic', 'component_diagram', 'component breakdown'),
            (r'(comparison[^.]{20,100})', 'chart', 'comparison_table', 'comparison data'),
            (r'(budget[^.]{20,100})', 'chart', 'bar_chart', 'budget breakdown'),
        ]
        
        for pattern, content_type, suggested_format, description in visual_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                data_content = match.group(1).strip()
                
                # Determine priority based on data richness
                if any(keyword in data_content.lower() for keyword in ['critical', 'important', 'key', 'essential']):
                    priority = 'high'
                elif len(data_content) > 100:
                    priority = 'medium'
                else:
                    priority = 'low'
                
                opportunity = VisualOpportunity(
                    location=f"{chapter_name} - {description}",
                    content_type=content_type,
                    data_content=data_content,
                    suggested_format=suggested_format,
                    priority_level=priority
                )
                opportunities.append(opportunity)
        
        logger.info(f"Identified {len(opportunities)} visual opportunities")
        return opportunities
    
    def save_research_results(self, quotes: List[Quote], citations: List[Citation], 
                            fact_checks: List[FactCheckResult], visual_ops: List[VisualOpportunity]) -> bool:
        """Save all research results to database."""
        if not self.db_path.exists():
            logger.error(f"Database not found: {self.db_path}")
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Save citations
            for citation in citations:
                cursor.execute("""
                    INSERT INTO research_citations 
                    (citation_text, source_url, author, relevance_score, verification_status, notes, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    citation.quote_text, citation.source_url, citation.author,
                    citation.relevance_score, citation.verification_status, citation.notes,
                    datetime.now().isoformat()
                ))
            
            # Save visual opportunities
            for visual_op in visual_ops:
                cursor.execute("""
                    INSERT INTO visual_opportunities 
                    (location_description, content_type, data_content, suggested_format, 
                     priority_level, implementation_status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    visual_op.location, visual_op.content_type, visual_op.data_content,
                    visual_op.suggested_format, visual_op.priority_level, 'pending',
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Saved research results: {len(citations)} citations, {len(visual_ops)} visual opportunities")
            return True
            
        except Exception as e:
            logger.error(f"Error saving research results: {e}")
            return False
    
    def generate_research_report(self, quotes: List[Quote], citations: List[Citation], 
                               fact_checks: List[FactCheckResult], visual_ops: List[VisualOpportunity]) -> str:
        """Generate comprehensive research report."""
        report = []
        report.append("=" * 60)
        report.append("🔍 DEEP RESEARCH ANALYSIS REPORT")
        report.append("=" * 60)
        
        # Quote analysis
        report.append(f"\n📋 Quote Analysis:")
        report.append(f"  • Total quotes found: {len(quotes)}")
        if quotes:
            avg_relevance = sum(self.verify_quote_relevance(q, "") for q in quotes) / len(quotes)
            report.append(f"  • Average relevance score: {avg_relevance:.2f}")
            high_relevance = sum(1 for q in quotes if self.verify_quote_relevance(q, "") > 0.7)
            report.append(f"  • High relevance quotes: {high_relevance}")
        
        # Citation verification
        report.append(f"\n📚 Citation Verification:")
        report.append(f"  • Citations researched: {len(citations)}")
        verified = sum(1 for c in citations if c.verification_status == 'verified')
        report.append(f"  • Verified citations: {verified}")
        
        # Fact checking
        report.append(f"\n✅ Fact Checking:")
        report.append(f"  • Claims identified: {len(fact_checks)}")
        if fact_checks:
            verified_facts = sum(1 for f in fact_checks if f.verification_status == 'verified')
            disputed_facts = sum(1 for f in fact_checks if f.verification_status == 'disputed')
            report.append(f"  • Verified claims: {verified_facts}")
            report.append(f"  • Disputed claims: {disputed_facts}")
            report.append(f"  • Require verification: {len(fact_checks) - verified_facts - disputed_facts}")
        
        # Visual opportunities
        report.append(f"\n🎨 Visual Enhancement Opportunities:")
        report.append(f"  • Total opportunities: {len(visual_ops)}")
        if visual_ops:
            by_type = {}
            by_priority = {}
            for vo in visual_ops:
                by_type[vo.content_type] = by_type.get(vo.content_type, 0) + 1
                by_priority[vo.priority_level] = by_priority.get(vo.priority_level, 0) + 1
            
            report.append(f"  • By type: {dict(by_type)}")
            report.append(f"  • By priority: {dict(by_priority)}")
        
        # Recommendations
        report.append(f"\n💡 Recommendations:")
        if quotes and sum(self.verify_quote_relevance(q, "") for q in quotes) / len(quotes) < 0.6:
            report.append(f"  • Review quote relevance - some quotes may not align with chapter content")
        if fact_checks and sum(1 for f in fact_checks if f.verification_status == 'unverified') > 0:
            report.append(f"  • Verify statistical claims before publication")
        if visual_ops and sum(1 for v in visual_ops if v.priority_level == 'high') > 0:
            report.append(f"  • Prioritize high-priority visual enhancements for better readability")
        
        report.append("=" * 60)
        
        return '\n'.join(report)

def main():
    """Main function to run deep research analysis."""
    print("🔍 Deep Research Agent for Wellspring Book")
    print("=" * 50)
    
    # Initialize research agent
    agent = DeepResearchAgent()
    
    # Sample content for testing
    sample_content = """
Chapter 2: Strategic Planning and Feasibility Analysis

"The key to successful behavioral health facility development lies in comprehensive planning and stakeholder alignment" — Brian V Jones

Research indicates that 75% of behavioral health projects succeed when proper due diligence is conducted.

The development process consists of several phases:
1. Concept planning and vision development
2. Site analysis and acquisition
3. Design development and permitting
4. Construction and commissioning

Studies show that facilities with integrated design approaches achieve 30% better patient outcomes.

According to the National Institute of Mental Health, there is a critical shortage of behavioral health infrastructure nationwide.

Budget components typically include:
- Land acquisition: 15-25% of total budget
- Design and soft costs: 20-30%
- Construction hard costs: 50-60%
- FF&E and contingency: 10-15%

"Proper planning prevents poor performance in complex healthcare projects" — Healthcare Design Magazine
"""
    
    # Perform research analysis
    print("🔍 Extracting quotes...")
    quotes = agent.extract_quotes(sample_content, "Chapter 2")
    
    print("📚 Researching citations...")
    citations = []
    for quote in quotes:
        citation = agent.research_quote_authenticity(quote)
        citation.relevance_score = agent.verify_quote_relevance(quote, sample_content)
        citations.append(citation)
    
    print("✅ Fact-checking claims...")
    fact_checks = agent.fact_check_claims(sample_content)
    
    print("🎨 Identifying visual opportunities...")
    visual_ops = agent.identify_visual_opportunities(sample_content, "Chapter 2")
    
    # Generate and display report
    report = agent.generate_research_report(quotes, citations, fact_checks, visual_ops)
    print(f"\n{report}")
    
    # Save results to database (if available)
    if agent.db_path.exists():
        agent.save_research_results(quotes, citations, fact_checks, visual_ops)
        print(f"\n✅ Results saved to database: {agent.db_path}")
    else:
        print(f"\n⚠️  Database not found - run init_database.py first")
    
    print(f"\n🎉 Deep research analysis completed!")

if __name__ == "__main__":
    main()