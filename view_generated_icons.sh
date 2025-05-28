#!/bin/bash

# View Generated Wellspring Icons
# Simple script to review the uniform icons created from chapter names

echo "🎨 WELLSPRING GENERATED ICONS VIEWER"
echo "====================================="
echo "✨ Reviewing uniform icons created from chapter names"
echo "🎯 All following 'Setting the Vision' style guide"
echo ""

ICONS_DIR="icons/wellspring_goldflake_batch_tool/generated_icons"

# Check if icons exist
if [ ! -d "$ICONS_DIR" ]; then
    echo "❌ Icons directory not found: $ICONS_DIR"
    echo "📋 Please run: python wellspring_icon_generator_from_names.py first"
    exit 1
fi

# Count icons
ICON_COUNT=$(find "$ICONS_DIR" -name "*.png" | wc -l)

echo "📊 GENERATION SUMMARY:"
echo "✅ Total icons generated: $ICON_COUNT"
echo "📁 Directory: $ICONS_DIR"
echo ""

# Show first few icons
echo "🔍 SAMPLE ICONS:"
find "$ICONS_DIR" -name "*.png" | head -5 | while read icon; do
    basename="$(basename "$icon")"
    size="$(du -h "$icon" | cut -f1)"
    echo "   📄 $basename ($size)"
done

if [ $ICON_COUNT -gt 5 ]; then
    echo "   ... and $(($ICON_COUNT - 5)) more icons"
fi

echo ""
echo "🚀 REVIEW OPTIONS:"
echo "1. 📂 Open icons directory in Finder"
echo "2. 📋 Show detailed icon list"
echo "3. 🔄 Regenerate icons (if needed)"
echo "4. ✅ Icons look good, continue"
echo ""

read -p "Choose an option (1-4): " choice

case $choice in
1)
    echo ""
    echo "📂 Opening icons directory..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$ICONS_DIR"
    else
        echo "📁 Directory path: $(pwd)/$ICONS_DIR"
    fi
    ;;
2)
    echo ""
    echo "📋 DETAILED ICON LIST:"
    echo "=" * 50
    find "$ICONS_DIR" -name "*.png" | sort | while read icon; do
        basename="$(basename "$icon")"
        size="$(du -h "$icon" | cut -f1)"
        printf "%-60s %s\n" "$basename" "$size"
    done
    ;;
3)
    echo ""
    echo "🔄 Regenerating icons..."
    python wellspring_icon_generator_from_names.py
    ;;
4)
    echo ""
    echo "✅ Great! Icons are ready for use."
    echo "📋 Next steps:"
    echo "   1. Icons can be imported into InDesign"
    echo "   2. Use for chapter headers and section dividers"
    echo "   3. Maintain consistent branding throughout manuscript"
    ;;
*)
    echo ""
    echo "📂 Opening icons directory by default..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$ICONS_DIR"
    fi
    ;;
esac

echo ""
echo "🌊 Icon review complete!"
