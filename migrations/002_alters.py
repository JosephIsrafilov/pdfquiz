def upgrade(connection, using_postgres):
    if using_postgres:
        alters = [
            "ALTER TABLE results ADD COLUMN IF NOT EXISTS attempt_json TEXT",
            "ALTER TABLE topics ADD COLUMN IF NOT EXISTS curriculum_key TEXT",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS curriculum_key TEXT",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS option_rationales_json TEXT",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS question_type TEXT NOT NULL DEFAULT 'mcq'",
            "ALTER TABLE question_templates ADD COLUMN IF NOT EXISTS question_type VARCHAR(50) DEFAULT 'mcq'",
            "ALTER TABLE quiz_sessions ADD COLUMN IF NOT EXISTS room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE",
            "ALTER TABLE results ADD COLUMN IF NOT EXISTS room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE",
            "ALTER TABLE quiz_sessions ADD COLUMN IF NOT EXISTS checked_questions_json TEXT DEFAULT '[]'",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS pool VARCHAR(20) DEFAULT 'pool_A'",
            "ALTER TABLE quiz_sessions ADD COLUMN IF NOT EXISTS generated_questions_json TEXT DEFAULT '[]'",
        ]
        for query in alters:
            try:
                connection.execute(query)
                connection.commit()
            except Exception:
                connection.rollback()
        
        try:
            connection.execute("CREATE INDEX IF NOT EXISTS idx_questions_pool ON questions(pool)")
            connection.commit()
        except Exception:
            connection.rollback()
    else:
        sqlite_alters = [
            "ALTER TABLE results ADD COLUMN attempt_json TEXT",
            "ALTER TABLE topics ADD COLUMN curriculum_key TEXT",
            "ALTER TABLE questions ADD COLUMN curriculum_key TEXT",
            "ALTER TABLE questions ADD COLUMN option_rationales_json TEXT",
            "ALTER TABLE questions ADD COLUMN question_type TEXT NOT NULL DEFAULT 'mcq'",
            "ALTER TABLE question_templates ADD COLUMN question_type VARCHAR(50) DEFAULT 'mcq'",
            "ALTER TABLE quiz_sessions ADD COLUMN room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE",
            "ALTER TABLE results ADD COLUMN room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE",
            "ALTER TABLE quiz_sessions ADD COLUMN checked_questions_json TEXT DEFAULT '[]'",
            "ALTER TABLE questions ADD COLUMN pool VARCHAR(20) DEFAULT 'pool_A'",
            "ALTER TABLE quiz_sessions ADD COLUMN generated_questions_json TEXT DEFAULT '[]'",
        ]
        for query in sqlite_alters:
            try:
                connection.execute(query)
                connection.commit()
            except Exception:
                connection.rollback()
        
        try:
            connection.execute("CREATE INDEX IF NOT EXISTS idx_questions_pool ON questions(pool)")
            connection.commit()
        except Exception:
            connection.rollback()
