#!/bin/bash

# Wellspring Experimental Workflow
# Safe iteration: Test → Evaluate → Restore → Improve

echo "🧪 WELLSPRING EXPERIMENTAL WORKFLOW"
echo "===================================="
echo ""
echo "📋 Available Tests:"
echo "  1. 🔍 Diagnostics (read-only, totally safe)"
echo "  2. 📐 Margins only (Brian's +3pt request)"
echo "  3. 🎨 Safe corner elements (small test)"
echo "  4. 🔄 Restore from backup"
echo "  5. 🏠 Exit"
echo ""

read -p "👉 Choose test (1-5): " choice

case $choice in
1)
    echo "🔍 Running diagnostic test (read-only)..."
    osascript -e "tell application \"Adobe InDesign 2025\" to do script \"/Users/ojeromyo/Desktop/wellspring_directory/output/test_1_diagnostics.jsx\" language javascript"
    ;;
2)
    echo "📐 Running margins-only test..."
    osascript -e "tell application \"Adobe InDesign 2025\" to do script \"/Users/ojeromyo/Desktop/wellspring_directory/output/wellspring_safe_formatting.jsx\" language javascript"
    ;;
3)
    echo "🎨 Corner elements test not ready yet..."
    echo "   We'll build this after margins work perfectly!"
    ;;
4)
    echo "🔄 Restoring from backup..."
    chmod +x restore_backup.sh && ./restore_backup.sh
    ;;
5)
    echo "👋 Happy experimenting!"
    ;;
*)
    echo "❌ Invalid choice. Please run again and choose 1-5."
    ;;
esac

echo ""
echo "🎯 Ready for next iteration!"
