from pydantic import BaseModel


class QueryRequest(BaseModel):
    """
    请求参数结构
    """
    text: str


class QueryResponse(BaseModel):
    """
    返回结构（可选）
    """
    success: bool
    sql: str
    data: list | None = None
    error: str | None = None