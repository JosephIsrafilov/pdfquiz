"""
Unit tests for parsers.common, parsers.pdf_parser, parsers.docx_parser.
"""

import pytest
from parsers.common import normalize_space, parse_questions


# ---------------------------------------------------------------------------
# normalize_space
# ---------------------------------------------------------------------------


def test_normalize_space_basic():
    assert normalize_space("  hello   world  ") == "hello world"


def test_normalize_space_nbsp():
    assert normalize_space("hello\u00a0world") == "hello world"


def test_normalize_space_empty():
    assert normalize_space("") == ""


def test_normalize_space_tabs():
    assert normalize_space("a\t\tb") == "a b"


# ---------------------------------------------------------------------------
# parse_questions — basic numbered list
# ---------------------------------------------------------------------------


SIMPLE_QUIZ = """
1. What is 2+2?
A) 1
B) 4
C) 3

2. What is the capital of France?
A) Berlin
B) Madrid
C) Paris
"""


def test_parse_questions_count():
    questions = parse_questions(SIMPLE_QUIZ)
    assert len(questions) == 2


def test_parse_questions_text():
    questions = parse_questions(SIMPLE_QUIZ)
    assert "2+2" in questions[0]["text"]
    assert "France" in questions[1]["text"]


def test_parse_questions_options_count():
    questions = parse_questions(SIMPLE_QUIZ)
    # Each question should have at least 2 options
    for q in questions:
        assert len(q["options"]) >= 2


def test_parse_questions_numbers():
    questions = parse_questions(SIMPLE_QUIZ)
    assert questions[0]["number"] == 1
    assert questions[1]["number"] == 2


# ---------------------------------------------------------------------------
# parse_questions — bullet-marked correct answers
# ---------------------------------------------------------------------------


MARKED_QUIZ = """
1. Which planet is closest to the sun?
A) Earth
B) Mercury *
C) Venus

2. Who wrote Romeo and Juliet?
A) Dickens
B) Shakespeare ✓
C) Tolstoy
"""


def test_parse_questions_marked_correct_star():
    questions = parse_questions(MARKED_QUIZ)
    q = questions[0]
    correct = [opt for opt in q["options"] if opt["is_correct"]]
    assert len(correct) >= 1
    assert "Mercury" in correct[0]["text"]


def test_parse_questions_marked_correct_check():
    questions = parse_questions(MARKED_QUIZ)
    q = questions[1]
    correct = [opt for opt in q["options"] if opt["is_correct"]]
    assert len(correct) >= 1
    assert "Shakespeare" in correct[0]["text"]


# ---------------------------------------------------------------------------
# parse_questions — edge cases
# ---------------------------------------------------------------------------


def test_parse_questions_empty_string():
    questions = parse_questions("")
    assert questions == []


def test_parse_questions_no_options():
    text = "1. Just a question with no options"
    questions = parse_questions(text)
    # Should return either empty or questions without valid option structure
    for q in questions:
        # Every returned question must have text
        assert q["text"]


def test_parse_questions_single_question():
    text = """
1. Single question?
A) Option one
B) Option two
"""
    questions = parse_questions(text)
    assert len(questions) == 1
    assert len(questions[0]["options"]) == 2


# ---------------------------------------------------------------------------
# parse_questions — Russian text
# ---------------------------------------------------------------------------


RUSSIAN_QUIZ = """
1. Столица России?
А) Москва
Б) Санкт-Петербург
В) Казань

2. Сколько дней в неделе?
А) 5
Б) 6
В) 7
"""


def test_parse_russian_quiz_count():
    questions = parse_questions(RUSSIAN_QUIZ)
    assert len(questions) >= 1


def test_parse_russian_quiz_text():
    questions = parse_questions(RUSSIAN_QUIZ)
    texts = [q["text"] for q in questions]
    assert any("Россия" in t or "Столица" in t for t in texts)


# ---------------------------------------------------------------------------
# parse_questions — dot-separated numbering
# ---------------------------------------------------------------------------


def test_parse_questions_dot_numbering():
    text = """
1. Question one
A. Option A
B. Option B

2. Question two
A. Option A
B. Option B
"""
    questions = parse_questions(text)
    assert len(questions) == 2


# ---------------------------------------------------------------------------
# normalize_imported_questions (from app.parsing)
# ---------------------------------------------------------------------------


def test_normalize_imported_questions_valid():
    from app.parsing import normalize_imported_questions

    raw = [
        {
            "text": "What is 1+1?",
            "options": [
                {"text": "1", "is_correct": False},
                {"text": "2", "is_correct": True},
            ],
        }
    ]
    result = normalize_imported_questions(raw)
    assert len(result) == 1
    assert result[0]["text"] == "What is 1+1?"
    assert result[0]["options"][1]["is_correct"] is True


def test_normalize_imported_questions_not_list():
    from app.parsing import normalize_imported_questions

    with pytest.raises(ValueError, match="массив"):
        normalize_imported_questions({"not": "a list"})


def test_normalize_imported_questions_empty_text():
    from app.parsing import normalize_imported_questions

    with pytest.raises(ValueError):
        normalize_imported_questions([
            {
                "text": "",
                "options": [{"text": "A"}, {"text": "B"}],
            }
        ])


def test_normalize_imported_questions_too_few_options():
    from app.parsing import normalize_imported_questions

    with pytest.raises(ValueError):
        normalize_imported_questions([
            {
                "text": "Valid question",
                "options": [{"text": "only one"}],
            }
        ])


# ---------------------------------------------------------------------------
# DOCX parser helpers (unit-level, no real DOCX needed)
# ---------------------------------------------------------------------------


def test_docx_parser_empty_paragraphs():
    from parsers.docx_parser import parse_docx_questions

    result = parse_docx_questions([])
    assert result == []


def test_docx_parser_no_options():
    """Paragraphs with only question text and no bullet options produce no questions."""
    from parsers.docx_parser import parse_docx_questions

    paragraphs = [
        {
            "text": "1. A question with no options",
            "is_bullet": False,
            "is_numbered": True,
            "num_fmt": "decimal",
            "lvl_text": "%1.",
            "level": "0",
            "num_id": "1",
            "abstract_id": "0",
            "list_number": 1,
            "marked_correct": False,
        }
    ]
    result = parse_docx_questions(paragraphs)
    # Without options, the question should not be included
    assert result == []


def test_docx_parser_with_options():
    from parsers.docx_parser import parse_docx_questions

    def make_para(text, is_bullet=False, is_numbered=False, num=None):
        return {
            "text": text,
            "is_bullet": is_bullet,
            "is_numbered": is_numbered,
            "num_fmt": "bullet" if is_bullet else ("decimal" if is_numbered else None),
            "lvl_text": "•" if is_bullet else ("%1." if is_numbered else None),
            "level": "1" if is_bullet else "0",
            "num_id": "1",
            "abstract_id": "0",
            "list_number": num,
            "marked_correct": False,
        }

    paragraphs = [
        make_para("1. What is the capital of France?", is_numbered=True, num=1),
        make_para("Paris", is_bullet=True),
        make_para("London", is_bullet=True),
        make_para("Berlin", is_bullet=True),
    ]
    result = parse_docx_questions(paragraphs)
    assert len(result) == 1
    assert len(result[0]["options"]) == 3
