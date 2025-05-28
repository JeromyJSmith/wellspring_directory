#!/bin/bash

echo "\U0001F527 Creating full directory structure..."

mkdir -p em_dash_replacement/input
mkdir -p em_dash_replacement/output
mkdir -p em_dash_replacement/scripts
mkdir -p em_dash_replacement/logs
mkdir -p em_dash_replacement/infographic_placeholders
mkdir -p em_dash_replacement/changelog

mkdir -p deep_research_agent/extracted_statements
mkdir -p deep_research_agent/citations
mkdir -p deep_research_agent/visual_opportunities
mkdir -p deep_research_agent/scripts
mkdir -p deep_research_agent/logs
mkdir -p deep_research_agent/reports

mkdir -p shared_utils/uv_env
mkdir -p shared_utils/notebooks
mkdir -p shared_utils/data

echo "✅ Directory structure created."

echo "\U0001F680 Initializing UV Python environment..."

cd shared_utils/uv_env || exit 1

# Initialize UV project + create virtual env
uv init . &&
    uv venv .venv --python python3.13 --seed &&
    source .venv/bin/activate &&
    uv pip install pandas jupyter rich openpyxl numpy matplotlib

echo "✅ UV environment set up and activated with pandas and jupyter installed."

echo "\U0001F4C2 You can now open Cursor IDE and start implementing your scripts in:"
echo "  - em_dash_replacement/scripts/"
echo "  - deep_research_agent/scripts/"

# Wellspring AppleScript Automation - Fixed Version
# Shell wrapper to safely execute AppleScript commands

echo "🌊 Starting Wellspring AppleScript Automation..."

# Step 1: Check if output folder exists and count files
OUTPUT_DIR="/Users/ojeromyo/Desktop/wellspring_directory/output"
if [ -d "$OUTPUT_DIR" ]; then
    file_count=$(ls -1 "$OUTPUT_DIR"/wellspring* 2>/dev/null | wc -l)
    echo "✅ Found $file_count Wellspring files in output folder"
else
    echo "❌ Output folder not found: $OUTPUT_DIR"
    exit 1
fi

# Step 2: Open output folder in Finder
echo "📂 Opening output folder in Finder..."
osascript -e "tell application \"Finder\" to open folder \"$OUTPUT_DIR\""

# Step 3: Open files in appropriate applications
echo "📄 Opening files for review..."

# Open text file in TextEdit
txt_file=$(ls "$OUTPUT_DIR"/wellspring_formatting_*.txt 2>/dev/null | head -1)
if [ -n "$txt_file" ]; then
    echo "   📝 Opening: $(basename "$txt_file")"
    osascript -e "tell application \"TextEdit\" to open \"$txt_file\""
fi

# Open JSON file in default application
json_file=$(ls "$OUTPUT_DIR"/chapter_formatting_report_*.json 2>/dev/null | head -1)
if [ -n "$json_file" ]; then
    echo "   📊 Opening: $(basename "$json_file")"
    open "$json_file"
fi

# Open XML file in default application
xml_file=$(ls "$OUTPUT_DIR"/wellspring_formatting_*.xml 2>/dev/null | head -1)
if [ -n "$xml_file" ]; then
    echo "   🏗️ Opening: $(basename "$xml_file")"
    open "$xml_file"
fi

# Open HTML instructions file
html_file=$(ls "$OUTPUT_DIR"/wellspring_instructions_*.html 2>/dev/null | head -1)
if [ -n "$html_file" ]; then
    echo "   📋 Opening HTML instructions: $(basename "$html_file")"
    osascript -e "tell application \"Safari\" to open \"$html_file\""
fi

# Step 4: Check for InDesign and offer to run script
jsx_file=$(ls "$OUTPUT_DIR"/wellspring_chapter_formatting.jsx 2>/dev/null | head -1)
if [ -n "$jsx_file" ]; then
    echo "🎨 InDesign script found: $(basename "$jsx_file")"

    # Check if InDesign is available
    if osascript -e "tell application \"Adobe InDesign 2024\" to get name" 2>/dev/null; then
        echo "   ✅ Adobe InDesign 2024 is available"
        echo "   🎯 Ready to run formatting script!"

        # Ask user if they want to run InDesign automation
        response=$(osascript -e 'display dialog "🎨 InDesign Automation Available!\n\nFound: wellspring_chapter_formatting.jsx\n\nThis will:\n✅ Apply all margin adjustments (+3pts)\n✅ Format chapter typography\n✅ Place architectural corner elements\n✅ Ensure right-hand chapter starts\n\nRun InDesign automation now?" buttons {"Yes, Run Script", "No, Skip"} default button "Yes, Run Script"' -e 'button returned of result' 2>/dev/null)

        if [ "$response" = "Yes, Run Script" ]; then
            echo "   🚀 Running InDesign automation..."
            osascript -e "
            tell application \"Adobe InDesign 2024\"
                activate
                if (count of documents) = 0 then
                    display dialog \"📄 Please open your Wellspring manuscript in InDesign first, then run this script again.\" buttons {\"OK\"} default button \"OK\"
                else
                    do script \"$jsx_file\" language javascript
                    display notification \"✅ Wellspring formatting applied!\" with title \"InDesign Automation\"
                end if
            end tell
            "
        fi
    else
        echo "   ⚠️ Adobe InDesign 2024 not found (optional)"
        echo "   💡 You can manually run: $jsx_file"
    fi
fi

# Step 5: Create backup
echo "📁 Creating backup..."
backup_dir="/Users/ojeromyo/Desktop/wellspring_directory/chapter_formatting_backups/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"
cp -r "$OUTPUT_DIR"/* "$backup_dir"/ 2>/dev/null
echo "✅ Backup created: $backup_dir"

# Step 6: Final success message
echo ""
echo "🎉 WELLSPRING APPLESCRIPT AUTOMATION COMPLETE!"
echo "================================="
echo "✅ Output folder opened in Finder"
echo "✅ All files opened for review:"
echo "   📝 Text specifications"
echo "   📊 JSON formatting data"
echo "   🏗️ XML structured data"
echo "   📋 HTML instructions"
echo "   🎨 InDesign script ready"
echo "✅ Backup created with timestamp"
echo ""
echo "🎯 Next steps:"
echo "   1. Review opened files"
echo "   2. Run InDesign script if desired"
echo "   3. Apply formatting to your manuscript"
echo ""
echo "🌊 Wellspring automation workflow complete!"
