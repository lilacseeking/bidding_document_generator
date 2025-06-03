# 构建阶段：使用Node.js环境构建前端应用
FROM node:18-alpine as builder

# 设置工作目录
WORKDIR /app

# 首先复制package.json文件，利用Docker缓存机制
# 如果package.json没有变化，将使用缓存的node_modules
COPY package*.json ./

# 安装项目依赖
RUN npm install

# 复制所有源代码
COPY . .

# 构建生产环境的应用
RUN npm run build

# 生产阶段：使用Nginx提供静态文件服务
FROM nginx:alpine

# 从构建阶段复制构建好的文件到Nginx服务目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制Nginx配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露80端口
EXPOSE 80

# 启动Nginx服务
# -g 'daemon off;' 参数使Nginx在前台运行，便于容器管理
CMD ["nginx", "-g", "daemon off;"] 