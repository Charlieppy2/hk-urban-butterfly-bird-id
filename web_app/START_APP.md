# 啟動應用指南

## React前端應用

React應用正在啟動中，通常需要10-30秒來編譯。

### 訪問地址
- **前端應用**: http://localhost:3000
- 應用會自動在瀏覽器中打開

### 如果沒有自動打開
1. 打開瀏覽器
2. 訪問: http://localhost:3000

### 停止應用
在終端中按 `Ctrl+C`

## Flask後端應用

要使用完整的識別功能，還需要啟動後端服務器：

### 啟動步驟

1. **安裝Python依賴**（如果還沒安裝）:
   ```powershell
   cd web_app/backend
   pip install -r requirements.txt
   ```

2. **啟動後端服務器**:
   ```powershell
   python app.py
   ```

3. **後端API地址**: http://localhost:5000

### 注意事項

- 後端需要訓練好的模型文件才能工作
- 模型文件應該位於: `models/trained/model.h5`
- 如果還沒有訓練模型，後端會顯示錯誤，但前端仍可正常顯示界面

## 完整功能流程

1. ✅ React前端運行在 http://localhost:3000
2. ⏳ Flask後端運行在 http://localhost:5000（需要手動啟動）
3. ⏳ 模型文件位於 models/trained/model.h5（需要先訓練）

## 開發模式

- React應用支持熱重載（Hot Reload）
- 修改代碼後會自動刷新瀏覽器
- 查看終端輸出了解編譯狀態

