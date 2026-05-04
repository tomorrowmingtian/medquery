# 医疗 NLP2SQL 查询系统

基于大语言模型的自然语言转 SQL 查询系统，用户输入中文问题即可自动生成 SQL 并查询数据库，无需手写 SQL。

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python 3.13 + FastAPI + PyMySQL |
| 前端 | Vue 3 + Vite + Element Plus |
| 大模型 | 阿里通义千问 Qwen-Plus（DashScope API） |

## 项目结构

```
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI 入口，CORS 中间件
│   │   ├── core/
│   │   │   ├── config.py            # 全局配置（数据库、API Key）
│   │   │   └── logger.py            # 日志系统（按天切割，保留7天）
│   │   ├── db/
│   │   │   ├── session.py           # 数据库连接
│   │   │   └── mysql.py             # SQL 执行封装
│   │   ├── api/v1/
│   │   │   ├── api.py               # 路由汇总
│   │   │   └── endpoints/
│   │   │       ├── query.py         # POST /api/v1/query/  自然语言查询
│   │   │       └── schema.py        # GET  /api/v1/schema/  获取表结构
│   │   ├── services/
│   │   │   ├── nlp2sql_service.py   # NLP→SQL：动态读取DB结构 + 拼接Prompt + 调用大模型
│   │   │   └── query_service.py     # 查询主流程编排
│   │   ├── schemas/query.py         # Pydantic 请求/响应模型
│   │   └── utils/sql_utils.py       # SQL 安全校验（白名单模式）
│   ├── logs/                        # 日志文件
│   └── requirement.txt              # Python 依赖
│
└── frontend/
    ├── src/
    │   ├── App.vue                  # 根组件
    │   ├── main.js                  # 入口文件
    │   ├── views/QueryView.vue      # 查询主界面
    │   ├── components/SchemaView.vue # 数据库结构浏览器
    │   ├── api/request.js           # Axios 封装
    │   └── utils/history.js         # 查询历史（localStorage，最多20条）
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## 快速开始

### 1. 环境要求

- Python >= 3.10
- Node.js >= 18
- MySQL 数据库

### 2. 后端配置

修改 `backend/app/core/config.py` 中的数据库连接信息和 API Key：

```python
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "medical_db"

DASHSCOPE_API_KEY = "your_dashscope_api_key"
```

### 3. 安装后端依赖

```bash
cd backend
pip install -r requirement.txt
```

### 4. 启动后端

```bash
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

后端启动后访问 http://127.0.0.1:8000/docs 查看接口文档。

### 5. 安装前端依赖

```bash
cd frontend
npm install
```

### 6. 启动前端

```bash
cd frontend
npm run dev
```

默认访问 http://localhost:5173。

## 功能说明

| 功能 | 说明 |
|---|---|
| 自然语言查询 | 输入中文问题，自动生成 SQL 并执行查询 |
| SQL 展示 | 展示生成的 SQL 语句，便于核对 |
| 结果表格 | 查询结果以表格形式呈现 |
| 数据库结构浏览 | 查看所有表及字段信息 |
| 查询历史 | 自动保存最近 20 条查询记录，支持回填 |
| SQL 安全校验 | 白名单模式，仅允许 SELECT 查询 |
| 动态 Schema | 每次查询自动读取数据库结构，无需手动维护表信息 |

## API 接口

### 自然语言查询

```
POST /api/v1/query/

请求体:
{
  "text": "查询糖尿病患者数量"
}

响应:
{
  "success": true,
  "sql": "SELECT COUNT(*) FROM patients WHERE ...",
  "data": [...]
}
```

### 获取表结构

```
GET /api/v1/schema/

响应:
{
  "success": true,
  "data": {
    "patients": [
      {"Field": "id", "Type": "int", "Null": "NO", "Key": "PRI"},
      ...
    ]
  }
}
```
