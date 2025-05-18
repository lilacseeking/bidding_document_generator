FROM python:3.10-slim

WORKDIR /app

# 使用国内源可选，加速依赖安装（如在国内且有需要可解开下面一行）
# RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list

# 系统依赖（如需编译C扩展，含常见最小依赖）
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

# 设定 Python 模块搜索路径，支持 from src.xxx import xxx
ENV PYTHONPATH=/app

# 如需代理可加环境变量
# ENV http_proxy=http://host.docker.internal:7890
# ENV https_proxy=http://host.docker.internal:7890

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]