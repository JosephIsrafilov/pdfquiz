import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


def normalize(text: str) -> str:
    text = (
        str(text)
        .lower()
        .replace("ё", "е")
        .replace("\u00ad", "")
        .replace("–", "-")
        .replace("—", "-")
    )
    text = re.sub(r"[^0-9a-zа-я]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokens(text: str) -> Set[str]:
    return {token for token in normalize(text).split() if len(token) > 2}


def overlap_score(left: str, right: str) -> float:
    left_tokens = tokens(left)
    right_tokens = tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    intersection = len(left_tokens & right_tokens)
    return intersection / max(len(left_tokens), len(right_tokens))


def option_matches(left: str, right: str) -> bool:
    left_norm = normalize(left)
    right_norm = normalize(right)
    if not left_norm or not right_norm:
        return False
    if left_norm == right_norm:
        return True
    if left_norm in right_norm or right_norm in left_norm:
        ratio = min(len(left_norm), len(right_norm)) / max(len(left_norm), len(right_norm))
        return ratio >= 0.70
    return overlap_score(left_norm, right_norm) >= 0.86


def find_best_key_question(target_question: Dict, key_questions: List[Dict]) -> Optional[Dict]:
    target_text = target_question.get("text", "")
    best: Optional[Tuple[float, Dict]] = None

    for key_question in key_questions:
        score = overlap_score(target_text, key_question.get("text", ""))
        if score < 0.86:
            continue
        if best is None or score > best[0]:
            best = (score, key_question)

    return best[1] if best is not None else None


def apply_answer(target_question: Dict, key_question: Dict) -> bool:
    correct_options = [
        option
        for option in key_question.get("options", [])
        if option.get("is_correct")
    ]
    if len(correct_options) != 1:
        return False

    correct_text = correct_options[0].get("text", "")
    matched_indexes = [
        index
        for index, option in enumerate(target_question.get("options", []))
        if option_matches(option.get("text", ""), correct_text)
    ]
    if len(matched_indexes) != 1:
        return False

    for option in target_question.get("options", []):
        option["is_correct"] = False
    target_question["options"][matched_indexes[0]]["is_correct"] = True
    return True


def main() -> int:
    if len(sys.argv) < 4:
        print(
            "Usage: python apply_answers_from_marked_json.py "
            "<target.json> <output.json> <marked-key.json> [more-key.json ...]"
        )
        return 1

    target_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    key_paths = [Path(value) for value in sys.argv[3:]]

    target_questions = json.loads(target_path.read_text(encoding="utf-8"))
    key_questions: List[Dict] = []
    for key_path in key_paths:
        key_questions.extend(json.loads(key_path.read_text(encoding="utf-8")))

    matched_numbers: List[int] = []
    unmatched_numbers: List[int] = []

    for question in target_questions:
        for option in question.get("options", []):
            option["is_correct"] = False

        key_question = find_best_key_question(question, key_questions)
        if key_question is not None and apply_answer(question, key_question):
            matched_numbers.append(question.get("number"))
        else:
            unmatched_numbers.append(question.get("number"))

    output_path.write_text(
        json.dumps(target_questions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Saved {len(target_questions)} questions to {output_path}")
    print(f"Marked answers: {len(matched_numbers)}")
    print(f"Unmarked questions: {len(unmatched_numbers)}")
    if unmatched_numbers:
        print(
            "First unmarked: "
            + ", ".join(str(number) for number in unmatched_numbers[:60])
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
