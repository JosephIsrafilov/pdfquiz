from app.models.grading import evaluate_display_answer, text_answer_matches


def test_text_answer_matches_is_case_insensitive_by_default():
    assert text_answer_matches("Paris", ["paris"])
    assert text_answer_matches("  paris  ", ["Paris"])


def test_text_answer_matches_collapses_whitespace():
    assert text_answer_matches("hello   world", ["hello world"])


def test_text_answer_matches_case_sensitive_mode():
    assert not text_answer_matches("Paris", ["paris"], case_sensitive=True)
    assert text_answer_matches("Paris", ["Paris"], case_sensitive=True)


def test_text_answer_matches_checks_all_variants():
    assert text_answer_matches("NYC", ["New York City", "NYC", "New York"])
    assert not text_answer_matches("Boston", ["New York City", "NYC"])


def test_text_answer_matches_empty_answer():
    assert not text_answer_matches("", ["anything"])
    assert not text_answer_matches(None, ["anything"])


def test_evaluate_display_answer_mcq():
    options = [{"text": "a", "is_correct": False}, {"text": "b", "is_correct": True}]
    assert evaluate_display_answer("mcq", options, 1)
    assert not evaluate_display_answer("mcq", options, 0)
    assert not evaluate_display_answer("mcq", options, None)


def test_evaluate_display_answer_multi_select():
    options = [
        {"text": "a", "is_correct": True},
        {"text": "b", "is_correct": False},
        {"text": "c", "is_correct": True},
    ]
    assert evaluate_display_answer("multi_select", options, [0, 2])
    assert not evaluate_display_answer("multi_select", options, [0])
    assert not evaluate_display_answer("multi_select", options, None)


def test_evaluate_display_answer_fill_in_the_blank_lenient():
    options = [{"text": "Paris", "is_correct": True}]
    assert evaluate_display_answer("fill_in_the_blank", options, "  paris ")
    assert not evaluate_display_answer("fill_in_the_blank", options, "London")


def test_evaluate_display_answer_code_output_case_sensitive():
    options = [{"text": "True", "is_correct": True}]
    assert evaluate_display_answer("code_output", options, "True")
    assert not evaluate_display_answer("code_output", options, "true")
