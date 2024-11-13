import pytest
from unittest.mock import patch, MagicMock, ANY
from core.services.event_log_service import EventLogService
from outbox.models import EventOutbox
from django.utils import timezone

@pytest.fixture
def event_log_service():
    return EventLogService()

@pytest.fixture
def sample_events():
    return [
        EventOutbox(
            event_type="user_created",
            event_date_time=timezone.now(),
            environment="Test",
            event_context={"email": "test@example.com", "first_name": "Test", "last_name": "User"},
            metadata_version=1,
        ),
        EventOutbox(
            event_type="user_created",
            event_date_time=timezone.now(),
            environment="Test",
            event_context={"email": "jane@example.com", "first_name": "Jane", "last_name": "Doe"},
            metadata_version=1,
        ),
    ]

def test_prepare_data(event_log_service, sample_events):
    prepared_data = EventLogService.prepare_data(sample_events)
    assert len(prepared_data) == 2
    assert prepared_data[0]["event_type"] == "user_created"
    assert prepared_data[0]["environment"] == "Test"
    assert prepared_data[0]["event_context"] == '{"email": "test@example.com", "first_name": "Test", "last_name": "User"}'
    assert prepared_data[0]["metadata_version"] == 1

@patch('core.event_log_client.EventLogClient.init')
def test_insert_events(mock_init, event_log_service, sample_events):
    mock_client = MagicMock()
    mock_init.return_value.__enter__.return_value = mock_client

    data = EventLogService.prepare_data(sample_events)
    event_log_service.insert_events(data)

    mock_client.insert.assert_called_once_with(data)

@patch('outbox.models.EventOutbox.objects.filter')
def test_mark_events_as_processed(mock_filter, event_log_service):
    mock_qs = MagicMock()
    mock_filter.return_value = mock_qs

    event_ids = [1, 2, 3]
    event_log_service.mark_events_as_processed(event_ids)

    mock_filter.assert_called_once_with(id__in=event_ids)
    mock_qs.update.assert_called_once_with(
        processed=True,
        processed_at=ANY
    )