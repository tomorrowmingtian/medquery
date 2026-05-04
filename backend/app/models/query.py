from pydantic import BaseModel


class QueryModel(BaseModel):
    """
    数据模型（内部使用）
    """
    text: str