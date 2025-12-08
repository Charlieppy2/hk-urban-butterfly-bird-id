FROM python:3.10-slim

WORKDIR /app

# 安裝系統依賴（包括 gnupg 用於 Git LFS 安裝）
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgl1 \
    libglib2.0-0 \
    git \
    curl \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Git LFS（用於下載模型文件）
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
    apt-get update && \
    apt-get install -y git-lfs && \
    git lfs install

# 複製 requirements.txt（從 web_app/backend）
COPY web_app/backend/requirements.txt /app/requirements.txt

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製整個項目（從項目根目錄，包括 .git 目錄用於 Git LFS）
COPY . /app/

# 下載 Git LFS 文件（優先下載模型文件，圖片文件可選）
# 使用超時機制避免構建超時
RUN cd /app && \
    if [ -d .git ]; then \
        echo "Found .git directory, pulling LFS files..."; \
        echo "Note: This may take several minutes for large files..."; \
        # 嘗試下載 LFS 文件（如果平台有超時限制，會自動處理） \
        # 注意：某些平台可能需要在設置中增加構建超時時間 \
        git lfs pull || \
        (echo "Git LFS pull timed out or failed. Checking if model file exists..."; \
         if [ -f models/trained/model.h5 ]; then \
             file_size=$(stat -c%s models/trained/model.h5 2>/dev/null || stat -f%z models/trained/model.h5 2>/dev/null || echo "0"); \
             if [ "$file_size" -gt 1000000 ]; then \
                 echo "Model file exists and is valid, continuing..."; \
             else \
                 echo "WARNING: Model file exists but may be a pointer. Build may fail at validation step."; \
             fi; \
         else \
             echo "WARNING: Model file not found after LFS pull timeout."; \
         fi); \
    else \
        echo "WARNING: No .git directory found!"; \
    fi && \
    # 驗證模型文件大小（應該 > 1MB，不是 LFS 指針）
    if [ -f models/trained/model.h5 ]; then \
        file_size=$(stat -c%s models/trained/model.h5 2>/dev/null || stat -f%z models/trained/model.h5 2>/dev/null || echo "0"); \
        echo "Model file size: $file_size bytes"; \
        if [ "$file_size" -lt 1000000 ]; then \
            echo "ERROR: Model file is too small ($file_size bytes), likely a LFS pointer!"; \
            echo "This usually means Git LFS pull did not complete. Try increasing build timeout."; \
            exit 1; \
        else \
            echo "Model file size OK: $file_size bytes"; \
        fi; \
    else \
        echo "ERROR: Model file not found!"; \
        exit 1; \
    fi && \
    # 創建 data/raw 目錄結構（圖片文件將在運行時按需加載） \
    mkdir -p data/raw && \
    echo "Note: Image files may not be fully downloaded. They will be loaded on-demand at runtime."

# 切換到後端目錄
WORKDIR /app/web_app/backend

# 設置環境變量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8080

# 暴露端口
EXPOSE 8080

# 啟動應用
CMD ["python", "app.py"]

