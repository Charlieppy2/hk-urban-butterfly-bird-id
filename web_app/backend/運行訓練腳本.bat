@echo off
chcp 65001 >nul
echo ========================================
echo AI Assistant 訓練腳本
echo ========================================
echo.
cd /d "%~dp0"
echo 當前目錄: %CD%
echo.
echo 請選擇操作:
echo 1. 互動式訓練 (add, stats, etc.)
echo 2. 從文件訓練 (training_data.json)
echo 3. 查看統計
echo 4. 創建訓練模板
echo.
set /p choice="請輸入選項 (1-4): "

if "%choice%"=="1" (
    echo.
    echo 啟動互動式訓練模式...
    echo 可用命令: add, stats, load, template, quit
    echo.
    python train_assistant.py
) else if "%choice%"=="2" (
    echo.
    echo 從 training_data.json 訓練...
    python train_assistant.py train training_data.json
) else if "%choice%"=="3" (
    echo.
    echo 顯示知識庫統計...
    python train_assistant.py stats
) else if "%choice%"=="4" (
    echo.
    echo 創建訓練模板...
    python train_assistant.py template
) else (
    echo 無效選項！
    pause
    exit /b 1
)

echo.
echo 完成！
pause

