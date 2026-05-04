from fastapi import APIRouter
from app.api.v1.endpoints import query,schema

# 创建总路由
api_router = APIRouter()

# 注册子模块
api_router.include_router(query.router, prefix="/query", tags=["自然语言查询"])
api_router.include_router(schema.router, prefix="/schema", tags=["表结构"])