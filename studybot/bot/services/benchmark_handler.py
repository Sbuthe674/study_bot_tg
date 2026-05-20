"""
bot/services/benchmark_handler.py
Алгоритмы — Lab 3: команда /benchmark

Сравнивает linear search vs binary search на случайных данных.
Показывает Big-O на практике.
"""
import random
from .base_handler import BaseHandler
from ..utils.sort_utils import benchmark, merge_sort, quick_sort


class BenchmarkHandler(BaseHandler):
    """Демонстрирует разницу алгоритмов поиска и сортировки."""

    def handle(self, message):
        parts = message.text.strip().split()
        # /benchmark [размер_массива]
        try:
            n = int(parts[1]) if len(parts) > 1 else 1000
            n = min(n, 100_000)  # защита от слишком больших чисел
        except ValueError:
            n = 1000

        arr    = [random.randint(1, n * 10) for _ in range(n)]
        target = random.choice(arr)  # гарантированно найдём
        result = benchmark(arr, target)

        # Также замеряем сортировки
        import time
        arr_copy = arr.copy()
        t0 = time.perf_counter()
        merge_sort(arr_copy)
        merge_ms = round((time.perf_counter() - t0) * 1000, 2)

        arr_copy = arr.copy()
        t0 = time.perf_counter()
        quick_sort(arr_copy)
        quick_ms = round((time.perf_counter() - t0) * 1000, 2)

        text = (
            f'📊 *Сравнение алгоритмов (n={n:,})*\n\n'
            f'*Поиск цели: {target}*\n'
            f'🔍 Linear search: `{result["linear_ms"]} мс` — O(n)\n'
            f'🔍 Binary search: `{result["binary_ms"]} мс` — O(log n)\n\n'
            f'*Сортировка:*\n'
            f'📦 Merge sort:  `{merge_ms} мс` — O(n log n)\n'
            f'⚡ Quick sort:  `{quick_ms} мс` — O(n log n) avg\n\n'
            f'_Чем больше n, тем заметнее разница._\n'
            f'Попробуй: /benchmark 50000'
        )
        self._bot.reply_to(message, text, parse_mode='Markdown')
