import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pdfplumber

from parsers.common import (
    match_question_line,
    normalize_space,
    parse_question_block,
)


MARKER_LINES = {"•", "∙", "·", "●", "◦", "✓", "✔", "√"}
CORRECT_CHARS = "✓✔√"
BULLET_CHARS = "•∙·●◦"
_CORRECT_RE = re.compile(r"^[" + re.escape(CORRECT_CHARS) + r"]\s*")
_BULLET_RE = re.compile(r"^[" + re.escape(BULLET_CHARS) + r"]\s*")
_ANY_MARKER_RE = re.compile(r"^[" + re.escape(CORRECT_CHARS + BULLET_CHARS) + r"]\s*")


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
        # Pass None for last_number to bypass the +5 gap limit; enforce only forward-ordering here
        match = match_question_line(line, 0, None)
        if match and (last_number is None or match[0] > last_number):
            number, rest = match

            # When the number sits on its own line (rest is empty), the question stem
            # may have started on the previous line(s), which got appended to the
            # previous block after its options. Move those trailing non-marker lines
            # to the new block so the stem stays intact.
            moved: List[str] = []
            if current and not rest:
                if any(_ANY_MARKER_RE.match(l) for l in current["lines"]):
                    while current["lines"] and not _ANY_MARKER_RE.match(
                        current["lines"][-1]
                    ):
                        moved.insert(0, current["lines"].pop())

            if current:
                blocks.append(current)
            current = {"number": number, "lines": moved}
            if rest:
                current["lines"].append(rest)
            last_number = number
            continue

        if current:
            current["lines"].append(line)

    if current:
        blocks.append(current)

    return blocks


def parse_marked_block(block: Dict) -> Optional[Dict]:
    """Parse a block whose options are each prefixed by a marker.

    `√ ✓ ✔` marks the correct option; `• ∙ · ● ◦` marks distractors. Lines
    before the first marker form the question stem.

    pdfplumber sometimes places the marker glyph on its own line, splitting an
    option's text across the line(s) before and after it. We buffer unmarked
    lines as `pending` and resolve them when the next marker arrives:
      - inline marker (text on the marker line): pending lines were a wrapped
        continuation of the previous option;
      - standalone marker (no text): the last pending line is part-A of THIS
        option; any earlier pending lines continue the previous option.
    Trailing pending lines continue the final option.
    """
    lines = [normalize_space(l) for l in block["lines"]]
    lines = [l for l in lines if l and not is_noise_line(l)]

    question_lines: List[str] = []
    options: List[Dict] = []
    pending: List[str] = []
    seen_marker = False

    def extend_last(parts: List[str]) -> None:
        if options and parts:
            options[-1]["text"] = normalize_space(
                " ".join([options[-1]["text"], *parts]).strip()
            )

    for line in lines:
        correct_m = _CORRECT_RE.match(line)
        bullet_m = _BULLET_RE.match(line)
        if correct_m or bullet_m:
            marker = correct_m or bullet_m
            own_text = normalize_space(line[marker.end():])
            if own_text:
                # inline marker: pending was a continuation of the previous option
                extend_last(pending)
                options.append({"text": own_text, "is_correct": bool(correct_m)})
            else:
                # standalone marker: last pending line is this option's part-A
                part_a = ""
                if pending:
                    part_a = pending[-1]
                    extend_last(pending[:-1])
                elif not seen_marker and len(question_lines) > 1:
                    # first option's part-A landed in the question buffer
                    part_a = question_lines.pop()
                options.append({"text": part_a, "is_correct": bool(correct_m)})
            pending = []
            seen_marker = True
        elif not seen_marker:
            question_lines.append(line)
        else:
            pending.append(line)

    extend_last(pending)

    options = [opt for opt in options if opt["text"]]
    if len(options) < 2 or not question_lines:
        return None

    return {
        "number": block["number"],
        "text": normalize_space(" ".join(question_lines)),
        "options": options,
        "answer_hint": None,
    }


def strip_answer_markers(lines: List[str]) -> Tuple[List[str], List[str]]:
    stripped_lines: List[str] = []
    correct_hints: List[str] = []

    for index, line in enumerate(lines):
        stripped = line.strip()

        # Standalone marker line
        if stripped in MARKER_LINES:
            for next_line in lines[index + 1 :]:
                cleaned = normalize_space(next_line)
                # Strip inline marker from the next line too
                cleaned = _INLINE_MARKER_RE.sub("", cleaned).strip()
                if cleaned and cleaned not in MARKER_LINES and not is_noise_line(cleaned):
                    correct_hints.append(cleaned)
                    break
            continue

        # Inline marker at start of line (e.g. "√ Some answer text")
        inline_match = _INLINE_MARKER_RE.match(stripped)
        if inline_match:
            clean_text = normalize_space(stripped[inline_match.end():])
            if clean_text and not is_noise_line(clean_text):
                correct_hints.append(clean_text)
                stripped_lines.append(clean_text)
            continue

        stripped_lines.append(line)

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
    unmatched: List[int] = []

    for block in blocks:
        parsed = parse_marked_block(block)
        if parsed is None:
            unmatched.append(block["number"])
            continue
        if not any(opt["is_correct"] for opt in parsed["options"]):
            unmatched.append(block["number"])
        questions.append(parsed)

    if unmatched:
        preview = ", ".join(str(n) for n in unmatched[:20])
        more = "" if len(unmatched) <= 20 else f" (+{len(unmatched) - 20} more)"
        print(f"Warning: no correct option matched for questions: {preview}{more}")

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
