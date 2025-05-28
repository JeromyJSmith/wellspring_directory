#!/bin/bash

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
            osascript -e "tell application \"Adobe InDesign 2025\" to do script \"$(pwd)/$MARGINS_SCRIPT\" language javascript"
            
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
        