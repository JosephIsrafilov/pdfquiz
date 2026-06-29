## Role & Goal

You are a senior backend engineer working on a bilingual (EN/RU) Flask knowledge-check
platform. The app uses an application factory (`create_app()` in `main.py`), SQLite by
default, PostgreSQL when `DATABASE_URL` is set. Questions are imported from PDF/DOCX/JSON.

Your job: fix security vulnerabilities, remove technical debt, and optimize the project
**without breaking anything**. Work one task at a time and run the full test suite after
every change before moving on.

---

## Project map

```
main.py                       # entry point: calls create_app()
app/__init__.py               # factory: CSRF, errorhandler, route registration, init_db
app/config.py                 # Config class (SECRET_KEY, DB settings, limits)
app/database.py               # DB layer: connection pool, get_db_connection,
                              #   db_query/db_execute placeholder translator, init_db
app/parsing.py                # upload dispatch: routes PDF/DOCX/JSON to correct parser
app/routes/{auth,main,admin,api}.py
app/models/{user,quiz,knowledge,result,room,group,document,
            mastery,question_history,template_engine}.py
app/curriculum/{python_core,python_deep,templates}.py
parsers/{common,pdf_parser,docx_parser}.py
templates/*.html
static/{app.js,styles.css,page-i18n.js}
tests/{conftest,test_routes,test_parsers}.py   # ~45 tests
web_app.py, refactor.py, prepare_*.py, apply_answers_*.py   # legacy / one-off scripts
Dockerfile, docker-compose.yml, docker-compose.prod.yml, render.yaml, nginx.conf
```

---

## HARD CONSTRAINTS — never violate these

1. **Keep all existing tests green.** Run `pytest -q` after every task. Do not move on
   until the suite passes.

2. **Keep dual SQLite + PostgreSQL support.** Use `db_execute(conn, query, params)`
   for every SQL statement. Never concatenate or f-string user-controlled values into
   SQL. The only exception is building an `IN (...)` placeholder list with `%s`
   (already done in `_load_quiz_rows` — follow that pattern).

3. **Keep server-side answer grading.** The `option_orders` stored in `quiz_sessions`
   must stay the single source of truth for correct answers. The client must never
   receive the correct-answer flag before submitting.

4. **Do not change the public API contract consumed by `static/app.js`:**
   `POST /api/quizzes`, `POST /api/quizzes/<token>/check`,
   `POST /api/quizzes/<token>/submit`, `POST /api/quizzes/room`.
   If you must change a response shape, update the frontend in the same commit.

5. **Preserve EN/RU bilingual support** in all user-facing text.

6. **Secure defaults:** new settings must be controlled by environment variables.
   Production mode must default to the safe setting; local development to the
   convenient one.

7. **Atomic commits with clear messages.** Maintain a `CHANGELOG_AGENT.md` file —
   append one entry per completed task describing what changed and why.

---

## Definition of Done

- `pytest -q` is green and the **total test count has grown** (every security fix and
  new feature must have at least one new test).
- The app starts cleanly on SQLite (`python main.py`) and in Docker Compose with
  PostgreSQL.
- `GET /health` returns `{"status":"ok","db":"connected"}` in both modes.
- No legacy duplicates or one-off scripts remain in the project root.
- `README.md` and `.env.example` accurately describe the real behaviour.

---

# TASKS BY PRIORITY

## P0 — Security & Data Integrity

### P0.1 — Lock down `/api/parse`
File: `app/routes/api.py`

- Add `@login_required` (or `@admin_required` — inspect `static/app.js` to confirm
  which user roles actually call this endpoint, then choose the least-permissive level).
- In the `document_id` branch: wrap `json.loads(document["questions_json"])` in
  try/except (malformed JSON → 400, not 500). **Add an ownership/admin check** so a
  logged-in user cannot enumerate other users' documents by guessing IDs (IDOR).
- Acceptance: unauthenticated request → 401/403; IDOR against another user's
  `document_id` → 403. Add tests for both cases.

### P0.2 — Remove score forgery via `/api/results`
Files: `app/routes/api.py`, `app/models/result.py`

- The endpoint currently accepts `correct`, `graded`, etc. from the client — these
  values are trivially forgeable. `static/app.js` does not call this endpoint at all.
  Choose one option and justify the choice in `CHANGELOG_AGENT.md`:
  (a) Delete the endpoint entirely, or
  (b) If it is needed for file-upload quiz flows, recompute the score on the server
      from the stored session data — never trust client-supplied numeric scores.
- Acceptance: it must be impossible to persist an arbitrary `correct` value. Add a
  test that proves this.

### P0.3 — Fail fast on weak `SECRET_KEY`
Files: `app/config.py`, `app/__init__.py`

- When `DEBUG` is off and `SECRET_KEY` is missing or equals the default string
  `"change-this-secret-key"`, the application must raise a clear error at startup —
  not silently run with a predictable key.
- In development mode a randomly-generated ephemeral key is acceptable; log a warning.
- Acceptance: starting without a proper `SECRET_KEY` in production mode raises an
  exception. Add a test.

### P0.4 — Harden session cookies
Files: `app/__init__.py` / `app/config.py`

- Set `SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SAMESITE = "Lax"`, and
  `SESSION_COOKIE_SECURE = True` when not in DEBUG mode (controlled by env var so
  local http development still works).
- Acceptance: values are present in `app.config`; a test asserts them.

### P0.5 — Security response headers
File: `app/__init__.py` (or a new `app/security.py`)

- Add via `after_request` (or Flask-Talisman if you add the dependency):
  `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`,
  `Referrer-Policy: same-origin`, and a reasonable `Content-Security-Policy`
  (the frontend loads `static/app.js` and `styles.css` from the same origin — allow
  that). Add `Strict-Transport-Security` only when not in DEBUG mode.
- Acceptance: headers are present on all responses; a test asserts the key ones.

### P0.6 — Rate limiting
New dependency: `Flask-Limiter` (add to requirements)

- Apply rate limits to `/login` and `/register` (brute-force protection) and to
  `/api/parse` (resource-abuse protection). Expose limits as environment variables
  with sensible defaults.
- Acceptance: exceeding the limit returns 429. Add a test for `/login`.

---

## P1 — Technical Debt & Code Cleanliness

### P1.1 — Delete legacy files
- Delete `web_app.py` — it is a 928-line copy of the entire old monolithic application.
  Production uses `main:app` → `create_app()`. Nothing should import it.
- Delete `refactor.py` — a one-off script that edited `web_app.py`. No longer needed.
- Verify no file imports either. Run tests.

### P1.2 — Remove duplicates and dead code
- `generate_csrf_token` and `validate_csrf` are defined in both `app/__init__.py` and
  `app/utils.py`. Keep a single source of truth in `app/utils.py`; import from there
  in the factory. Confirm the Jinja global `csrf_token` and the `before_request`
  CSRF check still work (add a test that a POST without the token returns 403).
- Remove the `add_ngrok_skip_header` `after_request` hook — it is a leftover from
  ngrok dev tunnelling and should not ship to production.
- Decide what to do with `_balanced_sample` in `app/models/quiz.py`. It is currently
  dead code (sampling goes through `get_weighted_question_sample`). Either delete it
  or actively use it and document why. Record the decision in `CHANGELOG_AGENT.md`.

### P1.3 — Clean up the project root
- Move `prepare_questions_json.py`, `prepare_marked_pdf_json.py`, and
  `apply_answers_from_marked_json.py` into a `scripts/` directory. Update any
  README references.

### P1.4 — Consistent line endings and editor config
- Normalize all files to LF (`web_app.py` and `render.yaml` currently contain CRLF).
- Add `.gitattributes` (`* text=auto eol=lf`) and `.editorconfig`.
- Add `.env.production` to `.gitignore` (it contains only placeholders, but it should
  not be tracked). Verify no real `.env` file is committed.

---

## P2 — Performance & Database

### P2.1 — Missing indexes on hot foreign keys
File: `app/database.py` (`init_db`, both the SQLite and PostgreSQL branches)

Add `CREATE INDEX IF NOT EXISTS` for:
- `questions(topic_id)`
- `questions(topic_id, is_active)`
- `topics(course_id)`
- `results(user_id)`
- `results(room_id)`
- `group_members(user_id)`
- `quiz_sessions(completed)`

Acceptance: indexes are created idempotently in both database engines; tests stay green.

### P2.2 — SQLite lock resilience
File: `app/database.py` (SQLite branch of `get_db_connection`)

- Enable `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=5000;` on every new
  SQLite connection. Use `check_same_thread=False` carefully (or manage connections
  per-request via Flask `g`). Do not break existing test behaviour.
- Acceptance: tests remain green; no regressions on concurrent access.

### P2.3 — Reconcile and parameterise worker count
- `render.yaml` uses `--workers 1`; `Dockerfile` uses `--workers 2`. Unify by reading
  `WEB_CONCURRENCY` and `GUNICORN_TIMEOUT` from environment variables with sensible
  defaults. For the Render free tier keep 1 worker but add `--threads` or explicitly
  document the constraint (heavy PDF import blocks the single worker).
- Acceptance: startup commands read from env; behaviour is documented in
  `DEPLOYMENT.md`.

### P2.4 — Race-safe startup & curriculum sync
Files: `app/__init__.py`, `app/database.py`, `app/models/knowledge.py`

- `synchronize_python_curriculum()` runs on every worker startup. With multiple
  workers on first deploy there is a potential race condition (no UNIQUE constraint on
  `courses.title_en`). Fix with one of: a UNIQUE constraint + idempotent upsert,
  a PostgreSQL advisory lock, or moving curriculum sync to a CLI command / Render
  release step rather than every import. Choose the cleanest approach.
- Acceptance: repeated or concurrent calls do not create duplicate courses. The
  existing `test_python_curriculum_sync_is_idempotent` test stays green; add a new
  test that calls sync twice and asserts exactly one course exists.

---

## P3 — Reliability, Dependencies & Process

### P3.1 — Pin dependencies
- Pin all versions in `requirements.txt` (use `==`).
- Move `pytest` and `pytest-flask` (and any other test-only packages) to a separate
  `requirements-dev.txt`. The production Docker image must not install test
  dependencies.
- Update `Dockerfile` to install only `requirements.txt`.

### P3.2 — Replace silent migration swallowing
File: `app/database.py`

- The `ALTER TABLE ... except Exception: rollback` blocks silently swallow all errors.
  At minimum, log unexpected failures (distinguish "column already exists" from a real
  error). Ideally, introduce a simple migration tracker (a `schema_migrations` table
  or numbered `.sql` files) so applied migrations are not re-run.

### P3.3 — Proper exception logging
- Audit all broad `except Exception:` blocks in `app/routes/admin.py` and
  `app/models/*`. Add `app.logger.exception(...)` (or the module logger equivalent)
  so errors are not silently lost. The user still sees a friendly message; the server
  log contains the full traceback.

### P3.4 — Local `.env` loading
- Add optional `.env` loading in development via `python-dotenv` (do not fail if the
  file is absent). Production relies on real environment variables injected by the
  platform.

### P3.5 — CI pipeline
- Add `.github/workflows/ci.yml` that installs dependencies and runs `pytest` on every
  push and pull request (SQLite mode at minimum). Bonus: a second job that spins up a
  PostgreSQL service container and runs the full suite against it.

### P3.6 — Tests for new behaviour
Add tests for:
- `/api/parse` returns 401/403 for unauthenticated requests and 403 for IDOR attempts.
- `/api/results` (or its replacement) cannot accept a client-supplied score.
- Security headers and cookie flags are present on responses.
- Rate limit on `/login` triggers 429.
- Curriculum sync called twice produces exactly one course (no duplicates).

Bonus: expand the DOCX parser tests — the parser is hand-written XML and is brittle.
Cover tables, numbered lists, and mixed EN/RU content.

### P3.7 — Documentation
Update `README.md` and `DEPLOYMENT.md` to reflect:
- All supported environment variables and their defaults.
- How each import format works (PDF via pdfplumber, DOCX via hand-written XML
  parsing — no python-docx, JSON legacy format).
- How to run the app locally, in Docker, and on Render.
- The single-worker limitation and its effect on concurrent PDF uploads.
- How to run the test suite.

---

## Execution order

Work strictly in priority order: **P0 → P1 → P2 → P3**. Within a priority, work in
the listed order. After each task: run `pytest -q`, make an atomic commit, and append
an entry to `CHANGELOG_AGENT.md`.

When a task has a decision fork (e.g. delete or rewrite `/api/results`), choose the
better option, record the rationale in `CHANGELOG_AGENT.md`, and keep moving — do not
pause to ask.

When all tasks are done, print a final summary: tasks completed, files changed, test
count before and after.
