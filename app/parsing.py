import json
import os
import tempfile
from typing import Dict, List

from parsers.common import normalize_space, parse_questions
from parsers.docx_parser import extract_docx_paragraphs, parse_docx_questions
from parsers.pdf_parser import parse_pdf_questions


def normalize_imported_questions(questions: object) -> List[Dict]:
    if not isinstance(questions, list):
        raise ValueError("JSON должен содержать массив вопросов.")

    normalized: List[Dict] = []
    for index, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            raise ValueError(f"Вопрос {index}: ожидается объект.")

        text = normalize_space(str(question.get("text", "")))
        if not text:
            raise ValueError(f"Вопрос {index}: отсутствует текст вопроса.")

        raw_options = question.get("options")
        if not isinstance(raw_options, list) or len(raw_options) < 2:
            raise ValueError(f"Вопрос {index}: нужно минимум 2 варианта ответа.")

        options: List[Dict] = []
        for option_index, option in enumerate(raw_options, start=1):
            if not isinstance(option, dict):
                raise ValueError(
                    f"Вопрос {index}, вариант {option_index}: ожидается объект."
                )
            option_text = normalize_space(str(option.get("text", "")))
            if not option_text:
                raise ValueError(
                    f"Вопрос {index}, вариант {option_index}: пустой текст."
                )
            options.append(
                {
                    "text": option_text,
                    "is_correct": bool(option.get("is_correct")),
                }
            )

        normalized.append(
            {
                "number": question.get("number"),
                "text": text,
                "options": options,
                "answer_hint": question.get("answer_hint"),
            }
        )

    return normalized


def parse_uploaded_json(file_bytes: bytes) -> List[Dict]:
    if not file_bytes:
        raise ValueError("JSON файл пустой.")

    try:
        payload_text = file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ValueError("JSON файл должен быть в кодировке UTF-8.") from error

    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Некорректный JSON: строка {error.lineno}, столбец {error.colno}."
        ) from error

    return normalize_imported_questions(payload)


def parse_uploaded_file(filename: str, file_storage) -> List[Dict]:
    lowered = filename.lower()
    if lowered.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            file_storage.save(tmp)
            tmp_path = tmp.name
        try:
            return parse_pdf_questions(tmp_path)
        finally:
            os.unlink(tmp_path)
    file_bytes = file_storage.read()
    if lowered.endswith(".docx"):
        return parse_docx_questions(extract_docx_paragraphs(file_bytes))
    if lowered.endswith(".json"):
        return parse_uploaded_json(file_bytes)
    raise ValueError("Поддерживаются только PDF, DOCX и JSON.")
