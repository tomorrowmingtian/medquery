from openai import OpenAI
from app.core.config import settings
from app.db.session import get_conn

# 初始化大模型客户端
client = OpenAI(
    api_key=settings.DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def get_db_schema():
    """
    自动读取数据库表结构（高分点）

    返回：
        表结构字符串，用于拼接Prompt
    """
    conn = get_conn()
    schema = ""

    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            for table in tables:
                table_name = list(table.values())[0]

                cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                columns = cursor.fetchall()

                schema += f"\n表 {table_name}:\n"
                for col in columns:
                    schema += f"{col['Field']}({col['Type']})\n"

    finally:
        conn.close()

    return schema


def nlp_to_sql(text: str) -> str:
    """
    自然语言转SQL
    """

    # 动态获取数据库结构
    schema = get_db_schema()

    prompt = f"""
你是一个SQL生成助手。

数据库结构：
{schema}

要求：
1. 只能生成 SELECT 查询语句
2. 严禁生成 INSERT / UPDATE / DELETE / DROP
3. 不允许修改数据库
4. 只用于数据查询分析
5. 只返回SQL，不要解释

如果用户问题涉及修改数据，请返回：
SELECT '仅支持查询操作' as message;

用户问题：
{text}
"""

    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()