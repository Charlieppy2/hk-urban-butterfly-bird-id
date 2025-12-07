# VS Code 安裝指南 - Butterfly & Bird Identifier

本指南將幫助您使用 Visual Studio Code (VS Code) 來安裝和運行蝴蝶與鳥類識別系統。

## 📋 前置要求

在開始之前，請確保已安裝以下軟件：

1. **Visual Studio Code**
   - 下載地址：https://code.visualstudio.com/
   - 安裝時請勾選 "Add to PATH" (Windows) 或使用默認設置 (Mac)

2. **Python 3.8 或更高版本**
   - 下載地址：https://www.python.org/downloads/
   - 安裝時請勾選 "Add Python to PATH" (Windows)
   - Mac 通常已預裝 Python，或使用 Homebrew: `brew install python3`

3. **Node.js 16 或更高版本**
   - 下載地址：https://nodejs.org/
   - 建議安裝 LTS 版本

4. **Git**
   - Windows: https://git-scm.com/download/win
   - Mac: 通常已預裝，或使用 Homebrew: `brew install git`

5. **Git LFS** (用於下載大文件)
   - Windows: https://git-lfs.github.com/
   - Mac: `brew install git-lfs` 或下載安裝包

## 🚀 安裝步驟

### 步驟 1: 安裝 VS Code 擴展

打開 VS Code，安裝以下推薦擴展：

1. **Python** (Microsoft)
   - 擴展 ID: `ms-python.python`
   - 用於 Python 開發和調試

2. **ES7+ React/Redux/React-Native snippets** (可選)
   - 擴展 ID: `dsznajder.es7-react-js-snippets`
   - 用於 React 開發

3. **GitLens** (可選)
   - 擴展 ID: `eamodio.gitlens`
   - 用於 Git 版本控制

**安裝方法：**
- 按 `Ctrl+Shift+X` (Windows) 或 `Cmd+Shift+X` (Mac) 打開擴展面板
- 搜索擴展名稱並點擊 "Install"

### 步驟 2: 從 GitHub 克隆項目

#### 方法一：使用 VS Code 內置 Git

1. 打開 VS Code
2. 按 `Ctrl+Shift+P` (Windows) 或 `Cmd+Shift+P` (Mac) 打開命令面板
3. 輸入 `Git: Clone` 並選擇
4. 輸入倉庫 URL: `https://github.com/Charlieppy2/butterfly-bird-identifier.git`
5. 選擇要保存項目的文件夾（可以是任何位置，例如 `Documents` 或 `Desktop`）
6. 點擊 "Open" 打開克隆的項目

#### 方法二：使用終端

**Windows (PowerShell 或 Command Prompt):**
```powershell
# 導航到您想要保存項目的目錄（例如 Documents）
cd Documents

# 克隆項目
git clone https://github.com/Charlieppy2/butterfly-bird-identifier.git

# 進入項目目錄
cd butterfly-bird-identifier

# 在 VS Code 中打開項目
code .
```

**Mac (Terminal):**
```bash
# 導航到您想要保存項目的目錄（例如 Documents）
cd ~/Documents

# 克隆項目
git clone https://github.com/Charlieppy2/butterfly-bird-identifier.git

# 進入項目目錄
cd butterfly-bird-identifier

# 在 VS Code 中打開項目
code .
```

### 步驟 3: 安裝 Git LFS 並下載大文件

在 VS Code 的終端中（`Ctrl+`` 或 `Cmd+`` 打開終端）：

**Windows:**
```powershell
# 安裝 Git LFS（如果還沒安裝）
git lfs install

# 下載大文件（模型文件）
git lfs pull
```

**Mac:**
```bash
# 安裝 Git LFS（如果還沒安裝）
git lfs install

# 下載大文件（模型文件）
git lfs pull
```

⚠️ **重要**：必須運行 `git lfs pull` 才能下載模型文件！

### 步驟 4: 安裝後端依賴

1. 在 VS Code 中打開終端（`Ctrl+`` 或 `Cmd+``）
2. 確保終端在項目根目錄

**Windows:**
```powershell
cd web_app\backend
pip install -r requirements.txt
```

**Mac:**
```bash
cd web_app/backend
pip install -r requirements.txt
```

⚠️ **注意**：首次安裝可能需要 2-5 分鐘，特別是 TensorFlow

**如果遇到權限問題：**
- Windows: 使用 `pip install --user -r requirements.txt`
- Mac: 使用 `pip3 install -r requirements.txt` 或 `python3 -m pip install -r requirements.txt`

### 步驟 5: 安裝前端依賴

1. 打開**新的終端**（點擊終端右上角的 `+` 按鈕）
2. 確保在項目根目錄

**Windows:**
```powershell
cd web_app\frontend
npm install
```

**Mac:**
```bash
cd web_app/frontend
npm install
```

⚠️ **注意**：首次安裝可能需要 2-5 分鐘，會安裝約 1344 個包

## 🎯 啟動應用

### 方法一：使用 VS Code 終端（推薦）

#### 啟動後端服務

1. 打開第一個終端（`Ctrl+`` 或 `Cmd+``）
2. 導航到後端目錄：

**Windows:**
```powershell
cd web_app\backend
python app.py
```

**Mac:**
```bash
cd web_app/backend
python app.py
```

3. 等待看到以下信息表示啟動成功：
```
Model loaded successfully from ...
Starting Flask server...
Running on http://0.0.0.0:5001
```

4. **保持此終端打開**

#### 啟動前端服務

1. 點擊終端右上角的 `+` 按鈕打開**新的終端**
2. 導航到前端目錄：

**Windows:**
```powershell
cd web_app\frontend
npm start
```

**Mac:**
```bash
cd web_app/frontend
npm start
```

3. 等待編譯完成（約 10-30 秒）
4. 瀏覽器會自動打開 http://localhost:3000
5. **保持此終端打開**

### 方法二：使用 VS Code 任務（Task）

VS Code 可以配置任務來同時啟動前端和後端。創建 `.vscode/tasks.json` 文件：

**Windows 配置：**
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Backend",
      "type": "shell",
      "command": "python",
      "args": ["app.py"],
      "options": {
        "cwd": "${workspaceFolder}/web_app/backend"
      },
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Start Frontend",
      "type": "shell",
      "command": "npm",
      "args": ["start"],
      "options": {
        "cwd": "${workspaceFolder}/web_app/frontend"
      },
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Start All",
      "dependsOn": ["Start Backend", "Start Frontend"],
      "problemMatcher": []
    }
  ]
}
```

**Mac/Linux 配置：**
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Backend",
      "type": "shell",
      "command": "python3",
      "args": ["app.py"],
      "options": {
        "cwd": "${workspaceFolder}/web_app/backend"
      },
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Start Frontend",
      "type": "shell",
      "command": "npm",
      "args": ["start"],
      "options": {
        "cwd": "${workspaceFolder}/web_app/frontend"
      },
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Start All",
      "dependsOn": ["Start Backend", "Start Frontend"],
      "problemMatcher": []
    }
  ]
}
```

**使用方法：**
1. 按 `Ctrl+Shift+P` (Windows) 或 `Cmd+Shift+P` (Mac) 打開命令面板
2. 輸入 `Tasks: Run Task`
3. 選擇 `Start All` 來同時啟動前端和後端

## 🌐 訪問應用

啟動成功後，您可以通過以下地址訪問：

- **前端界面**：http://localhost:3000
  - 這是主要的用戶界面
  - 用於上傳圖片和查看識別結果

- **後端 API**：http://localhost:5001
  - 這是 API 服務器
  - 可以查看 API 狀態信息
  - ⚠️ **注意**：後端使用端口 5001（不是 5000），以避免與 macOS AirPlay Receiver 衝突

## ✅ 驗證服務是否運行

### 檢查後端服務

在瀏覽器中訪問：http://localhost:5001

應該看到：
```json
{
  "status": "success",
  "message": "HK Urban Ecological Identification API is running",
  "model_loaded": true
}
```

### 檢查前端服務

在瀏覽器中訪問：http://localhost:3000

應該看到主應用界面，包含上傳區域和按鈕。

## 🛠️ VS Code 調試配置

### 配置 Python 調試（後端）

創建 `.vscode/launch.json` 文件：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/web_app/backend/app.py",
      "console": "integratedTerminal",
      "justMyCode": true,
      "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "development"
      }
    }
  ]
}
```

**使用方法：**
1. 在 `app.py` 中設置斷點
2. 按 `F5` 開始調試
3. 使用調試工具欄控制執行

### 配置 Node.js 調試（前端）

在 `launch.json` 中添加：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/web_app/backend/app.py",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Launch Chrome",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/web_app/frontend"
    }
  ]
}
```

## ⚠️ 常見問題

### Q1: VS Code 終端無法識別命令

**問題**：`python` 或 `npm` 命令未找到

**解決方法：**
1. 確保已安裝 Python 和 Node.js
2. 重啟 VS Code
3. 檢查系統 PATH 環境變量
4. 在 VS Code 設置中配置 Python 解釋器路徑：
   - 按 `Ctrl+,` (Windows) 或 `Cmd+,` (Mac) 打開設置
   - 搜索 "python path"
   - 設置正確的 Python 路徑

### Q2: 端口已被占用

**問題**：端口 5001 或 3000 已被使用

**解決方法：**
1. 在終端中查找占用端口的進程：
   - Windows: `netstat -ano | findstr :5001`
   - Mac: `lsof -i :5001`
2. 關閉占用端口的程序
3. 或修改 `app.py` 中的端口號（後端）

### Q3: Git LFS 文件未下載

**問題**：模型文件不存在

**解決方法：**
1. 確認已安裝 Git LFS
2. 運行 `git lfs install`
3. 運行 `git lfs pull`
4. 檢查 `models/trained/model.h5` 文件是否存在

### Q4: 依賴安裝失敗

**問題**：`pip install` 或 `npm install` 失敗

**解決方法：**
1. **Python 依賴**：
   - Windows: 使用 `python -m pip install -r requirements.txt`
   - Mac: 使用 `python3 -m pip install -r requirements.txt`
   - 或使用虛擬環境：`python -m venv venv` 然後激活

2. **Node.js 依賴**：
   - 刪除 `node_modules` 文件夾和 `package-lock.json`
   - 運行 `npm cache clean --force`
   - 重新運行 `npm install`

### Q5: VS Code 無法打開終端

**解決方法：**
1. 檢查終端設置：`Ctrl+,` → 搜索 "terminal"
2. 設置默認終端：
   - Windows: PowerShell 或 Command Prompt
   - Mac: Terminal 或 zsh

## 📝 推薦的 VS Code 設置

在項目根目錄創建 `.vscode/settings.json`：

```json
{
  "python.defaultInterpreterPath": "python3",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/node_modules": true
  },
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/.git/objects/**": true
  }
}
```

## 🎯 快速啟動檢查清單

- [ ] VS Code 已安裝
- [ ] Python 擴展已安裝
- [ ] 項目已從 GitHub 克隆
- [ ] Git LFS 已安裝並運行 `git lfs pull`
- [ ] 後端依賴已安裝（`pip install -r requirements.txt`）
- [ ] 前端依賴已安裝（`npm install`）
- [ ] 後端服務已啟動（端口 5001）
- [ ] 前端服務已啟動（端口 3000）
- [ ] 瀏覽器可以訪問 http://localhost:3000

## 📚 有用的 VS Code 快捷鍵

### Windows
- `Ctrl+Shift+P`: 命令面板
- `Ctrl+``: 打開/關閉終端
- `Ctrl+B`: 切換側邊欄
- `F5`: 開始調試
- `Ctrl+F5`: 運行而不調試

### Mac
- `Cmd+Shift+P`: 命令面板
- `Ctrl+``: 打開/關閉終端
- `Cmd+B`: 切換側邊欄
- `F5`: 開始調試
- `Ctrl+F5`: 運行而不調試

---

**祝您使用愉快！** 🦋🐦

如有問題，請查看 `README.md` 或 `如何啟動項目.md` 獲取更多幫助。

