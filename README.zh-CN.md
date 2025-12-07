# HK Urban Ecological Identification System

香港城市生态识别系统 - 一个基于深度学习的蝴蝶与鸟类识别Web应用

## 项目简介

这是一个使用深度学习技术开发的Web应用系统，用于识别香港城市中的蝴蝶与鸟类。系统采用迁移学习技术，基于MobileNetV2构建分类模型，能够识别300+种物种（200种鸟类 + 100+种蝴蝶/蛾类），并提供友好的Web界面供用户上传图片进行识别。

## ✨ 主要功能

### 🔍 核心识别功能
- **图片上传识别**: 支持拖拽上传或选择文件（PNG, JPG, JPEG, GIF, WEBP）
- **批量识别**: 一次上传多张图片进行批量识别
- **智能识别**: 基于深度学习的图像分类，提供Top-3预测结果和置信度
- **低置信度警告**: 自动检测并警告上传的图片不是蝴蝶或鸟类，或图片质量不足

### 📊 图片质量分析
- **多维度分析**: 亮度、对比度、清晰度、饱和度、分辨率
- **质量评分**: 总体质量分数（0-100）
- **智能建议**: 根据图片质量问题提供改进建议

### 💬 AI聊天助手
- **智能问答**: 回答关于物种识别、观察技巧等问题
- **知识库**: 包含栖息地、观察时间、拍照技巧等信息
- **可训练**: 支持扩展和训练AI助手的知识库

### 📈 统计分析
- **识别历史统计**: 总识别次数、独特物种数、平均置信度
- **类别分布**: 鸟类、蝴蝶/蛾类的分布统计
- **置信度分布**: 高/中/低置信度的分布图表
- **Top物种**: 最常识别的物种排行榜
- **时间分布**: 识别活动的时间趋势

### ❤️ 收藏功能
- **收藏物种**: 一键收藏感兴趣的识别结果
- **收藏管理**: 查看、管理所有收藏的物种
- **数据持久化**: 使用localStorage保存收藏数据

### 📜 历史记录
- **识别历史**: 自动保存最近的识别记录
- **快速查看**: 快速浏览历史识别结果
- **标签切换**: 在历史记录和收藏之间轻松切换

## 技术栈

### 模型训练
- **TensorFlow/Keras**: 深度学习框架
- **MobileNetV2**: 预训练模型（迁移学习）
- **Python 3.8+**: 编程语言
- **OpenCV**: 图像处理和质量分析

### Web应用
- **前端**: React 18.2.0
  - Axios: HTTP客户端
  - 响应式设计，支持移动端
- **后端**: Flask 3.0.0
  - Flask-CORS: 跨域支持
  - TensorFlow: 模型推理
  - PIL/OpenCV: 图像处理

## 项目结构

```
butterfly-bird-identifier/
├── data/
│   ├── raw/              # 原始数据集
│   ├── processed/        # 处理后的数据（train/val/test）
│   └── dataset_info.txt  # 数据集信息
├── models/
│   ├── training/         # 训练脚本
│   │   ├── train_model.py      # 模型训练
│   │   ├── prepare_data.py     # 数据准备
│   │   ├── test_model.py       # 模型测试
│   │   └── check_training.py   # 训练进度检查
│   └── trained/          # 训练好的模型
│       ├── model.h5           # 训练好的模型（使用Git LFS）
│       └── class_names.json   # 类别名称列表
├── web_app/
│   ├── frontend/         # React前端应用
│   │   ├── src/
│   │   │   ├── App.js         # 主应用组件
│   │   │   ├── App.css        # 样式文件
│   │   │   └── index.js       # 入口文件
│   │   ├── public/
│   │   │   └── index.html     # HTML模板
│   │   └── package.json       # 前端依赖
│   ├── backend/          # Flask后端API
│   │   ├── app.py             # Flask应用主文件
│   │   ├── requirements.txt   # Python依赖
│   │   ├── knowledge_base.json # AI助手知识库
│   │   └── train_assistant.py  # AI助手训练脚本
│   └── preview.html      # 预览页面
├── notebooks/            # Jupyter notebooks（数据探索）
├── report/              # 项目报告
├── .gitattributes        # Git LFS配置
├── .gitignore           # Git忽略文件
└── README.md            # 本文件
```

## 🚀 快速开始

### 前置要求

1. **Python 3.8+**
   - 下载地址：https://www.python.org/downloads/
   - 安装时请勾选 "Add Python to PATH"

2. **Node.js 16+**
   - 下载地址：https://nodejs.org/
   - 建议安装 LTS 版本

3. **Git LFS** (用于下载大文件)
   ```bash
   git lfs install
   ```

### 安装步骤

#### 1. 克隆仓库

```bash
git clone https://github.com/Charlieppy2/butterfly-bird-identifier.git
cd butterfly-bird-identifier
```

#### 2. 安装后端依赖

**Windows (PowerShell):**
```powershell
cd web_app/backend
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
cd web_app/backend
pip install -r requirements.txt
```

**注意**：首次安装可能需要 2-5 分钟，特别是 TensorFlow 的安装。

#### 3. 安装前端依赖

**Windows (PowerShell):**
```powershell
cd web_app/frontend
npm install
```

**Linux/Mac:**
```bash
cd web_app/frontend
npm install
```

**注意**：首次安装可能需要 2-5 分钟，会安装约 1344 个包。

### 启动应用

#### 方法一：手动启动（推荐）

**启动后端服务：**

**Windows (PowerShell):**
```powershell
cd web_app/backend
python app.py
```

**Linux/Mac:**
```bash
cd web_app/backend
python app.py
```

后端服务将在 `http://localhost:5001` 启动

您应该看到：
```
Loading model...
Model loaded successfully from ...
Starting Flask server...
Running on http://0.0.0.0:5001
```

**注意**：后端默认使用端口 5001，以避免与 macOS AirPlay Receiver 在端口 5000 上的冲突。

**启动前端应用：**

打开**新的终端窗口**：

**Windows (PowerShell):**
```powershell
cd web_app/frontend
npm start
```

**Linux/Mac:**
```bash
cd web_app/frontend
npm start
```

前端应用将在 `http://localhost:3000` 启动，编译完成后（10-30秒）浏览器会自动打开。

#### 方法二：使用批处理文件（Windows）

**后端：**
双击 `web_app\backend\start_backend.bat` 或运行：
```powershell
cd web_app/backend
.\start_backend.bat
```

**前端：**
双击 `web_app\frontend\start_frontend.bat` 或运行：
```powershell
cd web_app/frontend
.\start_frontend.bat
```

### 验证服务

**检查后端：**
打开浏览器访问：`http://localhost:5001`

您应该看到：
```json
{
  "status": "success",
  "message": "HK Urban Ecological Identification API is running",
  "model_loaded": true
}
```

**检查前端：**
打开浏览器访问：`http://localhost:3000`

您应该看到主应用界面，包含上传区域和按钮。

## 📖 使用指南

### 识别物种

1. **上传图片**：
   - 点击 "Choose File" 按钮选择图片
   - 或直接拖拽图片到上传区域

2. **查看结果**：
   - 系统会显示识别结果和置信度
   - 显示Top-3预测结果
   - 自动进行图片质量分析
   - 如果图片不是蝴蝶或鸟类，或置信度较低，将显示警告信息和建议

### 使用AI助手

1. 点击右下角的聊天图标打开AI助手
2. 可以询问：
   - 识别技巧
   - 最佳观察时间
   - 拍照建议
   - 物种信息

### 查看统计

1. 在历史记录区域点击 "📊 View Statistics"
2. 查看：
   - 总识别次数
   - 类别分布（鸟类/蝴蝶）
   - 置信度分布
   - Top识别物种

### 收藏功能

1. **收藏物种**：
   - 识别完成后，点击结果标题旁的❤️按钮

2. **查看收藏**：
   - 点击 "❤️ Favorites" 标签
   - 查看所有收藏的物种

3. **移除收藏**：
   - 在收藏列表中点击 "❌ Remove" 按钮
   - 或再次点击❤️按钮取消收藏

## 🎓 模型训练

### 数据准备

将原始图片按类别组织到 `data/raw/` 目录下：

```
data/raw/
├── 001.Black_footed_Albatross/
│   ├── image1.jpg
│   └── ...
├── 002.Laysan_Albatross/
│   └── ...
└── ...
```

运行数据准备脚本：

```bash
cd models/training
python prepare_data.py
```

### 训练模型

```bash
cd models/training
python train_model.py
```

训练参数可在 `train_model.py` 中调整：
- `IMAGE_SIZE`: 图片尺寸 (224, 224)
- `BATCH_SIZE`: 批次大小 (32)
- `EPOCHS`: 训练轮数 (100)
- `LEARNING_RATE`: 学习率 (0.0001)

训练完成后，模型将保存在 `models/trained/model.h5`

### 检查训练进度

```bash
cd models/training
python check_training.py
```

### 测试模型

```bash
cd models/training
python test_model.py
```

## 🤖 训练AI助手

详细指南请参考：[如何訓練AI助手.md](如何訓練AI助手.md)

快速开始：

```bash
cd web_app/backend
python train_assistant.py
```

## 📊 数据集信息

- **总类别数**: 301种（200种鸟类 + 101种蝴蝶/蛾类）
- **数据增强**: 旋转、翻转、缩放、亮度调整
- **图片尺寸**: 224x224
- **训练/验证/测试**: 自动划分

## 🔧 API端点

### 后端API

- `GET /` - 健康检查
- `GET /api/health` - 模型状态
- `GET /api/classes` - 获取所有类别名称
- `POST /api/predict` - 图片识别
- `POST /api/analyze-quality` - 图片质量分析
- `POST /api/statistics` - 获取统计数据
- `POST /api/chat` - AI聊天助手

## 🛠️ 开发环境

- **Python**: 3.8+ (测试版本 3.13.9)
- **Node.js**: 16+ (测试版本 24.11.1)
- **TensorFlow**: 2.16.0+ (测试版本 2.20.0)
- **React**: 18.2.0
- **Flask**: 3.0.0
- **Flask-CORS**: 4.0.0
- **OpenCV**: 4.8.0+ (测试版本 4.12.0.88)
- **Pillow**: 10.1.0+
- **NumPy**: 1.24.3+

## ⚠️ 注意事项

1. **Git LFS**: 模型文件使用Git LFS存储，克隆后需要运行 `git lfs install`
2. **首次运行**: 首次运行需要加载模型，可能需要一些时间（10-30秒）
3. **GPU加速**: 训练模型建议使用GPU加速（Google Colab推荐）
4. **磁盘空间**: 确保有足够的磁盘空间存储数据集和模型（模型约19MB）
5. **浏览器兼容性**: 建议使用Chrome、Firefox或Edge最新版本
6. **端口冲突**: 如果端口 5001（后端）或 3000（前端）已被占用，请停止冲突的服务或修改配置中的端口
7. **Windows PowerShell**: 在 PowerShell 中使用 `;` 而不是 `&&` 来连接命令
8. **保持终端打开**: 后端和前端服务必须保持运行 - 请保持终端窗口打开

## ❓ 常见问题

### 后端无法启动

**问题**：提示 "Model not found" 或 "Model not loaded"

**解决方法**：
1. 确认模型文件存在：`models/trained/model.h5`
2. 确认类别文件存在：`models/trained/class_names.json`
3. 如果文件不存在，需要先训练模型（见模型训练部分）

### 前端无法连接到后端

**问题**：显示 "无法连上这个网站" 或 "Connection refused"

**解决方法**：
1. 确认后端服务正在运行（检查 http://localhost:5001）
2. 确保两个服务都在运行
3. 尝试清除浏览器缓存并刷新
4. 检查防火墙设置

### 前端编译错误

**问题**：运行 `npm start` 时出现错误

**解决方法**：
1. 删除 `node_modules` 文件夹
2. 删除 `package-lock.json` 文件
3. 重新运行 `npm install`
4. 再次运行 `npm start`

### 端口已被占用

**问题**：端口 5001（后端）或 3000（前端）已被使用

**解决方法**：
1. 关闭使用这些端口的其他程序
2. 或修改 `app.py` 中的端口号（后端）或设置 `PORT=3001` 环境变量（前端）
3. 注意：后端默认使用端口 5001，以避免与 macOS AirPlay Receiver 的冲突

### 安装时间过长

**解决方法**：
- 首次安装这是正常的
- 后端依赖（特别是 TensorFlow）可能需要 5-10 分钟
- 前端依赖可能需要 2-5 分钟
- 确保网络连接稳定

## 🌐 部署信息

### 生产环境 URL
- **前端**: https://butterfly-bird-id.vercel.app
- **后端 API**: https://butterfly-bird-id.koyeb.app

### 部署平台
- **前端**: 部署在 Vercel（从 GitHub 自动部署）
- **后端**: 部署在 Koyeb（使用 Dockerfile.koyeb）

### 环境变量
对于 Vercel 前端部署，设置：
- `REACT_APP_API_URL`: 您的后端 API URL（例如：`https://butterfly-bird-id.koyeb.app`）

对于 Koyeb 后端部署：
- `FLASK_ENV`: `production`
- `PORT`: `8080`（由 Koyeb 自动设置）

## 📝 更新日志

### v1.1.0 (最新)
- ✨ 新增低置信度警告系统，用于非目标图片
- ✨ 改进 UI，根据置信度条件性显示结果
- 🔧 将后端默认端口改为 5001，避免 macOS 冲突
- 🚀 部署到生产环境（Vercel + Koyeb）
- 🌐 更新生产部署的 API URL 配置
- 📝 更新文档，包含部署信息

### v1.0.0
- ✨ 新增收藏功能
- ✨ 新增图片质量分析
- ✨ 新增AI聊天助手
- ✨ 新增识别历史统计和分析
- ✨ 新增批量识别模式
- 🐛 修复分类分布问题（蝴蝶正确分类）
- 📦 使用Git LFS管理大文件
- 📝 更新安装和设置文档

## 📚 参考资料

- [TensorFlow官方文档](https://www.tensorflow.org/)
- [Keras迁移学习指南](https://keras.io/guides/transfer_learning/)
- [React官方文档](https://react.dev/)
- [Flask官方文档](https://flask.palletsprojects.com/)
- [Git LFS文档](https://git-lfs.github.com/)

## 📄 授权

本项目仅用于学术和教育目的。

## 👥 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

如有问题或建议，请通过GitHub Issues联系。

---

**注意**: 请确保在提交前完成所有必要的配置和测试。

## 📄 其他语言版本

- [English Version](README.md)
- [繁體中文版 (Traditional Chinese)](README.zh-TW.md)

