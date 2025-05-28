#!/bin/bash

# 🚀 Wellspring OpenAI Batch Processing Setup
# ============================================

echo "🚀 Setting up OpenAI Batch Processing for Wellspring..."

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Not in a virtual environment. Consider activating one first."
    echo "   To create one: python -m venv .venv && source .venv/bin/activate"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update pip first
echo "📦 Updating pip..."
pip install --upgrade pip

# Install required packages
echo "📦 Installing OpenAI SDK and dependencies..."
pip install --upgrade openai
pip install fastapi uvicorn python-multipart

# Install optional dependencies if not already present
echo "📦 Installing additional dependencies..."
pip install requests httpx rich click python-dotenv pandas

echo "✅ Dependencies installed successfully!"

# Check if OpenAI API key is set
if [[ -z "$OPENAI_API_KEY" ]]; then
    echo ""
    echo "⚠️  OPENAI_API_KEY environment variable not set!"
    echo "   Please set it in your .env file or export it:"
    echo "   export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    echo "   Your .env file should contain:"
    echo "   OPENAI_API_KEY=sk-proj-your-key-here"
    echo ""
else
    echo "✅ OPENAI_API_KEY is configured"
fi

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x openai_batch_processor.py
chmod +x batch_endpoint.py
chmod +x example_usage.py

# Test the installation
echo "🧪 Testing installation..."
python -c "
try:
    from openai import OpenAI
    print('✅ OpenAI SDK imported successfully')
except ImportError as e:
    print(f'❌ Error importing OpenAI: {e}')

try:
    import fastapi
    print('✅ FastAPI imported successfully')
except ImportError as e:
    print(f'❌ Error importing FastAPI: {e}')
"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📖 Usage Examples:"
echo "   1. CLI Usage:"
echo "      python openai_batch_processor.py --input /path/to/visual_batch_prompts.json"
echo ""
echo "   2. API Server:"
echo "      python batch_endpoint.py"
echo "      # Server will run on http://localhost:8000"
echo ""
echo "   3. Example Script:"
echo "      python example_usage.py"
echo ""
echo "📁 Files created:"
echo "   - openai_batch_processor.py  (Main batch processing class)"
echo "   - batch_endpoint.py          (FastAPI REST endpoint)"
echo "   - example_usage.py           (Usage examples)"
echo "   - setup_batch_processing.sh  (This setup script)"
echo ""
echo "🔗 API Documentation will be available at:"
echo "   http://localhost:8000/docs (when server is running)"
echo ""