# 使用官方 Python 3.11.6 镜像作为基础镜像
FROM python:3.11.6

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到工作目录中
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/  -r requirements.txt


# 在容器启动时执行的命令
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]