import logging
import os
from logging.handlers import TimedRotatingFileHandler

# 日志目录
LOG_DIR = "logs"

# 如果日志目录不存在则创建
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def get_logger(name: str) -> logging.Logger:
    """
    获取日志对象（支持多模块调用）

    参数：
        name -> 日志名称（一般传 __name__）

    返回：
        logger对象
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 防止重复添加handler（重要！）
    if logger.handlers:
        return logger

    # ================= 控制台输出 =================
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # ================= 文件输出（按天切割） =================
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, "app.log"),
        when="midnight",       # 每天切割
        interval=1,
        backupCount=7,         # 保留7天
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)

    # ================= 日志格式 =================
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 添加handler
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger