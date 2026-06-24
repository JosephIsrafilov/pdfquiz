"""
Dynamic question templates for arithmetic, strings, and lists.
Generates infinite variations for anti-memorization.
"""

ARITHMETIC_TEMPLATES = [
    {
        "template_key": "arithmetic_add",
        "template_en": "What does {a} + {b} return?",
        "template_ru": "Что вернет {a} + {b}?",
        "variables_spec": {
            "a": {"type": "int", "range": [1, 20]},
            "b": {"type": "int", "range": [1, 20]},
        },
        "answer_expression": "a + b",
        "difficulty": "beginner",
        "topic_key": "operators",
    },
    {
        "template_key": "arithmetic_subtract",
        "template_en": "What does {a} - {b} return?",
        "template_ru": "Что вернет {a} - {b}?",
        "variables_spec": {
            "a": {"type": "int", "range": [10, 30]},
            "b": {"type": "int", "range": [1, 10]},
        },
        "answer_expression": "a - b",
        "difficulty": "beginner",
        "topic_key": "operators",
    },
    {
        "template_key": "arithmetic_multiply",
        "template_en": "What does {a} * {b} return?",
        "template_ru": "Что вернет {a} * {b}?",
        "variables_spec": {
            "a": {"type": "int", "range": [2, 12]},
            "b": {"type": "int", "range": [2, 12]},
        },
        "answer_expression": "a * b",
        "difficulty": "beginner",
        "topic_key": "operators",
    },
    {
        "template_key": "arithmetic_divide",
        "template_en": "What does {a} // {b} return?",
        "template_ru": "Что вернет {a} // {b}?",
        "variables_spec": {
            "a": {"type": "int", "range": [10, 50]},
            "b": {"type": "int", "range": [2, 10]},
        },
        "answer_expression": "a // b",
        "difficulty": "intermediate",
        "topic_key": "operators",
    },
    {
        "template_key": "arithmetic_modulo",
        "template_en": "What does {a} % {b} return?",
        "template_ru": "Что вернет {a} % {b}?",
        "variables_spec": {
            "a": {"type": "int", "range": [10, 30]},
            "b": {"type": "int", "range": [2, 10]},
        },
        "answer_expression": "a % b",
        "difficulty": "intermediate",
        "topic_key": "operators",
    },
    {
        "template_key": "arithmetic_power",
        "template_en": "What does {a} ** {b} return?",
        "template_ru": "Что вернет {a} ** {b}?",
        "variables_spec": {
            "a": {"type": "int", "range": [2, 10]},
            "b": {"type": "int", "range": [2, 4]},
        },
        "answer_expression": "a ** b",
        "difficulty": "intermediate",
        "topic_key": "operators",
    },
]

STRING_TEMPLATES = [
    {
        "template_key": "string_index",
        "template_en": 'What does "{s}"[{i}] return?',
        "template_ru": 'Что вернет "{s}"[{i}]?',
        "variables_spec": {
            "s": {"type": "choice", "values": ["hello", "python", "world", "code"]},
            "i": {"type": "int", "range": [0, 3]},
        },
        "answer_expression": "s[i]",
        "difficulty": "beginner",
        "topic_key": "strings",
    },
    {
        "template_key": "string_negative_index",
        "template_en": 'What does "{s}"[{i}] return?',
        "template_ru": 'Что вернет "{s}"[{i}]?',
        "variables_spec": {
            "s": {"type": "choice", "values": ["data", "test", "loop", "func"]},
            "i": {"type": "choice", "values": [-1, -2, -3]},
        },
        "answer_expression": "s[i]",
        "difficulty": "intermediate",
        "topic_key": "strings",
    },
]

LIST_TEMPLATES = [
    {
        "template_key": "list_index",
        "template_en": "What is [{a}, {b}, {c}][{i}]?",
        "template_ru": "Что такое [{a}, {b}, {c}][{i}]?",
        "variables_spec": {
            "a": {"type": "int", "range": [1, 20]},
            "b": {"type": "int", "range": [1, 20]},
            "c": {"type": "int", "range": [1, 20]},
            "i": {"type": "choice", "values": [0, 1, 2]},
        },
        "answer_expression": "[a, b, c][i]",
        "difficulty": "beginner",
        "topic_key": "lists",
    },
    {
        "template_key": "list_negative_index",
        "template_en": "What is [{a}, {b}, {c}][{i}]?",
        "template_ru": "Что такое [{a}, {b}, {c}][{i}]?",
        "variables_spec": {
            "a": {"type": "int", "range": [1, 20]},
            "b": {"type": "int", "range": [1, 20]},
            "c": {"type": "int", "range": [1, 20]},
            "i": {"type": "choice", "values": [-1, -2, -3]},
        },
        "answer_expression": "[a, b, c][i]",
        "difficulty": "intermediate",
        "topic_key": "lists",
    },
]

ALL_TEMPLATES = [*ARITHMETIC_TEMPLATES, *STRING_TEMPLATES, *LIST_TEMPLATES]
