"""
الاستثناءات المخصصة
"""


class BotException(Exception):
    """الاستثناء الأساسي للبوت."""
    pass


class UnauthorizedError(BotException):
    """خطأ صلاحية المستخدم."""
    pass


class DeviceNotFoundError(BotException):
    """خطأ عدم وجود الجهاز."""
    pass


class CommandExecutionError(BotException):
    """خطأ في تنفيذ الأمر."""
    pass


class InvalidInputError(BotException):
    """خطأ في المدخلات."""
    pass


class StorageError(BotException):
    """خطأ في التخزين."""
    pass