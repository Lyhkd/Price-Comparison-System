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

# 使用 Nginx 作为最终的运行环境
FROM nginx:latest

# 复制构建的前端项目到 Nginx 的默认静态文件目录
COPY --from=build /app/dist /usr/share/nginx/html

# 复制 Nginx 配置文件
COPY default.conf /etc/nginx/conf.d/default.conf

# 暴露服务端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]