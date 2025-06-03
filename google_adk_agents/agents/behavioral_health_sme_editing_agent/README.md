# Behavioral Health SME-Aware Editing Agent

## Overview

A Google ADK agent designed to enhance behavioral health real estate development content with deep expertise in California's DHCS Behavioral Health Continuum Infrastructure Program (BHCIP). The agent improves text readability, ensures industry-standard terminology, and aligns documents strategically with regulatory compliance and best practices.

## Features

### 🏗️ Architectural Terminology Consistency
- Replaces "pillar" analogies with unified building metaphors
- Maintains thematic coherence with real estate development focus
- Preserves original capitalization and sentence structure

### 📝 Readability Enhancement
- Identifies sentences exceeding 35 words (configurable)
- Suggests logical split points using linguistic patterns
- Optimizes for diverse stakeholder accessibility

### 🎯 Active Voice Enforcement
- Detects passive voice constructions
- Suggests authoritative active alternatives
- Strengthens professional communication impact

### 🔍 Precision and Clarity
- Eliminates vague sentence openers ("It is," "There are," etc.)
- Replaces with specific, actionable subjects
- Enhances professional credibility

### 🏥 BHSME Terminology Standardization
- Ensures compliance with DHCS/BHCIP standards
- Standardizes facility types with proper acronyms
- Aligns with Proposition 1 and CARE Act requirements

### 📊 Comprehensive Reporting
- Detailed changelog with rationale for each edit
- Compliance scoring (0-10 scale)
- Strategic recommendations for further improvement
- Statistics on editing impact and readability gains

## Domain Expertise

### BHCIP Program Knowledge
- **Funding Structure**: $4.4B infrastructure investment under Proposition 1
- **Facility Types**: PHF, STRTP, CSU, BHUC, PRTF, CTF, MHRC, SNF/STP
- **Regulatory Framework**: DHCS licensing, OSHPD requirements, CARE Act alignment
- **Grant Processes**: PAC requirements, match guidelines, compliance standards

### Industry Standards
- Trauma-informed care principles
- Evidence-based design terminology
- California behavioral health regulatory framework
- Professional communication best practices

## Installation and Usage

### Google ADK Integration
```bash
# Install agent in ADK environment
gdk install behavioral_health_sme_editing_agent

# Run agent
gdk run behavioral_health_sme_editing_agent --input chapter.md
```

### Command Line Usage
```bash
# Process a chapter file
python implementation.py chapter1.md --chapter-title "Chapter 1: Foundations" --output results.json

# View results
cat results.json | jq '.statistics'
```

### Python Integration
```python
from behavioral_health_sme_editing_agent.implementation import process_agent_request

input_data = {
    "text": "Your chapter content here...",
    "chapter_title": "Chapter 1: Foundations",
    "max_sentence_length": 35,
    "focus_areas": ["pillar_replacement", "long_sentences", "passive_voice", "vague_openers", "bhsme_terminology"]
}

result = process_agent_request(input_data)
print(f"Compliance Score: {result['bhsme_compliance_score']}/10")
```

## Input Schema

```json
{
  "text": "string (required) - Full markdown-formatted chapter text",
  "chapter_title": "string (required) - Chapter identifier", 
  "max_sentence_length": "integer (optional, default: 35) - Maximum words before suggesting splits",
  "focus_areas": "array (optional) - Specific editing areas to apply"
}
```

## Output Schema

```json
{
  "edited_text": "string - Improved and edited markdown text",
  "changelog": "string - Detailed documentation of all edits",
  "statistics": "object - Summary of editing metrics",
  "recommendations": "array - Strategic improvement suggestions",
  "bhsme_compliance_score": "number - Compliance rating (0-10)"
}
```

## Quality Standards

### BHCIP Compliance Score
- **9-10**: Full alignment with DHCS standards, optimal stakeholder communication
- **7-8**: Strong compliance with minor terminology adjustments needed
- **5-6**: Adequate content requiring moderate improvements
- **Below 5**: Significant revisions needed for regulatory alignment

### Success Metrics
- **Regulatory Precision**: 100% accurate DHCS/BHCIP terminology
- **Stakeholder Clarity**: Accessible to developers, clinicians, policymakers
- **Professional Authority**: Strong, confident communication tone
- **Strategic Alignment**: Content supports funding and operational objectives

## Example Results

### Before
```markdown
The first pillar of behavioral health real estate development is needs validation. 
It is critical that projects are designed by teams who understand the complexities 
that are involved in this specialized field of work.
```

### After
```markdown
The primary cornerstone of behavioral health real estate development is rigorous needs validation. 
Teams must understand the complexities involved in this specialized field. 
Experienced professionals design projects that meet regulatory and clinical requirements.
```

### Generated Recommendations
- ✅ ARCHITECTURAL CONSISTENCY: Applied 1 cornerstone terminology replacement
- 🎯 ACTIVE VOICE AUTHORITY: Converted 1 passive construction for professional strength
- 📝 READABILITY ENHANCEMENT: Split 1 complex sentence for stakeholder accessibility
- 🏥 DHCS COMPLIANCE: Terminology aligns with BHCIP program standards

## Testing and Validation

The agent has been tested with:
- Chapter content from behavioral health real estate development guides
- DHCS BHCIP program documentation
- California regulatory frameworks
- Industry best practice standards

### Validation Metrics
- **Terminology Accuracy**: Cross-referenced with current DHCS guidelines
- **Professional Standards**: Reviewed by behavioral health development SMEs
- **Stakeholder Accessibility**: Validated for diverse audience comprehension
- **Regulatory Compliance**: Aligned with Proposition 1 and CARE Act requirements

## Contributing

To improve the agent's capabilities:

1. **Update BHSME Terminology**: Add new regulatory terms to `_load_bhsme_terminology()`
2. **Enhance Building Analogies**: Expand `_load_building_analogies()` with additional replacements
3. **Improve Analysis**: Refine detection patterns for better accuracy
4. **Add Domain Knowledge**: Incorporate new DHCS program updates and industry standards

## Support and Documentation

- **Agent Documentation**: See `agent.md` for detailed behavioral specifications
- **Configuration**: Review `agent.json` for input/output schemas
- **Implementation**: Examine `implementation.py` for processing logic
- **BHSME Knowledge Base**: Incorporate latest DHCS/BHCIP program updates

## Version History

- **v1.0.0**: Initial release with core editing capabilities and BHCIP compliance
- Full DHCS terminology standardization
- Architectural consistency enforcement
- Comprehensive changelog generation
- Strategic recommendation system

---

*Developed for the Wellspring behavioral health real estate development ecosystem*
*Incorporating California DHCS BHCIP program standards and industry best practices*