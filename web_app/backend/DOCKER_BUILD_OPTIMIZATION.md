# Docker 构建优化说明

## 问题
Docker 构建时执行 `git lfs pull` 会下载 1.5GB 的图片文件，导致构建超时。

## 解决方案

### 方案 1：增加构建超时时间（推荐用于部署平台）

如果你使用的是 Koyeb、Render 或其他部署平台，可以在平台设置中增加构建超时时间：

- **Koyeb**: 在项目设置中增加构建超时（默认可能是 10-15 分钟）
- **Render**: 在服务设置中增加构建超时
- **其他平台**: 查看平台文档了解如何增加超时时间

**建议超时时间**: 至少 15-20 分钟（因为需要下载 1.5GB 文件）

### 方案 2：分离模型和图片文件

**选项 A：只下载模型文件（当前实现）**

Dockerfile 已经优化为：
- 使用 `timeout` 命令限制 Git LFS pull 的时间（10 分钟）
- 如果超时，检查模型文件是否已下载
- 图片文件在运行时按需加载

**选项 B：使用外部存储（CDN/对象存储）**

1. 将图片文件上传到：
   - AWS S3
   - Google Cloud Storage
   - Azure Blob Storage
   - 或其他对象存储服务

2. 修改后端代码，从外部存储加载图片

3. 在 Dockerfile 中排除 `data/raw` 目录

### 方案 3：多阶段构建

创建两个 Dockerfile：
1. `Dockerfile.model` - 只下载模型文件
2. `Dockerfile.full` - 下载所有文件（用于完整部署）

### 方案 4：使用 .dockerignore 排除图片

创建 `.dockerignore` 文件：
```
data/raw/**
!data/raw/.gitkeep
```

然后在运行时从外部存储加载图片。

## 当前 Dockerfile 优化

当前 Dockerfile 已经包含以下优化：

1. **超时机制**: 使用 `timeout 600` (10分钟) 限制 Git LFS pull 时间
2. **容错处理**: 如果超时，检查模型文件是否已下载
3. **按需加载**: 图片文件在运行时按需加载

## 部署建议

### 对于 Koyeb/Render 等平台：

1. **增加构建超时**:
   - 在平台设置中找到 "Build Timeout" 或类似选项
   - 设置为至少 20 分钟

2. **或者使用环境变量**:
   ```bash
   BUILD_TIMEOUT=1200  # 20 分钟
   ```

3. **监控构建日志**:
   - 查看 Git LFS pull 的进度
   - 如果经常超时，考虑使用方案 2（外部存储）

### 对于本地构建：

```bash
# 构建时设置超时（如果平台支持）
docker build --build-arg BUILD_TIMEOUT=1200 -t your-image .

# 或者直接构建（使用 Dockerfile 中的默认超时）
docker build -t your-image .
```

## 验证构建

构建完成后，检查：

1. **模型文件大小**:
   ```bash
   docker run your-image ls -lh models/trained/model.h5
   ```
   应该显示文件大小 > 1MB

2. **图片目录**:
   ```bash
   docker run your-image ls -la data/raw/ | head -20
   ```
   图片文件可能不存在（如果构建超时），这是正常的

## 运行时加载图片

如果图片文件在构建时没有下载，可以在容器启动时下载：

1. 创建启动脚本 `start.sh`:
   ```bash
   #!/bin/bash
   # 如果图片文件不存在，尝试下载
   if [ ! -f "data/raw/.gitkeep" ]; then
       echo "Downloading image files..."
       git lfs pull --include="data/raw/**" || echo "Failed to download images"
   fi
   # 启动应用
   python app.py
   ```

2. 修改 Dockerfile CMD:
   ```dockerfile
   CMD ["/app/start.sh"]
   ```

## 故障排除

### 问题：构建仍然超时

**解决方案**:
1. 增加平台构建超时时间
2. 使用 `.dockerignore` 排除图片文件
3. 考虑使用外部存储

### 问题：模型文件是 LFS 指针

**原因**: Git LFS pull 没有完成

**解决方案**:
1. 检查网络连接
2. 增加构建超时时间
3. 手动验证 Git LFS 配置

### 问题：图片无法加载

**原因**: 图片文件在构建时没有下载

**解决方案**:
1. 使用运行时下载脚本
2. 或使用外部存储/CDN
3. 或确保构建完成（增加超时时间）

