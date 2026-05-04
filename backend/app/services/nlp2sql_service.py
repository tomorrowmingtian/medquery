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
你是一个医疗数据库 SQL 生成助手。根据用户的自然语言问题，生成对应的 SQL 查询语句。

## 数据库结构
{schema}

## 规则
1. 只生成 SELECT 语句，严禁 INSERT / UPDATE / DELETE / DROP / TRUNCATE 等任何修改操作。
2. 只返回纯 SQL，不要加解释、注释或 markdown 标记。
3. 若问题无法用现有表结构回答，返回：SELECT '无法回答该问题，请检查表结构' AS message;
4. 若涉及修改或删除数据，返回：SELECT '仅支持查询操作' AS message;

## 注意事项
- 用户输入为中文，需要将中文条件映射到对应英文字段（如"糖尿病"可能对应 disease_name 或 diagnosis 等字段）。
- 合理使用聚合函数（COUNT / SUM / AVG）、分组（GROUP BY）、排序（ORDER BY）和分页（LIMIT）。
- 涉及年龄、日期范围等条件时注意字段类型，确保 SQL 语法正确。
- 字段别名建议使用中文（AS 'xxx'），便于前端展示。

用户问题：{text}
"""

    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
