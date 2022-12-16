CREATE TABLE IF NOT EXISTS modlog (
    id PRIMARY key,
    action,
    mod,
    details,
    target_body,
    target_title,
    target_permalink,
    target_author,
    created_utc INT,
    timestamp_db_updated INT
);