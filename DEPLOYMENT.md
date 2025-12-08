# 網站部署指南 / Website Deployment Guide

## 📋 目錄 / Table of Contents
- [部署選項 / Deployment Options](#部署選項)
- [方法一：Vercel + Railway（推薦）](#方法一vercel--railway推薦)
- [方法二：Netlify + Render](#方法二netlify--render)
- [方法三：全站部署到 Render](#方法三全站部署到-render)
- [本地構建測試](#本地構建測試)

---

## 部署選項 / Deployment Options

這個項目包含兩個部分：
- **前端 (Frontend)**: React 應用
- **後端 (Backend)**: Flask API 服務器

### 免費部署平台推薦：

| 平台 | 前端 | 後端 | 費用 |
|------|------|------|------|
| Vercel | ✅ | ❌ | 免費 |
| Netlify | ✅ | ❌ | 免費 |
| Railway | ❌ | ✅ | 免費（有限額） |
| Render | ✅ | ✅ | 免費（有限額） |

---

## 方法一：Vercel + Railway（推薦）

### 步驟 1：部署前端到 Vercel

1. **構建前端**
   ```bash
   cd web_app/frontend
   npm install
   npm run build
   ```

2. **創建 Vercel 帳號**
   - 訪問 https://vercel.com
   - 使用 GitHub 帳號登錄

3. **部署到 Vercel**
   - 點擊 "New Project"
   - 選擇你的 GitHub 倉庫
   - 設置：
     - **Framework Preset**: Create React App
     - **Root Directory**: `web_app/frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `build`
   - 添加環境變量：
     ```
     REACT_APP_API_URL=https://your-railway-app.railway.app
     ```
   - 點擊 "Deploy"

### 步驟 2：部署後端到 Railway

1. **創建 Railway 帳號**
   - 訪問 https://railway.app
   - 使用 GitHub 帳號登錄

2. **部署到 Railway**
   - 點擊 "New Project" → "Deploy from GitHub repo"
   - 選擇你的倉庫
   - 設置：
     - **Root Directory**: `web_app/backend`
     - **Start Command**: `python app.py`
   - 添加環境變量（如果需要）：
     ```
     FLASK_ENV=production
     PORT=5000
     ```
   - Railway 會自動檢測 Python 並安裝依賴

3. **獲取後端 URL**
   - 部署完成後，Railway 會提供一個 URL（例如：`https://your-app.railway.app`）
   - 將此 URL 更新到 Vercel 的環境變量中

---

## 方法二：Netlify + Render

### 步驟 1：部署前端到 Netlify

1. **構建前端**
   ```bash
   cd web_app/frontend
   npm install
   npm run build
   ```

2. **創建 Netlify 帳號**
   - 訪問 https://netlify.com
   - 使用 GitHub 帳號登錄

3. **部署到 Netlify**
   - 點擊 "Add new site" → "Import an existing project"
   - 選擇你的 GitHub 倉庫
   - 設置：
     - **Base directory**: `web_app/frontend`
     - **Build command**: `npm run build`
     - **Publish directory**: `web_app/frontend/build`
   - 添加環境變量：
     ```
     REACT_APP_API_URL=https://your-render-app.onrender.com
     ```
   - 點擊 "Deploy site"

### 步驟 2：部署後端到 Render

1. **創建 Render 帳號**
   - 訪問 https://render.com
   - 使用 GitHub 帳號登錄

2. **部署到 Render**
   - 點擊 "New" → "Web Service"
   - 選擇你的 GitHub 倉庫
   - 設置：
     - **Name**: `hk-butterfly-bird-api`
     - **Root Directory**: `web_app/backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python app.py`
   - 添加環境變量：
     ```
     FLASK_ENV=production
     PORT=5000
     ```
   - 點擊 "Create Web Service"

3. **更新前端環境變量**
   - 獲取 Render 提供的 URL
   - 在 Netlify 中更新 `REACT_APP_API_URL`

---

## 方法三：全站部署到 Render

### 步驟 1：修改後端以服務前端靜態文件

需要修改 `app.py` 來同時服務前端和後端：

```python
# 在 app.py 末尾添加
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# 設置靜態文件夾
app.static_folder = '../frontend/build'
```

### 步驟 2：構建前端

```bash
cd web_app/frontend
npm install
npm run build
```

### 步驟 3：部署到 Render

1. **創建 Render 帳號**
   - 訪問 https://render.com

2. **部署到 Render**
   - 點擊 "New" → "Web Service"
   - 選擇你的 GitHub 倉庫
   - 設置：
     - **Root Directory**: `web_app/backend`
     - **Environment**: `Python 3`
     - **Build Command**: 
       ```bash
       cd ../frontend && npm install && npm run build && cd ../backend && pip install -r requirements.txt
       ```
     - **Start Command**: `python app.py`
   - 添加環境變量：
     ```
     FLASK_ENV=production
     PORT=5000
     REACT_APP_API_URL=https://your-app.onrender.com
     ```

---

## 本地構建測試

在部署前，建議先在本地測試構建：

### 1. 構建前端

```bash
cd web_app/frontend
npm install
npm run build
```

構建完成後，會在 `web_app/frontend/build` 目錄生成靜態文件。

### 2. 測試生產環境

#### 選項 A：使用 serve 測試前端

```bash
npm install -g serve
cd web_app/frontend/build
serve -s . -l 3000
```

#### 選項 B：使用後端服務前端

修改 `app.py` 添加靜態文件服務（見方法三），然後：

```bash
cd web_app/backend
python app.py
```

訪問 http://localhost:5000

---

## 重要配置檢查

### 1. 檢查 CORS 設置

確保 `app.py` 中的 CORS 設置允許你的前端域名：

```python
from flask_cors import CORS

# 允許所有來源（生產環境建議限制特定域名）
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### 2. 檢查環境變量

前端需要設置正確的 API URL：

```javascript
// web_app/frontend/src/App.js
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

### 3. 檢查文件上傳限制

確保後端配置了適當的文件大小限制：

```python
# app.py
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
```

---

## 常見問題

### Q: 部署後前端無法連接到後端
**A**: 檢查：
1. 環境變量 `REACT_APP_API_URL` 是否正確設置
2. CORS 設置是否允許前端域名
3. 後端 URL 是否可訪問

### Q: 圖片上傳失敗
**A**: 檢查：
1. 文件大小是否超過限制
2. 後端是否有寫入權限（Render/Railway 可能需要配置持久化存儲）

### Q: 模型文件太大無法上傳
**A**: 
- 使用 Git LFS 管理大文件
- 或將模型文件上傳到雲存儲（如 AWS S3），然後在部署時下載

---

## 下一步

部署完成後：
1. ✅ 測試所有功能
2. ✅ 設置自定義域名（可選）
3. ✅ 配置 HTTPS（平台通常自動提供）
4. ✅ 設置監控和日誌

---

## 需要幫助？

如果遇到問題，請檢查：
- 平台部署日誌
- 瀏覽器控制台錯誤
- 後端服務器日誌

祝部署順利！🎉

