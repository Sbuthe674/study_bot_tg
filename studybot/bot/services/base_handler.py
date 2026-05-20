"""
bot/services/base_handler.py
ООП — Lab 2: абстракция, наследование, инкапсуляция, полиморфизм.

Демонстрирует:
  - ABC + @abstractmethod  (абстракция)
  - Наследование: все хендлеры → BaseHandler
  - Полиморфизм: метод handle() у каждого свой
  - Инкапсуляция: __cache (private), _bot (protected)
  - @property для доступа к кэшу
"""
from abc import ABC, abstractmethod


class BaseHandler(ABC):
    """Абстрактный базовый класс для всех команд бота."""

    def __init__(self, bot):
        self._bot = bot          # protected — доступен наследникам
        self.__cache = {}        # private — только через property

    @abstractmethod
    def handle(self, message):
        """Каждый наследник реализует свою логику."""
        ...

    @property
    def cache(self):
        """Безопасный доступ к кэшу через @property."""
        return self.__cache

    def _save_to_cache(self, key: str, value):
        self.__cache[key] = value

    def _get_from_cache(self, key: str):
        return self.__cache.get(key)

    def __str__(self):
        return f"<{self.__class__.__name__}>"
