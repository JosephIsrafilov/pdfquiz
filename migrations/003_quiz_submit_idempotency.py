def upgrade(connection, using_postgres):
    if using_postgres:
        alters = [
            "ALTER TABLE quiz_sessions ADD COLUMN IF NOT EXISTS submitted_answers_json TEXT",
            "ALTER TABLE quiz_sessions ADD COLUMN IF NOT EXISTS result_json TEXT",
            "ALTER TABLE quiz_sessions ADD COLUMN IF NOT EXISTS saved_result_id INTEGER REFERENCES results(id) ON DELETE SET NULL",
        ]
    else:
        alters = [
            "ALTER TABLE quiz_sessions ADD COLUMN submitted_answers_json TEXT",
            "ALTER TABLE quiz_sessions ADD COLUMN result_json TEXT",
            "ALTER TABLE quiz_sessions ADD COLUMN saved_result_id INTEGER REFERENCES results(id) ON DELETE SET NULL",
        ]

    for query in alters:
        try:
            connection.execute(query)
            connection.commit()
        except Exception:
            connection.rollback()
