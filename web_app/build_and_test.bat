@echo off
REM Build and Test Script for Production (Windows)
REM This script builds the frontend and tests the production build locally

echo 🚀 Starting build process...

REM Navigate to frontend directory
cd frontend

REM Install dependencies
echo 📦 Installing frontend dependencies...
call npm install

REM Build for production
echo 🔨 Building frontend for production...
call npm run build

if %ERRORLEVEL% EQU 0 (
    echo ✅ Frontend build successful!
    echo 📁 Build files are in: web_app\frontend\build
    echo.
    echo To test the production build:
    echo 1. Install serve: npm install -g serve
    echo 2. Run: cd build ^&^& serve -s . -l 3000
    echo 3. Open http://localhost:3000 in your browser
) else (
    echo ❌ Build failed. Please check the errors above.
    exit /b 1
)

pause

