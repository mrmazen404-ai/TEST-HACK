"""
نموذج بيانات الجهاز
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Device:
    """نموذج جهاز المراقبة."""

    device_id: str
    name: Optional[str] = None
    registered_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_active: bool = True
    info: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Device":
        """إنشاء جهاز من قاموس."""
        return cls(
            device_id=data.get("device_id", ""),
            name=data.get("name"),
            registered_at=data.get("registered_at", datetime.now().isoformat()),
            is_active=data.get("is_active", True),
            info=data.get("info", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        """تحويل الجهاز إلى قاموس للتخزين."""
        return {
            "device_id": self.device_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "is_active": self.is_active,
            "info": self.info,
        }

    def get_display_name(self) -> str:
        """الحصول على اسم الجهاز للعرض."""
        return self.name if self.name else self.device_id[:8]

    def get_info_text(self) -> str:
        """تنسيق معلومات الجهاز للنص."""
        return (
            f"📱 **الجهاز:** {self.get_display_name()}\n"
            f"🆔 **ID:** `{self.device_id}`\n"
            f"📅 **التسجيل:** {self.registered_at}\n"
            f"📶 **الحالة:** {'✅ متصل' if self.is_active else '❌ غير متصل'}"
        )