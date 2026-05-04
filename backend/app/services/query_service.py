from app.services.nlp2sql_service import nlp_to_sql
from app.db.mysql import execute_sql
from app.utils.sql_utils import check_sql_safe
from app.core.logger import get_logger

logger = get_logger(__name__)


def handle_query(text: str):
    """
    查询主流程（带完整日志）
    """

    logger.info(f"用户输入: {text}")

    # 生成SQL
    sql = nlp_to_sql(text)
    logger.info(f"生成SQL: {sql}")

    # SQL安全校验
    if not check_sql_safe(sql):
        logger.warning(f"危险SQL被拦截: {sql}")

        # 👇 自动替换为安全查询
        safe_sql = "SELECT '仅支持查询操作' AS message"

        return {
            "success": False,
            "sql": safe_sql,  # 不返回原危险SQL！
            "data": [{"message": "仅支持SELECT查询"}]
        }

    try:
        result = execute_sql(sql)
        logger.info(f"SQL执行成功，返回{len(result)}条数据")

        return {
            "success": True,
            "sql": sql,
            "data": result
        }

    except Exception as e:
        logger.error(f"SQL执行失败: {e} | SQL: {sql}")

        return {
            "success": False,
            "sql": sql,
            "error": str(e)
        }