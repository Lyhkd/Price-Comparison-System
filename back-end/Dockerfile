# 使用 Python 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 设置 Flask 的环境变量
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# 暴露 Flask 端口
EXPOSE 5000

# 运行 Flask
CMD ["flask", "run"]
