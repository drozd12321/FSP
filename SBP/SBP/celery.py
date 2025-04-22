import os
from celery import Celery

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SBP.settings')

app = Celery('win')

# Используем строку настроек из Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим и регистрируем задачи из `tasks.py` в приложениях
app.autodiscover_tasks()