"""
معالج أمر /start
"""
from telegram import Update
from telegram.ext import ContextTypes

from handlers.base_handler import BaseHandler
from keyboards.menu_keyboards import MenuKeyboards
from utils.logger import get_logger

logger = get_logger(__name__)


class StartHandler(BaseHandler):
    """معالج أمر البدء."""

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """معالجة أمر /start."""
        if not await self._check_auth(update):
            return

        devices_count = self.device_service.get_device_count()

        await self._reply(
            update,
            f"👋 **مرحباً بك في نظام التحكم بالفروع**\n\n"
            f"📱 **عدد الأجهزة المسجلة:** {devices_count}\n"
            f"🔹 استخدم الأزرار أدناه للتنقل وإرسال الأوامر.",
            reply_markup=MenuKeyboards.main_menu(devices_count),
        )
        logger.info(f"المستخدم {update.effective_chat.id} بدأ البوت")