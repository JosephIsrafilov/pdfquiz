# Knowledge Check

A bilingual English/Russian knowledge-check platform for IT courses.

Students select a course, choose the topics they have studied, configure the
question count and difficulty, and complete a randomized test. Questions are
balanced across the selected topics and graded on the server.

## Features

- English and Russian student interface
- Courses and topic-based question banks
- Balanced random tests across multiple topics
- Beginner, intermediate, and advanced difficulty levels
- Instant per-question checking or final submission
- Server-side answer keys and grading
- Explanations and topic-level score breakdowns
- Saved attempt history for registered students
- Teacher panel for courses, topics, questions, users, and imports
- PDF, DOCX, and JSON import into a selected topic
- Built-in Python curriculum with 40 topics and 140 bilingual questions
- Detailed teaching feedback after every checked answer

The foundation topic order follows the core language path in the
[W3Schools Python tutorial](https://www.w3schools.com/python/), reorganized
into progressive stages for younger learners. A separate deep-dive stage adds
mutability, comprehensions, built-ins, function design, advanced OOP,
dataclasses and typing, context managers, testing, algorithms, and async
programming. Questions and explanations are original project content.

The first application user becomes an administrator.

## Run locally

```bash
pip install -r requirements.txt
python main.py
```

Open `http://127.0.0.1:5000`.

SQLite is used by default. Set `DATABASE_URL` to use PostgreSQL.

## Teacher workflow

1. Open the teacher panel.
2. Create a course and its topics.
3. Add bilingual questions manually, including answer options, the correct
   answer, explanation, and difficulty.
4. Alternatively, import a PDF, DOCX, or JSON file into a selected topic and
   source language.
5. Translate imported questions through the question editor when required.
6. Disable a question to remove it from new tests without deleting it.

Imported questions without a valid answer key are skipped because they cannot
be graded safely.

## Import format

The legacy question JSON format remains supported:

```json
[
  {
    "text": "What does input() return?",
    "options": [
      {"text": "A string", "is_correct": true},
      {"text": "An integer", "is_correct": false}
    ],
    "answer_hint": "input() returns text as a string."
  }
]
```

Choose the destination topic and whether the file content is English or
Russian before importing it.

For large PDFs, prepare JSON locally:

```bash
python prepare_questions_json.py "path/to/file.pdf"
```

## Deployment

Render is configured to run the modular application:

```bash
gunicorn main:app --bind 0.0.0.0:$PORT --workers 1 --timeout 180
```
