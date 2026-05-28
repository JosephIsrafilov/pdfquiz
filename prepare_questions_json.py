import json
import sys
from pathlib import Path

from web_app import parse_uploaded_questions


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python prepare_questions_json.py <input.pdf|input.docx> [output.json]")
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

    file_bytes = input_path.read_bytes()
    questions = parse_uploaded_questions(input_path.name, file_bytes)

    if not questions:
        print("No questions were parsed.")
        return 1

    output_path.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Saved {len(questions)} questions to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
