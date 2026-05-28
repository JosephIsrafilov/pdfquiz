import re
from typing import Dict, List, Optional, Tuple

QUESTION_PATTERNS = [
    re.compile(r"^\s*(\d{1,4})[\.\)\-]\s*(.*)$"),
    re.compile(r"^\s*(\d{1,4})\s+(.+)$"),
    re.compile(r"^\s*(\d{1,4})\s*$"),
    re.compile(
        r"^\s*(?:Вопрос|Question)\s*(\d{1,4})[\.:\-\)]?\s*(.*)$",
        re.IGNORECASE,
    ),
]

OPTION_PATTERN = re.compile(r"^\s*([A-ZА-Я]|\d{1,2})[\.\)\:\-]\s+(.*)$")
ANSWER_LINE_PATTERN = re.compile(
    r"^(?:Ответ|Answer|Correct(?: answer)?|Правильный ответ)\s*[:\-]\s*(.+)$",
    re.IGNORECASE,
)
QUESTION_SCORE_PATTERN = re.compile(r"^\(\s*\d+\s*т\s*\)\s*", re.IGNORECASE)

BULLET_CHARS = "•·∙‣◦◉○●▪▫■\uf0b7"
CHECK_CHARS = "✓✔√☑✅🗸"
OPTION_PREFIX_CHARS = BULLET_CHARS + CHECK_CHARS


def make_char_class(chars: str) -> str:
    return "".join(re.escape(ch) for ch in chars)


_MARKER_CLASS = make_char_class(OPTION_PREFIX_CHARS)
OPTION_BULLET_PATTERN = re.compile(rf"^\s*[{_MARKER_CLASS}]\s*(.+)$")
BULLET_SPLIT_PATTERN = re.compile(rf"(?=[{_MARKER_CLASS}])")


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u00a0", " ")).strip()


def strip_question_leading_noise(text: str) -> str:
    cleaned = normalize_space(text)
    previous = None
    while cleaned != previous:
        previous = cleaned
        if cleaned.startswith("+"):
            cleaned = normalize_space(cleaned[1:])
        cleaned = QUESTION_SCORE_PATTERN.sub("", cleaned)
        cleaned = normalize_space(cleaned)
    return cleaned


def strip_correct_markers(text: str) -> Tuple[str, bool]:
    cleaned = text.strip()
    is_correct = False

    if re.search(r"\((?:верно|правильно|correct)\)", cleaned, re.IGNORECASE):
        is_correct = True
        cleaned = re.sub(
            r"\((?:верно|правильно|correct)\)",
            "",
            cleaned,
            flags=re.IGNORECASE,
        ).strip()

    if re.search(r"\[\s*[xX]\s*\]", cleaned):
        is_correct = True
        cleaned = re.sub(r"\[\s*[xX]\s*\]", "", cleaned).strip()

    if cleaned.endswith("*"):
        is_correct = True
        cleaned = cleaned.rstrip("*").strip()

    if any(cleaned.endswith(ch) for ch in CHECK_CHARS):
        is_correct = True
        cleaned = cleaned.rstrip(CHECK_CHARS).strip()

    return cleaned, is_correct


def clean_option_text(text: str, pre_marked_correct: bool = False) -> Tuple[str, bool]:
    has_check = any(ch in text for ch in CHECK_CHARS)
    cleaned = text
    for ch in CHECK_CHARS:
        cleaned = cleaned.replace(ch, " ")
    for ch in BULLET_CHARS:
        cleaned = cleaned.replace(ch, " ")
    cleaned = normalize_space(cleaned)
    cleaned, marker_correct = strip_correct_markers(cleaned)
    return cleaned, has_check or marker_correct or pre_marked_correct


def first_marker_index(line: str) -> int:
    indices = [line.find(ch) for ch in OPTION_PREFIX_CHARS if line.find(ch) != -1]
    return min(indices) if indices else -1


def expand_bullet_lines(lines: List[str]) -> List[str]:
    expanded: List[str] = []
    marker_chars = OPTION_PREFIX_CHARS
    i = 0

    def ends_sentence(text: str) -> bool:
        return text.rstrip().endswith((".", ";", ":", "!", "?"))

    while i < len(lines):
        line = lines[i]
        if not line:
            i += 1
            continue

        stripped = line.strip()
        next_line = lines[i + 1] if i + 1 < len(lines) else ""
        next_stripped = next_line.strip()
        next_next_line = lines[i + 2] if i + 2 < len(lines) else ""
        next_next_stripped = next_next_line.strip()
        if (
            stripped
            and next_stripped
            and len(next_stripped) == 1
            and next_stripped in marker_chars
            and next_next_stripped
            and not ends_sentence(stripped)
        ):
            combined = f"{next_stripped} {stripped} {next_next_stripped}"
            line = combined
            i += 2
        else:
            next_match = (
                OPTION_BULLET_PATTERN.match(next_line.strip()) if next_line else None
            )
            if (
                not OPTION_BULLET_PATTERN.match(stripped)
                and next_match
                and stripped
                and not ends_sentence(stripped)
            ):
                marker = next_line.strip()[0]
                combined = f"{marker} {stripped} {next_match.group(1).strip()}"
                line = combined
                i += 1

        stripped = line.strip()
        if len(stripped) == 1 and stripped in marker_chars:
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                line = f"{stripped} {lines[j].lstrip()}"
                i = j
            else:
                i += 1
                continue

        marker_count = sum(line.count(ch) for ch in marker_chars)
        if marker_count >= 2:
            parts = [part.strip() for part in BULLET_SPLIT_PATTERN.split(line)]
            for part in parts:
                if part:
                    expanded.append(part)
        elif marker_count == 1 and not OPTION_BULLET_PATTERN.match(line):
            first_idx = first_marker_index(line)
            if first_idx > 0:
                before = line[:first_idx].rstrip()
                after = line[first_idx:].lstrip()
                if before:
                    expanded.append(before)
                if after:
                    expanded.append(after)
                continue
            expanded.append(line)
        else:
            expanded.append(line)
        i += 1
    return expanded


def leading_ws_count(line: str) -> int:
    return len(line) - len(line.lstrip(" \t\u00a0"))


def is_decimal_line(line: str) -> bool:
    if re.match(r"^\s*(\d{1,4})\.\1(?:[\.\)\-]|\s)", line):
        return False
    return bool(re.match(r"^\s*\d{1,4}\.\d", line))


def is_option_line(line: str) -> bool:
    return bool(OPTION_PATTERN.match(line) or OPTION_BULLET_PATTERN.match(line))


def is_answer_line(line: str) -> bool:
    return bool(ANSWER_LINE_PATTERN.match(line.strip()))


def is_page_marker_line(line: str) -> bool:
    return bool(re.match(r"^\s*\d+\s*/\s*\d+\s*$", line))


def match_question_line(
    line: str, min_indent: int, last_number: Optional[int]
) -> Optional[Tuple[int, str]]:
    cleaned_line = line
    stripped = line.strip()
    if stripped and stripped[0] in OPTION_PREFIX_CHARS:
        cleaned_line = stripped[1:].lstrip()
    cleaned_line = strip_question_leading_noise(cleaned_line)

    if is_decimal_line(cleaned_line):
        return None

    if leading_ws_count(line) > min_indent + 1:
        return None

    for pattern in QUESTION_PATTERNS:
        match = pattern.match(cleaned_line)
        if not match:
            continue

        number = int(match.group(1)) if match.group(1) else None
        if number is None:
            return None

        if last_number is not None:
            if number % 10 == 0 and number // 10 == last_number + 1:
                number = number // 10
            if number <= last_number:
                return None
            if number > last_number + 5:
                return None

        if match.lastindex and match.lastindex >= 2:
            rest = (match.group(2) or "").strip()
        else:
            rest = line[match.end() :].strip()

        duplicate_prefix = re.compile(rf"^{number}[\.\)\-]\s*")
        while duplicate_prefix.match(rest):
            rest = duplicate_prefix.sub("", rest, count=1).strip()
        rest = strip_question_leading_noise(rest)

        if rest and rest[0].isdigit() and len(rest) > 1 and rest[1].isdigit():
            return None

        return number, rest

    return None


def split_into_question_blocks(lines: List[str]) -> List[Dict]:
    blocks: List[Dict] = []
    current: Optional[Dict] = None
    last_number: Optional[int] = None

    non_empty_lines = [line for line in lines if line.strip()]
    if not non_empty_lines:
        return []
    min_indent = min(leading_ws_count(line) for line in non_empty_lines)

    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        match = match_question_line(line, min_indent, last_number)
        if match:
            number, rest = match
            if current and not rest:
                option_indices = [
                    idx for idx, value in enumerate(current["lines"]) if is_option_line(value)
                ]
                if option_indices:
                    last_option_idx = option_indices[-1]
                    trailing = current["lines"][last_option_idx + 1 :]
                    if trailing and all(
                        not is_option_line(value) and not is_answer_line(value)
                        for value in trailing
                    ):
                        if all(
                            leading_ws_count(value) <= min_indent + 1
                            for value in trailing
                        ):
                            current["lines"] = current["lines"][: last_option_idx + 1]
                            blocks.append(current)
                            current = {"number": number, "lines": trailing}
                            last_number = number
                            i += 1
                            continue
            if current:
                blocks.append(current)
            current = {"number": number, "lines": [rest] if rest else []}
            last_number = number
            i += 1
            continue

        if current:
            has_options = any(is_option_line(value) for value in current["lines"])
            if has_options and not is_option_line(line) and not is_answer_line(line):
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    next_match = match_question_line(lines[j], min_indent, last_number)
                    if next_match:
                        number, rest = next_match
                        blocks.append(current)
                        current = {"number": number, "lines": [line]}
                        if rest:
                            current["lines"].append(rest)
                        last_number = number
                        i = j + 1
                        continue
            current["lines"].append(line)
        i += 1

    if current:
        blocks.append(current)

    return blocks


def parse_question_block(block: Dict) -> Dict:
    question_lines: List[str] = []
    options: List[Dict] = []
    current_option: Optional[Dict] = None
    answer_hint: Optional[str] = None
    base_indent = None

    for raw_line in block["lines"]:
        line_clean = raw_line.strip()
        if not line_clean:
            continue
        if ANSWER_LINE_PATTERN.match(line_clean):
            continue
        if OPTION_PATTERN.match(raw_line) or OPTION_BULLET_PATTERN.match(raw_line):
            continue
        indent = leading_ws_count(raw_line)
        if base_indent is None or indent < base_indent:
            base_indent = indent

    if base_indent is None:
        base_indent = 0

    def option_looks_complete(text: str) -> bool:
        return text.rstrip().endswith((";", ".", ":", "!", "?"))

    def line_has_marker(text: str) -> bool:
        return any(ch in text for ch in OPTION_PREFIX_CHARS)

    def looks_like_definition_head(text: str) -> bool:
        lower = text.lower()
        return text.rstrip().endswith(":") or "это" in lower

    def looks_like_stem_boundary(text: str) -> bool:
        stripped = text.rstrip()
        lower_text = stripped.lower()
        has_question_word = any(
            lower_text.startswith(word) or f" {word} " in lower_text or lower_text.endswith(f" {word}")
            for word in ["какие", "какой", "какая", "что", "где", "как", "почему", "зачем", "кто", "укажите", "выберите", "назовите", "найдите"]
        )
        return (
            "?" in stripped
            or stripped.endswith(":")
            or stripped.endswith(("...", "…", "….", "…..", "."))
            or has_question_word
        )

    def split_bare_options(
        lines: List[str], existing_option_count: int = 0
    ) -> Optional[Tuple[List[str], List[str]]]:
        filtered = [
            normalize_space(value)
            for value in lines
            if normalize_space(value) and not is_page_marker_line(value)
        ]
        if len(filtered) < 3:
            return None

        best_index = None
        best_score = -1
        for idx in range(len(filtered) - 1):
            trailing_count = len(filtered) - idx - 1 + existing_option_count
            if trailing_count < 2:
                continue
                
            trailing = filtered[idx + 1 :]

            score = 0
            if looks_like_stem_boundary(filtered[idx]):
                score += 3
            if idx == 0 and len(filtered) - 1 >= 4:
                score += 1
                
            starts_upper = sum(1 for t in trailing if t and t[0].isupper())
            if starts_upper == len(trailing):
                score += 2
            elif starts_upper == 0:
                score += 1
                
            avg_len = sum(len(t) for t in trailing) / len(trailing)
            if avg_len < 60:
                score += 1

            if score > best_score:
                best_index = idx
                best_score = score

        if best_index is None or best_score < 1:
            return None

        return filtered[: best_index + 1], filtered[best_index + 1 :]

    def should_treat_as_question_intro(line: str, line_index: int) -> bool:
        opt_match = OPTION_PATTERN.match(line)
        if not opt_match:
            return False

        marker = opt_match.group(1)
        if not marker or len(marker) != 1:
            return False

        remaining = [
            value
            for value in block["lines"][line_index + 1 :]
            if value.strip() and not is_answer_line(value)
        ]
        if not remaining or any(is_option_line(value) for value in remaining):
            return False

        intro_text = opt_match.group(2).strip()
        if not intro_text:
            return False

        return intro_text[0].isupper()

    def should_ignore_single_letter_option_marker(line: str, line_index: int) -> bool:
        opt_match = OPTION_PATTERN.match(line)
        if not opt_match:
            return False

        marker = opt_match.group(1)
        if not marker or len(marker) != 1 or marker.isdigit():
            return False

        remaining = [
            value
            for value in block["lines"][line_index + 1 :]
            if value.strip()
            and not is_answer_line(value)
            and not is_page_marker_line(value)
        ]
        if not remaining or any(is_option_line(value) for value in remaining):
            return False

        text = opt_match.group(2).strip()
        return bool(text) and text[0].isupper()

    for line_index, raw_line in enumerate(block["lines"]):
        line = raw_line.rstrip()
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if is_page_marker_line(line_stripped):
            continue

        answer_match = ANSWER_LINE_PATTERN.match(line_stripped)
        if answer_match:
            answer_hint = answer_match.group(1).strip()
            continue

        opt_match = OPTION_PATTERN.match(line)
        bullet_match = None
        if not opt_match:
            bullet_match = OPTION_BULLET_PATTERN.match(line)
        elif not question_lines and not current_option and should_treat_as_question_intro(
            line, line_index
        ):
            opt_match = None
        elif not current_option and should_ignore_single_letter_option_marker(
            line, line_index
        ):
            opt_match = None

        if opt_match or bullet_match:
            if current_option:
                options.append(current_option)
            if opt_match:
                text = opt_match.group(2).strip()
                cleaned_text, is_correct = clean_option_text(text)
            else:
                prefix = line_stripped[0]
                text = bullet_match.group(1).strip()
                cleaned_text, is_correct = clean_option_text(text)
                if prefix in CHECK_CHARS:
                    is_correct = True
            if not cleaned_text:
                continue
            current_option = {
                "text": cleaned_text,
                "is_correct": is_correct,
            }
        else:
            if current_option:
                line_indent = leading_ws_count(line)
                if line_has_marker(line_stripped):
                    cleaned_text, is_correct = clean_option_text(line_stripped)
                    if cleaned_text:
                        options.append(current_option)
                        current_option = {
                            "text": cleaned_text,
                            "is_correct": is_correct,
                        }
                        continue
                if line_indent > base_indent + 1:
                    current_option["text"] = normalize_space(
                        f"{current_option['text']} {line_stripped}"
                    )
                elif option_looks_complete(current_option["text"]):
                    cleaned_text, is_correct = clean_option_text(line_stripped)
                    if cleaned_text:
                        options.append(current_option)
                        current_option = {
                            "text": cleaned_text,
                            "is_correct": is_correct,
                        }
                else:
                    current_option["text"] = normalize_space(
                        f"{current_option['text']} {line_stripped}"
                    )
            else:
                line_indent = leading_ws_count(line)
                if question_lines and (
                    line_indent > base_indent + 1 or line_has_marker(line_stripped)
                ):
                    cleaned_text, is_correct = clean_option_text(line_stripped)
                    if cleaned_text:
                        current_option = {
                            "text": cleaned_text,
                            "is_correct": is_correct,
                        }
                        continue
                question_lines.append(line_stripped)

    if current_option:
        options.append(current_option)

    split_result = None
    if len(options) <= 1:
        split_result = split_bare_options(question_lines, len(options))

    if split_result is not None:
        question_lines, trailing_options = split_result
        promoted_options = [
            {"text": value, "is_correct": False} for value in trailing_options
        ]
        if options:
            options = promoted_options + options
        else:
            options = promoted_options

    if len(question_lines) > 1 and options:
        head = question_lines[0]
        tail_text = normalize_space(" ".join(question_lines[1:]))
        if (
            looks_like_definition_head(head)
            and tail_text
            and len(tail_text) > 40
            and not tail_text.endswith("?")
        ):
            cleaned_text, is_correct = clean_option_text(tail_text)
            if cleaned_text:
                options.insert(
                    0,
                    {
                        "text": cleaned_text,
                        "is_correct": is_correct,
                    },
                )
                question_lines = [head]

    question_text = normalize_space(" ".join(question_lines))

    return {
        "number": block.get("number"),
        "text": question_text,
        "options": options,
        "answer_hint": answer_hint,
    }


def parse_questions(text: str) -> List[Dict]:
    raw_lines = [
        line.replace("\u00a0", " ").rstrip()
        for line in text.replace("\r", "\n").split("\n")
    ]
    raw_lines = [line for line in raw_lines if line.strip()]
    raw_lines = expand_bullet_lines(raw_lines)
    blocks = split_into_question_blocks(raw_lines)

    if not blocks:
        return []

    questions = []
    for block in blocks:
        parsed = parse_question_block(block)
        if parsed["text"]:
            questions.append(parsed)

    return questions
