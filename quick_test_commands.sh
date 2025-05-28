#!/bin/bash

# Quick Direct Test Commands for Wellspring Experiments

echo "🎯 WELLSPRING QUICK TESTS"
echo "========================"

# Quick command functions
function test_diagnostics() {
    echo "🔍 Running diagnostics (read-only)..."
    osascript -e "tell application \"Adobe InDesign 2025\" to do script \"/Users/ojeromyo/Desktop/wellspring_directory/output/test_1_diagnostics.jsx\" language javascript"
    echo "✅ Diagnostics complete!"
}

function test_safe_margins() {
    echo "📐 Running safe margins test..."
    osascript -e "tell application \"Adobe InDesign 2025\" to do script \"/Users/ojeromyo/Desktop/wellspring_directory/output/wellspring_safe_formatting.jsx\" language javascript"
    echo "✅ Margins test complete!"
}

function restore_backup() {
    echo "🔄 Restoring from backup..."
    ./restore_backup.sh
}

# Show available commands
echo "Available quick commands:"
echo "  ./quick_test_commands.sh diagnostics   # 🔍 Read-only document info"
echo "  ./quick_test_commands.sh margins       # 📐 Safe margin changes only"
echo "  ./quick_test_commands.sh restore       # 🔄 Restore from backup"
echo ""

# Handle command line arguments
case "$1" in
diagnostics | diag)
    test_diagnostics
    ;;
margins | margin)
    test_safe_margins
    ;;
restore | backup)
    restore_backup
    ;;
*)
    echo "💡 Usage examples:"
    echo "  ./quick_test_commands.sh diagnostics"
    echo "  ./quick_test_commands.sh margins"
    echo "  ./quick_test_commands.sh restore"
    echo ""
    echo "🎮 Or run: ./experiment.sh for interactive menu"
    ;;
esac
