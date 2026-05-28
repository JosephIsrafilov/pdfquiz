import io
import re
from typing import Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET
from xml.sax.saxutils import unescape
from zipfile import ZipFile

from .common import (
    BULLET_CHARS,
    OPTION_BULLET_PATTERN,
    make_char_class,
    normalize_space,
)

DOCX_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
DOCX_NUMBERED_FORMATS = {"decimal", "lowerLetter", "upperLetter", "lowerRoman", "upperRoman"}


def is_docx_bullet_paragraph(text: str, num_fmt: Optional[str]) -> bool:
    return num_fmt == "bullet" or bool(OPTION_BULLET_PATTERN.match(text))


def is_docx_numbered_paragraph(text: str, num_fmt: Optional[str]) -> bool:
    return num_fmt in DOCX_NUMBERED_FORMATS and not is_docx_bullet_paragraph(text, num_fmt)


def split_table_option_text(text: str, expected_parts: int) -> List[str]:
    cleaned = normalize_space(text)
    if not cleaned or expected_parts <= 1:
        return [cleaned] if cleaned else []

    sentence_parts = [
        normalize_space(part)
        for part in re.findall(r"[^.!?;]+[.!?;]?", cleaned)
        if normalize_space(part)
    ]
    if len(sentence_parts) >= expected_parts:
        return sentence_parts

    boundary_parts = [
        normalize_space(part)
        for part in re.split(r"(?<=[а-яa-z])\s+(?=[А-ЯA-Z«])", cleaned)
        if normalize_space(part)
    ]
    if len(boundary_parts) >= expected_parts:
        return boundary_parts

    return sentence_parts if sentence_parts else [cleaned]


def extract_docx_paragraphs(file_bytes: bytes) -> List[Dict]:
    with ZipFile(io.BytesIO(file_bytes)) as archive:
        document_root = ET.fromstring(archive.read("word/document.xml"))
        numbering_root = None
        if "word/numbering.xml" in archive.namelist():
            numbering_root = ET.fromstring(archive.read("word/numbering.xml"))

    num_map: Dict[str, str] = {}
    fmt_map: Dict[Tuple[str, str], Tuple[Optional[str], Optional[str]]] = {}
    override_starts: Dict[Tuple[str, str], int] = {}
    if numbering_root is not None:
        for num in numbering_root.findall("./w:num", DOCX_NS):
            num_id = num.get(f"{{{DOCX_NS['w']}}}numId")
            abstract = num.find("./w:abstractNumId", DOCX_NS)
            if num_id and abstract is not None:
                num_map[num_id] = abstract.get(f"{{{DOCX_NS['w']}}}val", "")
            for level_override in num.findall("./w:lvlOverride", DOCX_NS):
                ilvl = level_override.get(f"{{{DOCX_NS['w']}}}ilvl", "0")
                start_override = level_override.find("./w:startOverride", DOCX_NS)
                if num_id and start_override is not None:
                    override_starts[(num_id, ilvl)] = int(
                        start_override.get(f"{{{DOCX_NS['w']}}}val", "1")
                    )

        for abstract in numbering_root.findall("./w:abstractNum", DOCX_NS):
            abstract_id = abstract.get(f"{{{DOCX_NS['w']}}}abstractNumId")
            if abstract_id is None:
                continue
            for level in abstract.findall("./w:lvl", DOCX_NS):
                ilvl = level.get(f"{{{DOCX_NS['w']}}}ilvl", "0")
                num_fmt = level.find("./w:numFmt", DOCX_NS)
                lvl_text = level.find("./w:lvlText", DOCX_NS)
                start_value = level.find("./w:start", DOCX_NS)
                fmt_map[(abstract_id, ilvl)] = (
                    num_fmt.get(f"{{{DOCX_NS['w']}}}val") if num_fmt is not None else None,
                    lvl_text.get(f"{{{DOCX_NS['w']}}}val") if lvl_text is not None else None,
                    int(start_value.get(f"{{{DOCX_NS['w']}}}val", "1"))
                    if start_value is not None
                    else 1,
                )

    list_counters: Dict[Tuple[str, str], int] = {}

    def extract_paragraph_data(paragraph: ET.Element) -> Dict:
        text_parts = []
        is_bold = False
        is_highlighted = False

        for run in paragraph.findall(".//w:r", DOCX_NS):
            rpr = run.find("./w:rPr", DOCX_NS)
            run_is_bold = False
            run_is_highlighted = False

            if rpr is not None:
                if rpr.find("./w:b", DOCX_NS) is not None:
                    run_is_bold = True
                if rpr.find("./w:highlight", DOCX_NS) is not None:
                    run_is_highlighted = True

            run_text_parts = []
            for node in run.iter():
                tag = node.tag.rsplit("}", 1)[-1]
                if tag == "t":
                    run_text_parts.append(node.text or "")
                elif tag == "tab":
                    run_text_parts.append("\t")

            run_text = unescape("".join(run_text_parts))
            
            # Only consider it a bold/highlighted answer if there's actual significant text formatted
            # This ignores bolded markers like "A)" or just spaces.
            if run_text.strip() and not re.match(r"^[A-ZА-Яa-zа-я\d]+[\.\)\-]?$", run_text.strip()):
                if run_is_bold:
                    is_bold = True
                if run_is_highlighted:
                    is_highlighted = True
                    
            text_parts.append(run_text)

        text = normalize_space("".join(text_parts))
        return {
            "text": text,
            "marked_correct": is_bold or is_highlighted
        }

    def build_paragraph_record(paragraph: ET.Element) -> Optional[Dict]:
        p_data = extract_paragraph_data(paragraph)
        text = p_data["text"]
        if not text:
            return None
            
        p_style = paragraph.find("./w:pPr/w:pStyle", DOCX_NS)
        num_pr = paragraph.find("./w:pPr/w:numPr", DOCX_NS)
        num_fmt = None
        lvl_text = None
        ilvl = "0"
        num_id = None
        abstract_id = None
        list_number = None
        if num_pr is not None:
            num_id_el = num_pr.find("./w:numId", DOCX_NS)
            ilvl_el = num_pr.find("./w:ilvl", DOCX_NS)
            num_id = num_id_el.get(f"{{{DOCX_NS['w']}}}val") if num_id_el is not None else None
            ilvl = ilvl_el.get(f"{{{DOCX_NS['w']}}}val", "0") if ilvl_el is not None else "0"
            abstract_id = num_map.get(num_id or "")
            if abstract_id is not None:
                num_fmt, lvl_text, start_value = fmt_map.get(
                    (abstract_id, ilvl), (None, None, 1)
                )
                if num_fmt == "decimal" and num_id is not None:
                    counter_key = (num_id, ilvl)
                    effective_start = override_starts.get(counter_key, start_value)
                    if counter_key not in list_counters:
                        list_counters[counter_key] = effective_start
                    else:
                        list_counters[counter_key] += 1
                    list_number = list_counters[counter_key]

        return {
            "text": text,
            "style": p_style.get(f"{{{DOCX_NS['w']}}}val") if p_style is not None else None,
            "num_fmt": num_fmt,
            "lvl_text": lvl_text,
            "level": ilvl,
            "num_id": num_id,
            "abstract_id": abstract_id,
            "list_number": list_number,
            "is_bullet": is_docx_bullet_paragraph(text, num_fmt),
            "is_numbered": is_docx_numbered_paragraph(text, num_fmt),
            "marked_correct": p_data["marked_correct"]
        }

    def make_synthetic_record(
        text: str,
        *,
        list_number: Optional[int] = None,
        is_bullet: bool = False,
        is_numbered: bool = False,
        marked_correct: bool = False
    ) -> Optional[Dict]:
        cleaned_text = normalize_space(text)
        if not cleaned_text:
            return None
        return {
            "text": cleaned_text,
            "style": "table",
            "num_fmt": "bullet" if is_bullet else ("decimal" if is_numbered else None),
            "lvl_text": "•" if is_bullet else ("%1." if is_numbered else None),
            "level": "1" if is_bullet else "0",
            "num_id": None,
            "abstract_id": None,
            "list_number": list_number,
            "is_bullet": is_bullet,
            "is_numbered": is_numbered,
            "marked_correct": marked_correct
        }

    def extract_table_records(table: ET.Element) -> List[Dict]:
        records: List[Dict] = []
        for row in table.findall("./w:tr", DOCX_NS):
            cell_data: List[List[Dict]] = []
            for cell in row.findall("./w:tc", DOCX_NS):
                c_data: List[Dict] = []
                for paragraph in cell.findall("./w:p", DOCX_NS):
                    p_data = extract_paragraph_data(paragraph)
                    if p_data["text"]:
                        c_data.append(p_data)
                cell_data.append(c_data)

            if not any(cell_data):
                continue

            question_number = None
            for c_data in cell_data:
                for data in c_data:
                    match = re.match(r"^\s*(\d{1,4})[\.\)]\s*$", data["text"])
                    if match:
                        question_number = int(match.group(1))
                        break
                if question_number is not None:
                    break

            if question_number is not None:
                question_text = ""
                for c_data in reversed(cell_data):
                    joined = normalize_space(" ".join(d["text"] for d in c_data))
                    if joined and not re.match(r"^\d{1,4}[\.\)]$", joined):
                        question_text = joined
                        break
                record = make_synthetic_record(
                    f"{question_number}. {question_text}",
                    list_number=question_number,
                    is_numbered=True,
                )
                if record:
                    records.append(record)
                continue

            bullet_count = sum(
                1
                for c_data in cell_data
                for data in c_data
                if data["text"] and set(data["text"].replace(" ", "")) <= set(BULLET_CHARS)
            )
            option_source = next(
                (
                    [
                        data
                        for data in c_data
                        if data["text"] and not set(data["text"].replace(" ", "")) <= set(BULLET_CHARS)
                    ]
                    for c_data in reversed(cell_data)
                    if any(
                        data["text"] and not set(data["text"].replace(" ", "")) <= set(BULLET_CHARS)
                        for data in c_data
                    )
                ),
                [],
            )

            if bullet_count and option_source:
                joined_text = normalize_space(" ".join(d["text"] for d in option_source))
                is_marked = any(d["marked_correct"] for d in option_source)
                option_texts = split_table_option_text(joined_text, bullet_count + 1)
                if len(option_texts) < bullet_count:
                    option_texts = [d["text"] for d in option_source]
                for idx, option_text in enumerate(option_texts):
                    record = make_synthetic_record(
                        option_text,
                        is_bullet=idx < bullet_count,
                        marked_correct=is_marked
                    )
                    if record:
                        records.append(record)
                continue
            if bullet_count:
                continue

            for c_data in cell_data:
                for data in c_data:
                    record = make_synthetic_record(data["text"], marked_correct=data["marked_correct"])
                    if record:
                        records.append(record)

        return records

    paragraphs: List[Dict] = []
    body = document_root.find(".//w:body", DOCX_NS)
    if body is None:
        return paragraphs

    for child in list(body):
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            record = build_paragraph_record(child)
            if record:
                paragraphs.append(record)
        elif tag == "tbl":
            paragraphs.extend(extract_table_records(child))

    return paragraphs


def parse_docx_questions(paragraphs: List[Dict]) -> List[Dict]:
    from .common import clean_option_text, strip_question_leading_noise, match_question_line

    questions: List[Dict] = []
    current: Optional[Dict] = None
    last_number: Optional[int] = None
    continuation_words = {
        "в", "во", "и", "или", "по", "на", "с", "со", "к", "ко", "о", "об",
        "от", "до", "для", "при", "из", "под", "над", "за", "без",
    }

    def finalize_current() -> None:
        nonlocal current
        if not current:
            return

        question_text = normalize_space(" ".join(current["question_lines"]))
        options = [
            {
                "text": normalize_space(option["text"]),
                "is_correct": option["is_correct"],
            }
            for option in current["options"]
            if normalize_space(option["text"])
        ]

        if question_text and options:
            questions.append(
                {
                    "number": current["number"],
                    "text": question_text,
                    "options": options,
                    "answer_hint": None,
                }
            )
        current = None

    def next_non_empty(index: int) -> Optional[Dict]:
        for offset in range(index + 1, len(paragraphs)):
            candidate = paragraphs[offset]
            if candidate["text"]:
                return candidate
        return None

    def is_question_start(paragraph: Dict) -> bool:
        nonlocal current, last_number
        text = paragraph["text"]
        if paragraph["is_bullet"]:
            return False

        match = match_question_line(text, 0, last_number)
        if match:
            return True

        raw_text = text.lstrip()
        cleaned = strip_question_leading_noise(text)
        if raw_text.startswith("+"):
            return True

        if current and not current["options"]:
            return False

        if paragraph["is_numbered"] and cleaned and not cleaned.startswith("("):
            return True

        return False

    def start_question(paragraph: Dict) -> None:
        nonlocal current, last_number
        text = paragraph["text"]
        match = match_question_line(text, 0, last_number)
        question_number = None
        question_text = strip_question_leading_noise(text)

        if match:
            question_number, question_text = match
        elif paragraph.get("list_number") is not None:
            question_number = paragraph["list_number"]
        elif paragraph["is_numbered"]:
            question_number = (last_number + 1) if last_number is not None else None

        question_text = strip_question_leading_noise(question_text)
        current = {
            "number": question_number,
            "question_lines": [question_text] if question_text else [],
            "options": [],
        }
        if question_number is not None:
            last_number = question_number

    def looks_like_first_plain_option(index: int) -> bool:
        if current is None or current["options"]:
            return False
        if not current["question_lines"]:
            return False
        paragraph = paragraphs[index]
        text = paragraph["text"].strip()
        if paragraph["is_numbered"]:
            return False
        if text.startswith("(") and text.endswith(")"):
            return False
        next_item = next_non_empty(index)
        if next_item and next_item["is_bullet"]:
            return True
        question_text = normalize_space(" ".join(current["question_lines"]))
        lowered = question_text.lower()
        return question_text.endswith(":") or "выделите" in lowered

    def should_append_to_previous_option(previous_text: str, next_text: str) -> bool:
        cleaned_next, _ = clean_option_text(next_text)
        if not cleaned_next:
            return False
        if cleaned_next in {".", ",", ";", ":"}:
            return True
        previous_trimmed = previous_text.rstrip()
        if previous_trimmed.endswith((",", "(", "«", "-", "—")):
            return True
        last_word = previous_trimmed.split()[-1].strip(".,;:!?()\"«»").lower()
        if last_word in continuation_words:
            return True
        if (
            cleaned_next[0].islower()
            and len(previous_trimmed) >= 60
            and not previous_trimmed.endswith((".", ";", ":", "!", "?"))
        ):
            return True
        return False

    for index, paragraph in enumerate(paragraphs):
        text = paragraph["text"]
        if not text:
            continue

        if is_question_start(paragraph):
            finalize_current()
            start_question(paragraph)
            continue

        if current is None:
            continue

        bullet_like = paragraph["is_bullet"] or bool(re.match(r"^[A-ZА-Яa-zа-я\d]\)[\s\.]+", text))

        if bullet_like or looks_like_first_plain_option(index) or current["options"]:
            cleaned_text, marker_correct = clean_option_text(text, pre_marked_correct=paragraph.get("marked_correct", False))
            if not cleaned_text:
                continue
            
            if re.match(r"^[A-ZА-Яa-zа-я\d]\)", cleaned_text):
                cleaned_text = re.sub(r"^[A-ZА-Яa-zа-я\d]\)\s*", "", cleaned_text)
                
            previous_option = current["options"][-1] if current["options"] else None
            
            if previous_option and should_append_to_previous_option(
                previous_option["text"], text
            ) and not bullet_like:
                previous_option["text"] = normalize_space(
                    f"{previous_option['text']} {cleaned_text}"
                )
                if paragraph.get("marked_correct", False):
                    previous_option["is_correct"] = True
                continue
                
            current["options"].append(
                {
                    "text": cleaned_text,
                    "is_correct": marker_correct,
                }
            )
            continue

        if current["number"] is None and paragraph.get("list_number") is not None:
            current["number"] = paragraph["list_number"]
            last_number = paragraph["list_number"]

        current["question_lines"].append(strip_question_leading_noise(text))

    finalize_current()
    return questions
