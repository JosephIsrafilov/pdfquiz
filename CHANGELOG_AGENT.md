# Changelog
- P0.1: Locked down `/api/parse` by adding `@login_required` decorator, handling invalid JSON safely to avoid 500 errors, adding a document ownership/admin check to prevent IDOR, and updating related tests.
