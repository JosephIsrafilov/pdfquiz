import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pdfplumber

from web_app import (
    match_question_line,
    normalize_space,
    parse_question_block,
)


MARKER_LINES = {"•", "∙", "·", "●", "◦", "✓", "✔", "√"}


def normalize_for_match(text: str) -> str:
    text = (
        text.lower()
        .replace("ё", "е")
        .replace("\u00ad", "")
        .replace("–", "-")
        .replace("—", "-")
    )
    text = re.sub(r"[^0-9a-zа-я]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def is_noise_line(line: str) -> bool:
    if re.match(r"^\d{1,2}/\d{1,3}$", line):
        return True
    if re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", line):
        return True
    prefixes = (
        "Fənn",
        "Fәnn",
        "BAXI",
        "AXI",
        "TEST",
        "Test ",
        "T :",
        "EST ",
        "Müəllif",
        "Müәllif",
        "Təsviri",
        "Tәsviri",
        "BÖLMƏ",
        "BÖLMӘ",
        "Ad ",
        "Suallardan",
        "Maksimal faiz",
        "Sualları",
        "Suallar ",
        "Suala vaxt",
        "Növ",
        "N\xf6v",
        "Keçid",
        "Ke\xe7id",
        "Köçürməyə",
        "K\xf6\xe7\xfcrm",
        "Ancaq",
        "Son variant",
    )
    return line.startswith(prefixes)


def extract_pdf_lines(path: Path) -> List[str]:
    lines: List[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
            for raw_line in text.replace("\r", "\n").split("\n"):
                line = normalize_space(raw_line)
                if line and not is_noise_line(line):
                    lines.append(line)
    return lines


def split_numbered_blocks(lines: List[str]) -> List[Dict]:
    blocks: List[Dict] = []
    current: Optional[Dict] = None
    last_number: Optional[int] = None

    for line in lines:
        match = match_question_line(line, 0, last_number)
        if match:
            number, rest = match
            if current:
                blocks.append(current)
            current = {"number": number, "lines": [rest] if rest else []}
            last_number = number
            continue

        if current:
            current["lines"].append(line)

    if current:
        blocks.append(current)

    return blocks


def strip_answer_markers(lines: List[str]) -> Tuple[List[str], List[str]]:
    stripped_lines: List[str] = []
    correct_hints: List[str] = []

    for index, line in enumerate(lines):
        if line.strip() not in MARKER_LINES:
            stripped_lines.append(line)
            continue

        for next_line in lines[index + 1 :]:
            cleaned = normalize_space(next_line)
            if cleaned and cleaned not in MARKER_LINES and not is_noise_line(cleaned):
                correct_hints.append(cleaned)
                break

    return stripped_lines, correct_hints


def mark_correct_options(question: Dict, correct_hints: List[str]) -> None:
    for option in question.get("options", []):
        option["is_correct"] = False

    for hint in correct_hints:
        hint_norm = normalize_for_match(hint)
        if not hint_norm:
            continue

        best_index = None
        best_score = 0
        for index, option in enumerate(question.get("options", [])):
            option_norm = normalize_for_match(option.get("text", ""))
            if not option_norm:
                continue
            if option_norm.startswith(hint_norm) or hint_norm.startswith(option_norm):
                score = 1000 + min(len(option_norm), len(hint_norm))
            elif hint_norm in option_norm or option_norm in hint_norm:
                score = 500 + min(len(option_norm), len(hint_norm))
            else:
                score = 0
            if score > best_score:
                best_index = index
                best_score = score

        if best_index is not None and best_score >= 500:
            question["options"][best_index]["is_correct"] = True


def parse_block_by_last_options(
    block: Dict, stripped_lines: List[str], correct_hints: List[str]
) -> Optional[Dict]:
    cleaned_lines = [
        normalize_space(line)
        for line in stripped_lines
        if normalize_space(line) and not is_noise_line(normalize_space(line))
    ]
    if len(cleaned_lines) < 6:
        return None

    option_start = len(cleaned_lines) - 5
    question_lines = cleaned_lines[:option_start]
    option_lines = cleaned_lines[option_start:]
    if not question_lines or len(option_lines) < 2:
        return None

    question = {
        "number": block["number"],
        "text": normalize_space(" ".join(question_lines)),
        "options": [
            {"text": normalize_space(option), "is_correct": False}
            for option in option_lines
        ],
        "answer_hint": None,
    }
    mark_correct_options(question, correct_hints)
    if not any(option.get("is_correct") for option in question["options"]):
        return None
    return question


def parse_marked_pdf(path: Path) -> List[Dict]:
    blocks = split_numbered_blocks(extract_pdf_lines(path))
    questions: List[Dict] = []

    for block in blocks:
        stripped_lines, correct_hints = strip_answer_markers(block["lines"])
        if not correct_hints:
            continue

        parsed = parse_question_block(
            {"number": block["number"], "lines": stripped_lines}
        )
        if not parsed.get("text") or len(parsed.get("options", [])) < 2:
            fallback = parse_block_by_last_options(block, stripped_lines, correct_hints)
            if fallback is not None:
                questions.append(fallback)
            continue

        mark_correct_options(parsed, correct_hints)
        if not any(option.get("is_correct") for option in parsed.get("options", [])):
            fallback = parse_block_by_last_options(block, stripped_lines, correct_hints)
            if fallback is not None:
                parsed = fallback
        questions.append(parsed)

    return questions


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python prepare_marked_pdf_json.py <marked.pdf> [output.json]")
        return 1

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"File not found: {input_path}")
        return 1

    output_path = (
        Path(sys.argv[2])
        if len(sys.argv) >= 3
        else input_path.with_suffix(".questions.json")
    )

    questions = parse_marked_pdf(input_path)
    if not questions:
        print("No marked questions were parsed.")
        return 1

    missing_answers = [
        question["number"]
        for question in questions
        if not any(option.get("is_correct") for option in question.get("options", []))
    ]
    if missing_answers:
        print(
            "Warning: no correct option matched for questions: "
            + ", ".join(map(str, missing_answers[:30]))
        )

    output_path.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Saved {len(questions)} questions to {output_path}")
    print(
        "Marked answers: "
        f"{sum(any(option.get('is_correct') for option in question.get('options', [])) for question in questions)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
