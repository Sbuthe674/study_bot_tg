"""bot/views.py — веб-страница с историей запросов"""
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import UserQuery


@staff_member_required
def history_view(request):
    queries = UserQuery.objects.all()[:50]
    return render(request, 'bot/history.html', {'queries': queries})
