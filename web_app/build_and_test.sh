#!/bin/bash

# Build and Test Script for Production
# This script builds the frontend and tests the production build locally

echo "🚀 Starting build process..."

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Build for production
echo "🔨 Building frontend for production..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Frontend build successful!"
    echo "📁 Build files are in: web_app/frontend/build"
    echo ""
    echo "To test the production build:"
    echo "1. Install serve: npm install -g serve"
    echo "2. Run: cd build && serve -s . -l 3000"
    echo "3. Open http://localhost:3000 in your browser"
else
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi

