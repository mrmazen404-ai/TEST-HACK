"""
إعداد نظام التسجيل (Logging)
"""
import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """الحصول على مسجل (Logger) مع التنسيق المناسب."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # تعيين المستوى الافتراضي
        logger.setLevel(level or logging.INFO)

    return logger