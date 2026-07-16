"""
إعدادات التطبيق المركزية
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Settings:
    """إعدادات التطبيق الثابتة."""

    BOT_TOKEN: str
    OWNER_CHAT_ID: str
    DEVICES_FILE: str = "devices.json"
    LOG_LEVEL: str = "INFO"
    REQUEST_TIMEOUT: int = 30
    POLLING_INTERVAL: float = 1.0
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 1
    CONVERSATION_TIMEOUT: int = 60  # ثواني

    @classmethod
    def from_env(cls) -> "Settings":
        """تحميل الإعدادات من متغيرات البيئة."""
        token = os.getenv("BOT_TOKEN")
        owner_id = os.getenv("OWNER_CHAT_ID")

        if not token or not owner_id:
            raise ValueError("BOT_TOKEN و OWNER_CHAT_ID مطلوبان")

        return cls(
            BOT_TOKEN=token,
            OWNER_CHAT_ID=owner_id,
            LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
            DEVICES_FILE=os.getenv("DEVICES_FILE", "devices.json"),
        )


settings = Settings(
    BOT_TOKEN="8777992302:AAEKiIcVIhWIc16xUYqiNY4HdA6Hds0Yqhw",
    OWNER_CHAT_ID="6929860618",
)