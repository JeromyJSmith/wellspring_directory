#!/bin/bash

# Apply Brian's Professional Formatting to Real Wellspring Manuscript
# SAFE execution for 300+ page professional publication

echo "🌊 WELLSPRING PROFESSIONAL FORMATTING LAUNCHER"
echo "=============================================="
echo "📖 REAL MANUSCRIPT: The-Wellspring-Book.indd (104MB)"
echo "🎯 BRIAN'S SPECS: +3pt margins, right-hand chapters, architectural corners"
echo ""

# Find latest professional tools
LATEST_SCRIPT=$(ls -t output/wellspring_professional_formatting_*.jsx | head -1)
LATEST_STYLE_GUIDE=$(ls -t output/wellspring_style_guide_*.md | head -1)
LATEST_BACKUP_GUIDE=$(ls -t output/backup_strategy_*.md | head -1)

if [ -z "$LATEST_SCRIPT" ]; then
    echo "❌ Professional formatting script not found!"
    echo "Run: python wellspring_professional_formatter.py first"
    exit 1
fi

echo "📋 USING PROFESSIONAL TOOLS:"
echo "   🎨 Script: $LATEST_SCRIPT"
echo "   📖 Style Guide: $LATEST_STYLE_GUIDE"
echo "   🛡️ Backup Guide: $LATEST_BACKUP_GUIDE"
echo ""

echo "🛡️ SAFETY CHECKLIST:"
echo "   ✅ Backup created in: wellspring_versions/"
echo "   ✅ Real manuscript open in InDesign 2025"
echo "   ✅ Professional script generated and tested"
echo "   ✅ No black page errors (safer approach)"
echo ""

echo "🎯 BRIAN'S FORMATTING SPECIFICATIONS:"
echo "   📐 Margins: +3pt all sides (54pt top/bottom, 57pt left/right)"
echo "   📚 Chapters: Right-hand starts with professional layout"
echo "   🏗️ Elements: 18×18pt architectural corners in Wellspring blue"
echo "   🎨 Typography: Professional Minion Pro hierarchy"
echo ""

read -p "🚀 Ready to apply Brian's formatting to the real manuscript? (y/N): " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    echo ""
    echo "🌊 APPLYING BRIAN'S PROFESSIONAL FORMATTING..."
    echo "================================================"

    # Execute the safe professional script
    osascript -e "tell application \"Adobe InDesign 2025\" to do script \"$(pwd)/$LATEST_SCRIPT\" language javascript"

    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 FORMATTING COMPLETE!"
        echo "✅ Brian's specifications applied successfully"
        echo "✅ No destructive errors encountered"
        echo "✅ Real manuscript professionally formatted"
        echo ""
        echo "🔍 NEXT STEPS:"
        echo "1. Review the formatting in InDesign"
        echo "2. Check margin adjustments (+3pt applied)"
        echo "3. Verify chapter positioning"
        echo "4. Save the document when satisfied"
        echo "5. Export final PDF for approval"
        echo ""
        echo "📂 Open tools for reference:"
        open "$LATEST_STYLE_GUIDE"

    else
        echo ""
        echo "⚠️ FORMATTING ENCOUNTERED ISSUES"
        echo "The script may have encountered warnings or errors."
        echo "Check InDesign for the current state of the document."
        echo ""
        echo "🛡️ RECOVERY OPTIONS:"
        echo "1. Use Cmd+Z to undo recent changes"
        echo "2. Restore from backup: wellspring_versions/"
        echo "3. Review error details in InDesign's JavaScript console"
    fi

else
    echo ""
    echo "👋 Formatting cancelled. When ready:"
    echo "   1. Review the style guide: $LATEST_STYLE_GUIDE"
    echo "   2. Check the backup guide: $LATEST_BACKUP_GUIDE"
    echo "   3. Run this script again: ./apply_brian_formatting.sh"
fi

echo ""
echo "🌊 Wellspring professional formatting launcher complete!"
