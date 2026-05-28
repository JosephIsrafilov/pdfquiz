import io
from typing import Dict, List, Optional
import pdfplumber

from .common import (
    is_page_marker_line,
    match_question_line,
    normalize_space,
    parse_questions,
)


def is_pdf_header_line(text: str) -> bool:
    stripped = text.strip()
    return (
        stripped.startswith("www.")
        or stripped.startswith("Bu f")
        or "Yekun imtahan" in stripped
        or stripped == "00830 Sosiologiya"
    )


def extract_pdf_line_groups(page, page_number: int) -> List[Dict]:
    words = page.extract_words(
        x_tolerance=2,
        y_tolerance=2,
        keep_blank_chars=False,
        extra_attrs=["fontname"],
    )
    lines: List[Dict] = []

    for word in words:
        for line in lines:
            if abs(line["top"] - word["top"]) < 3:
                line["words"].append(word)
                line["top"] = min(line["top"], word["top"])
                line["bottom"] = max(line["bottom"], word["bottom"])
                break
        else:
            lines.append(
                {
                    "page": page_number,
                    "top": word["top"],
                    "bottom": word["bottom"],
                    "words": [word],
                }
            )

    grouped_lines: List[Dict] = []
    for line in lines:
        sorted_words = sorted(line["words"], key=lambda value: value["x0"])
        text = normalize_space(" ".join(word["text"] for word in sorted_words))
        if not text or is_pdf_header_line(text):
            continue
            
        # Detect bold: if any word in the line has "bold" in its fontname (and isn't just a marker like "A)")
        is_bold = False
        for word in sorted_words:
            if word["text"].strip() and not word["text"].strip() in ["A)", "B)", "C)", "D)", "E)"]:
                fontname = word.get("fontname", "").lower()
                if "bold" in fontname or "black" in fontname or "heavy" in fontname:
                    is_bold = True
                    break

        grouped_lines.append(
            {
                "page": page_number,
                "top": line["top"],
                "bottom": line["bottom"],
                "x0": sorted_words[0]["x0"],
                "x1": sorted_words[-1]["x1"],
                "text": text,
                "is_bold": is_bold,
            }
        )

    return sorted(grouped_lines, key=lambda line: line["top"])


def extract_pdf_radio_rows(page, page_number: int, lines: List[Dict]) -> List[Dict]:
    outer_circles = []
    selected_dots = []

    for curve in page.objects.get("curve", []):
        x0 = curve.get("x0", 0)
        width = curve.get("width", 0)
        height = curve.get("height", 0)

        if 25 <= x0 <= 40 and 4 <= width <= 6 and 4 <= height <= 6:
            outer_circles.append(curve)

        if (
            curve.get("non_stroking_color") == (0.0, 0.0, 0.0)
            and 25 <= x0 <= 40
            and 1 <= width <= 3
            and 1 <= height <= 3
        ):
            selected_dots.append(curve)

    centers: List[float] = []
    for circle in outer_circles:
        center_y = (circle["top"] + circle["bottom"]) / 2
        if not any(abs(center_y - existing) < 1.2 for existing in centers):
            centers.append(center_y)

    rows: List[Dict] = []
    for center_y in sorted(centers):
        candidates = [
            line
            for line in lines
            if 35 < line["x0"] < 90
            and line["top"] - 5 <= center_y <= line["bottom"] + 5
        ]
        if not candidates:
            continue

        line = min(
            candidates,
            key=lambda value: abs(((value["top"] + value["bottom"]) / 2) - center_y),
        )
        selected = any(
            abs(((dot["top"] + dot["bottom"]) / 2) - center_y) < 2.5
            for dot in selected_dots
        )
        rows.append(
            {
                "page": page_number,
                "center_y": center_y,
                "line": line,
                "selected": selected,
            }
        )

    return rows


def parse_radio_pdf_questions(file_bytes: bytes) -> List[Dict]:
    all_lines: List[Dict] = []
    all_radio_rows: List[Dict] = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            lines = extract_pdf_line_groups(page, page_number)
            all_lines.extend(lines)
            all_radio_rows.extend(extract_pdf_radio_rows(page, page_number, lines))

    if not all_radio_rows:
        return []

    all_lines.sort(key=lambda line: (line["page"], line["top"], line["x0"]))
    all_radio_rows.sort(key=lambda row: (row["page"], row["center_y"]))

    question_starts: List[Dict] = []
    last_number: Optional[int] = None
    for line in all_lines:
        if line["x0"] > 40:
            continue
        match = match_question_line(line["text"], 0, last_number)
        if not match:
            continue
        number, rest = match
        question_starts.append({"line": line, "number": number, "rest": rest})
        last_number = number

    if not question_starts:
        return []

    questions: List[Dict] = []
    for index, start in enumerate(question_starts):
        end_page = (
            question_starts[index + 1]["line"]["page"]
            if index + 1 < len(question_starts)
            else 999999
        )
        end_top = (
            question_starts[index + 1]["line"]["top"]
            if index + 1 < len(question_starts)
            else 999999
        )

        def line_in_question(line: Dict) -> bool:
            if line["page"] < start["line"]["page"] or line["page"] > end_page:
                return False
            if line["page"] == start["line"]["page"] and line["top"] < start["line"]["top"] - 1:
                return False
            if line["page"] == end_page and line["top"] >= end_top - 1:
                return False
            return True

        def radio_in_question(row: Dict) -> bool:
            if row["page"] < start["line"]["page"] or row["page"] > end_page:
                return False
            if row["page"] == start["line"]["page"] and row["center_y"] < start["line"]["top"] - 1:
                return False
            if row["page"] == end_page and row["center_y"] >= end_top - 1:
                return False
            return True

        block_lines = [
            line
            for line in all_lines
            if line_in_question(line) and not is_page_marker_line(line["text"])
        ]
        radio_rows = [row for row in all_radio_rows if radio_in_question(row)]
        if not radio_rows:
            continue

        first_radio_line = radio_rows[0]["line"]
        question_lines = [
            dict(line)
            for line in block_lines
            if line["page"] < first_radio_line["page"]
            or (
                line["page"] == first_radio_line["page"]
                and line["top"] < first_radio_line["top"] - 1
            )
        ]
        if question_lines:
            question_lines[0]["text"] = start["rest"]

        options: List[Dict] = []
        for option_index, row in enumerate(radio_rows):
            next_row = (
                radio_rows[option_index + 1]
                if option_index + 1 < len(radio_rows)
                else None
            )
            option_lines = []
            for line in block_lines:
                if line["page"] < row["page"] or (
                    line["page"] == row["page"]
                    and line["top"] < row["line"]["top"] - 1
                ):
                    continue
                if next_row and (
                    line["page"] > next_row["page"]
                    or (
                        line["page"] == next_row["page"]
                        and line["top"] >= next_row["line"]["top"] - 1
                    )
                ):
                    continue
                if line["x0"] < 35:
                    continue
                option_lines.append(line)

            option_text = normalize_space(" ".join(line["text"] for line in option_lines))
            is_bold = any(line.get("is_bold") for line in option_lines)
            if option_text:
                options.append({"text": option_text, "is_correct": row["selected"] or is_bold})

        question_text = normalize_space(" ".join(line["text"] for line in question_lines))
        if question_text and len(options) >= 2:
            questions.append(
                {
                    "number": start["number"],
                    "text": question_text,
                    "options": options,
                    "answer_hint": None,
                }
            )

    if len(questions) != len(question_starts):
        return []
    if len(questions) != sum(
        1 for question in questions if any(option["is_correct"] for option in question["options"])
    ):
        return []

    return questions


def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    text_parts: List[str] = []
    pages_lines: List[List[str]] = []
    header_counts: Dict[str, int] = {}
    footer_counts: Dict[str, int] = {}
    header_footer_lines = 3
    
    # We also keep track of bold lines to pass them through.
    # Since parse_questions takes a raw string, we can inject a checkmark
    # or an asterisk at the end of a line if it's bold!
    
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            lines = extract_pdf_line_groups(page, page_number)
            
            page_text_lines = []
            for line in lines:
                text = line["text"]
                if line.get("is_bold"):
                    # Inject a marker so the downstream regex parser knows it's correct
                    text += " (верно)"
                page_text_lines.append(text)
                
            pages_lines.append(page_text_lines)

            for line in page_text_lines[:header_footer_lines]:
                # strip the injected marker for header checking
                clean_l = line.replace(" (верно)", "")
                header_counts[clean_l] = header_counts.get(clean_l, 0) + 1
            for line in page_text_lines[-header_footer_lines:]:
                clean_l = line.replace(" (верно)", "")
                footer_counts[clean_l] = footer_counts.get(clean_l, 0) + 1

    header_remove = {line for line, count in header_counts.items() if count >= 2}
    footer_remove = {line for line, count in footer_counts.items() if count >= 2}

    for lines in pages_lines:
        cleaned: List[str] = []
        total = len(lines)
        for index, line in enumerate(lines):
            clean_l = line.replace(" (верно)", "")
            if index < header_footer_lines and clean_l in header_remove:
                continue
            if index >= total - header_footer_lines and clean_l in footer_remove:
                continue
            cleaned.append(line)
        text_parts.extend(cleaned)

    return "\n".join(text_parts)


def parse_pdf_questions(file_bytes: bytes) -> List[Dict]:
    radio_questions = parse_radio_pdf_questions(file_bytes)
    if radio_questions:
        return radio_questions
    return parse_questions(extract_text_from_pdf_bytes(file_bytes))
