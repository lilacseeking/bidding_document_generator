# 招标文件生成系统前端

## 项目介绍
本项目是招标文件生成系统的前端部分，基于Vue 3 + Vite + Element Plus开发。

## 技术栈
- Vue 3
- Vite
- Element Plus
- Pinia
- Vue Router
- Axios

## 开发环境要求
- Node.js >= 16.0.0
- npm >= 7.0.0

## 项目设置
1. 安装依赖
```bash
npm install
```

2. 启动开发服务器
```bash
npm run dev
```

3. 构建生产版本
```bash
npm run build
```

4. 预览生产构建
```bash
npm run preview
```

## 项目结构
```
frontend/
├── src/                # 源代码
│   ├── api/           # API请求
│   ├── assets/        # 静态资源
│   ├── components/    # 公共组件
│   ├── layouts/       # 布局组件
│   ├── router/        # 路由配置
│   ├── stores/        # 状态管理
│   ├── views/         # 页面组件
│   ├── App.vue        # 根组件
│   └── main.js        # 入口文件
├── public/            # 公共资源
├── index.html         # HTML模板
├── vite.config.js     # Vite配置
└── package.json       # 项目配置
```

## 开发规范
1. 组件命名采用PascalCase
2. 文件名采用kebab-case
3. 使用Composition API和`<script setup>`
4. 使用TypeScript进行类型检查
5. 遵循ESLint规则

## 部署说明
1. 构建项目
```bash
npm run build
```

2. 将dist目录下的文件部署到Web服务器

## 环境变量
- `VITE_API_URL`: API服务器地址

## 贡献指南
1. Fork本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证
MIT 