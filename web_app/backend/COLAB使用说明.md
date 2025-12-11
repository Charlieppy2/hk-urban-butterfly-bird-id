# 📘 Colab 训练指南 - 超简单版

## 🎯 只需要1个文件！

### 文件: `colab_train.py` 
**完整训练脚本（复制整个文件到Colab）**

**新功能**：如果CSV文件不存在，脚本会自动创建测试数据！

---

## 🚀 在Colab中的操作步骤

### 方式1: 使用真实数据（推荐）
1. 上传 `training_data_interpretation_en.csv` 到Colab
2. 复制 `colab_train.py` 全部内容到Colab
3. 运行

### 方式2: 快速测试（无需上传）
1. 直接复制 `colab_train.py` 全部内容到Colab
2. 运行（脚本会自动创建测试数据）

就这么简单！脚本会自动：
- ✅ 检查CSV文件，不存在则创建测试数据
- ✅ 安装所有依赖
- ✅ 加载模型
- ✅ 开始训练（快速测试模式：3 epochs）
- ✅ 保存模型

### 修改训练模式

在脚本底部找到 `QUICK_TEST = True`，可以切换：
- `QUICK_TEST = True`: 快速测试（3 epochs, max_length=128）
- `QUICK_TEST = False`: 完整训练（10 epochs, max_length=256）

---

## 📁 文件位置

训练完成后，模型保存在：
```
interpretation_model/
├── config.json
├── model.safetensors
├── tokenizer files...
└── training_history.json
```

---

## ⚙️ 修改训练参数（可选）

如果想修改训练参数，在 `colab_train.py` 最底部找到：

```python
train_model(
    csv_path='training_data_interpretation_en.csv',
    output_dir='interpretation_model',
    num_epochs=10,        # 修改这里：训练轮数
    batch_size=4,          # 修改这里：批次大小
    learning_rate=5e-5,   # 修改这里：学习率
    max_length=256,        # 修改这里：最大长度
    warmup_steps=50        # 修改这里：预热步数
)
```

---

## 📥 下载训练好的模型

训练完成后，下载模型：

```python
# 在Colab中运行
from google.colab import files
import shutil

# 压缩模型文件夹
shutil.make_archive('interpretation_model', 'zip', 'interpretation_model')

# 下载
files.download('interpretation_model.zip')
```

---

## ✅ 总结

**只需要做2件事：**
1. 上传 `training_data_interpretation_en.csv`
2. 复制粘贴 `colab_train.py` 并运行

**就这么简单！** 🎉

