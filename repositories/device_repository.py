"""
طبقة الوصول إلى البيانات (Repository Pattern)
"""
import json
import os
from typing import Dict, Optional

from models.device import Device
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class DeviceRepository:
    """مستودع الأجهزة - مسؤول عن عمليات CRUD."""

    def __init__(self, file_path: str = settings.DEVICES_FILE):
        self.file_path = file_path
        self._cache: Dict[str, Device] = {}
        self._load()

    def _load(self) -> None:
        """تحميل الأجهزة من الملف."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._cache = {
                        device_id: Device.from_dict(device_data)
                        for device_id, device_data in data.items()
                    }
                logger.info(f"تم تحميل {len(self._cache)} جهازاً")
            else:
                self._cache = {}
                self._save()
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"خطأ في تحميل الأجهزة: {e}")
            self._cache = {}

    def _save(self) -> None:
        """حفظ الأجهزة في الملف."""
        try:
            data = {
                device_id: device.to_dict()
                for device_id, device in self._cache.items()
            }
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"تم حفظ {len(self._cache)} جهازاً")
        except IOError as e:
            logger.error(f"خطأ في حفظ الأجهزة: {e}")
            raise

    def get_all(self) -> Dict[str, Device]:
        """الحصول على جميع الأجهزة."""
        return self._cache.copy()

    def get(self, device_id: str) -> Optional[Device]:
        """الحصول على جهاز محدد."""
        return self._cache.get(device_id)

    def add(self, device: Device) -> None:
        """إضافة جهاز جديد."""
        self._cache[device.device_id] = device
        self._save()
        logger.info(f"تم إضافة جهاز: {device.device_id}")

    def update(self, device: Device) -> None:
        """تحديث جهاز موجود."""
        if device.device_id in self._cache:
            self._cache[device.device_id] = device
            self._save()
            logger.info(f"تم تحديث جهاز: {device.device_id}")

    def delete(self, device_id: str) -> bool:
        """حذف جهاز."""
        if device_id in self._cache:
            del self._cache[device_id]
            self._save()
            logger.info(f"تم حذف جهاز: {device_id}")
            return True
        return False

    def exists(self, device_id: str) -> bool:
        """التحقق من وجود جهاز."""
        return device_id in self._cache

    def count(self) -> int:
        """عدد الأجهزة."""
        return len(self._cache)

    def reload(self) -> None:
        """إعادة تحميل الأجهزة من الملف."""
        self._load()