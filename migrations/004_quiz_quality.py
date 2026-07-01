def upgrade(connection, using_postgres):
    if using_postgres:
        alters = [
            "ALTER TABLE quiz_sessions ADD COLUMN IF NOT EXISTS expires_at TIMESTAMP",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS answer_variants_json TEXT",
            "ALTER TABLE results ADD COLUMN IF NOT EXISTS expired BOOLEAN DEFAULT FALSE",
        ]
    else:
        alters = [
            "ALTER TABLE quiz_sessions ADD COLUMN expires_at TIMESTAMP",
            "ALTER TABLE questions ADD COLUMN answer_variants_json TEXT",
            "ALTER TABLE results ADD COLUMN expired BOOLEAN DEFAULT 0",
        ]

    for query in alters:
        try:
            connection.execute(query)
            connection.commit()
        except Exception:
            connection.rollback()
