# 🚀 Koyeb 新帳號部署指南

## 📋 前置準備

1. **新郵箱地址**（用於註冊新 Koyeb 帳號）
2. **GitHub 帳號**（已連接你的專案）
3. **專案已推送到 GitHub**

---

## 🎯 步驟 1：註冊新 Koyeb 帳號

### 1.1 訪問 Koyeb

1. 打開瀏覽器，訪問 https://koyeb.com
2. 點擊右上角 **"Sign Up"** 或 **"Get Started"**

### 1.2 選擇註冊方式

**方法一：使用郵箱註冊**
1. 輸入新的郵箱地址（與舊帳號不同）
2. 設置密碼
3. 驗證郵箱

**方法二：使用 GitHub 註冊**
1. 點擊 **"Sign up with GitHub"**
2. 授權 Koyeb 訪問 GitHub
3. 完成註冊

### 1.3 完成註冊

- 確認郵箱驗證（如果使用郵箱註冊）
- 完成帳號設置

---

## 🔗 步驟 2：連接 GitHub 倉庫

### 2.1 在 Koyeb 中連接 GitHub

1. 登入新 Koyeb 帳號
2. 進入 Dashboard
3. 點擊 **"Create App"** 或 **"New Service"**
4. 選擇 **"GitHub"** 作為來源
5. 如果首次連接，會要求授權：
   - 點擊 **"Authorize Koyeb"**
   - 選擇要授權的倉庫（或授權所有倉庫）
   - 確認授權

### 2.2 選擇倉庫

1. 在倉庫列表中，找到 `butterfly-bird-identifier`
2. 選擇該倉庫

---

## ⚙️ 步驟 3：配置和部署應用

### 3.1 基本設置

在部署配置頁面：

**應用名稱：**
- `butterfly-bird-api`（或你喜歡的名稱）

**區域：**
- 選擇離你最近的區域（如 `Asia Pacific`）

**套餐：**
- 選擇 **"Starter"**（免費套餐，$0/月）

### 3.2 Docker 設置

**構建方式：**
- 選擇 **"Docker"**

**Dockerfile 路徑：**
- `web_app/backend/Dockerfile.koyeb`

**構建命令：**
- 留空（Koyeb 會自動使用 Dockerfile）

### 3.3 環境變數設置

在 **"Environment Variables"** 中添加：

| 變數名稱 | 值 | 說明 |
|---------|-----|------|
| `FLASK_ENV` | `production` | 生產環境模式 |
| `PORT` | `8080` | Koyeb 使用的端口（Dockerfile 中已設置） |

### 3.4 高級設置（可選）

**資源限制：**
- CPU: 0.25 vCPU（免費套餐）
- Memory: 512 MB（免費套餐）

**自動擴展：**
- 保持默認設置

### 3.5 部署

1. 檢查所有設置
2. 點擊 **"Deploy"** 或 **"Create App"**
3. 等待部署完成（5-10 分鐘）

---

## 🔍 步驟 4：檢查部署狀態

### 4.1 查看部署日誌

1. 在 Koyeb Dashboard 中，點擊你的應用
2. 查看 **"Logs"** 標籤
3. 確認：
   - ✅ Git LFS 文件已下載
   - ✅ 模型文件已載入
   - ✅ Flask 服務已啟動

### 4.2 測試 API

部署完成後，Koyeb 會提供一個 URL（例如：`https://xxx.koyeb.app`）

**測試根路徑：**
```
https://your-app.koyeb.app/
```

應該看到：
```json
{
  "status": "success",
  "message": "Butterfly and Bird Identification API is running",
  "model_loaded": true
}
```

**測試健康檢查：**
```
https://your-app.koyeb.app/api/health
```

---

## ⚠️ 步驟 5：保持應用活躍（重要！）

Koyeb 免費套餐在 7 天未活動後可能會暫停服務。為了避免這個問題：

### 方法一：定期登入（最簡單）

- **每天登入一次 Koyeb Dashboard**
- 查看應用狀態
- 這會保持帳號活躍

### 方法二：使用監控服務（推薦）

使用免費的 Uptime Robot 保持應用活躍：

#### 設置 Uptime Robot：

1. **註冊 Uptime Robot**
   - 訪問 https://uptimerobot.com
   - 使用郵箱註冊（免費）

2. **添加監控**
   - 點擊 **"Add New Monitor"**
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: `Butterfly Bird API`
   - **URL**: 你的 Koyeb 應用 URL
   - **Monitoring Interval**: 每 5 分鐘（免費套餐）

3. **保存設置**
   - 點擊 **"Create Monitor"**
   - Uptime Robot 會每 5 分鐘訪問你的應用
   - 這會保持應用活躍，避免暫停

### 方法三：設置自動訪問腳本（進階）

如果你有服務器，可以設置 cron job 定期訪問：

```bash
# 每小時訪問一次
0 * * * * curl https://your-app.koyeb.app/ > /dev/null 2>&1
```

---

## 📊 部署檢查清單

- [ ] 新 Koyeb 帳號已註冊
- [ ] GitHub 倉庫已連接
- [ ] Dockerfile 路徑正確：`web_app/backend/Dockerfile.koyeb`
- [ ] 環境變數已設置
- [ ] 部署成功完成
- [ ] API 測試通過
- [ ] 模型文件已載入
- [ ] 已設置監控服務（Uptime Robot）

---

## 🔧 常見問題

### Q1: 部署失敗，提示 "Git LFS pull failed"

**解決方案：**
1. 確保 GitHub 倉庫中模型文件已通過 Git LFS 上傳
2. 檢查 `.gitattributes` 文件是否正確配置
3. 在 Dockerfile 中確認 Git LFS 已安裝

### Q2: 模型文件未載入

**解決方案：**
1. 檢查構建日誌，確認 `git lfs pull` 成功執行
2. 檢查模型文件路徑是否正確
3. 查看應用日誌確認模型載入狀態

### Q3: 應用啟動後立即停止

**解決方案：**
1. 檢查 Dockerfile 中的 CMD 命令
2. 確認端口設置為 8080
3. 查看日誌找出錯誤原因

### Q4: 7 天後服務被暫停

**解決方案：**
1. 設置 Uptime Robot 監控（推薦）
2. 或每天登入 Koyeb Dashboard
3. 或升級到付費套餐

---

## 💡 最佳實踐

### 1. 監控設置

**強烈建議設置 Uptime Robot：**
- 免費且可靠
- 自動保持應用活躍
- 可以監控應用狀態

### 2. 定期檢查

- 每 2-3 天檢查一次應用狀態
- 查看日誌確認沒有錯誤
- 測試 API 功能

### 3. 備份方案

考慮同時部署到 Railway 作為備選：
- 如果 Koyeb 出現問題，可以快速切換
- Railway 無休眠機制，更穩定

---

## 🎉 完成！

部署完成後，你的應用就可以使用了！

**應用 URL 範例：**
```
https://butterfly-bird-api.koyeb.app
```

**記住：**
- ✅ 設置 Uptime Robot 保持活躍
- ✅ 定期檢查應用狀態
- ✅ 在 11/12 交作業前測試所有功能

---

## 📞 需要幫助？

如果遇到問題：
1. 查看 Koyeb Dashboard 的日誌
2. 檢查 GitHub 倉庫配置
3. 參考 Koyeb 官方文檔：https://www.koyeb.com/docs

祝部署順利！🚀

