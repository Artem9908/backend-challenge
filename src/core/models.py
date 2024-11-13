from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class EventOutbox(models.Model):
    event_type = models.CharField(max_length=255)
    event_date_time = models.DateTimeField(auto_now_add=True)
    environment = models.CharField(max_length=255)
    event_context = models.JSONField()
    metadata_version = models.IntegerField(default=1)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.event_type} at {self.event_date_time}"

    class Meta:
        app_label = 'core'
        verbose_name = 'Event Outbox'
        verbose_name_plural = 'Events Outbox'
        indexes = [
            # Композитный индекс для быстрого поиска непросмотренных событий по времени
            models.Index(fields=['processed', 'event_date_time']),
            
            # Отдельные индексы для часто используемых полей в фильтрах
            models.Index(fields=['event_type']),
            models.Index(fields=['environment']),
            
            # Индекс для поля metadata_version, если часто используется в запросах
            models.Index(fields=['metadata_version']),
        ]
        ordering = ['-event_date_time']