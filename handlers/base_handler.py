"""
المعالج الأساسي - يحتوي على الوظائف المشتركة
"""
from typing import Optional
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from services.device_service import DeviceService
from services.command_service import CommandService
from security.auth import auth_service
from utils.logger import get_logger
from exceptions.custom_exceptions import UnauthorizedError

logger = get_logger(__name__)


class BaseHandler:
    """المعالج الأساسي لجميع المعالجات."""

    def __init__(
        self,
        device_service: DeviceService,
        command_service: CommandService,
    ):
        self.device_service = device_service
        self.command_service = command_service

    async def _check_auth(self, update: Update) -> bool:
        """التحقق من صلاحية المستخدم."""
        chat_id = update.effective_chat.id
        if not auth_service.is_authorized(chat_id):
            if update.message:
                await update.message.reply_text("⛔ هذا البوت خاص بالتاجر فقط.")
            return False
        return True

    async def _reply(
        self,
        update: Update,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        parse_mode: str = "Markdown",
    ):
        """إرسال رد موحد."""
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
        elif update.message:
            await update.message.reply_text(
                text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )

    async def _answer_callback(self, update: Update, text: str = None, show_alert: bool = False):
        """الرد على استعلام الأزرار."""
        if update.callback_query:
            await update.callback_query.answer(text, show_alert=show_alert)