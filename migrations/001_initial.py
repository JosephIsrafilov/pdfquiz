def upgrade(connection, using_postgres):
    if using_postgres:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_admin BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                questions_json TEXT NOT NULL,
                uploaded_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                document_id INTEGER REFERENCES documents(id) ON DELETE SET NULL,
                source_label TEXT,
                total_questions INTEGER,
                quiz_size INTEGER,
                graded INTEGER,
                correct INTEGER,
                unanswered INTEGER,
                missing_answer_key INTEGER,
                mistake_numbers_json TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id SERIAL PRIMARY KEY,
                title_en TEXT NOT NULL,
                title_ru TEXT NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id SERIAL PRIMARY KEY,
                course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
                title_en TEXT NOT NULL,
                title_ru TEXT NOT NULL,
                description_en TEXT,
                description_ru TEXT,
                sort_order INTEGER NOT NULL DEFAULT 0,
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id SERIAL PRIMARY KEY,
                topic_id INTEGER NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
                text_en TEXT,
                text_ru TEXT,
                options_json TEXT NOT NULL,
                explanation_en TEXT,
                explanation_ru TEXT,
                difficulty TEXT NOT NULL DEFAULT 'beginner',
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS quiz_sessions (
                id SERIAL PRIMARY KEY,
                token TEXT UNIQUE NOT NULL,
                user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                language TEXT NOT NULL,
                question_order_json TEXT NOT NULL,
                option_orders_json TEXT NOT NULL,
                topic_ids_json TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                code TEXT UNIQUE NOT NULL,
                created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS group_members (
                id SERIAL PRIMARY KEY,
                group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                joined_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(group_id, user_id)
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id SERIAL PRIMARY KEY,
                code TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                topic_ids_json TEXT NOT NULL,
                difficulty TEXT,
                question_count INTEGER,
                time_limit_minutes INTEGER,
                max_attempts INTEGER,
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW(),
                expires_at TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS user_question_history (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
                seen_at TIMESTAMP DEFAULT NOW(),
                was_correct BOOLEAN
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS question_templates (
                id SERIAL PRIMARY KEY,
                topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
                template_key VARCHAR(100) UNIQUE,
                template_en TEXT,
                template_ru TEXT,
                variables_spec_json TEXT,
                answer_expression TEXT,
                difficulty VARCHAR(50),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS user_topic_mastery (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
                difficulty VARCHAR(50),
                total_attempts INTEGER DEFAULT 0,
                correct_attempts INTEGER DEFAULT 0,
                mastery_score REAL DEFAULT 0.0,
                locked BOOLEAN DEFAULT FALSE,
                last_attempt_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(user_id, topic_id, difficulty)
            )
        """)
        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_mastery_lookup ON user_topic_mastery(user_id, topic_id, difficulty)
        """)
        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_question_history_lookup
            ON user_question_history(user_id, question_id, seen_at DESC)
        """)
    else:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                questions_json TEXT NOT NULL,
                uploaded_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                document_id INTEGER REFERENCES documents(id) ON DELETE SET NULL,
                source_label TEXT,
                total_questions INTEGER,
                quiz_size INTEGER,
                graded INTEGER,
                correct INTEGER,
                unanswered INTEGER,
                missing_answer_key INTEGER,
                mistake_numbers_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title_en TEXT NOT NULL,
                title_ru TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
                title_en TEXT NOT NULL,
                title_ru TEXT NOT NULL,
                description_en TEXT,
                description_ru TEXT,
                sort_order INTEGER NOT NULL DEFAULT 0,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
                text_en TEXT,
                text_ru TEXT,
                options_json TEXT NOT NULL,
                explanation_en TEXT,
                explanation_ru TEXT,
                difficulty TEXT NOT NULL DEFAULT 'beginner',
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS quiz_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT UNIQUE NOT NULL,
                user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                language TEXT NOT NULL,
                question_order_json TEXT NOT NULL,
                option_orders_json TEXT NOT NULL,
                topic_ids_json TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT UNIQUE NOT NULL,
                created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS group_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(group_id, user_id)
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                topic_ids_json TEXT NOT NULL,
                difficulty TEXT,
                question_count INTEGER,
                time_limit_minutes INTEGER,
                max_attempts INTEGER,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS user_question_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
                seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                was_correct INTEGER
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS question_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
                template_key VARCHAR(100) UNIQUE,
                template_en TEXT,
                template_ru TEXT,
                variables_spec_json TEXT,
                answer_expression TEXT,
                difficulty VARCHAR(50),
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS user_topic_mastery (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
                difficulty VARCHAR(50),
                total_attempts INTEGER DEFAULT 0,
                correct_attempts INTEGER DEFAULT 0,
                mastery_score REAL DEFAULT 0.0,
                locked INTEGER DEFAULT 0,
                last_attempt_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, topic_id, difficulty)
            )
        """)
        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_mastery_lookup ON user_topic_mastery(user_id, topic_id, difficulty)
        """)
        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_question_history_lookup
            ON user_question_history(user_id, question_id, seen_at DESC)
        """)
