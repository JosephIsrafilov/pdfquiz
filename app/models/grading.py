def normalize_text_answer(text, case_sensitive: bool = False) -> str:
    """Collapse whitespace runs and optionally casefold for lenient text comparison."""
    normalized = " ".join(str(text).split())
    return normalized if case_sensitive else normalized.casefold()


def text_answer_matches(user_answer, accepted_answers, case_sensitive: bool = False) -> bool:
    """Compare a free-text answer against one or more accepted answers.

    Used by both live quiz grading (quiz.py) and room analytics replay (room.py)
    so fill_in_the_blank/code_output correctness rules never drift between the two.
    """
    if not user_answer:
        return False
    normalized_user = normalize_text_answer(user_answer, case_sensitive)
    return any(
        normalized_user == normalize_text_answer(candidate, case_sensitive)
        for candidate in accepted_answers
        if candidate
    )


def evaluate_display_answer(question_type: str, options: list, selected) -> bool:
    """Correctness check for options already in the display order the student saw.

    Room analytics (room.py) replays stored attempt_json, which embeds options
    with an `is_correct` flag directly rather than the original/display index
    split that live grading (quiz.py's _assess_question) works with. This keeps
    both call sites using one definition of "correct" per question type.
    """
    correct_indices = {index for index, option in enumerate(options) if option.get("is_correct")}

    if question_type == "multi_select":
        if selected is None:
            return False
        try:
            selected_indices = {int(i) for i in selected}
        except (TypeError, ValueError):
            return False
        return selected_indices == correct_indices

    if question_type in ("fill_in_the_blank", "code_output"):
        accepted_answers = [option.get("text", "") for option in options if option.get("is_correct")]
        return text_answer_matches(selected, accepted_answers, case_sensitive=question_type == "code_output")

    if selected is None:
        return False
    try:
        selected_index = int(selected)
    except (TypeError, ValueError):
        return False
    if not (0 <= selected_index < len(options)):
        return False
    return options[selected_index].get("is_correct", False)
