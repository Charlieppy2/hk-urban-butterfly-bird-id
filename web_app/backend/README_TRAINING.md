# 🚀 模型训练指南

## 📋 文件说明

### 训练相关文件
- `train_model.py` - 主训练脚本（使用英文GPT-2）
- `training_data_interpretation_en.csv` - 英文训练数据（45条）
- `generate_interpretation_en.py` - 推理模块
- `species_name_mapping.json` - 中文到英文物种名称映射

### 集成文件
- `enhanced_ai_assistant.py` - 已集成模型生成功能

## 🎯 训练步骤

### 1. 安装依赖
```bash
cd web_app/backend
source venv/bin/activate
pip install torch transformers pandas numpy tqdm nltk
```

### 2. 准备数据
数据文件已准备好：`training_data_interpretation_en.csv`

数据格式：
- `species_en`: 英文物种名称
- `category`: 类别（fun_fact, behavior, habitat）
- `interpretation_text`: 英文解读文本

### 3. 开始训练
```bash
python train_model.py
```

训练参数（可在脚本中修改）：
- Epochs: 10
- Batch size: 4
- Learning rate: 5e-5
- Max length: 256

### 4. 检查训练结果
训练完成后，模型会保存到：`models/interpretation_model/`

查看训练历史：
```bash
cat models/interpretation_model/training_history.json | python3 -m json.tool
```

### 5. 测试生成
```bash
python generate_interpretation_en.py
```

## 🔧 输入格式

训练时使用的输入格式：
```
Species: {species_en}, Category: {category}, Interpretation: {interpretation_text}
```

生成时使用的输入格式：
```
Species: {species_en}, Category: {category}, Interpretation:
```

## 📊 模型特点

1. **纯英文输入输出**：避免中英文混合导致的模型混淆
2. **结构化输入**：使用"Species: ... Category: ..."格式，帮助模型理解结构
3. **物种名称映射**：支持中文物种名称自动转换为英文

## 🎨 使用示例

### 在代码中使用
```python
from generate_interpretation_en import InterpretationGenerator

generator = InterpretationGenerator('models/interpretation_model')
result = generator.generate("Taiwan Blue Magpie", "fun_fact")
# 或者使用中文名称（会自动转换）
result = generator.generate("臺灣藍鵲", "fun_fact")
```

### 在AI助手中
模型已自动集成到 `enhanced_ai_assistant.py`，当用户询问物种信息时会自动触发。

## ⚙️ 自定义训练

### 修改训练参数
编辑 `train_model.py` 中的 `train_model()` 函数调用：

```python
train_model(
    csv_path='training_data_interpretation_en.csv',
    output_dir='models/interpretation_model',
    num_epochs=10,      # 修改训练轮数
    batch_size=4,       # 修改批次大小
    learning_rate=5e-5, # 修改学习率
    max_length=256,     # 修改最大长度
    warmup_steps=50     # 修改预热步数
)
```

### 添加更多训练数据
编辑 `training_data_interpretation_en.csv`，添加更多数据：
- 保持格式一致
- 使用英文物种名称
- 使用英文解读文本

## 📈 训练指标

训练过程中会显示：
- **Training loss**: 训练损失（越低越好）
- **Validation loss**: 验证损失（越低越好）
- **Perplexity**: 困惑度（越低越好）
- **BLEU score**: BLEU分数（越高越好，每2个epoch计算一次）

最佳模型会根据验证损失自动保存。

## ⚠️ 注意事项

1. **数据量**：当前只有45条数据，建议增加到200-500条以获得更好效果
2. **训练时间**：根据硬件配置，10个epoch可能需要30-60分钟
3. **GPU支持**：如果有GPU会自动使用，否则使用CPU（较慢）
4. **模型大小**：训练好的模型约475MB

## ✅ 完成检查

训练完成后检查：
1. ✅ 模型文件存在：`models/interpretation_model/model.safetensors`
2. ✅ 训练历史存在：`models/interpretation_model/training_history.json`
3. ✅ 测试生成成功：运行 `python generate_interpretation_en.py`

现在可以开始训练了！🎉

