"""
نقطة الدخول الرئيسية للتطبيق
"""

import asyncio
from telegram import Update  # <-- أضف هذا السطر
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from config.settings import settings
from repositories.device_repository import DeviceRepository
from services.device_service import DeviceService
from services.command_service import CommandService
from handlers.start_handler import StartHandler
from handlers.device_handler import DeviceHandler
from handlers.command_handler import CommandHandler as CmdHandler
from handlers.callback_handler import CallbackHandler
from handlers.conversation_handler import ConversationHandler
from utils.logger import get_logger

logger = get_logger(__name__)


def main() -> None:
    """تشغيل البوت."""
    logger.info("بدء تشغيل البوت...")

    # ===== تهيئة التبعيات (Dependency Injection) =====
    device_repository = DeviceRepository(settings.DEVICES_FILE)
    device_service = DeviceService(device_repository)
    command_service = CommandService()

    start_handler = StartHandler(device_service, command_service)
    device_handler = DeviceHandler(device_service, command_service)
    command_handler = CmdHandler(device_service, command_service)
    callback_handler = CallbackHandler(device_handler, command_handler)
    conversation_handler = ConversationHandler(command_handler)

    # ===== إنشاء التطبيق =====
    application = Application.builder().token(settings.BOT_TOKEN).build()

    # ===== تسجيل المعالجات =====
    application.add_handler(CommandHandler("start", start_handler.handle))
    application.add_handler(CommandHandler("help", callback_handler._show_help))
    application.add_handler(CommandHandler("cancel", callback_handler._cancel_command))
    application.add_handler(CallbackQueryHandler(callback_handler.handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, conversation_handler.handle_text))

    # ===== تشغيل البوت =====
    logger.info("✅ البوت جاهز للعمل...")
    print("✅ البوت شغال...")

asyncio.run(application.run_polling(
    allowed_updates=Update.ALL_TYPES,
    drop_pending_updates=True,
))


if __name__ == "__main__":
    main()