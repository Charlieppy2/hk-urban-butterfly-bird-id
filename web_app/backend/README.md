# AI Assistant 完整文件集合

## 📁 文件说明（共26个文件，6.5MB）

### 核心代码
- `enhanced_ai_assistant.py` - AI助手核心功能
- `app_chat_endpoint.py` - Flask API端点（从app.py提取的chat相关代码）

### 训练脚本
- `train_assistant.py` - AI助手知识库训练脚本
- `train_intent_classifier.py` - 意图分类模型训练脚本
- `train_interpretation_model.py` - 解讀生成模型训练脚本
- `train_model.py` - 解讀生成模型训练脚本（英文版）
- `train_description_model.py` - 描述识别模型训练脚本
- `colab_train.py` - Colab训练脚本（完整版）
- `colab_train_updated.py` - Colab训练脚本（更新版）

### 推理模块
- `generate_interpretation.py` - 解讀生成推理模块
- `generate_interpretation_en.py` - 解讀生成推理模块（英文版）
- `model_setup.py` - 模型设置和加载
- `semantic_matcher.py` - 语义匹配模块（描述识别功能）

### 配置文件
- `resource_library.json` - 资源推荐库（摄影网站等）
- `quiz_library.py` - 挑战游戏题库
- `knowledge_base.json` - 知识库
- `species_name_mapping.json` - 物种名称映射（中英文）
- `descriptions.json` - 物种描述数据（729KB）
- `species_index.json` - 物种索引（132KB）
- `species_embeddings.npz` - 物种嵌入向量（5.2MB）

### 模型文件
- `intent_classifier_model.pkl` - 意图分类模型
- `intent_vectorizer.pkl` - 文本向量化器

### 训练数据
- `training_data_interpretation.csv` - 解讀生成训练数据（中文）
- `training_data_interpretation_en.csv` - 解讀生成训练数据（英文）

### 依赖
- `requirements.txt` - Python依赖包

## 🚀 使用方法

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行AI Assistant
```python
from enhanced_ai_assistant import get_enhanced_assistant

assistant = get_enhanced_assistant()
response = assistant.generate_response("摄影网站", {}, "user1")
print(response)
```

### 训练模型
```bash
python train_intent_classifier.py
```

## 📝 功能特性

- ✅ 资源推荐（摄影网站、观察平台等）
- ✅ 挑战游戏
- ✅ 行为解读
- ✅ 意图分类
- ✅ 中英文双语支持
- ✅ 上下文记忆
- ✅ 个性化推荐

