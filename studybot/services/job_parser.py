import time
import requests
from bs4 import BeautifulSoup
from bot.services.base_handler import BaseHandler
from bot.utils.sort_utils import merge_sort


class JobParser(BaseHandler):
    URL = 'https://realpython.github.io/fake-jobs/'

    def handle(self, message):
        cached = self._get_from_cache('jobs')
        jobs   = cached if cached else self._fetch_jobs()
        if jobs:
            self._save_to_cache('jobs', jobs)

        if not jobs:
            self._bot.reply_to(message, '❌ Не удалось получить вакансии.')
            return

        sorted_titles = merge_sort([j['title'] for j in jobs])
        top5 = sorted_titles[:5]
        lines = ['📋 *Вакансии (топ-5):*\n']
        for i, title in enumerate(top5, 1):
            company = next((j['company'] for j in jobs if j['title'] == title), '—')
            lines.append(f'{i}. *{title}*\n   🏢 {company}')
        lines.append(f'\n_Всего: {len(jobs)} вакансий_')
        self._bot.reply_to(message, '\n'.join(lines), parse_mode='Markdown')

    def _fetch_jobs(self):
        try:
            r = requests.get(self.URL, timeout=8)
            r.raise_for_status()
        except requests.RequestException:
            return []
        soup  = BeautifulSoup(r.text, 'html.parser')
        cards = soup.select('.card-content')
        jobs  = []
        for card in cards:
            t = card.select_one('h2.title')
            c = card.select_one('h3.company')
            l = card.select_one('p.location')
            jobs.append({
                'title':    t.text.strip() if t else '—',
                'company':  c.text.strip() if c else '—',
                'location': l.text.strip() if l else '—',
            })
        time.sleep(1)
        return jobs
