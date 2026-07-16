"""
حزمة الاستثناءات
"""
from exceptions.custom_exceptions import (
    BotException,
    UnauthorizedError,
    DeviceNotFoundError,
    CommandExecutionError,
    InvalidInputError,
    StorageError,
)

__all__ = [
    "BotException",
    "UnauthorizedError",
    "DeviceNotFoundError",
    "CommandExecutionError",
    "InvalidInputError",
    "StorageError",
]