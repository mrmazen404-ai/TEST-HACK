"""
طبقة الأمان والصلاحيات
"""
from typing import Optional
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class AuthService:
    """خدمة المصادقة والصلاحيات."""

    def __init__(self):
        self.owner_chat_id = settings.OWNER_CHAT_ID

    def is_owner(self, chat_id: int) -> bool:
        """التحقق من أن المستخدم هو التاجر."""
        return str(chat_id) == str(self.owner_chat_id)

    def is_authorized(self, chat_id: int) -> bool:
        """التحقق من صلاحية المستخدم."""
        return self.is_owner(chat_id)

    def get_owner_id(self) -> str:
        """الحصول على معرف التاجر."""
        return self.owner_chat_id


# مثيل واحد للخدمة (Singleton)
auth_service = AuthService()