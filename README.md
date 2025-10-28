Запуск API проводится с помощью сервера uvicorn:
$ uvicorn app.main:app 
Для тестов celery запускался только с одним воркером:
$ celery app.core.celery_app worker -P solo
Подключаем Celery Beat для постановки задач в очередь:
$ celery app.core.celery_app beat
