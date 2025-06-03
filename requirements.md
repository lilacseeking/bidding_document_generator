# 招标文件生成系统需求文档

## 1. 系统概述

本系统是一个基于Python和Neo4j的智能招标文件生成系统，旨在通过人工智能和知识图谱技术，实现招标文件、标书、专家评标报告、答疑函件、中标通知书等文档的自动化生成。系统采用Docker容器化部署，提供直观的响应式用户界面。

## 2. 功能需求

### 2.1 知识图谱构建

#### 2.1.1 知识来源
- 历史招标文件
- 行业标准规范
- 法律法规文件
- 专家评估报告

#### 2.1.2 实体类型
- 项目（Project）
- 投标方（Bidder）
- 评标专家（Expert）
- 资质要求（Qualification）
- 技术规范（Specification）

#### 2.1.3 关系类型
- 项目-投标方（BELONGS_TO）
- 项目-专家（EVALUATED_BY）
- 项目-资质（REQUIRES）
- 项目-规范（FOLLOWS）

### 2.2 文档生成

#### 2.2.1 文档格式
- Word（.docx）作为主要格式
- PDF作为导出格式
- HTML作为预览格式

#### 2.2.2 模板结构
- JSON格式定义模板
- 支持变量替换
- 支持条件判断
- 支持循环结构

#### 2.2.3 业务规则
- 文档版本控制
- 文档审核流程
- 文档签名机制
- 文档水印功能

### 2.3 用户权限管理

#### 2.3.1 角色体系
- 超级管理员：系统管理
- 管理员：用户管理、模板管理
- 文档管理员：文档管理
- 普通用户：文档操作
- 审核员：文档审核

#### 2.3.2 权限控制
- 基于RBAC模型
- 支持角色继承
- 支持临时授权
- 支持权限组

## 3. 技术需求

### 3.1 开发环境
- Python 3.8+
- Neo4j 5.18.0
- PostgreSQL 15.0
- Docker Desktop

### 3.2 技术栈
- 后端：FastAPI
- 前端：Vue.js 3.0 + Element Plus
- 数据库：Neo4j + PostgreSQL
- 文档处理：python-docx, PyPDF2
- AI框架：LangChain, Transformers

### 3.3 部署要求
- 使用Docker Desktop进行本地部署
- 支持单机部署
- 使用docker-compose管理容器

## 4. 用户界面要求

### 4.1 设计原则
- 响应式设计，适配不同设备
- 直观的界面布局
- 清晰的操作流程
- 友好的用户提示

### 4.2 主要界面
- 登录界面
- 首页仪表盘
- 文档管理界面
- 用户管理界面
- 系统设置界面

### 4.3 交互要求
- 支持拖拽操作
- 支持快捷键
- 支持批量操作
- 支持实时预览

## 5. 数据存储

### 5.1 数据库设计
- Neo4j：存储知识图谱数据
- PostgreSQL：存储业务数据
- 文件系统：存储文档文件

### 5.2 数据模型
- 用户模型
- 文档模型
- 模板模型
- 知识图谱模型

## 6. 开发规范

### 6.1 代码规范
- 遵循PEP 8规范
- 使用类型注解
- 编写单元测试
- 添加注释文档

### 6.2 版本控制
- 使用Git进行版本控制
- 遵循Git Flow工作流
- 编写清晰的提交信息
- 进行代码审查

## 7. 项目计划

### 7.1 开发阶段
1. 环境搭建（1周）
2. 基础功能开发（2周）
3. 知识图谱开发（2周）
4. 文档生成开发（2周）
5. 用户界面开发（2周）
6. 测试与优化（1周）

### 7.2 里程碑
- 环境搭建完成
- 基础功能可用
- 知识图谱可用
- 文档生成可用
- 系统整体可用

## 8. 实现细节

### 8.1 知识图谱构建实现
#### 8.1.1 待确认问题
- 是否需要提供知识图谱的可视化界面？
- 知识图谱的更新是手动触发还是自动更新？
- 是否需要提供知识图谱的查询接口？
- 是否需要支持知识图谱的导入导出功能？

#### 8.1.2 推荐实现方案
- 提供基于D3.js的知识图谱可视化界面
- 支持手动触发更新，同时提供定时自动更新选项
- 提供RESTful API接口进行知识图谱查询
- 支持JSON格式的知识图谱导入导出

### 8.2 文档生成实现
#### 8.2.1 待确认问题
- 文档模板是否需要提供可视化编辑器？
- 文档生成时是否需要支持多人协作？
- 文档审核流程是否需要支持多级审核？
- 文档版本控制是否需要支持分支管理？

#### 8.2.2 推荐实现方案
- 提供基于TinyMCE的模板可视化编辑器
- 支持基于WebSocket的实时协作编辑
- 支持最多三级审核流程
- 支持基于Git的文档版本控制

### 8.3 用户权限管理实现
#### 8.3.1 待确认问题
- 是否需要提供权限管理的可视化界面？
- 临时授权的有效期如何设置？
- 权限组是否需要支持多级嵌套？
- 是否需要支持权限的批量操作？

#### 8.3.2 推荐实现方案
- 提供基于Element Plus的权限管理界面
- 临时授权默认有效期为24小时，可配置
- 支持最多三级权限组嵌套
- 支持基于Excel的权限批量导入导出

### 8.4 数据存储实现
#### 8.4.1 待确认问题
- 文件存储是否需要支持分片上传？
- 是否需要支持文件预览的缓存？
- 是否需要支持文件的历史版本存储？
- 是否需要支持文件的批量导入导出？

#### 8.4.2 推荐实现方案
- 支持基于WebSocket的分片上传
- 使用Redis缓存文件预览
- 使用Git LFS存储文件历史版本
- 支持ZIP格式的批量导入导出

### 8.5 用户界面实现
#### 8.5.1 待确认问题
- 是否需要支持主题切换？
- 是否需要支持多语言？
- 是否需要支持自定义布局？
- 是否需要支持快捷键的自定义配置？

#### 8.5.2 推荐实现方案
- 支持明暗两种主题切换
- 支持中英文双语切换
- 支持基于Grid的布局自定义
- 支持基于JSON的快捷键配置

### 8.6 开发规范实现
#### 8.6.1 待确认问题
- 是否需要配置自动化测试环境？
- 是否需要配置代码质量检查工具？
- 是否需要配置自动化部署流程？
- 是否需要配置文档自动生成工具？

#### 8.6.2 推荐实现方案
- 使用pytest进行自动化测试
- 使用pylint进行代码质量检查
- 使用GitHub Actions进行自动化部署
- 使用Sphinx生成API文档

### 8.7 项目计划实现
#### 8.7.1 待确认问题
- 是否需要设置具体的开发里程碑？
- 是否需要设置具体的测试计划？
- 是否需要设置具体的发布计划？
- 是否需要设置具体的培训计划？

#### 8.7.2 推荐实现方案
- 设置每周开发里程碑
- 设置单元测试和集成测试计划
- 设置每月发布计划
- 设置新功能培训计划

### 8.8 其他实现
#### 8.8.1 待确认问题
- 是否需要提供系统使用文档？
- 是否需要提供开发文档？
- 是否需要提供API文档？
- 是否需要提供部署文档？

#### 8.8.2 推荐实现方案
- 使用Markdown编写系统使用文档
- 使用Sphinx生成开发文档
- 使用Swagger生成API文档
- 使用Markdown编写部署文档

## 9. 实现细节确认

### 9.1 数据模型设计确认

#### 9.1.1 用户模型
##### 待确认问题
- 用户模型需要包含哪些基本字段？
- 用户模型需要包含哪些扩展字段？
- 用户模型需要包含哪些审计字段？
- 用户模型需要包含哪些状态字段？

##### 推荐实现方案
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    full_name VARCHAR(100),
    department VARCHAR(100),
    position VARCHAR(100),
    avatar_url VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_by INTEGER REFERENCES users(id)
);
```

#### 9.1.2 角色模型
##### 待确认问题
- 角色模型需要包含哪些基本字段？
- 角色模型需要包含哪些扩展字段？
- 角色模型需要包含哪些审计字段？
- 角色模型需要包含哪些状态字段？

##### 推荐实现方案
```sql
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    is_system BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_by INTEGER REFERENCES users(id)
);
```

#### 9.1.3 权限模型
##### 待确认问题
- 权限模型需要包含哪些基本字段？
- 权限模型需要包含哪些扩展字段？
- 权限模型需要包含哪些审计字段？
- 权限模型需要包含哪些状态字段？

##### 推荐实现方案
```sql
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    type VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_by INTEGER REFERENCES users(id)
);
```

#### 9.1.4 文档模型
##### 待确认问题
- 文档模型需要包含哪些基本字段？
- 文档模型需要包含哪些扩展字段？
- 文档模型需要包含哪些审计字段？
- 文档模型需要包含哪些状态字段？

##### 推荐实现方案
```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    content TEXT,
    file_path VARCHAR(255),
    file_size INTEGER,
    file_type VARCHAR(50),
    version VARCHAR(20),
    status VARCHAR(20),
    is_template BOOLEAN DEFAULT false,
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_by INTEGER REFERENCES users(id)
);
```

#### 9.1.5 知识图谱模型
##### 待确认问题
- 知识图谱模型需要包含哪些实体类型？
- 知识图谱模型需要包含哪些关系类型？
- 知识图谱模型需要包含哪些属性？
- 知识图谱模型需要包含哪些索引？

##### 推荐实现方案
```cypher
// 实体类型定义
CREATE (n:Project {
    id: String,
    name: String,
    type: String,
    description: String,
    created_at: DateTime,
    updated_at: DateTime
})

CREATE (n:Bidder {
    id: String,
    name: String,
    type: String,
    qualification: String,
    created_at: DateTime,
    updated_at: DateTime
})

// 关系类型定义
CREATE (p:Project)-[r:BELONGS_TO]->(b:Bidder)
CREATE (p:Project)-[r:REQUIRES]->(q:Qualification)
CREATE (p:Project)-[r:EVALUATED_BY]->(e:Expert)

// 索引定义
CREATE INDEX ON :Project(id)
CREATE INDEX ON :Bidder(id)
CREATE INDEX ON :Qualification(id)
CREATE INDEX ON :Expert(id)
```

### 9.2 API接口设计确认

#### 9.2.1 用户管理接口
##### 待确认问题
- 用户管理接口需要包含哪些基本接口？
- 用户管理接口需要包含哪些扩展接口？
- 用户管理接口需要包含哪些安全措施？
- 用户管理接口需要包含哪些错误处理？

##### 推荐实现方案
```python
# 用户管理接口
@router.post("/users", response_model=UserCreate)
async def create_user(user: UserCreate):
    """创建用户"""
    pass

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """获取用户信息"""
    pass

@router.put("/users/{user_id}", response_model=UserUpdate)
async def update_user(user_id: int, user: UserUpdate):
    """更新用户信息"""
    pass

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """删除用户"""
    pass

@router.post("/users/login")
async def login(user: UserLogin):
    """用户登录"""
    pass

@router.post("/users/logout")
async def logout():
    """用户登出"""
    pass
```

#### 9.2.2 文档管理接口
##### 待确认问题
- 文档管理接口需要包含哪些基本接口？
- 文档管理接口需要包含哪些扩展接口？
- 文档管理接口需要包含哪些安全措施？
- 文档管理接口需要包含哪些错误处理？

##### 推荐实现方案
```python
# 文档管理接口
@router.post("/documents", response_model=DocumentCreate)
async def create_document(document: DocumentCreate):
    """创建文档"""
    pass

@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int):
    """获取文档信息"""
    pass

@router.put("/documents/{document_id}", response_model=DocumentUpdate)
async def update_document(document_id: int, document: DocumentUpdate):
    """更新文档信息"""
    pass

@router.delete("/documents/{document_id}")
async def delete_document(document_id: int):
    """删除文档"""
    pass

@router.post("/documents/{document_id}/generate")
async def generate_document(document_id: int):
    """生成文档"""
    pass

@router.post("/documents/{document_id}/preview")
async def preview_document(document_id: int):
    """预览文档"""
    pass
```

#### 9.2.3 知识图谱接口
##### 待确认问题
- 知识图谱接口需要包含哪些基本接口？
- 知识图谱接口需要包含哪些扩展接口？
- 知识图谱接口需要包含哪些安全措施？
- 知识图谱接口需要包含哪些错误处理？

##### 推荐实现方案
```python
# 知识图谱接口
@router.post("/knowledge/entities", response_model=EntityCreate)
async def create_entity(entity: EntityCreate):
    """创建实体"""
    pass

@router.get("/knowledge/entities/{entity_id}", response_model=EntityResponse)
async def get_entity(entity_id: str):
    """获取实体信息"""
    pass

@router.post("/knowledge/relations", response_model=RelationCreate)
async def create_relation(relation: RelationCreate):
    """创建关系"""
    pass

@router.get("/knowledge/relations/{relation_id}", response_model=RelationResponse)
async def get_relation(relation_id: str):
    """获取关系信息"""
    pass

@router.post("/knowledge/query")
async def query_knowledge(query: KnowledgeQuery):
    """查询知识图谱"""
    pass
```

### 9.3 前端页面设计确认

#### 9.3.1 登录页面
##### 待确认问题
- 登录页面需要包含哪些基本组件？
- 登录页面需要包含哪些扩展组件？
- 登录页面需要包含哪些验证规则？
- 登录页面需要包含哪些错误处理？

##### 推荐实现方案
```vue
<template>
  <div class="login-container">
    <el-form :model="loginForm" :rules="loginRules" ref="loginForm">
      <el-form-item prop="username">
        <el-input v-model="loginForm.username" placeholder="用户名"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input v-model="loginForm.password" type="password" placeholder="密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleLogin">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          // 登录逻辑
        }
      })
    }
  }
}
</script>
```

#### 9.3.2 文档管理页面
##### 待确认问题
- 文档管理页面需要包含哪些基本组件？
- 文档管理页面需要包含哪些扩展组件？
- 文档管理页面需要包含哪些验证规则？
- 文档管理页面需要包含哪些错误处理？

##### 推荐实现方案
```vue
<template>
  <div class="document-container">
    <el-card>
      <div slot="header">
        <span>文档管理</span>
        <el-button type="primary" @click="handleCreate">新建文档</el-button>
      </div>
      <el-table :data="documentList">
        <el-table-column prop="title" label="标题"></el-table-column>
        <el-table-column prop="type" label="类型"></el-table-column>
        <el-table-column prop="status" label="状态"></el-table-column>
        <el-table-column prop="created_at" label="创建时间"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button @click="handleEdit(scope.row)">编辑</el-button>
            <el-button @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      documentList: []
    }
  },
  methods: {
    handleCreate() {
      // 创建文档逻辑
    },
    handleEdit(row) {
      // 编辑文档逻辑
    },
    handleDelete(row) {
      // 删除文档逻辑
    }
  }
}
</script>
```

### 9.4 开发环境配置确认

#### 9.4.1 后端环境配置
##### 待确认问题
- 后端环境需要配置哪些依赖？
- 后端环境需要配置哪些工具？
- 后端环境需要配置哪些参数？
- 后端环境需要配置哪些服务？

##### 推荐实现方案
```yaml
# requirements.txt
fastapi==0.68.0
uvicorn==0.15.0
pydantic==1.8.2
sqlalchemy==1.4.23
psycopg2-binary==2.9.1
neo4j==4.4.0
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.5
python-docx==0.8.11
PyPDF2==1.26.0
langchain==0.3.23
transformers==4.51.2
scikit-learn==1.6.1
```

#### 9.4.2 前端环境配置
##### 待确认问题
- 前端环境需要配置哪些依赖？
- 前端环境需要配置哪些工具？
- 前端环境需要配置哪些参数？
- 前端环境需要配置哪些服务？

##### 推荐实现方案
```json
{
  "dependencies": {
    "vue": "^3.3.0",
    "vue-router": "^4.2.0",
    "pinia": "^2.1.0",
    "element-plus": "^2.4.0",
    "axios": "^1.6.0",
    "lodash": "^4.17.21",
    "echarts": "^5.4.0",
    "tinymce": "^6.7.0",
    "pdfjs-dist": "^3.11.0"
  },
  "devDependencies": {
    "vite": "^4.5.0",
    "typescript": "^5.0.0",
    "sass": "^1.69.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0"
  }
}
```

### 9.5 部署环境配置确认

#### 9.5.1 Docker配置
##### 待确认问题
- Docker需要配置哪些容器？
- Docker需要配置哪些网络？
- Docker需要配置哪些卷？
- Docker需要配置哪些环境变量？

##### 推荐实现方案
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=password
    depends_on:
      - db
      - neo4j

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: postgres:15.0
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data

  neo4j:
    image: neo4j:5.18.0
    environment:
      - NEO4J_AUTH=neo4j/password
    volumes:
      - neo4j_data:/data

volumes:
  postgres_data:
  neo4j_data:
```

### 9.6 测试策略确认

#### 9.6.1 单元测试
##### 待确认问题
- 单元测试需要覆盖哪些模块？
- 单元测试需要覆盖哪些功能？
- 单元测试需要覆盖哪些场景？
- 单元测试需要覆盖哪些边界条件？

##### 推荐实现方案
```python
# test_user.py
def test_create_user():
    """测试创建用户"""
    pass

def test_get_user():
    """测试获取用户"""
    pass

def test_update_user():
    """测试更新用户"""
    pass

def test_delete_user():
    """测试删除用户"""
    pass

# test_document.py
def test_create_document():
    """测试创建文档"""
    pass

def test_get_document():
    """测试获取文档"""
    pass

def test_update_document():
    """测试更新文档"""
    pass

def test_delete_document():
    """测试删除文档"""
    pass
```

#### 9.6.2 集成测试
##### 待确认问题
- 集成测试需要覆盖哪些模块？
- 集成测试需要覆盖哪些功能？
- 集成测试需要覆盖哪些场景？
- 集成测试需要覆盖哪些边界条件？

##### 推荐实现方案
```python
# test_integration.py
def test_user_workflow():
    """测试用户工作流"""
    pass

def test_document_workflow():
    """测试文档工作流"""
    pass

def test_knowledge_workflow():
    """测试知识图谱工作流"""
    pass
```

### 9.7 错误处理确认

#### 9.7.1 错误码定义
##### 待确认问题
- 错误码需要包含哪些类型？
- 错误码需要包含哪些级别？
- 错误码需要包含哪些信息？
- 错误码需要包含哪些处理方式？

##### 推荐实现方案
```python
# error_codes.py
class ErrorCode:
    # 系统错误
    SYSTEM_ERROR = (1000, "系统错误")
    DATABASE_ERROR = (1001, "数据库错误")
    NETWORK_ERROR = (1002, "网络错误")
    
    # 用户错误
    USER_NOT_FOUND = (2000, "用户不存在")
    USER_ALREADY_EXISTS = (2001, "用户已存在")
    USER_PASSWORD_ERROR = (2002, "密码错误")
    
    # 文档错误
    DOCUMENT_NOT_FOUND = (3000, "文档不存在")
    DOCUMENT_ALREADY_EXISTS = (3001, "文档已存在")
    DOCUMENT_GENERATE_ERROR = (3002, "文档生成错误")
    
    # 知识图谱错误
    ENTITY_NOT_FOUND = (4000, "实体不存在")
    ENTITY_ALREADY_EXISTS = (4001, "实体已存在")
    RELATION_NOT_FOUND = (4002, "关系不存在")
```

#### 9.7.2 错误处理机制
##### 待确认问题
- 错误处理需要包含哪些类型？
- 错误处理需要包含哪些级别？
- 错误处理需要包含哪些信息？
- 错误处理需要包含哪些处理方式？

##### 推荐实现方案
```python
# error_handler.py
from fastapi import HTTPException
from .error_codes import ErrorCode

class ErrorHandler:
    @staticmethod
    def handle_error(error_code: ErrorCode, detail: str = None):
        """处理错误"""
        raise HTTPException(
            status_code=error_code[0] // 100,
            detail=detail or error_code[1]
        )

    @staticmethod
    def handle_system_error(error: Exception):
        """处理系统错误"""
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
```

### 9.8 安全机制确认

#### 9.8.1 用户认证
##### 待确认问题
- 用户认证需要包含哪些方式？
- 用户认证需要包含哪些信息？
- 用户认证需要包含哪些验证？
- 用户认证需要包含哪些处理？

##### 推荐实现方案
```python
# auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="无效的认证凭据"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user
```

#### 9.8.2 权限控制
##### 待确认问题
- 权限控制需要包含哪些方式？
- 权限控制需要包含哪些信息？
- 权限控制需要包含哪些验证？
- 权限控制需要包含哪些处理？

##### 推荐实现方案
```python
# permission.py
from fastapi import Depends, HTTPException
from .auth import get_current_user

def check_permission(required_permission: str):
    """检查权限"""
    async def permission_checker(user = Depends(get_current_user)):
        if not user.has_permission(required_permission):
            raise HTTPException(
                status_code=403,
                detail="没有权限执行此操作"
            )
        return user
    return permission_checker

def check_role(required_role: str):
    """检查角色"""
    async def role_checker(user = Depends(get_current_user)):
        if not user.has_role(required_role):
            raise HTTPException(
                status_code=403,
                detail="没有角色执行此操作"
            )
        return user
    return role_checker
``` 