# Changelog
- P0.1: Locked down `/api/parse` by adding `@login_required` decorator, handling invalid JSON safely to avoid 500 errors, adding a document ownership/admin check to prevent IDOR, and updating related tests.
- P0.2: Deleted the /api/results endpoint because it accepted client-supplied unverified scores (score forgery), and was unused since static/app.js submits via another secure endpoint. Test added to ensure it returns 404.
- P0.3: Enforced strong SECRET_KEY at app startup. App raises RuntimeError in production if SECRET_KEY is weak or missing, preventing silent vulnerabilities.
- P0.4: Set SESSION_COOKIE_HTTPONLY, SAMESITE, and SECURE flags in config to protect session cookies from XSS and CSRF.
- P0.5: Added security headers (nosniff, X-Frame-Options DENY, CSP, and HSTS in production). Removed leftover ngrok dev header.
