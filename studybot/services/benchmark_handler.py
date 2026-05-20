import random
import time
from bot.services.base_handler import BaseHandler
from bot.utils.sort_utils import benchmark, merge_sort, quick_sort


class BenchmarkHandler(BaseHandler):
    def handle(self, message):
        parts = message.text.strip().split()
        try:
            n = min(int(parts[1]), 100_000) if len(parts) > 1 else 1000
        except ValueError:
            n = 1000

        arr    = [random.randint(1, n * 10) for _ in range(n)]
        target = random.choice(arr)
        result = benchmark(arr, target)

        t0 = time.perf_counter()
        merge_sort(arr.copy())
        merge_ms = round((time.perf_counter() - t0) * 1000, 2)

        t0 = time.perf_counter()
        quick_sort(arr.copy())
        quick_ms = round((time.perf_counter() - t0) * 1000, 2)

        text = (
            f'📊 *Сравнение алгоритмов (n={n:,})*\n\n'
            f'*Поиск:*\n'
            f'🔍 Linear search: `{result["linear_ms"]} мс` — O(n)\n'
            f'🔍 Binary search: `{result["binary_ms"]} мс` — O(log n)\n\n'
            f'*Сортировка:*\n'
            f'📦 Merge sort: `{merge_ms} мс` — O(n log n)\n'
            f'⚡ Quick sort: `{quick_ms} мс` — O(n log n)\n\n'
            f'_Попробуй: /benchmark 50000_'
        )
        self._bot.reply_to(message, text, parse_mode='Markdown')
