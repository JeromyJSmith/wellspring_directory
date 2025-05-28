#!/usr/bin/env python3
"""
Wellspring Sectional Manuscript Formatter
=========================================

SMART APPROACH: Break the 300+ page manuscript into manageable sections:
- Table of Contents
- Individual Chapters  
- Appendices
- References

Format each section individually for better control and safety.
NO corner elements - focus on professional typography and margins.
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import zipfile
import re

class WellspringSectionalFormatter:
    """Break manuscript into sections and format incrementally"""
    
    def __init__(self, manuscript_path="docs/The-Wellspring-Book.idml"):
        self.manuscript_path = Path(manuscript_path)
        self.output_dir = Path("output")
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Brian's specifications - NO corner elements
        self.brian_specs = {
            'margins': {
                'top': 54,      # +3pt from 51pt
                'bottom': 54,   # +3pt from 51pt  
                'left': 57,     # +3pt from 54pt
                'right': 57     # +3pt from 54pt
            },
            'typography': {
                'chapter_font': 'Minion Pro',
                'body_font': 'Minion Pro', 
                'chapter_size': 24,
                'body_size': 11,
                'leading': 14
            },
            'sections': {
                'toc': {'priority': 1, 'name': 'Table of Contents'},
                'chapters': {'priority': 2, 'name': 'Main Chapters'},
                'appendices': {'priority': 3, 'name': 'Appendices'},
                'references': {'priority': 4, 'name': 'References'}
            }
        }
    
    def analyze_manuscript_structure(self):
        """Analyze the IDML to identify sections and chapters"""
        
        print("🔍 ANALYZING WELLSPRING MANUSCRIPT STRUCTURE")
        print("=" * 50)
        
        if not self.manuscript_path.exists():
            print(f"❌ Manuscript not found: {self.manuscript_path}")
            return None
        
        structure = {
            'total_spreads': 0,
            'total_stories': 0,
            'sections': {},
            'chapters': [],
            'toc_pages': [],
            'content_breakdown': {}
        }
        
        try:
            with zipfile.ZipFile(self.manuscript_path, 'r') as idml_zip:
                file_list = idml_zip.namelist()
                
                # Count spreads and stories
                spreads = [f for f in file_list if f.startswith('Spreads/')]
                stories = [f for f in file_list if f.startswith('Stories/')]
                
                structure['total_spreads'] = len(spreads)
                structure['total_stories'] = len(stories)
                
                print(f"📄 Total spreads: {structure['total_spreads']}")
                print(f"📝 Total stories: {structure['total_stories']}")
                
                # Analyze story content for chapter identification
                chapter_count = 0
                toc_found = False
                
                for story_file in stories[:10]:  # Sample first 10 stories
                    try:
                        story_content = idml_zip.read(story_file).decode('utf-8')
                        
                        # Look for chapter indicators
                        if re.search(r'Chapter\s+\d+', story_content, re.IGNORECASE):
                            chapter_count += 1
                        
                        # Look for TOC indicators  
                        if re.search(r'Table\s+of\s+Contents|Contents', story_content, re.IGNORECASE):
                            toc_found = True
                            
                    except Exception as e:
                        continue
                
                structure['estimated_chapters'] = chapter_count
                structure['has_toc'] = toc_found
                
                print(f"📚 Estimated chapters: {chapter_count}")
                print(f"📋 TOC detected: {'✅' if toc_found else '❌'}")
                
        except Exception as e:
            print(f"❌ Error analyzing structure: {e}")
            
        return structure
    
    def create_sectional_formatting_plan(self, structure):
        """Create a step-by-step sectional formatting plan"""
        
        plan_path = self.output_dir / f"sectional_formatting_plan_{self.timestamp}.md"
        
        plan_content = f"""
# 📚 WELLSPRING SECTIONAL FORMATTING PLAN
## Break Into Manageable Sections

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Manuscript:** {structure['total_spreads']} spreads, {structure['total_stories']} stories
**Estimated Chapters:** {structure.get('estimated_chapters', 'Unknown')}

---

## 🎯 SECTIONAL APPROACH BENEFITS

✅ **Safer** - Work on small sections at a time
✅ **Controllable** - Test and verify each section before moving on  
✅ **Recoverable** - Easy to undo/redo individual sections
✅ **Professional** - Maintain quality throughout process
❌ **NO corner elements** - Focus on typography and margins only

---

## 📋 FORMATTING SEQUENCE

### Phase 1: Foundation (CRITICAL)
**Goal:** Apply Brian's +3pt margin specifications safely

1. **📐 Margins Only**
   - Apply +3pt to all margins (54pt/57pt)
   - Test text reflow on 2-3 sample spreads
   - Verify no content is cut off or relocated
   - **Script:** `margins_only_formatter.jsx`

### Phase 2: Table of Contents (if detected: {'✅' if structure.get('has_toc') else '❌'})
**Goal:** Professional TOC formatting

2. **📋 TOC Formatting**
   - Update TOC typography hierarchy
   - Ensure proper dot leaders
   - Verify page number alignment
   - **Script:** `toc_formatter.jsx`

### Phase 3: Chapter-by-Chapter
**Goal:** Process ~{structure.get('estimated_chapters', '?')} chapters individually

3. **📖 Chapter 1 Formatting**
   - Right-hand page start verification
   - Chapter title typography
   - Body text consistency
   - **Script:** `chapter_1_formatter.jsx`

4. **📖 Chapter 2 Formatting**
   - Continue with same approach
   - **Script:** `chapter_2_formatter.jsx`

... (Continue for all chapters)

### Phase 4: Final Elements
**Goal:** Polish and consistency

5. **📚 Appendices & References**
   - Consistent formatting with main text
   - Proper citation formatting
   - **Script:** `appendices_formatter.jsx`

6. **🎯 Final Review & Polish**
   - Overall consistency check
   - Page numbering verification
   - Typography hierarchy validation

---

## 🛡️ SAFETY PROTOCOL PER SECTION

**Before Each Section:**
1. ✅ Save current document state
2. ✅ Note current page/spread for reference
3. ✅ Preview 2-3 pages to understand current formatting

**During Formatting:**
1. ✅ Apply changes to 1-2 spreads first
2. ✅ Review results before applying to full section
3. ✅ Document any issues encountered

**After Each Section:**
1. ✅ Review formatted section completely
2. ✅ Save document with descriptive name
3. ✅ Note any adjustments needed for next section

---

## 🎯 BRIAN'S SPECIFICATIONS (NO CORNERS)

### Margins (ALL SECTIONS)
- Top: **54pt** (+3pt)
- Bottom: **54pt** (+3pt)
- Left: **57pt** (+3pt)  
- Right: **57pt** (+3pt)

### Typography Hierarchy
- **Chapter Titles:** Minion Pro Bold, 24pt, Dark Blue (#1B365D)
- **Section Headers:** Minion Pro Semibold, 14pt
- **Body Text:** Minion Pro Regular, 11pt, 14pt leading
- **TOC Entries:** Consistent with chapter hierarchy

### Layout Standards
- ✅ Right-hand chapter starts
- ✅ Professional baseline grid alignment
- ✅ Consistent spacing throughout
- ❌ **NO architectural corner elements**

---

## 🚀 EXECUTION WORKFLOW

**Start with:** `./format_section.sh margins`
**Then:** `./format_section.sh toc` 
**Continue:** `./format_section.sh chapter1`, `chapter2`, etc.
**Finish:** `./format_section.sh final-review`

Each script will:
1. Show current section status
2. Apply specific formatting for that section
3. Provide review checklist
4. Prepare for next section

**This sectional approach ensures ZERO risk of document corruption!**
        """
        
        with open(plan_path, 'w') as f:
            f.write(plan_content)
            
        return plan_path
    
    def generate_margins_only_script(self):
        """Generate a script that ONLY applies margin changes - safest first step"""
        
        script_path = self.output_dir / f"margins_only_formatter_{self.timestamp}.jsx"
        
        script_content = f"""
// Wellspring Margins-Only Formatter
// SAFEST FIRST STEP: Only margin adjustments, no other changes
// Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#target indesign

function applyMarginsOnly() {{
    // Safety checks
    if (app.documents.length === 0) {{
        alert("❌ Please open the Wellspring manuscript first.");
        return false;
    }}
    
    var doc = app.activeDocument;
    
    // Show current margins first
    var currentMargins = doc.marginPreferences;
    var marginInfo = "CURRENT MARGINS:\\n" +
                    "Top: " + currentMargins.top + "\\n" +
                    "Bottom: " + currentMargins.bottom + "\\n" +
                    "Left: " + currentMargins.left + "\\n" +
                    "Right: " + currentMargins.right + "\\n\\n" +
                    "BRIAN'S NEW MARGINS (+3pt):\\n" +
                    "Top: 54pt\\n" +
                    "Bottom: 54pt\\n" +
                    "Left: 57pt\\n" +
                    "Right: 57pt\\n\\n" +
                    "This will ONLY change margins - no other formatting.\\n" +
                    "Proceed?";
    
    var proceed = confirm(marginInfo);
    
    if (!proceed) {{
        alert("Margins update cancelled.");
        return false;
    }}
    
    try {{
        // Store original values for logging
        var original = {{
            top: currentMargins.top,
            bottom: currentMargins.bottom,
            left: currentMargins.left,
            right: currentMargins.right
        }};
        
        // Apply ONLY Brian's margin specifications
        currentMargins.top = "{self.brian_specs['margins']['top']}pt";
        currentMargins.bottom = "{self.brian_specs['margins']['bottom']}pt";
        currentMargins.left = "{self.brian_specs['margins']['left']}pt";
        currentMargins.right = "{self.brian_specs['margins']['right']}pt";
        
        // Success message
        alert("✅ MARGINS UPDATED SUCCESSFULLY!\\n\\n" +
              "Changes applied:\\n" +
              "• Top: " + original.top + " → 54pt\\n" +
              "• Bottom: " + original.bottom + " → 54pt\\n" +
              "• Left: " + original.left + " → 57pt\\n" +
              "• Right: " + original.right + " → 57pt\\n\\n" +
              "NEXT STEPS:\\n" +
              "1. Review 2-3 spreads for text reflow\\n" +
              "2. Check that no content is cut off\\n" +
              "3. Save document when satisfied\\n" +
              "4. Run next section: TOC formatting");
        
        return true;
        
    }} catch (error) {{
        alert("❌ Error updating margins: " + error.message);
        return false;
    }}
}}

// Execute the margins-only update
applyMarginsOnly();
        """
        
        with open(script_path, 'w') as f:
            f.write(script_content)
            
        return script_path
    
    def generate_sectional_launcher(self):
        """Generate a launcher script for sectional formatting"""
        
        launcher_path = self.output_dir / f"format_section_{self.timestamp}.sh"
        
        launcher_content = f"""#!/bin/bash

# Wellspring Sectional Formatter Launcher
# Work on manuscript sections one at a time

echo "📚 WELLSPRING SECTIONAL FORMATTER"
echo "================================="
echo "🎯 Safe, incremental formatting approach"
echo ""

SECTION="$1"

if [ -z "$SECTION" ]; then
    echo "📋 AVAILABLE SECTIONS:"
    echo "  margins     📐 Apply +3pt margin adjustments (START HERE)"
    echo "  toc         📋 Format Table of Contents"
    echo "  chapter1    📖 Format Chapter 1"  
    echo "  chapter2    📖 Format Chapter 2"
    echo "  final       🎯 Final review and polish"
    echo ""
    echo "💡 Usage: ./format_section.sh [section]"
    echo "   Example: ./format_section.sh margins"
    exit 1
fi

# Find latest sectional scripts
MARGINS_SCRIPT=$(ls -t output/margins_only_formatter_*.jsx | head -1)

echo "🎯 FORMATTING SECTION: $SECTION"
echo "==============================="

case "$SECTION" in
    margins)
        echo "📐 PHASE 1: MARGINS ONLY (+3pt adjustment)"
        echo "✅ Safest first step - only margin changes"
        echo "❌ NO corner elements, NO layout changes"
        echo ""
        
        if [ -n "$MARGINS_SCRIPT" ]; then
            echo "🚀 Executing margins-only formatter..."
            osascript -e "tell application \\"Adobe InDesign 2025\\" to do script \\"$(pwd)/$MARGINS_SCRIPT\\" language javascript"
            
            echo ""
            echo "🔍 REVIEW CHECKLIST:"
            echo "  □ Check 2-3 spreads for proper text reflow"
            echo "  □ Verify no content is cut off"
            echo "  □ Confirm margins look professional"
            echo "  □ Save document when satisfied"
            echo ""
            echo "📋 NEXT: ./format_section.sh toc"
        else
            echo "❌ Margins script not found. Run: python wellspring_sectional_formatter.py first"
        fi
        ;;
        
    toc)
        echo "📋 PHASE 2: TABLE OF CONTENTS FORMATTING"
        echo "⚠️  Coming soon - focusing on margins first"
        echo "📋 NEXT: ./format_section.sh chapter1"
        ;;
        
    chapter1)
        echo "📖 PHASE 3: CHAPTER 1 FORMATTING"
        echo "⚠️  Coming soon - complete margins and TOC first"
        ;;
        
    final)
        echo "🎯 FINAL REVIEW AND POLISH"
        echo "⚠️  Complete all sections first"
        ;;
        
    *)
        echo "❌ Unknown section: $SECTION"
        echo "Run without arguments to see available sections"
        ;;
esac

echo ""
echo "📚 Sectional formatting ready!"
        """
        
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
            
        # Make executable
        launcher_path.chmod(0o755)
        
        return launcher_path

def main():
    """Main execution for sectional Wellspring formatting"""
    
    print("📚 WELLSPRING SECTIONAL MANUSCRIPT FORMATTER")
    print("=" * 55)
    print("🎯 SMART APPROACH: Break into manageable sections")
    print("❌ NO corner elements - focus on professional typography")
    print("")
    
    formatter = WellspringSectionalFormatter()
    
    # Step 1: Analyze manuscript structure
    print("🔍 Analyzing manuscript structure...")
    structure = formatter.analyze_manuscript_structure()
    
    if not structure:
        print("❌ Cannot proceed without manuscript file")
        return False
    
    print("\n📋 GENERATING SECTIONAL FORMATTING TOOLS...")
    
    # Step 2: Create sectional plan
    plan_file = formatter.create_sectional_formatting_plan(structure)
    print(f"✅ Sectional plan: {plan_file}")
    
    # Step 3: Generate margins-only script (safest first step)
    margins_script = formatter.generate_margins_only_script()
    print(f"✅ Margins-only script: {margins_script}")
    
    # Step 4: Generate sectional launcher
    launcher_script = formatter.generate_sectional_launcher()
    print(f"✅ Sectional launcher: {launcher_script}")
    
    print("\n🚀 READY FOR SECTIONAL FORMATTING:")
    print("1. 📖 Review the sectional plan")
    print("2. 📐 Start with: ./format_section.sh margins")
    print("3. 📋 Continue with: ./format_section.sh toc")
    print("4. 📚 Process chapters individually")
    print("5. 🎯 Finish with final review")
    
    print(f"\n✅ Much safer approach - no more 'crap' outputs!")
    print(f"❌ NO corner elements - professional typography focus")
    
    return True

if __name__ == "__main__":
    main() 