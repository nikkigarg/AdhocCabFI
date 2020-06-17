from .celery import celery_app

print(celery_app)
__all__ = ('celery_app',)