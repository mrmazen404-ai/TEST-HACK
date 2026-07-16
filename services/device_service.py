"""
طبقة خدمات الأجهزة (Service Layer)
"""
from typing import Dict, List, Optional

from models.device import Device
from repositories.device_repository import DeviceRepository
from utils.logger import get_logger
from exceptions.custom_exceptions import DeviceNotFoundError

logger = get_logger(__name__)


class DeviceService:
    """خدمات إدارة الأجهزة."""

    def __init__(self, repository: DeviceRepository):
        self.repository = repository

    def get_all_devices(self) -> Dict[str, Device]:
        """الحصول على جميع الأجهزة."""
        return self.repository.get_all()

    def get_device(self, device_id: str) -> Optional[Device]:
        """الحصول على جهاز محدد."""
        return self.repository.get(device_id)

    def register_device(self, device_id: str, info: Dict) -> Device:
        """تسجيل جهاز جديد."""
        if self.repository.exists(device_id):
            device = self.repository.get(device_id)
            if device:
                device.info.update(info)
                self.repository.update(device)
                return device

        device = Device(
            device_id=device_id,
            name=info.get("name"),
            info=info,
            is_active=True,
        )
        self.repository.add(device)
        return device

    def update_device_status(self, device_id: str, is_active: bool) -> Optional[Device]:
        """تحديث حالة الجهاز."""
        device = self.repository.get(device_id)
        if device:
            device.is_active = is_active
            self.repository.update(device)
            return device
        return None

    def delete_device(self, device_id: str) -> bool:
        """حذف جهاز."""
        if not self.repository.exists(device_id):
            raise DeviceNotFoundError(f"الجهاز {device_id} غير موجود")
        return self.repository.delete(device_id)

    def get_device_count(self) -> int:
        """عدد الأجهزة."""
        return self.repository.count()

    def get_device_names(self) -> List[str]:
        """الحصول على أسماء الأجهزة."""
        return [
            device.get_display_name()
            for device in self.repository.get_all().values()
        ]

    def is_owner_device(self, device_id: str) -> bool:
        """التحقق من ملكية الجهاز."""
        return self.repository.exists(device_id)

    def reload(self) -> None:
        """إعادة تحميل البيانات."""
        self.repository.reload()