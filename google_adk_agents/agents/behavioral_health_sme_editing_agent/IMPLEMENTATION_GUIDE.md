# Implementation & Usage Guide

## BHSME Agent v3.0.0 - Essential Files & Directories

## ⚠️ **CRITICAL SAFEGUARDS NOTICE**

🚨 **IMPORTANT**: This agent includes **critical safeguards** to prevent
internal performance metrics from appearing in published content.

❌ **FORBIDDEN IN PUBLISHED CONTENT:**

- "Time to Stakeholder Buy-in" → ✅ "Stakeholder Approval Achieved 41% Faster"
- "compliance score", "avg_confidence", "total edits applied" → Internal
  analytics only
- "performance metrics", "validation_status" → Development use only

🛡️ **SAFEGUARDS ACTIVE:**

- Automatic validation prevents metric leakage
- Human review protocols enforced
- SME validation required before publication

---

### **Quick Start: What You Actually Need**

---

## 🔧 **Core Files (Must Have)**

### **1. Primary Implementation**

```
📁 /behavioral_health_sme_editing_agent/
├── implementation_advanced.py      # 🎯 MAIN AGENT (this is what you run)
├── agent_advanced.json            # ⚙️ CONFIGURATION (settings & rules)
└── quick_test.py                  # ✅ SIMPLE TEST (verify it works)
```

**These 3 files are all you need to run the agent.**

---

## 📂 **Directory Structure for Usage**

### **Input Location**

```
📁 YOUR_PROJECT/
├── input_chapters/                # 🔤 PUT YOUR CONTENT HERE
│   ├── chapter_1.md              # Your markdown content
│   ├── chapter_2.md              # One file per chapter
│   └── facility_proposal.md      # Any .md files work
```

### **Output Location**

```
📁 YOUR_PROJECT/
├── output/                       # 📤 ENHANCED CONTENT APPEARS HERE
│   ├── chapter_1_enhanced.md    # Original + "_enhanced" 
│   ├── chapter_2_enhanced.md    # Same naming pattern
│   └── processing_log.txt       # Detailed change log
```

### **Configuration**

```
📁 /behavioral_health_sme_editing_agent/
├── agent_advanced.json          # 🎛️ EDIT THIS for custom settings
└── CORRECTED_METRICS.md         # 📊 Performance benchmarks
```

---

## ⚡ **How to Use the Agent**

### **Option 1: Simple Python Usage**

```python
# Basic usage - just process text
from implementation_advanced import process_agent_request

input_data = {
    "text": "Your chapter content here...",
    "chapter_title": "Chapter 1: Foundation Framework"
}

results = process_agent_request(input_data)
print("Enhanced:", results['edited_text'])
print("Score:", results['bhsme_compliance_score'])
```

### **Option 2: Advanced Context Usage**

```python
# Advanced usage with project context
from implementation_advanced import process_agent_request

input_data = {
    "text": "Your content...",
    "chapter_title": "Chapter 1: Crisis Response",
    "project_context": {
        "project_name": "BHCIP Grant Application",
        "facility_types": ["PHF", "CSU"],
        "funding_source": "BHCIP Bond Grant Round 1",
        "target_population": ["adults", "youth"]
    },
    "focus_areas": ["pillar_replacement", "bhsme_terminology"]
}

results = process_agent_request(input_data)
```

### **Option 3: Quick Test**

```bash
# Run this to verify everything works
python quick_test.py
```

---

## 📊 **Understanding the Output**

### **Main Results Object**

```python
results = {
    'edited_text': "Enhanced version of your content",
    'changelog': "Detailed list of all changes made",
    'statistics': {
        'total_edits_applied': 5,           # How many changes
        'avg_confidence': 0.92,             # How confident (0-1)
        'high_confidence_edits': 4          # Edits above 0.8 confidence
    },
    'bhsme_compliance_score': 9.2,         # Overall quality (0-10)
    'recommendations': [                    # Strategic suggestions
        "Consider adding DHCS reference...",
        "Enhance facility-specific language..."
    ]
}
```

### **Key Metrics to Watch**

- **`bhsme_compliance_score`**: Target 8.5+ (excellent is 9.0+)
- **`avg_confidence`**: Target 0.85+ (high precision)
- **`total_edits_applied`**: More edits ≠ better (quality over quantity)

---

## ⚙️ **Configuration (agent_advanced.json)**

### **Key Settings You Can Change**

```json
{
    "focus_areas": {
        "pillar_replacement": {
            "enabled": true, // Turn on/off pillar → cornerstone
            "auto_apply": true // Automatic vs manual approval
        },
        "passive_voice": {
            "enabled": true, // Active voice conversion
            "confidence_threshold": 0.8 // How confident before applying
        }
    },
    "compliance_targets": {
        "dhcs_compliance": 9.0, // Minimum DHCS score target
        "readability": 8.5 // Readability target
    }
}
```

### **Project Context Templates**

```json
{
    "project_templates": {
        "bhcip_grant": {
            "facility_types": ["PHF", "CSU", "BHUC"],
            "compliance_requirements": ["DHCS", "OSHPD", "Title 22"],
            "funding_source": "BHCIP Bond Grant Round 1"
        },
        "mhsa_proposal": {
            "facility_types": ["STRTP", "PRTF"],
            "compliance_requirements": ["MHSA", "Title 22"],
            "funding_source": "Mental Health Services Act"
        }
    }
}
```

---

## 🚨 **Common Issues & Solutions**

### **Problem: Low Compliance Scores**

```
❌ bhsme_compliance_score: 6.8/10
```

**Solution**: Add project context with facility types and funding source

```python
"project_context": {
    "facility_types": ["PHF", "CSU"],
    "funding_source": "BHCIP Bond Grant Round 1"
}
```

### **Problem: No Edits Applied**

```
❌ total_edits_applied: 0
```

**Solution**: Your content might already be excellent, or adjust focus areas

```python
"focus_areas": ["pillar_replacement", "passive_voice", "vague_openers"]
```

### **Problem: Too Many Edits**

```
❌ total_edits_applied: 47 (over-editing)
```

**Solution**: Increase confidence thresholds in `agent_advanced.json`

```json
"confidence_threshold": 0.9  // Higher = fewer, better edits
```

---

## 📁 **File Priority (What to Focus On)**

### **Essential Files (Start Here)**

1. **`implementation_advanced.py`** - The actual agent
2. **`agent_advanced.json`** - Configuration settings
3. **`quick_test.py`** - Verify it works

### **Helpful References**

4. **`README_COMPREHENSIVE.md`** - Complete documentation
5. **`CORRECTED_METRICS.md`** - Performance expectations
6. **`enhanced_context_demo.py`** - Advanced usage examples

### **Optional (For Learning)**

7. **`demo_advanced.py`** - Full feature demonstration
8. **`test_chapters_demo.py`** - Detailed testing

---

## 🎯 **Typical Workflow**

### **Step 1: Prepare Content**

```
1. Create your markdown file with chapter content
2. Put it in your input directory
3. Note the chapter title/purpose
```

### **Step 2: Configure Agent**

```
1. Edit agent_advanced.json if needed
2. Set your facility types, funding source
3. Choose focus areas (pillar_replacement, etc.)
```

### **Step 3: Process Content**

```
1. Run implementation_advanced.py
2. Check bhsme_compliance_score (target: 8.5+)
3. Review changelog for specific changes
```

### **Step 4: Review Results**

```
1. Read enhanced content
2. Check recommendations for strategic improvements
3. Apply feedback if stakeholder validation enabled
```

---

## 📋 **Quick Reference Commands**

```bash
# Test the system
python quick_test.py

# Run advanced demo
python demo_advanced.py

# Test on real chapters
python test_chapters_demo.py

# Check enhanced context features
python enhanced_context_demo.py
```

### **File Locations Summary**

- **Agent Code**: `implementation_advanced.py` (main directory)
- **Configuration**: `agent_advanced.json` (main directory)
- **Your Input**: Create your own input folder
- **Output**: Results returned in Python object (save where you want)
- **Logs**: Included in results object or create your own logging

**Bottom Line**: You need 3 files to get started, the rest is documentation and
examples. Focus on `implementation_advanced.py` + `agent_advanced.json` + your
content.
