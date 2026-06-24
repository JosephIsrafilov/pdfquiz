import json
import random
import re
from typing import Any, Dict, List


def generate_question(template: Dict[str, Any], seed: str) -> Dict[str, Any]:
    """
    Generate concrete question from template with deterministic seed.

    Args:
        template: dict with template_en, template_ru, variables_spec_json, answer_expression
        seed: unique string for deterministic generation (e.g. user_id + quiz_token + template_key)

    Returns:
        Question dict with text_en, text_ru, correct, wrong
    """
    rng = random.Random(seed)

    variables_spec = json.loads(template["variables_spec_json"]) if isinstance(template["variables_spec_json"], str) else template["variables_spec_json"]

    values = {}
    for var_name, spec in variables_spec.items():
        values[var_name] = _generate_value(spec, rng)

    text_en = _substitute_variables(template["template_en"], values)
    text_ru = _substitute_variables(template["template_ru"], values)

    correct_answer = _evaluate_answer(template["answer_expression"], values)

    wrong_answers = _generate_wrong_answers(template["answer_expression"], values, correct_answer, rng)

    return {
        "text_en": text_en,
        "text_ru": text_ru,
        "correct": str(correct_answer),
        "wrong": [str(w) for w in wrong_answers],
        "difficulty": template["difficulty"],
        "question_type": template.get("question_type", "mcq"),
    }


def _generate_value(spec: Dict[str, Any], rng: random.Random) -> Any:
    spec_type = spec["type"]

    if spec_type == "int":
        return rng.randint(spec["range"][0], spec["range"][1])

    elif spec_type == "float":
        return round(rng.uniform(spec["range"][0], spec["range"][1]), spec.get("decimals", 2))

    elif spec_type == "choice":
        return rng.choice(spec["values"])

    elif spec_type == "string":
        return rng.choice(spec["values"])

    elif spec_type == "list":
        count = spec.get("count", 3)
        item_spec = spec["item_spec"]
        return [_generate_value(item_spec, rng) for _ in range(count)]

    return None


def _substitute_variables(template: str, values: Dict[str, Any]) -> str:
    result = template
    for var_name, value in values.items():
        placeholder = f"{{{var_name}}}"
        if isinstance(value, list):
            result = result.replace(placeholder, ", ".join(str(v) for v in value))
        else:
            result = result.replace(placeholder, str(value))
    return result


def _evaluate_answer(expression: str, values: Dict[str, Any]) -> Any:
    """
    Safely evaluate answer expression.
    Supports: arithmetic, indexing, string ops.
    """
    safe_ops = {
        "a": values.get("a"),
        "b": values.get("b"),
        "c": values.get("c"),
        "d": values.get("d"),
        "i": values.get("i"),
        "s": values.get("s"),
        "op": values.get("op"),
        "x": values.get("x"),
        "y": values.get("y"),
        "z": values.get("z"),
    }

    if "op" in values:
        op = values["op"]
        a = values.get("a", 0)
        b = values.get("b", 0)

        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            return a // b if b != 0 else "Error"
        elif op == "%":
            return a % b if b != 0 else "Error"
        elif op == "//":
            return a // b if b != 0 else "Error"
        elif op == "**":
            return a ** b if b < 10 else "Error"

    if "[" in expression and "]" in expression:
        match = re.match(r"(\w+)\[(\w+)\]", expression)
        if match:
            container_name = match.group(1)
            index_name = match.group(2)
            container = values.get(container_name)
            index = values.get(index_name)

            if container and index is not None:
                try:
                    return container[index]
                except (IndexError, KeyError, TypeError):
                    return "Error"

    if expression in values:
        return values[expression]

    try:
        return eval(expression, {"__builtins__": {}}, safe_ops)
    except Exception:
        return "Error"


def _generate_wrong_answers(expression: str, values: Dict[str, Any], correct: Any, rng: random.Random) -> List[Any]:
    """
    Generate plausible wrong answers based on common mistakes.
    """
    wrong = []

    if "op" in values:
        op = values["op"]
        a = values.get("a", 0)
        b = values.get("b", 0)

        if op == "+":
            wrong.extend([a - b, a * b, b - a])
        elif op == "-":
            wrong.extend([a + b, b - a, a * b])
        elif op == "*":
            wrong.extend([a + b, a - b, a ** b if b < 10 else a + b * 2])
        elif op == "/":
            if b != 0:
                wrong.extend([a * b, a % b, a - b])
        elif op == "%":
            if b != 0:
                wrong.extend([a // b, a - b, b])
        elif op == "//":
            if b != 0:
                wrong.extend([a / b, a % b, a - b])
        elif op == "**":
            if b < 10:
                wrong.extend([a * b, a + b, a])

    elif "[" in expression:
        match = re.match(r"(\w+)\[(\w+)\]", expression)
        if match:
            container_name = match.group(1)
            index_name = match.group(2)
            container = values.get(container_name)
            index = values.get(index_name)

            if container and index is not None:
                try:
                    if index > 0:
                        wrong.append(container[index - 1])
                    if index < len(container) - 1:
                        wrong.append(container[index + 1])
                    wrong.append("IndexError")
                except (IndexError, TypeError):
                    pass

    wrong = [w for w in wrong if w != correct]
    seen = set()
    unique_wrong = []
    for w in wrong:
        if w not in seen:
            seen.add(w)
            unique_wrong.append(w)
    wrong = unique_wrong

    if len(wrong) < 3:
        if isinstance(correct, int):
            wrong.extend([correct + 1, correct - 1, correct + 10])
        elif isinstance(correct, str):
            wrong.extend(["Error", "None", "''"])
        else:
            wrong.extend([0, 1, -1])

    wrong = list(dict.fromkeys(w for w in wrong if w != correct))

    rng.shuffle(wrong)
    return wrong[:3]
