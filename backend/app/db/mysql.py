from app.db.session import get_conn


def execute_sql(sql: str):
    """
    执行SQL语句

    参数：
        sql -> SQL字符串

    返回：
        查询结果
    """
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        conn.commit()
        return result
    finally:
        conn.close()