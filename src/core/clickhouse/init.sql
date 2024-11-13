CREATE TABLE IF NOT EXISTS default.event_log
(
    event_id String,
    event_type String,
    event_date_time DateTime,
    environment String,
    event_context String,
    metadata_version UInt32
) ENGINE = MergeTree()
ORDER BY (event_date_time, event_id); 