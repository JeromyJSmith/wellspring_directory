#!/bin/bash

# Multiple TOC Approaches - Try Different Methods
# Learning from the failure and trying new approaches

echo "🔄 WELLSPRING TOC - MULTIPLE APPROACHES"
echo "======================================"
echo "💪 Learning from the fail, trying different methods"
echo ""

echo "📋 AVAILABLE APPROACHES:"
echo ""
echo "1. 🔍 diagnostic    - Scan document to see what content exists"
echo "2. 🎯 manual        - Select TOC text first, then apply spacing"
echo "3. 🔄 retry-auto    - Try the automatic TOC finder again"
echo "4. 📖 help          - Show manual formatting tips"
echo ""

read -p "Which approach would you like to try? (1-4): " choice

case $choice in
1 | diagnostic)
    echo ""
    echo "🔍 RUNNING DIAGNOSTIC SCAN..."
    echo "This will show what text content actually exists in your document."
    echo ""

    osascript -e "tell application \"Adobe InDesign 2025\" to do script \"$(pwd)/diagnostic_content_scanner.jsx\" language javascript"

    echo ""
    echo "📋 Check the InDesign alert for the diagnostic report!"
    echo "This will help us understand why the first approach failed."
    ;;

2 | manual)
    echo ""
    echo "🎯 MANUAL SELECTION APPROACH"
    echo "=============================="
    echo ""
    echo "📋 STEPS:"
    echo "1. In InDesign, use the Text tool (T)"
    echo "2. Select/highlight your Table of Contents text"
    echo "3. With text selected, run the spacing script"
    echo ""

    read -p "Ready to run manual spacing script? (y/N): " manual_confirm

    if [[ $manual_confirm =~ ^[Yy]$ ]]; then
        echo "🎯 Running manual spacing script..."
        osascript -e "tell application \"Adobe InDesign 2025\" to do script \"$(pwd)/toc_manual_spacing.jsx\" language javascript"
    else
        echo "👋 Select your TOC text first, then run: ./try_toc_approaches.sh 2"
    fi
    ;;

3 | retry-auto)
    echo ""
    echo "🔄 RETRYING AUTOMATIC TOC FINDER..."
    echo "Maybe it will work better this time!"
    echo ""

    osascript -e "tell application \"Adobe InDesign 2025\" to do script \"$(pwd)/toc_line_spacing_formatter.jsx\" language javascript"
    ;;

4 | help)
    echo ""
    echo "📖 MANUAL TOC FORMATTING TIPS"
    echo "============================="
    echo ""
    echo "If scripts aren't working, you can format manually:"
    echo ""
    echo "1. 🎯 Select TOC text in InDesign"
    echo "2. 📐 Open Paragraph panel (Window > Type & Tables > Paragraph)"
    echo "3. 📝 Set Leading to 16pt (line spacing)"
    echo "4. 📏 Set Space After to 8pt"
    echo "5. ✅ Keep alignment as is"
    echo ""
    echo "This gives you the same result as the scripts!"
    ;;

*)
    echo ""
    echo "❌ Invalid choice. Please run again with option 1-4."
    echo ""
    echo "Quick options:"
    echo "  ./try_toc_approaches.sh 1  (diagnostic)"
    echo "  ./try_toc_approaches.sh 2  (manual)"
    ;;
esac

echo ""
echo "🔄 Keep trying different approaches until we find what works!"
