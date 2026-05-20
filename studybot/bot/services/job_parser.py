"""
bot/services/job_parser.py
Парсинг — Lab 1, Variant 12: realpython.github.io/fake-jobs

Демонстрирует:
  - requests.get() + BeautifulSoup
  - CSS-селекторы для извлечения данных
  - try/except для сетевых ошибок
  - time.sleep() — вежливая пауза
  - ООП: класс JobParser наследует BaseHandler
"""
import time
import requests
from bs4 import BeautifulSoup

from .base_handler import BaseHandler
from ..utils.sort_utils import merge_sort


class JobParser(BaseHandler):
    """Парсит вакансии с учебного сайта и отвечает в Telegram."""

    URL = 'https://realpython.github.io/fake-jobs/'

    def handle(self, message):
        """Полиморфный метод — точка входа из бота."""
        # Проверяем кэш перед парсингом
        cached = self._get_from_cache('jobs')
        if cached:
            jobs = cached
        else:
            jobs = self._fetch_jobs()
            self._save_to_cache('jobs', jobs)

        if not jobs:
            self._bot.reply_to(message, '❌ Не удалось получить вакансии. Попробуй позже.')
            return

        # Сортируем через merge sort (алгоритмы — Lab 3)
        sorted_jobs = merge_sort([j['title'] for j in jobs])
        top5 = sorted_jobs[:5]

        lines = ['📋 *Вакансии (топ-5, сортировка merge sort):*\n']
        for i, title in enumerate(top5, 1):
            # Находим компанию для этого названия
            company = next((j['company'] for j in jobs if j['title'] == title), '—')
            lines.append(f'{i}. *{title}*\n   🏢 {company}')

        lines.append(f'\n_Всего найдено: {len(jobs)} вакансий_')
        self._bot.reply_to(message, '\n'.join(lines), parse_mode='Markdown')

    def _fetch_jobs(self) -> list:
        """Парсит HTML-страницу и возвращает список вакансий."""
        try:
            response = requests.get(self.URL, timeout=8)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            return []
        except requests.exceptions.RequestException:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.select('.card-content')
        jobs = []

        for card in cards:
            title    = card.select_one('h2.title')
            company  = card.select_one('h3.company')
            location = card.select_one('p.location')
            link_tag = card.select_one('a[href]')

            jobs.append({
                'title':    title.text.strip()    if title    else 'Без названия',
                'company':  company.text.strip()  if company  else 'Без компании',
                'location': location.text.strip() if location else 'Без локации',
                'link':     link_tag['href']      if link_tag else '',
            })

        time.sleep(1)  # вежливая пауза — обязательное требование Lab 1
        return jobs
