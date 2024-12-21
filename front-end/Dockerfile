# 使用 Node.js 20.x 镜像作为构建阶段
FROM node:20 AS build

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制所有项目文件
COPY . .

# 构建前端项目
RUN npm run build

# 暴露服务端口
EXPOSE 5173

# 启动 Nginx
CMD ["npm", "run", "start"]
