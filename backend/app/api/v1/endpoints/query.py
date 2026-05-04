from fastapi import APIRouter
from app.schemas.query import QueryRequest
from app.services.query_service import handle_query

router = APIRouter()


@router.post("/")
def query_api(req: QueryRequest):
    """
    自然语言查询接口

    流程：
    1. 接收前端输入
    2. 调用业务逻辑层
    3. 返回查询结果
    """
    return handle_query(req.text)