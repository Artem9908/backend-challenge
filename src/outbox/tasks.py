from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.db import transaction
from .models import EventOutbox
import logging
from django.conf import settings

from core.services import EventLogService

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 5, 'countdown': 60},
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True
)
def process_event_outbox(self):
    """Process events from EventOutbox in batches."""
    logger.info('Starting process_event_outbox task')
    
    try:
        event_log_service = EventLogService()
        
        while True:
            with transaction.atomic():
                events = _get_unprocessed_events()
                if not events:
                    logger.info('No more events to process')
                    break
                
                _process_events(events, event_log_service)
                logger.info(f'Processed batch of {len(events)} events')
                
    except Exception as e:
        logger.error(f'Error processing event outbox: {str(e)}')
        raise self.retry(exc=e)

def _get_unprocessed_events():
    """Fetch a batch of unprocessed events."""
    events = (EventOutbox.objects
        .select_for_update(skip_locked=True)
        .filter(processed=False)
        .order_by('id')[:settings.EVENT_BATCH_SIZE])
    return list(events)

def _process_events(events, event_log_service):
    """Process a batch of events using EventLogService."""
    prepared_data = event_log_service.prepare_data(events)
    event_log_service.insert_events(prepared_data)
    
    event_ids = [event.id for event in events]
    event_log_service.mark_events_as_processed(event_ids)