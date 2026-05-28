# Wispbyte deploy

This project is intended to run as a web version on Wispbyte with Supabase
Postgres as the database.

## Recommended setup

1. Create a Python server in Wispbyte.
2. Upload all tracked project files.
3. Create a Supabase project.
4. Copy the Supabase Postgres session pooler connection string.
5. Set these Wispbyte environment variables:

```env
SECRET_KEY=replace-with-a-long-random-secret
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DATABASE
```

6. Use this startup command:

```bash
pip install -r requirements.txt && python main.py
```

The app creates the required tables on first startup.

## Alternative startup command

If the panel allows custom startup commands and exposes `PORT`, Gunicorn can be
used instead:

```bash
pip install -r requirements.txt && gunicorn web_app:app --bind 0.0.0.0:${PORT:-${SERVER_PORT:-5000}} --workers 1 --timeout 180
```

## Move data from Render to Supabase

Use a Postgres dump/restore from Render Postgres into Supabase, or copy the data
through a temporary migration script if needed.

## Important notes

- This project is web-first.
- Do not rely on Wispbyte local files for production data.
- Keep `app.db` out of git because it can contain local test user data.
