# 如何訓練 AI 助手

## 訓練方法

### 方法 1: 互動式訓練（推薦）

1. 進入後端目錄：
```bash
cd web_app/backend
```

2. 運行訓練腳本：
```bash
python train_assistant.py
```

3. 使用命令：
   - `add` - 添加新的問答對
   - `stats` - 查看知識庫統計
   - `template` - 創建訓練模板文件
   - `load <文件名>` - 從文件加載訓練數據
   - `quit` - 退出訓練模式

### 方法 2: 從文件訓練

1. 創建訓練模板：
```bash
python train_assistant.py template
```

2. 編輯 `training_template.json`，添加你的問答對：
```json
[
  {
    "category": "identification_tips",
    "question": "如何識別蝴蝶？",
    "answer": "To identify butterflies, look at wing patterns, colors, body shape, and habitat."
  },
  {
    "category": "observation_time",
    "question": "什麼時候最適合觀察鳥類？",
    "answer": "Early morning (6-9 AM) is usually the best time to observe birds."
  }
]
```

3. 訓練助手：
```bash
python train_assistant.py train training_template.json
```

## 類別說明

可用的類別包括：

- `greetings` - 問候語
- `identification_tips` - 識別技巧
- `observation_time` - 觀察時間
- `photo_tips` - 拍照技巧
- `species_info` - 物種信息
- `confidence` - 置信度相關
- `habitat` - 棲息地
- `system_info` - 系統信息
- `help` - 幫助信息
- `default` - 默認回答

## 重要提示

1. **問題可以是中文或英文**：訓練腳本會自動提取關鍵詞
2. **回答必須是英文**：AI 助手始終用英文回答
3. **支持中文關鍵詞**：可以在 patterns 中添加中文關鍵詞
4. **自動保存**：訓練後會自動保存到 `knowledge_base.json`

## 示例

### 添加問答對

```
Enter command: add
Category: identification_tips
Question: 如何區分蝴蝶和蛾？
Answer: Butterflies and moths can be distinguished by:
• Butterflies have clubbed antennae, moths have feathery or straight antennae
• Butterflies are active during the day, moths are mostly nocturnal
• Butterflies rest with wings closed, moths rest with wings open
✓ Training example added!
```

### 查看統計

```
Enter command: stats
==================================================
AI Assistant Knowledge Base Statistics
==================================================

IDENTIFICATION_TIPS:
  Patterns: 15
  Responses: 3

OBSERVATION_TIME:
  Patterns: 12
  Responses: 2

...
```

## 訓練後部署

訓練完成後，需要：

1. 提交更改到 Git：
```bash
git add web_app/backend/knowledge_base.json
git commit -m "Update AI assistant knowledge base"
git push origin main
```

2. 後端會自動重新加載知識庫（無需重啟）

## 注意事項

- 回答必須是英文
- 問題可以是中文或英文
- 關鍵詞會自動提取
- 重複的問答對不會重複添加
- 建議定期查看統計信息，確保知識庫質量

