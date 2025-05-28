#!/bin/bash

# Simple TOC Line Spacing Formatter
# Focus on JUST the Table of Contents spacing

echo "📋 WELLSPRING TOC LINE SPACING FORMATTER"
echo "========================================"
echo "🎯 SIMPLE FOCUS: Adjust line spacing in Table of Contents only"
echo ""

# Check if TOC script exists
if [ ! -f "toc_line_spacing_formatter.jsx" ]; then
    echo "❌ TOC spacing script not found!"
    echo "The script 'toc_line_spacing_formatter.jsx' should be in this directory."
    exit 1
fi

echo "📋 WHAT THIS WILL DO:"
echo "✅ Find Table of Contents in your document"
echo "✅ Adjust line spacing to 16pt (more readable)"
echo "✅ Add 6pt spacing after each TOC line"
echo "✅ Keep dot leaders and page numbers aligned"
echo ""

echo "🛡️ SAFETY:"
echo "✅ Only affects TOC content"
echo "✅ No other document changes"
echo "✅ Easy to undo with Cmd+Z"
echo ""

read -p "🚀 Ready to improve TOC line spacing? (y/N): " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    echo ""
    echo "📋 Executing TOC line spacing formatter..."

    # Run the InDesign script
    osascript -e "tell application \"Adobe InDesign 2025\" to do script \"$(pwd)/toc_line_spacing_formatter.jsx\" language javascript"

    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 TOC SPACING UPDATE COMPLETE!"
        echo ""
        echo "🔍 REVIEW CHECKLIST:"
        echo "  □ Check Table of Contents pages"
        echo "  □ Verify improved line spacing (16pt leading)"
        echo "  □ Confirm dot leaders still align properly"
        echo "  □ Check page numbers are still readable"
        echo "  □ Save document when satisfied"
        echo ""
        echo "💡 If spacing looks good, this was much simpler than the complex approach!"
    else
        echo ""
        echo "⚠️ Script completed with warnings"
        echo "Check InDesign for the current state of TOC formatting."
    fi

else
    echo ""
    echo "👋 TOC spacing adjustment cancelled."
    echo ""
    echo "📋 When ready to improve TOC spacing:"
    echo "   1. Open the Wellspring manuscript in InDesign 2025"
    echo "   2. Run: ./toc_spacing.sh"
    echo "   3. Review the improved line spacing"
fi

echo ""
echo "📋 Simple TOC formatting complete!"
