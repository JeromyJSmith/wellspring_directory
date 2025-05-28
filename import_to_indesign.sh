#!/bin/bash

# Wellspring PDF → InDesign Safe Import Helper
# Automates the safe import process for properly formatted PDF

echo "🎨 WELLSPRING PDF → INDESIGN IMPORT HELPER"
echo "=========================================="

# Find the latest PDF
LATEST_PDF=$(ls -t output/wellspring_formatted_*.pdf | head -1)
LATEST_GUIDE=$(ls -t output/indesign_import_guide_*.md | head -1)

if [ -z "$LATEST_PDF" ]; then
    echo "❌ No formatted PDF found. Run the PDF workflow first!"
    exit 1
fi

echo "📄 Using PDF: $LATEST_PDF"
echo "📋 Guide: $LATEST_GUIDE"
echo ""

echo "🎯 SAFE IMPORT PROCESS:"
echo "======================"
echo ""
echo "✅ Step 1: PDF Generated with Brian's formatting:"
echo "   • +3pt margins (54pt top/bottom, 57pt left/right)"
echo "   • Right-hand chapter starts"
echo "   • Architectural corner elements"
echo "   • Professional typography"
echo ""

echo "📝 Step 2: InDesign Import (MANUAL):"
echo "   1. Open Adobe InDesign 2025"
echo "   2. File → New Document"
echo "   3. Set margins: Top 54pt, Bottom 54pt, Left 57pt, Right 57pt"
echo "   4. File → Place → Select: $LATEST_PDF"
echo "   5. Check 'Import All Pages' and 'Vector Graphics'"
echo "   6. Click to place - DONE!"
echo ""

echo "🚀 Starting InDesign and opening files..."

# Open InDesign (if available)
if command -v osascript >/dev/null 2>&1; then
    echo "🎨 Opening InDesign 2025..."
    osascript -e 'tell application "Adobe InDesign 2025" to activate' 2>/dev/null || echo "   ℹ️  InDesign not running - please open manually"

    echo "📄 Opening PDF for reference..."
    open "$LATEST_PDF"

    echo "📋 Opening import guide..."
    open "$LATEST_GUIDE"

    echo ""
    echo "🎯 READY FOR IMPORT!"
    echo "Follow the guide to import the PDF safely into InDesign."
    echo ""
    echo "🛡️ ADVANTAGES OF THIS APPROACH:"
    echo "   ✅ No risky InDesign scripting"
    echo "   ✅ No black page errors"
    echo "   ✅ Predictable formatting"
    echo "   ✅ Easy to review before import"
    echo "   ✅ Can restart if needed"

else
    echo "❌ AppleScript not available. Please:"
    echo "   1. Open InDesign 2025 manually"
    echo "   2. Follow the import guide: $LATEST_GUIDE"
    echo "   3. Import PDF: $LATEST_PDF"
fi

echo ""
echo "🌊 Wellspring safe import ready!"
