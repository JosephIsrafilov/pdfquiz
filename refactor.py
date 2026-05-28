import os

file_path = "web_app.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find where QUESTION_PATTERNS starts
start_idx = -1
for i, line in enumerate(lines):
    if line.startswith("QUESTION_PATTERNS = ["):
        start_idx = i
        break

# Find where @app.route("/") starts
end_idx = -1
for i in range(start_idx, len(lines)):
    if line.startswith("@app.route"):
        end_idx = i
        break
for i in range(start_idx, len(lines)):
    if "@app.route(\"/\")" in lines[i]:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    imports = "from parsers.common import parse_questions\nfrom parsers.docx_parser import parse_docx_questions, extract_docx_paragraphs\nfrom parsers.pdf_parser import parse_pdf_questions\n\n"
    new_lines = lines[:start_idx] + [imports] + lines[end_idx:]
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("Refactored web_app.py")
else:
    print(f"Could not find indices: {start_idx}, {end_idx}")
