from abc import ABC, abstractmethod


class BaseHandler(ABC):
    def __init__(self, bot):
        self._bot = bot
        self.__cache = {}

    @abstractmethod
    def handle(self, message):
        ...

    @property
    def cache(self):
        return self.__cache

    def _save_to_cache(self, key, value):
        self.__cache[key] = value

    def _get_from_cache(self, key):
        return self.__cache.get(key)
