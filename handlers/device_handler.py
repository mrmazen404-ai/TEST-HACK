"""
معالج إدارة الأجهزة
"""
from telegram import Update
from telegram.ext import ContextTypes

from handlers.base_handler import BaseHandler
from keyboards.menu_keyboards import MenuKeyboards
from models.device import Device
from utils.logger import get_logger
from exceptions.custom_exceptions import DeviceNotFoundError

logger = get_logger(__name__)


class DeviceHandler(BaseHandler):
    """معالج إدارة الأجهزة."""

    async def list_devices(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """عرض قائمة الأجهزة."""
        if not await self._check_auth(update):
            return

        devices = self.device_service.get_all_devices()

        if devices:
            await self._reply(
                update,
                "📱 **قائمة الأجهزة المسجلة:**\n\nاختر جهازاً للتحكم فيه:",
                reply_markup=MenuKeyboards.devices_list(devices),
            )
        else:
            await self._reply(
                update,
                "📱 **لا توجد أجهزة مسجلة**\n\n"
                "قم بتثبيت تطبيق الفرع على جهاز أندرويد لتسجيله.",
                reply_markup=MenuKeyboards.main_menu(0),
            )

    async def show_device(self, update: Update, context: ContextTypes.DEFAULT_TYPE, device_id: str) -> None:
        """عرض جهاز محدد مع أزرار التحكم."""
        if not await self._check_auth(update):
            return

        device = self.device_service.get_device(device_id)
        if not device:
            await self._reply(
                update,
                "❌ **الجهاز غير موجود**\nتم حذفه أو لم يتم تسجيله بعد.",
                reply_markup=MenuKeyboards.back_button("back_devices"),
            )
            return

        await self._reply(
            update,
            f"📱 **جهاز:** {device.get_display_name()}\n\n"
            f"{device.get_info_text()}\n\n"
            "📸 **اختر الأمر:**",
            reply_markup=MenuKeyboards.device_controls(device),
        )

    async def refresh_devices(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """تحديث قائمة الأجهزة."""
        if not await self._check_auth(update):
            return

        self.device_service.reload()
        devices_count = self.device_service.get_device_count()

        await self._reply(
            update,
            f"✅ **تم تحديث القائمة**\n\n"
            f"📱 **عدد الأجهزة المسجلة:** {devices_count}",
            reply_markup=MenuKeyboards.main_menu(devices_count),
        )
        logger.info(f"تم تحديث الأجهزة من قبل {update.effective_chat.id}")

    async def back_to_devices(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """العودة إلى قائمة الأجهزة."""
        if not await self._check_auth(update):
            return

        devices = self.device_service.get_all_devices()
        await self._reply(
            update,
            "📱 **قائمة الأجهزة المسجلة:**",
            reply_markup=MenuKeyboards.devices_list(devices),
        )