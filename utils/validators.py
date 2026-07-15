"""
وظائف التحقق من صحة المدخلات
"""
import re
from typing import Optional, Tuple


class Validators:
    """مدقق الصحة."""

    @staticmethod
    def validate_seconds(text: str) -> Optional[int]:
        """التحقق من عدد الثواني (1-60)."""
        try:
            seconds = int(text)
            if 1 <= seconds <= 60:
                return seconds
        except ValueError:
            pass
        return None

    @staticmethod
    def validate_path(text: str) -> bool:
        """التحقق من صحة المسار."""
        if not text.startswith('/'):
            return False
        # منع الأحرف الخطيرة
        if '..' in text or ';' in text or '|' in text:
            return False
        return True

    @staticmethod
    def validate_sms_input(text: str) -> Tuple[Optional[str], Optional[str]]:
        """التحقق من مدخلات الرسالة النصية."""
        parts = text.split(",", 1)
        if len(parts) != 2:
            return None, None

        phone = parts[0].strip()
        message = parts[1].strip()

        # التحقق من رقم الهاتف (بسيط)
        if not re.match(r'^[0-9]{7,15}$', phone.replace('+', '')):
            return None, None

        if not message:
            return None, None

        return phone, message