from celery import Celery
from app.core.config import settings
from celery.schedules import crontab
import app.tasks.parse_chats, app.tasks.parse_messages, app.tasks.check_promos, app.tasks.update_stats


celery_app = Celery(
    "ozon_chat_manager",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_routes={},
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)


# Автоматически находит задачи по пути app.tasks.*
celery_app.autodiscover_tasks(["app.tasks"])

# Конфигурация расписания задач Celery
celery_app.conf.beat_schedule = {
    "parse-chats-every-10-minutes": {
        "task": "app.tasks.parse_chats.parse_chats_task",
        "schedule": crontab(minute='*/10'),
    },
    "parse-messages-every-10-minutes": {
        "task": "app.tasks.parse_messages.parse_messages_task",
        "schedule": crontab(minute='*/10'),
    },
    "check-promos-every-5-minutes": {
        "task": "app.tasks.check_promos.check_promos_task",
        "schedule": crontab(minute='*/5'),
    },
    "update-stats-every-15-minutes": {
        "task": "app.tasks.update_stats.update_stats_task",
        "schedule": crontab(minute='*/15'),
    },
}


@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request:{self.request!r}")
