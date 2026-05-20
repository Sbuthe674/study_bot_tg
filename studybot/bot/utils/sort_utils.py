"""
bot/utils/sort_utils.py
Алгоритмы — Lab 3: сортировка и поиск с Big-O анализом.

Варианты:
  Variant 10 — merge sort + binary search  O(n log n) / O(log n)
  Variant 4  — binary search + quick sort
  Variant 21 — сравнение linear vs binary search
"""
import bisect
import time


# ── Сортировки ────────────────────────────────────────────────

def merge_sort(arr: list) -> list:
    """
    Merge sort — O(n log n) в любом случае.
    Стабильная, хорошо работает на больших данных.
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr: list) -> list:
    """
    Quick sort — O(n log n) среднее, O(n²) худший случай.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left   = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right  = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


# ── Поиск ─────────────────────────────────────────────────────

def linear_search(arr: list, target) -> int:
    """Линейный поиск — O(n). Не требует сортировки."""
    for i, item in enumerate(arr):
        if item == target:
            return i
    return -1


def binary_search(arr: list, target) -> int:
    """
    Бинарный поиск — O(log n). Требует сортированного массива.
    Использует bisect из стандартной библиотеки.
    """
    idx = bisect.bisect_left(arr, target)
    if idx < len(arr) and arr[idx] == target:
        return idx
    return -1


# ── Сравнение производительности ─────────────────────────────

def benchmark(arr: list, target) -> dict:
    """
    Сравнивает время linear vs binary search.
    Возвращает словарь с результатами — для команды /benchmark.
    """
    sorted_arr = sorted(arr)

    t0 = time.perf_counter()
    li = linear_search(arr, target)
    linear_time = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    bi = binary_search(sorted_arr, target)
    binary_time = (time.perf_counter() - t0) * 1000

    return {
        'n':           len(arr),
        'linear_idx':  li,
        'binary_idx':  bi,
        'linear_ms':   round(linear_time, 4),
        'binary_ms':   round(binary_time, 4),
    }
