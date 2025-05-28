#!/bin/bash

# Wellspring OpenAI Batch Image Generator - Launcher
# Creates professional chapter images using OpenAI 4o with real textures

echo "🎨 WELLSPRING OPENAI BATCH IMAGE GENERATOR"
echo "=" * 50
echo "🎯 Creating professional chapter images with OpenAI 4o"
echo "✨ Using real gold flake textures and rich imagery"
echo ""

cd "$(dirname "$0")"
cd ../..

# Check for background texture
if [ -f "icons/background - 01.png" ]; then
    echo "✅ Found background texture: icons/background - 01.png"
else
    echo "❌ Background texture not found!"
    echo "Please ensure 'background - 01.png' is in the icons/ directory"
    exit 1
fi

# Check OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OpenAI API key not found!"
    echo "Please set OPENAI_API_KEY environment variable"
    echo ""
    echo "Example:"
    echo "export OPENAI_API_KEY='your-api-key-here'"
    exit 1
else
    echo "✅ OpenAI API key found"
fi

echo ""
echo "📋 WHAT THIS WILL CREATE:"
echo "✅ Professional chapter cover images (1024×1792)"
echo "✅ Dark leather background with rich texture"
echo "✅ Ornate gold borders and decorative elements"
echo "✅ Large, prominent symbolic imagery (NOT tiny icons)"
echo "✅ Context-aware imagery based on chapter content"
echo "✅ Batch processing with OpenAI 4o (DALL-E 3)"
echo ""

echo "💰 COST ESTIMATE:"
echo "📊 ~20-25 images at $0.080 each = ~$1.60-2.00"
echo "⏱️  Processing time: 15-30 minutes"
echo ""

echo "📁 OUTPUT DIRECTORY:"
echo "icons/wellspring_goldflake_batch_tool/openai_batch_processing/generated_images/"
echo ""

read -p "🚀 Ready to start OpenAI batch generation? (y/N): " confirm

if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    echo ""
    echo "🎬 LAUNCHING BATCH GENERATOR..."
    echo ""

    python wellspring_openai_image_batch_generator.py

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ BATCH GENERATOR COMPLETED!"
        echo ""
        echo "🔄 TO CHECK STATUS:"
        echo "python wellspring_openai_image_batch_generator.py status"
        echo ""
        echo "📥 TO DOWNLOAD WHEN READY:"
        echo "python wellspring_openai_image_batch_generator.py check"
    else
        echo ""
        echo "❌ BATCH GENERATOR FAILED!"
        echo "Check error messages above for details."
    fi
else
    echo ""
    echo "📋 Batch generation cancelled."
    echo "Run this script again when ready to proceed."
fi
