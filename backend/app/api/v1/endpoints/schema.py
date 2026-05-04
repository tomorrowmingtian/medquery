from fastapi import APIRouter
from app.db.session import get_conn

router = APIRouter()


@router.get("/")
def get_schema():
    """
    获取数据库表结构信息
    """
    conn = get_conn()
    result = {}

    try:
        with conn.cursor() as cursor:
            # 获取所有表
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            for t in tables:
                table_name = list(t.values())[0]

                cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                columns = cursor.fetchall()

                result[table_name] = columns

        return {"success": True, "data": result}

    finally:
        conn.close()