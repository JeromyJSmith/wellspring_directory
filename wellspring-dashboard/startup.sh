#!/bin/bash

# 🚀 Wellspring Dashboard Startup Script

echo "🚀 Starting Wellspring Project Ops Command Center..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm detected"

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
else
    echo "✅ Dependencies already installed"
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "⚠️  No .env.local file found. Creating from .env.example..."
    cp .env.example .env.local
    echo "📝 Please update .env.local with your Supabase credentials"
fi

# Run type checking
echo "🔍 Running type check..."
npm run type-check
if [ $? -ne 0 ]; then
    echo "⚠️  Type check failed, but continuing..."
fi

# Start the development server
echo "🌟 Starting development server..."
echo "🔗 Dashboard will be available at: http://localhost:3000/dashboard/overview"
echo "⏹️  Press Ctrl+C to stop"

npm run dev