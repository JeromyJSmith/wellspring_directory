#!/bin/bash

# Wellspring Chapter Branding Launcher
# Creates uniform chapter covers matching "Setting the Vision" style

echo "🎨 WELLSPRING CHAPTER BRANDING AGENT"
echo "===================================="
echo "✨ Creating professional chapter covers"
echo "🎯 Matching 'Setting the Vision' aesthetic"
echo ""

cd "$(dirname "$0")"
cd ../..

echo "📋 WHAT THIS AGENT DOES:"
echo "✅ Dark leather background texture"
echo "✅ Ornate gold decorative borders"
echo "✅ Classical architectural columns"
echo "✅ Mystical sun symbol with radiating beams"
echo "✅ Open book symbol at bottom"
echo "✅ Professional gold typography"
echo "✅ Consistent layout and spacing"
echo ""

echo "📁 DIRECTORY SETUP:"
echo "Input:  icons/wellspring_goldflake_batch_tool/input_images/"
echo "Output: icons/wellspring_goldflake_batch_tool/processed_images/"
echo ""

# Check if input directory has images
INPUT_DIR="icons/wellspring_goldflake_batch_tool/input_images"
IMAGE_COUNT=$(find "$INPUT_DIR" -name "*.png" -o -name "*.jpg" 2>/dev/null | wc -l)

if [ "$IMAGE_COUNT" -eq 0 ]; then
    echo "📋 SETUP NEEDED:"
    echo "1. Add your chapter images to: $INPUT_DIR"
    echo "2. Run this script again"
    echo ""
    echo "💡 Currently no images found to process."

    # Create input directory if it doesn't exist
    mkdir -p "$INPUT_DIR"
    echo "✅ Created input directory: $INPUT_DIR"

else
    echo "📁 Found $IMAGE_COUNT images ready to process"
    echo ""

    read -p "🚀 Ready to create professional chapter covers? (y/N): " confirm

    if [[ $confirm =~ ^[Yy]$ ]]; then
        echo ""
        echo "🎨 Creating chapter covers matching 'Setting the Vision' style..."
        echo ""

        # Run the Python agent
        python3 wellspring_chapter_branding_agent.py

        if [ $? -eq 0 ]; then
            echo ""
            echo "🎉 CHAPTER BRANDING COMPLETE!"
            echo ""
            echo "📁 Check your new covers in:"
            echo "   icons/wellspring_goldflake_batch_tool/processed_images/"
            echo ""
            echo "🔍 NEXT STEPS:"
            echo "1. Review the generated covers"
            echo "2. Compare with 'Setting the Vision' reference"
            echo "3. Let me know what adjustments you'd like!"
            echo ""

            # Open output directory if on macOS
            if [[ "$OSTYPE" == "darwin"* ]]; then
                echo "📂 Opening output directory..."
                open "icons/wellspring_goldflake_batch_tool/processed_images/"
            fi

        else
            echo ""
            echo "⚠️ Processing completed with some issues"
            echo "Check the output above for details"
        fi

    else
        echo ""
        echo "👋 Chapter branding cancelled."
        echo "When ready, run: ./icons/wellspring_goldflake_batch_tool/create_chapter_branding.sh"
    fi
fi

echo ""
echo "🌊 Chapter branding agent ready!"
