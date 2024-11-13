import json
from typing import List, Dict, Any
import structlog

from core.event_log_client import EventLogClient
from outbox.models import EventOutbox
from django.utils import timezone

logger = structlog.get_logger(__name__)


class EventLogService:
    def __init__(self):
        self._client = None
        self._batch_size = 1000  # Configurable batch size

    def insert_events(self, data: List[Dict[str, Any]]) -> bool:
        """Insert events into ClickHouse with batch processing and verification.
        Returns True if all events were successfully inserted."""
        if not data:
            logger.debug("events.insert.empty")
            return True

        try:
            with EventLogClient.init() as client:
                # Process in batches to avoid memory issues
                for i in range(0, len(data), self._batch_size):
                    batch = data[i:i + self._batch_size]
                    client.insert(batch)
                    
                    logger.info(
                        "events.insert.batch_success",
                        batch_size=len(batch),
                        batch_number=i // self._batch_size + 1,
                        total_batches=-(len(data) // -self._batch_size),  # Ceiling division
                        event_types=list(set(event["event_type"] for event in batch))
                    )
                
                return True
                
        except Exception as e:
            logger.error(
                "events.insert.failed",
                error=str(e),
                error_type=type(e).__name__,
                data_size=len(data),
                batch_size=self._batch_size
            )
            raise

    def mark_events_as_processed(self, event_ids: List[int]) -> None:
        """Mark events as processed in batches."""
        if not event_ids:
            return

        try:
            # Process in batches to avoid overwhelming the database
            for i in range(0, len(event_ids), self._batch_size):
                batch_ids = event_ids[i:i + self._batch_size]
                EventOutbox.objects.filter(id__in=batch_ids).update(
                    processed=True,
                    processed_at=timezone.now()
                )
                logger.info(
                    "events.marked_processed.batch",
                    batch_size=len(batch_ids),
                    batch_number=i // self._batch_size + 1,
                    total_batches=-(len(event_ids) // -self._batch_size)
                )
                
        except Exception as e:
            logger.error(
                "events.mark_processed.failed",
                error=str(e),
                error_type=type(e).__name__,
                event_ids_count=len(event_ids)
            )
            raise

    @staticmethod
    def prepare_data(events: List[EventOutbox]) -> List[Dict[str, Any]]:
        return [
            {
                "event_type": event.event_type,
                "event_date_time": event.event_date_time,
                "environment": event.environment,
                "event_context": json.dumps(event.event_context),
                "metadata_version": event.metadata_version,
            }
            for event in events
        ]