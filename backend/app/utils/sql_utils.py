import re

def check_sql_safe(sql: str) -> bool:
    """
    SQL安全校验（白名单模式）

    仅允许 SELECT 查询，拒绝所有修改操作。

    返回：
        True -> 安全
        False -> 不安全
    """
    stripped = sql.strip()

    if not re.match(r'^SELECT\b', stripped, re.IGNORECASE):
        return False

    dangerous = [
        r'\bINTO\s+(OUT|DUMP)FILE\b',
        r'\bINTO\s+@\w+\b',
    ]
    for pattern in dangerous:
        if re.search(pattern, stripped, re.IGNORECASE):
            return False

    return True
