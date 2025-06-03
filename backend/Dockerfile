# 使用Python 3.11精简版作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
# gcc: 用于编译某些Python包
# libpq-dev: PostgreSQL客户端开发库
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 首先复制依赖文件，利用Docker缓存机制
# 如果requirements.txt没有变化，将使用缓存的pip安装
COPY requirements.txt .

# 安装Python项目依赖
# --no-cache-dir: 不缓存pip包，减小镜像大小
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码到容器中
COPY . .

# 设置Python模块搜索路径
# 确保可以正确导入app包
ENV PYTHONPATH=/app

# 暴露8000端口
# 这是FastAPI应用的默认端口
EXPOSE 8000

# 启动FastAPI应用
# --host 0.0.0.0: 允许外部访问
# --port 8000: 指定端口
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 