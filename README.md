# Event Log Processing System

A robust event logging system that implements the transactional outbox pattern to reliably process and store event logs in ClickHouse for business analysis, incident investigations, and security audits.

## Architecture

### System Overview

The system implements the transactional outbox pattern to ensure reliable event processing:
1. **Events are first stored in PostgreSQL (outbox table).**
2. **Celery workers process events in batches.**
3. **Processed events are stored in ClickHouse.**
4. **Events are marked as processed in PostgreSQL.**

## Tech Stack

- **Backend**: Python 3.13, Django
- **Databases**: 
  - PostgreSQL (transactional storage)
  - ClickHouse (analytical storage)
- **Task Processing**: Celery with Redis
- **Monitoring**: 
  - OpenTelemetry
  - Structlog
  - Sentry
- **Infrastructure**: Docker & Docker Compose
- **Testing**: pytest with pytest-django

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Make (optional, but recommended)
- Python 3.13 (for local development)

### Installation

1. **Clone the repository:**

    ```bash
    git clone [repository-url]
    cd [repository-name]
    ```

2. **Copy environment files:**

    ```bash
    cp src/core/.env.example src/core/.env
    ```

3. **Build and start services:**

    ```bash
    make run
    ```

4. **Initialize the database:**

    ```bash
    make install
    ```

    This will:
    - Create database migrations
    - Apply migrations
    - Create a superuser

### Development Commands

- **Start all services:**
    ```bash
    make run
    ```
- **Create database migrations:**
    ```bash
    make migrations
    ```
- **Apply migrations:**
    ```bash
    make migrate
    ```
- **Create superuser:**
    ```bash
    make superuser
    ```
- **Access Django shell:**
    ```bash
    make shell
    ```
- **Run linting:**
    ```bash
    make lint
    ```
- **Run tests:**
    ```bash
    make test
    ```
- **Reset test database:**
    ```bash
    make reset-test-db
    ```

## Configuration

### Environment Variables

Key environment variables can be set in `src/core/.env` or overridden in `docker-compose.yml`:

#### General

- `DEBUG=true`
- `SECRET_KEY="v3rys3cr3tk3y"`
- `ALLOWED_HOSTS=localhost,`
- `ENVIRONMENT=dev`
- `TIME_ZONE=Europe/Moscow`

#### Database

- `DATABASE_URL=postgres://test_user:123456@db:5432/test_database`
- `POSTGRES_DB=test_database`
- `POSTGRES_USER=test_user`
- `POSTGRES_PASSWORD=123456`
- `POSTGRES_HOST=db`
- `POSTGRES_PORT=5432`

#### ClickHouse

- `CLICKHOUSE_HOST=clickhouse`
- `CLICKHOUSE_PORT=8123`
- `CLICKHOUSE_USER=default`
- `CLICKHOUSE_PASSWORD=`
- `CLICKHOUSE_SCHEMA=default`
- `CLICKHOUSE_PROTOCOL=http`
- `CLICKHOUSE_URI=http://default:@clickhouse:8123/default`
- `CLICKHOUSE_EVENT_LOG_TABLE_NAME=event_log`
- `CLICKHOUSE_CONNECT_TIMEOUT=30`
- `CLICKHOUSE_SEND_RECEIVE_TIMEOUT=10`

#### Celery

- `CELERY_BROKER_URL=redis://redis:6379/0`
- `CELERY_RESULT_BACKEND=redis://redis:6379/0`
- `CELERY_ALWAYS_EAGER=true`
- `CELERY_TASK_ALWAYS_EAGER=true`
- `CELERY_TASK_EAGER_PROPAGATES=true`

#### Batch Processing

- `EVENT_BATCH_SIZE=1000`
- `EVENT_PROCESSING_INTERVAL=60`
- `CLICKHOUSE_BATCH_SIZE=10000`

#### Monitoring

- `SENTRY_CONFIG_DSN=your-sentry-dsn`
- `SENTRY_CONFIG_ENVIRONMENT=dev`
- `OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317`

## Monitoring and Logging

### Structured Logging

- **Uses `structlog` for structured logging.**
- **Log format includes context, timestamps, and trace IDs.**
- **Logs are available in JSON format for easy ingestion by monitoring tools.**

### Tracing

- **OpenTelemetry integration for distributed tracing.**
- **Traces are visible in OpenTelemetry Collector and can be viewed in tools like Jaeger or Zipkin.**
- **Sentry integration for error tracking and alerting.**

### Metrics

- **Basic Django metrics for request handling and performance.**
- **Celery task metrics to monitor task execution and failures.**
- **Database performance metrics to track query performance and database health.**

## Performance Considerations

### Batch Processing

- **Events are processed in configurable batches (`EVENT_BATCH_SIZE`).**
- **Celery tasks run at configurable intervals (`EVENT_PROCESSING_INTERVAL`).**
- **Uses PostgreSQL `SELECT FOR UPDATE SKIP LOCKED` for efficient batch processing without locking issues.**

### Database Optimization

- **Proper indexing on the outbox table to optimize query performance.**
- **Efficient ClickHouse table structure with appropriate partitioning for fast analytical queries.**
- **Batch inserts to ClickHouse minimize network overhead and improve insertion performance.**

### Error Handling

- **Retry mechanism for failed Celery tasks with exponential backoff.**
- **Dead letter queue for unprocessable events to prevent blocking the main processing pipeline.**
- **Comprehensive error logging and monitoring to detect and respond to issues promptly.**

## Testing

### Running Tests

- **Run all tests:**
    ```bash
    make test
    ```
- **Run a specific test file:**
    ```bash
    docker compose -f docker-compose.test.yml run --rm test pytest path/to/test.py
    ```
- **Run tests with coverage:**
    ```bash
    docker compose -f docker-compose.test.yml run --rm test pytest --cov
    ```

### Test Structure

- **Unit tests for core business logic and services.**
- **Integration tests for database operations and event processing.**
- **End-to-end tests for complete workflows involving multiple components.**
- **Fixtures for common test scenarios and setup.**

## Contributing

1. **Fork the repository.**
2. **Create your feature branch:**
    ```bash
    git checkout -b feature/AmazingFeature
    ```
3. **Commit your changes:**
    ```bash
    git commit -m 'Add some AmazingFeature'
    ```
4. **Push to the branch:**
    ```bash
    git push origin feature/AmazingFeature
    ```
5. **Open a Pull Request.**
