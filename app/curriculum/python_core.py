SOURCE_URL = "https://www.w3schools.com/python/"
COURSE_TITLE_EN = "Python"
COURSE_TITLE_RU = "Python"

OPTION_TRANSLATIONS_RU = {
    "Indentation": "Отступы",
    "Curly braces only": "Только фигурные скобки",
    "Semicolons": "Точки с запятой",
    "Quotation marks": "Кавычки",
    "A string": "Строка",
    "A boolean": "Логическое значение",
    "Nothing": "Ничего",
    "Always an integer": "Всегда целое число",
    "The integer 12": "Целое число 12",
    "The text '12'": "Текст '12'",
    "An error": "Ошибка",
    "True and False": "True и False",
    "Yes and No": "Да и нет",
    "On and Off": "Вкл. и выкл.",
    "Duplicate values": "Повторяющиеся значения",
    "All numbers": "Все числа",
    "All strings": "Все строки",
    "The first value": "Первое значение",
    "Key-value pairs": "Пары ключ-значение",
    "Rows and columns": "Строки и столбцы",
    "Unique values only": "Только уникальные значения",
    "Its condition": "Его условие",
    "A file": "Файл",
    "A comment": "Комментарий",
    "A function name": "Имя функции",
    "It performs no action": "Не выполняет никаких действий",
    "It stops Python": "Останавливает Python",
    "It repeats the block": "Повторяет блок",
    "It prints pass": "Выводит pass",
    "A name in a function definition": "Имя в определении функции",
    "The final printed value": "Последнее выведенное значение",
    "A Python file": "Файл Python",
    "A loop condition": "Условие цикла",
    "Local": "Локальная",
    "Global": "Глобальная",
    "Imported": "Импортированная",
    "Constant": "Константа",
    "Extra positional arguments": "Дополнительные позиционные аргументы",
    "Extra keyword arguments": "Дополнительные именованные аргументы",
    "Only keyword arguments": "Только именованные аргументы",
    "Only numbers": "Только числа",
    "Errors": "Ошибки",
    "Modules": "Модули",
    "Loop values": "Значения цикла",
    "Return statements": "Инструкции return",
    "A function calling itself": "Функция вызывает сама себя",
    "A list sorting itself": "Список сортирует сам себя",
    "A variable changing type": "Переменная меняет тип",
    "A module import": "Импорт модуля",
    "To stop the repeated calls": "Чтобы остановить повторные вызовы",
    "To print every result": "Чтобы вывести каждый результат",
    "To create a class": "Чтобы создать класс",
    "To import math": "Чтобы импортировать math",
    "They produce values lazily": "Они создают значения по мере необходимости",
    "They always sort values": "Они всегда сортируют значения",
    "They replace every class": "Они заменяют все классы",
    "They disable loops": "Они отключают циклы",
    "Installing Python packages": "Установка пакетов Python",
    "Writing comments": "Написание комментариев",
    "Creating loops": "Создание циклов",
    "Drawing windows": "Рисование окон",
    "To isolate project dependencies": "Чтобы изолировать зависимости проекта",
    "To speed up every loop": "Чтобы ускорить каждый цикл",
    "To replace Python": "Чтобы заменить Python",
    "To hide source code": "Чтобы скрыть исходный код",
    "Exchanging structured data": "Обмен структурированными данными",
    "Drawing pictures": "Рисование картинок",
    "Compiling Python": "Компиляция Python",
    "Styling web pages": "Оформление веб-страниц",
    "A matching pattern anywhere in the text": "Подходящий шаблон в любой части текста",
    "Only at the final character": "Только в последнем символе",
    "Only Python keywords": "Только ключевые слова Python",
    "A file on disk": "Файл на диске",
    "Setting initial object data": "Задание начальных данных объекта",
    "Deleting every object": "Удаление всех объектов",
    "Importing modules": "Импорт модулей",
    "Starting a loop": "Запуск цикла",
    "The current object": "Текущий объект",
    "The parent file": "Родительский файл",
    "Every class at once": "Все классы одновременно",
    "Python itself": "Сам Python",
    "Reuse behavior from a parent class": "Повторно использовать поведение родительского класса",
    "Delete Python": "Удалить Python",
    "Avoid all methods": "Не использовать методы",
    "Become a list": "Стать списком",
    "A child class provides its own version": "Дочерний класс создаёт свою версию",
    "A method runs twice": "Метод запускается дважды",
    "A variable becomes global": "Переменная становится глобальной",
    "A file is renamed": "Файл переименовывается",
    "Controlling access to object details": "Управление доступом к деталям объекта",
    "Sorting every collection": "Сортировка каждой коллекции",
    "Replacing functions with loops": "Замена функций циклами",
    "Installing packages": "Установка пакетов",
    "It closes the file automatically": "Файл закрывается автоматически",
    "It makes every file public": "Все файлы становятся публичными",
    "It converts files to JSON": "Файлы преобразуются в JSON",
    "It prevents all errors": "Предотвращает все ошибки",
    "No": "Нет",
    "Yes, always": "Да, всегда",
    "Only strings": "Только строки",
    "Only the first item": "Только первый элемент",
    "A trailing comma": "Запятая после элемента",
    "Two values": "Два значения",
    "Square brackets": "Квадратные скобки",
    "The tuple keyword": "Ключевое слово tuple",
    "False only": "Только False",
    "0 only": "Только 0",
    "empty": "empty",
}


def _q(level, text_en, text_ru, correct, wrong, explanation_en="", explanation_ru="", option_rationales_en=None, option_rationales_ru=None):
    return {
        "difficulty": level,
        "text_en": text_en,
        "text_ru": text_ru,
        "correct": correct,
        "wrong": wrong,
        "explanation_en": explanation_en,
        "explanation_ru": explanation_ru,
        "option_rationales_en": option_rationales_en or {},
        "option_rationales_ru": option_rationales_ru or {},
    }


PYTHON_TOPICS = [
    {
        "key": "syntax",
        "title_en": "Getting Started and Syntax",
        "title_ru": "Начало работы и синтаксис",
        "description_en": "Running Python, indentation, statements and code blocks.",
        "description_ru": "Запуск Python, отступы, инструкции и блоки кода.",
        "questions": [
            _q("beginner", "Which file extension is normally used for Python code?", "Какое расширение обычно используется для файлов Python?", ".py", [".html", ".css", ".jpg"],
               explanation_en="Python source files use the .py extension.",
               explanation_ru="Исходные файлы Python имеют расширение .py.",
               option_rationales_en={
                   ".py": "Correct. This is the standard Python extension.",
                   ".html": "Incorrect. HTML is for web structure, not Python.",
                   ".css": "Incorrect. CSS is for styling web pages.",
                   ".jpg": "Incorrect. JPG is an image format."
               },
               option_rationales_ru={
                   ".py": "Верно. Это стандартное расширение Python.",
                   ".html": "Неверно. HTML используется для структуры веб-страниц.",
                   ".css": "Неверно. CSS используется для стилизации.",
                   ".jpg": "Неверно. JPG — это формат изображений."
               }),
            _q("intermediate", "What does Python use to mark a block of code?", "Что Python использует для обозначения блока кода?", "Indentation", ["Curly braces only", "Semicolons", "Quotation marks"],
               explanation_en="Python uses whitespace indentation to define code blocks.",
               explanation_ru="Python использует пробельные отступы для определения блоков кода.",
               option_rationales_en={
                   "Indentation": "Correct. Indentation groups statements together in Python.",
                   "Curly braces only": "Incorrect. Languages like C or JavaScript use curly braces, not Python.",
                   "Semicolons": "Incorrect. Semicolons separate statements in other languages.",
                   "Quotation marks": "Incorrect. Quotation marks define strings."
               },
               option_rationales_ru={
                   "Indentation": "Верно. Отступы объединяют инструкции в блоки в Python.",
                   "Curly braces only": "Неверно. Фигурные скобки используют C или JS.",
                   "Semicolons": "Неверно. Точки с запятой разделяют инструкции в других языках.",
                   "Quotation marks": "Неверно. Кавычки определяют строки."
               }),
            _q("advanced", "Which line is valid Python syntax?", "Какая строка содержит правильный синтаксис Python?", "if score > 5:", ["if (score > 5) then", "if score > 5 {}", "if score > 5 do"],
               explanation_en="Python conditions end with a colon and don't require parentheses around the expression.",
               explanation_ru="Условия в Python заканчиваются двоеточием и не требуют скобок вокруг выражения.",
               option_rationales_en={
                   "if score > 5:": "Correct. The statement ends with a colon, starting a new indented block.",
                   "if (score > 5) then": "Incorrect. Python does not use 'then'.",
                   "if score > 5 {}": "Incorrect. Python uses a colon and indentation, not curly braces.",
                   "if score > 5 do": "Incorrect. 'do' is not used to start if-blocks in Python."
               },
               option_rationales_ru={
                   "if score > 5:": "Верно. Инструкция заканчивается двоеточием, начиная новый блок с отступом.",
                   "if (score > 5) then": "Неверно. Python не использует ключевое слово 'then'.",
                   "if score > 5 {}": "Неверно. Python использует двоеточие и отступы, а не фигурные скобки.",
                   "if score > 5 do": "Неверно. 'do' не используется для if-блоков в Python."
               }),
        ],
    },
    {
        "key": "output_comments",
        "title_en": "Output and Comments",
        "title_ru": "Вывод и комментарии",
        "description_en": "Using print() and writing notes that Python ignores.",
        "description_ru": "Использование print() и комментариев, которые Python не выполняет.",
        "questions": [
            _q("beginner", "Which function prints text?", "Какая функция выводит текст?", "print()", ["input()", "len()", "type()"],
               explanation_en="The print() function outputs data to the console.",
               explanation_ru="Функция print() выводит данные в консоль.",
               option_rationales_en={
                   "print()": "Correct. print() is the standard output function.",
                   "input()": "Incorrect. input() reads text from the user.",
                   "len()": "Incorrect. len() calculates the length of a sequence.",
                   "type()": "Incorrect. type() returns the data type of an object."
               },
               option_rationales_ru={
                   "print()": "Верно. print() — стандартная функция вывода.",
                   "input()": "Неверно. input() считывает текст от пользователя.",
                   "len()": "Неверно. len() вычисляет длину последовательности.",
                   "type()": "Неверно. type() возвращает тип данных объекта."
               }),
            _q("intermediate", "Which symbol starts a single-line comment?", "Какой символ начинает однострочный комментарий?", "#", ["//", "<!--", "**"],
               explanation_en="In Python, comments begin with the hash (#) symbol.",
               explanation_ru="В Python комментарии начинаются с символа решётки (#).",
               option_rationales_en={
                   "#": "Correct. Python ignores anything after a # on the same line.",
                   "//": "Incorrect. This is used for comments in C/Java/JS, but means floor division in Python.",
                   "<!--": "Incorrect. This is an HTML comment.",
                   "**": "Incorrect. This is the exponentiation operator in Python."
               },
               option_rationales_ru={
                   "#": "Верно. Python игнорирует всё после # на той же строке.",
                   "//": "Неверно. Это комментарий в C/Java/JS, а в Python — целочисленное деление.",
                   "<!--": "Неверно. Это комментарий HTML.",
                   "**": "Неверно. Это оператор возведения в степень в Python."
               }),
            _q("advanced", "What does print('A', 'B', sep='-') display?", "Что выведет print('A', 'B', sep='-')?", "A-B", ["AB", "A B", "A, B"],
               explanation_en="The 'sep' argument specifies the separator between multiple printed items.",
               explanation_ru="Аргумент 'sep' определяет разделитель между несколькими выводимыми элементами.",
               option_rationales_en={
                   "A-B": "Correct. The items are joined by a hyphen.",
                   "AB": "Incorrect. That would happen if sep=''.",
                   "A B": "Incorrect. This is the default output when no sep is provided.",
                   "A, B": "Incorrect. Commas separate the arguments, they aren't printed unless specified in sep."
               },
               option_rationales_ru={
                   "A-B": "Верно. Элементы объединяются дефисом.",
                   "AB": "Неверно. Так было бы при sep=''.",
                   "A B": "Неверно. Это стандартный вывод (по умолчанию пробел).",
                   "A, B": "Неверно. Запятые разделяют аргументы, они не выводятся."
               }),
        ],
    },
    {
        "key": "variables",
        "title_en": "Variables",
        "title_ru": "Переменные",
        "description_en": "Creating, naming, assigning and using variables.",
        "description_ru": "Создание, именование, присваивание и использование переменных.",
        "questions": [
            _q("beginner", "Which line creates a variable named age?", "Какая строка создаёт переменную age?", "age = 10", ["10 = age", "var age = 10", "age == 10"],
               explanation_en="Variables are created by putting the name on the left and the value on the right of the = sign.",
               explanation_ru="Переменные создаются путём указания имени слева и значения справа от знака =.",
               option_rationales_en={
                   "age = 10": "Correct. This assigns the integer 10 to the variable 'age'.",
                   "10 = age": "Incorrect. The variable name must be on the left side of the = sign.",
                   "var age = 10": "Incorrect. Python does not use the 'var' keyword.",
                   "age == 10": "Incorrect. The == operator checks for equality, it does not assign a value."
               },
               option_rationales_ru={
                   "age = 10": "Верно. Это присваивает число 10 переменной 'age'.",
                   "10 = age": "Неверно. Имя переменной должно быть слева от знака =.",
                   "var age = 10": "Неверно. Python не использует ключевое слово 'var'.",
                   "age == 10": "Неверно. Оператор == проверяет равенство, а не присваивает значение."
               }),
            _q("intermediate", "Which is a valid variable name?", "Какое имя переменной допустимо?", "player_score", ["2score", "player-score", "class"],
               explanation_en="Variable names can contain letters, numbers, and underscores, but cannot start with a number.",
               explanation_ru="Имена переменных могут содержать буквы, цифры и подчёркивания, но не могут начинаться с цифры.",
               option_rationales_en={
                   "player_score": "Correct. It uses allowed characters and starts with a letter.",
                   "2score": "Incorrect. Variable names cannot start with a number.",
                   "player-score": "Incorrect. Hyphens (-) are not allowed, only underscores (_).",
                   "class": "Incorrect. 'class' is a reserved keyword in Python."
               },
               option_rationales_ru={
                   "player_score": "Верно. Содержит допустимые символы и начинается с буквы.",
                   "2score": "Неверно. Имена переменных не могут начинаться с цифры.",
                   "player-score": "Неверно. Дефисы (-) недопустимы, только подчёркивания (_).",
                   "class": "Неверно. 'class' — зарезервированное ключевое слово."
               }),
            _q("advanced", "After x, y = 3, 7, what is y?", "После x, y = 3, 7 чему равен y?", "7", ["3", "10", "x"],
               explanation_en="Python supports multiple assignment, unpacking the tuple on the right into variables on the left.",
               explanation_ru="Python поддерживает множественное присваивание, распаковывая кортеж справа в переменные слева.",
               option_rationales_en={
                   "7": "Correct. The second variable 'y' gets the second value, 7.",
                   "3": "Incorrect. The value 3 is assigned to 'x'.",
                   "10": "Incorrect. The values are not added together.",
                   "x": "Incorrect. y is assigned the integer 7, not the variable name x."
               },
               option_rationales_ru={
                   "7": "Верно. Вторая переменная 'y' получает второе значение, 7.",
                   "3": "Неверно. Значение 3 присваивается 'x'.",
                   "10": "Неверно. Значения не складываются.",
                   "x": "Неверно. Переменной y присваивается число 7, а не имя x."
               }),
        ],
    },
    {
        "key": "data_types",
        "title_en": "Data Types",
        "title_ru": "Типы данных",
        "description_en": "Strings, numbers, booleans, collections and type().",
        "description_ru": "Строки, числа, логические значения, коллекции и type().",
        "questions": [
            _q("beginner", "Which type stores text?", "Какой тип хранит текст?", "str", ["int", "bool", "float"],
               explanation_en="The str (string) type is used to store text in Python.",
               explanation_ru="Тип str (строка) используется для хранения текста в Python.",
               option_rationales_en={
                   "str": "Correct. 'str' stands for string, which is text.",
                   "int": "Incorrect. 'int' is for whole numbers.",
                   "bool": "Incorrect. 'bool' is for True/False logic.",
                   "float": "Incorrect. 'float' is for decimal numbers."
               },
               option_rationales_ru={
                   "str": "Верно. 'str' означает string, то есть строку (текст).",
                   "int": "Неверно. 'int' используется для целых чисел.",
                   "bool": "Неверно. 'bool' для логических значений True/False.",
                   "float": "Неверно. 'float' для дробных чисел."
               }),
            _q("intermediate", "What is the type of [1, 2, 3]?", "Какой тип имеет [1, 2, 3]?", "list", ["tuple", "set", "dict"],
               explanation_en="Square brackets [] are used to create lists in Python.",
               explanation_ru="Квадратные скобки [] используются для создания списков в Python.",
               option_rationales_en={
                   "list": "Correct. Square brackets create a mutable list.",
                   "tuple": "Incorrect. Tuples use parentheses ().",
                   "set": "Incorrect. Sets use curly braces {}.",
                   "dict": "Incorrect. Dictionaries use curly braces with key-value pairs {k: v}."
               },
               option_rationales_ru={
                   "list": "Верно. Квадратные скобки создают изменяемый список.",
                   "tuple": "Неверно. Кортежи используют круглые скобки ().",
                   "set": "Неверно. Множества используют фигурные скобки {}.",
                   "dict": "Неверно. Словари используют фигурные скобки с парами {ключ: значение}."
               }),
            _q("advanced", "What does type(True) report?", "Что покажет type(True)?", "bool", ["int", "str", "None"],
               explanation_en="True and False are boolean values, represented by the 'bool' type.",
               explanation_ru="True и False — это логические значения, представленные типом 'bool'.",
               option_rationales_en={
                   "bool": "Correct. True and False belong to the bool type.",
                   "int": "Incorrect. Although True behaves like 1 in math, its type is bool.",
                   "str": "Incorrect. It is not surrounded by quotes, so it's not a string.",
                   "None": "Incorrect. None is a special type (NoneType) representing absence of value."
               },
               option_rationales_ru={
                   "bool": "Верно. True и False относятся к типу bool.",
                   "int": "Неверно. Хотя True ведёт себя как 1 в математике, его тип — bool.",
                   "str": "Неверно. Оно не заключено в кавычки, поэтому это не строка.",
                   "None": "Неверно. None — это специальный тип (NoneType)."
               }),
        ],
    },
    {
        "key": "numbers_casting",
        "title_en": "Numbers and Casting",
        "title_ru": "Числа и преобразование типов",
        "description_en": "Integers, floats, complex numbers and type conversion.",
        "description_ru": "Целые, дробные, комплексные числа и преобразование типов.",
        "questions": [
            _q("beginner", "What is the type of 3.5?", "Какой тип имеет 3.5?", "float", ["int", "str", "bool"],
               explanation_en="Numbers with a decimal point are floating-point numbers (float).",
               explanation_ru="Числа с десятичной точкой — это числа с плавающей точкой (float).",
               option_rationales_en={
                   "float": "Correct. A decimal point makes it a float.",
                   "int": "Incorrect. 'int' is for integers (whole numbers) without decimals.",
                   "str": "Incorrect. It lacks quotes, so it is a number, not a string.",
                   "bool": "Incorrect. It is not True or False."
               },
               option_rationales_ru={
                   "float": "Верно. Наличие десятичной точки делает его float.",
                   "int": "Неверно. 'int' — это целые числа без десятичной части.",
                   "str": "Неверно. Без кавычек это число, а не строка.",
                   "bool": "Неверно. Это не True или False."
               }),
            _q("intermediate", "What does int('12') produce?", "Что вернёт int('12')?", "The integer 12", ["The text '12'", "12.0", "An error"],
               explanation_en="The int() function converts a string of digits into a mathematical integer.",
               explanation_ru="Функция int() преобразует строку из цифр в математическое целое число.",
               option_rationales_en={
                   "The integer 12": "Correct. int() parses the string and returns a real integer.",
                   "The text '12'": "Incorrect. The input was text, but the output is an integer.",
                   "12.0": "Incorrect. int() returns whole numbers; float('12') would return 12.0.",
                   "An error": "Incorrect. '12' is perfectly valid for integer conversion."
               },
               option_rationales_ru={
                   "The integer 12": "Верно. int() анализирует строку и возвращает целое число.",
                   "The text '12'": "Неверно. На входе текст, но на выходе целое число.",
                   "12.0": "Неверно. int() возвращает целые числа; float('12') вернул бы 12.0.",
                   "An error": "Неверно. '12' полностью корректно для преобразования в целое число."
               }),
            _q("advanced", "What is int(4.9)?", "Чему равно int(4.9)?", "4", ["5", "4.9", "An error"],
               explanation_en="Casting a float to an int always truncates (chops off) the decimal part; it does not round.",
               explanation_ru="Приведение float к int всегда отбрасывает десятичную часть; округления не происходит.",
               option_rationales_en={
                   "4": "Correct. int() truncates the decimal part, leaving just 4.",
                   "5": "Incorrect. int() does not round up. Use round(4.9) for that.",
                   "4.9": "Incorrect. int() must return a whole integer without decimals.",
                   "An error": "Incorrect. Floats can be safely cast to integers."
               },
               option_rationales_ru={
                   "4": "Верно. int() отбрасывает дробную часть, оставляя 4.",
                   "5": "Неверно. int() не округляет. Для этого используется round(4.9).",
                   "4.9": "Неверно. int() должен возвращать целое число без дробей.",
                   "An error": "Неверно. Дробные числа безопасно приводятся к целым."
               }),
        ],
    },
    {
        "key": "strings",
        "title_en": "Strings",
        "title_ru": "Строки",
        "description_en": "Indexing, slicing, methods, joining, formatting and escapes.",
        "description_ru": "Индексы, срезы, методы, объединение, форматирование и экранирование.",
        "questions": [
            _q("beginner", "Which value is a string?", "Какое значение является строкой?", "'hello'", ["42", "True", "[1, 2]"],
               explanation_en="Strings in Python are surrounded by single or double quotation marks.",
               explanation_ru="Строки в Python заключаются в одинарные или двойные кавычки.",
               option_rationales_en={
                   "'hello'": "Correct. It is surrounded by quotation marks.",
                   "42": "Incorrect. This is an integer.",
                   "True": "Incorrect. This is a boolean.",
                   "[1, 2]": "Incorrect. This is a list."
               },
               option_rationales_ru={
                   "'hello'": "Верно. Значение заключено в кавычки.",
                   "42": "Неверно. Это целое число.",
                   "True": "Неверно. Это логическое значение.",
                   "[1, 2]": "Неверно. Это список."
               }),
            _q("intermediate", "What is 'Python'[0]?", "Чему равно 'Python'[0]?", "P", ["y", "Python", "0"],
               explanation_en="Python uses 0-based indexing, so index 0 is the very first character.",
               explanation_ru="Python использует индексацию с 0, поэтому индекс 0 — это самый первый символ.",
               option_rationales_en={
                   "P": "Correct. 'P' is the first letter, located at index 0.",
                   "y": "Incorrect. 'y' is at index 1.",
                   "Python": "Incorrect. The [0] syntax extracts only a single character.",
                   "0": "Incorrect. It extracts the character at that position, not the index itself."
               },
               option_rationales_ru={
                   "P": "Верно. 'P' — первая буква, находящаяся под индексом 0.",
                   "y": "Неверно. Буква 'y' находится под индексом 1.",
                   "Python": "Неверно. Синтаксис [0] извлекает только один символ.",
                   "0": "Неверно. Извлекается символ по позиции, а не сам индекс."
               }),
            _q("advanced", "What is 'coding'[1:4]?", "Чему равно 'coding'[1:4]?", "odi", ["cod", "oding", "di"],
               explanation_en="Slicing [start:end] starts at index 1 ('o') and stops before index 4 ('n').",
               explanation_ru="Срез [start:end] начинается с индекса 1 ('o') и останавливается перед индексом 4 ('n').",
               option_rationales_en={
                   "odi": "Correct. Index 1 is 'o', 2 is 'd', 3 is 'i'. It stops before 4.",
                   "cod": "Incorrect. That would be [0:3].",
                   "oding": "Incorrect. That would be [1:].",
                   "di": "Incorrect. It includes the character at index 1."
               },
               option_rationales_ru={
                   "odi": "Верно. Индекс 1 — это 'o', 2 — 'd', 3 — 'i'. Срез останавливается перед 4.",
                   "cod": "Неверно. Это был бы срез [0:3].",
                   "oding": "Неверно. Это был бы срез [1:].",
                   "di": "Неверно. Срез должен включать символ с индексом 1."
               }),
        ],
    },
    {
        "key": "booleans",
        "title_en": "Booleans",
        "title_ru": "Логические значения",
        "description_en": "True, False, comparisons and truthy or falsy values.",
        "description_ru": "True, False, сравнения и истинность значений.",
        "questions": [
            _q("beginner", "Which are Python's boolean values?", "Какие логические значения есть в Python?", "True and False", ["Yes and No", "1 and 2", "On and Off"],
               explanation_en="Python has exactly two boolean values: True and False (capitalized).",
               explanation_ru="В Python есть ровно два логических значения: True и False (с заглавной буквы).",
               option_rationales_en={
                   "True and False": "Correct. These are Python's built-in boolean values.",
                   "Yes and No": "Incorrect. Python does not use Yes/No.",
                   "1 and 2": "Incorrect. These are integers. (Although 1 and 0 can act like booleans).",
                   "On and Off": "Incorrect. Python does not use On/Off."
               },
               option_rationales_ru={
                   "True and False": "Верно. Это встроенные логические значения Python.",
                   "Yes and No": "Неверно. Python не использует Yes/No.",
                   "1 and 2": "Неверно. Это целые числа.",
                   "On and Off": "Неверно. В Python нет значений On/Off."
               }),
            _q("intermediate", "What is 8 > 3?", "Чему равно 8 > 3?", "True", ["False", "8", "3"],
               explanation_en="8 is greater than 3, so the comparison evaluates to True.",
               explanation_ru="8 больше 3, поэтому сравнение возвращает True.",
               option_rationales_en={
                   "True": "Correct. The mathematical statement is correct.",
                   "False": "Incorrect. 8 is not less than or equal to 3.",
                   "8": "Incorrect. A comparison returns a boolean, not the numbers themselves.",
                   "3": "Incorrect. A comparison returns a boolean."
               },
               option_rationales_ru={
                   "True": "Верно. Математическое утверждение корректно.",
                   "False": "Неверно. 8 не меньше или равно 3.",
                   "8": "Неверно. Операция сравнения возвращает логическое значение.",
                   "3": "Неверно. Сравнение возвращает логическое значение."
               }),
            _q("advanced", "What is bool('')?", "Чему равно bool('')?", "False", ["True", "None", "An error"],
               explanation_en="Empty collections, including empty strings, evaluate to False in Python.",
               explanation_ru="Пустые коллекции, включая пустые строки, преобразуются в False в Python.",
               option_rationales_en={
                   "False": "Correct. An empty string is 'falsy'.",
                   "True": "Incorrect. Any non-empty string is True, but this string is empty.",
                   "None": "Incorrect. bool() only ever returns True or False.",
                   "An error": "Incorrect. bool() can convert any Python object."
               },
               option_rationales_ru={
                   "False": "Верно. Пустая строка считается 'ложной' (falsy).",
                   "True": "Неверно. Любая непустая строка даёт True, но эта пустая.",
                   "None": "Неверно. bool() всегда возвращает только True или False.",
                   "An error": "Неверно. bool() может преобразовать любой объект Python."
               }),
        ],
    },
    {
        "key": "operators",
        "title_en": "Operators",
        "title_ru": "Операторы",
        "description_en": "Arithmetic, assignment, comparison, logical and membership operators.",
        "description_ru": "Арифметические операторы, присваивание, сравнение, логика и принадлежность.",
        "questions": [
            _q("beginner", "Which operator adds two numbers?", "Какой оператор складывает два числа?", "+", ["-", "*", "=="],
               explanation_en="The + operator is used for addition.",
               explanation_ru="Оператор + используется для сложения.",
               option_rationales_en={
                   "+": "Correct. This is the addition operator.",
                   "-": "Incorrect. This is for subtraction.",
                   "*": "Incorrect. This is for multiplication.",
                   "==": "Incorrect. This is for equality comparison."
               },
               option_rationales_ru={
                   "+": "Верно. Это оператор сложения.",
                   "-": "Неверно. Это оператор вычитания.",
                   "*": "Неверно. Это оператор умножения.",
                   "==": "Неверно. Это оператор проверки на равенство."
               }),
            _q("intermediate", "What is 11 // 4?", "Чему равно 11 // 4?", "2", ["2.75", "3", "1"],
               explanation_en="The // operator performs floor division, discarding the remainder.",
               explanation_ru="Оператор // выполняет целочисленное деление, отбрасывая остаток.",
               option_rationales_en={
                   "2": "Correct. 11 divided by 4 is 2.75, and floor division truncates it to 2.",
                   "2.75": "Incorrect. That would be the result of normal division (11 / 4).",
                   "3": "Incorrect. Floor division rounds down, not to the nearest integer.",
                   "1": "Incorrect. 11 divided by 4 goes into it 2 times, not 1."
               },
               option_rationales_ru={
                   "2": "Верно. 11 поделить на 4 равно 2.75, и целочисленное деление отбрасывает дробь.",
                   "2.75": "Неверно. Это результат обычного деления (11 / 4).",
                   "3": "Неверно. Целочисленное деление округляет вниз, а не к ближайшему целому.",
                   "1": "Неверно. Четвёрка помещается в 11 два раза, а не один."
               }),
            _q("advanced", "What is 2 + 3 * 4?", "Чему равно 2 + 3 * 4?", "14", ["20", "24", "10"],
               explanation_en="Python follows standard mathematical order of operations (PEMDAS), so multiplication happens before addition.",
               explanation_ru="Python соблюдает стандартный порядок математических операций, поэтому умножение выполняется перед сложением.",
               option_rationales_en={
                   "14": "Correct. 3 * 4 is 12, plus 2 is 14.",
                   "20": "Incorrect. This would happen if you did (2 + 3) * 4.",
                   "24": "Incorrect. This is not how the math works out.",
                   "10": "Incorrect. Math operations must follow proper order."
               },
               option_rationales_ru={
                   "14": "Верно. Сначала 3 * 4 равно 12, плюс 2 равно 14.",
                   "20": "Неверно. Так было бы при (2 + 3) * 4.",
                   "24": "Неверно. Математически это неверный ответ.",
                   "10": "Неверно. Операции должны выполняться в правильном порядке."
               }),
        ],
    },
    {
        "key": "lists",
        "title_en": "Lists",
        "title_ru": "Списки",
        "description_en": "Accessing, changing, adding, removing, sorting and copying list items.",
        "description_ru": "Доступ, изменение, добавление, удаление, сортировка и копирование списков.",
        "questions": [
            _q("beginner", "Which brackets create a list?", "Какие скобки создают список?", "[]", ["()", "{}", "<>"],
               explanation_en="Lists are created using square brackets.",
               explanation_ru="Списки создаются с помощью квадратных скобок.",
               option_rationales_en={
                   "[]": "Correct. Square brackets represent lists.",
                   "()": "Incorrect. Parentheses represent tuples.",
                   "{}": "Incorrect. Curly braces represent dictionaries or sets.",
                   "<>": "Incorrect. Angle brackets are not used for collections in Python."
               },
               option_rationales_ru={
                   "[]": "Верно. Квадратные скобки обозначают списки.",
                   "()": "Неверно. Круглые скобки обозначают кортежи.",
                   "{}": "Неверно. Фигурные скобки обозначают словари или множества.",
                   "<>": "Неверно. Угловые скобки не используются для коллекций в Python."
               }),
            _q("intermediate", "Which method adds one item to the end of a list?", "Какой метод добавляет один элемент в конец списка?", "append()", ["add()", "push()", "join()"],
               explanation_en="The append() method modifies the list by placing the new item at the very end.",
               explanation_ru="Метод append() изменяет список, помещая новый элемент в самый конец.",
               option_rationales_en={
                   "append()": "Correct. This is the built-in method for adding an item to a list.",
                   "add()": "Incorrect. add() is used for sets, not lists.",
                   "push()": "Incorrect. push() is used in JavaScript, but not natively for Python lists.",
                   "join()": "Incorrect. join() combines a list of strings into a single string."
               },
               option_rationales_ru={
                   "append()": "Верно. Это встроенный метод для добавления элемента в список.",
                   "add()": "Неверно. add() используется для множеств, а не списков.",
                   "push()": "Неверно. push() используется в JS, а не в списках Python.",
                   "join()": "Неверно. join() объединяет список строк в одну строку."
               }),
            _q("advanced", "What is [x * 2 for x in range(3)]?", "Чему равно [x * 2 for x in range(3)]?", "[0, 2, 4]", ["[2, 4, 6]", "[0, 1, 2]", "[0, 2, 4, 6]"],
               explanation_en="This is a list comprehension. range(3) produces 0, 1, 2. Multiplying each by 2 gives 0, 2, 4.",
               explanation_ru="Это генератор списков. range(3) даёт 0, 1, 2. Умножение каждого на 2 даёт 0, 2, 4.",
               option_rationales_en={
                   "[0, 2, 4]": "Correct. 0*2=0, 1*2=2, and 2*2=4.",
                   "[2, 4, 6]": "Incorrect. range(3) starts at 0, not 1.",
                   "[0, 1, 2]": "Incorrect. This is just list(range(3)) without the multiplication.",
                   "[0, 2, 4, 6]": "Incorrect. range(3) produces 3 items, not 4."
               },
               option_rationales_ru={
                   "[0, 2, 4]": "Верно. 0*2=0, 1*2=2 и 2*2=4.",
                   "[2, 4, 6]": "Неверно. range(3) начинается с 0, а не с 1.",
                   "[0, 1, 2]": "Неверно. Это просто list(range(3)) без умножения.",
                   "[0, 2, 4, 6]": "Неверно. range(3) генерирует 3 элемента, а не 4."
               }),
        ],
    },
    {
        "key": "tuples",
        "title_en": "Tuples",
        "title_ru": "Кортежи",
        "description_en": "Ordered immutable collections, packing and unpacking.",
        "description_ru": "Упорядоченные неизменяемые коллекции, упаковка и распаковка.",
        "questions": [
            _q("beginner", "Which brackets usually create a tuple?", "Какие скобки обычно создают кортеж?", "()", ["[]", "{}", "<>"],
               explanation_en="Tuples are created using parentheses, though the commas are what truly define them.",
               explanation_ru="Кортежи создаются с помощью круглых скобок, хотя истинным определителем служат запятые.",
               option_rationales_en={
                   "()": "Correct. Parentheses group tuple items.",
                   "[]": "Incorrect. Square brackets are for lists.",
                   "{}": "Incorrect. Curly braces are for dictionaries and sets.",
                   "<>": "Incorrect. Angle brackets are not used for collections."
               },
               option_rationales_ru={
                   "()": "Верно. Круглые скобки группируют элементы кортежа.",
                   "[]": "Неверно. Квадратные скобки для списков.",
                   "{}": "Неверно. Фигурные скобки для словарей и множеств.",
                   "<>": "Неверно. Угловые скобки не используются для коллекций."
               }),
            _q("intermediate", "Can tuple items be changed directly?", "Можно ли напрямую изменить элементы кортежа?", "No", ["Yes, always", "Only strings", "Only the first item"],
               explanation_en="Tuples are immutable, meaning their elements cannot be changed after creation.",
               explanation_ru="Кортежи неизменяемы, что означает, что их элементы нельзя изменить после создания.",
               option_rationales_en={
                   "No": "Correct. Tuples are completely immutable.",
                   "Yes, always": "Incorrect. Lists are mutable, but tuples are not.",
                   "Only strings": "Incorrect. No items can be changed, regardless of type.",
                   "Only the first item": "Incorrect. All items are permanently fixed."
               },
               option_rationales_ru={
                   "No": "Верно. Кортежи полностью неизменяемы.",
                   "Yes, always": "Неверно. Списки изменяемы, а кортежи нет.",
                   "Only strings": "Неверно. Никакие элементы нельзя менять, независимо от типа.",
                   "Only the first item": "Неверно. Все элементы фиксированы навсегда."
               }),
            _q("advanced", "What is needed for a one-item tuple?", "Что необходимо для кортежа из одного элемента?", "A trailing comma", ["Two values", "Square brackets", "The tuple keyword"],
               explanation_en="A single item in parentheses is evaluated as a mathematical expression unless there's a comma.",
               explanation_ru="Один элемент в скобках вычисляется как математическое выражение, если нет запятой.",
               option_rationales_en={
                   "A trailing comma": "Correct. (5,) is a tuple, while (5) is just an integer.",
                   "Two values": "Incorrect. A tuple can have one item if it has a comma.",
                   "Square brackets": "Incorrect. Square brackets make a list.",
                   "The tuple keyword": "Incorrect. While tuple() works, a trailing comma is the standard syntax."
               },
               option_rationales_ru={
                   "A trailing comma": "Верно. (5,) — это кортеж, тогда как (5) — просто целое число.",
                   "Two values": "Неверно. Кортеж может иметь один элемент при наличии запятой.",
                   "Square brackets": "Неверно. Квадратные скобки создают список.",
                   "The tuple keyword": "Неверно. Использование запятой — основной синтаксис для кортежей."
               }),
        ],
    },
    {
        "key": "sets",
        "title_en": "Sets and Frozensets",
        "title_ru": "Множества и frozenset",
        "description_en": "Unique items, set operations and immutable frozensets.",
        "description_ru": "Уникальные элементы, операции множеств и неизменяемый frozenset.",
        "questions": [
            _q("beginner", "What does a set remove automatically?", "Что множество удаляет автоматически?", "Duplicate values", ["All numbers", "All strings", "The first value"],
               explanation_en="Sets only store unique elements, automatically dropping any duplicates.",
               explanation_ru="Множества хранят только уникальные элементы, автоматически удаляя дубликаты.",
               option_rationales_en={
                   "Duplicate values": "Correct. A set cannot contain two of the same item.",
                   "All numbers": "Incorrect. Sets can contain numbers perfectly fine.",
                   "All strings": "Incorrect. Sets can contain strings perfectly fine.",
                   "The first value": "Incorrect. Order doesn't matter, but it only drops duplicates."
               },
               option_rationales_ru={
                   "Duplicate values": "Верно. Множество не может содержать двух одинаковых элементов.",
                   "All numbers": "Неверно. Множества отлично работают с числами.",
                   "All strings": "Неверно. Множества отлично работают со строками.",
                   "The first value": "Неверно. Порядок не имеет значения, удаляются только дубликаты."
               }),
            _q("intermediate", "Which method adds an item to a set?", "Какой метод добавляет элемент в множество?", "add()", ["append()", "push()", "insert()"],
               explanation_en="The add() method places a new item into a set.",
               explanation_ru="Метод add() помещает новый элемент в множество.",
               option_rationales_en={
                   "add()": "Correct. This is the set method for adding elements.",
                   "append()": "Incorrect. append() is used for lists.",
                   "push()": "Incorrect. push() is not a native Python set method.",
                   "insert()": "Incorrect. insert() is used for lists because sets are unordered."
               },
               option_rationales_ru={
                   "add()": "Верно. Это метод множества для добавления элементов.",
                   "append()": "Неверно. append() используется для списков.",
                   "push()": "Неверно. push() нет в стандартных методах множеств Python.",
                   "insert()": "Неверно. insert() используется для списков, так как множества не упорядочены."
               }),
            _q("advanced", "Which operator finds common items in two sets?", "Какой оператор находит общие элементы двух множеств?", "&", ["|", "+", "//"],
               explanation_en="The & operator performs a set intersection, returning items found in both sets.",
               explanation_ru="Оператор & выполняет пересечение множеств, возвращая элементы, присутствующие в обоих множествах.",
               option_rationales_en={
                   "&": "Correct. This is the intersection operator.",
                   "|": "Incorrect. This is the union operator (combines items).",
                   "+": "Incorrect. The + operator is not supported for sets.",
                   "//": "Incorrect. This is floor division for numbers."
               },
               option_rationales_ru={
                   "&": "Верно. Это оператор пересечения.",
                   "|": "Неверно. Это оператор объединения.",
                   "+": "Неверно. Оператор + не поддерживается для множеств.",
                   "//": "Неверно. Это целочисленное деление для чисел."
               }),
        ],
    },
    {
        "key": "dictionaries",
        "title_en": "Dictionaries",
        "title_ru": "Словари",
        "description_en": "Key-value data, access, updates, loops and nested dictionaries.",
        "description_ru": "Пары ключ-значение, доступ, изменение, циклы и вложенные словари.",
        "questions": [
            _q("beginner", "A dictionary stores data as what?", "В каком виде словарь хранит данные?", "Key-value pairs", ["Only numbers", "Rows and columns", "Unique values only"],
               explanation_en="Dictionaries map unique keys to specific values.",
               explanation_ru="Словари связывают уникальные ключи с определёнными значениями.",
               option_rationales_en={
                   "Key-value pairs": "Correct. Like {'name': 'Alice'}.",
                   "Only numbers": "Incorrect. Dictionaries can store strings, lists, objects, etc.",
                   "Rows and columns": "Incorrect. That describes a 2D array or database table.",
                   "Unique values only": "Incorrect. Values can repeat; only the keys must be unique."
               },
               option_rationales_ru={
                   "Key-value pairs": "Верно. Например, {'name': 'Alice'}.",
                   "Only numbers": "Неверно. Словари могут хранить строки, списки и другие объекты.",
                   "Rows and columns": "Неверно. Это описывает двумерный массив или таблицу БД.",
                   "Unique values only": "Неверно. Значения могут повторяться, уникальными должны быть только ключи."
               }),
            _q("intermediate", "How do you read the age in {'age': 12}?", "Как получить age из {'age': 12}?", "data['age']", ["data.age()", "data(0)", "data->age"],
               explanation_en="Dictionary values are accessed using square brackets and the key name.",
               explanation_ru="Доступ к значениям словаря осуществляется с помощью квадратных скобок и имени ключа.",
               option_rationales_en={
                   "data['age']": "Correct. This is the standard syntax for accessing a dictionary by key.",
                   "data.age()": "Incorrect. This looks like a method call.",
                   "data(0)": "Incorrect. Dictionaries are not accessed by numerical index in parentheses.",
                   "data->age": "Incorrect. This syntax is used in PHP or C++, not Python."
               },
               option_rationales_ru={
                   "data['age']": "Верно. Это стандартный синтаксис доступа к словарю по ключу.",
                   "data.age()": "Неверно. Это похоже на вызов метода.",
                   "data(0)": "Неверно. Доступ к словарям не осуществляется по числовому индексу в скобках.",
                   "data->age": "Неверно. Этот синтаксис используется в PHP или C++, а не в Python."
               }),
            _q("advanced", "Which method safely returns a value or a default?", "Какой метод безопасно возвращает значение или значение по умолчанию?", "get()", ["append()", "sort()", "index()"],
               explanation_en="The get() method returns None or a specified default if the key does not exist.",
               explanation_ru="Метод get() возвращает None или указанное значение по умолчанию, если ключ не существует.",
               option_rationales_en={
                   "get()": "Correct. dict.get('key', 'default') is safe and avoids KeyError.",
                   "append()": "Incorrect. This is a list method.",
                   "sort()": "Incorrect. This is a list method.",
                   "index()": "Incorrect. This is used in lists to find an item's position."
               },
               option_rationales_ru={
                   "get()": "Верно. dict.get('key', 'default') безопасно и избегает KeyError.",
                   "append()": "Неверно. Это метод списков.",
                   "sort()": "Неверно. Это метод списков.",
                   "index()": "Неверно. Используется в списках для поиска позиции элемента."
               }),
        ],
    },
    {
        "key": "conditions",
        "title_en": "If, Elif and Else",
        "title_ru": "Условия if, elif и else",
        "description_en": "Making decisions, combining conditions and nested if statements.",
        "description_ru": "Принятие решений, объединение условий и вложенные условия.",
        "questions": [
            _q("beginner", "Which keyword begins a condition?", "Какое ключевое слово начинает условие?", "if", ["for", "def", "try"],
               explanation_en="The 'if' keyword is used to conditionally execute code.",
               explanation_ru="Ключевое слово 'if' используется для условного выполнения кода.",
               option_rationales_en={
                   "if": "Correct. 'if' starts a conditional block.",
                   "for": "Incorrect. 'for' starts a loop.",
                   "def": "Incorrect. 'def' defines a function.",
                   "try": "Incorrect. 'try' starts an exception handling block."
               },
               option_rationales_ru={
                   "if": "Верно. 'if' начинает условный блок.",
                   "for": "Неверно. 'for' начинает цикл.",
                   "def": "Неверно. 'def' создаёт функцию.",
                   "try": "Неверно. 'try' начинает блок обработки исключений."
               }),
            _q("intermediate", "Which block runs when earlier conditions are false?", "Какой блок выполняется, если предыдущие условия ложны?", "else", ["import", "return", "while"],
               explanation_en="The 'else' block catches any cases where the 'if' and 'elif' conditions were not met.",
               explanation_ru="Блок 'else' перехватывает случаи, когда условия 'if' и 'elif' не были выполнены.",
               option_rationales_en={
                   "else": "Correct. 'else' acts as a catch-all at the end of a condition chain.",
                   "import": "Incorrect. 'import' brings in external modules.",
                   "return": "Incorrect. 'return' sends a value back from a function.",
                   "while": "Incorrect. 'while' starts a loop."
               },
               option_rationales_ru={
                   "else": "Верно. 'else' срабатывает в самом конце, если всё остальное ложно.",
                   "import": "Неверно. 'import' подключает внешние модули.",
                   "return": "Неверно. 'return' возвращает значение из функции.",
                   "while": "Неверно. 'while' начинает цикл."
               }),
            _q("advanced", "What does pass do inside an empty if block?", "Что делает pass внутри пустого блока if?", "It performs no action", ["It stops Python", "It repeats the block", "It prints pass"],
               explanation_en="The 'pass' statement is a null operation; it does nothing but allows empty blocks to be syntactically valid.",
               explanation_ru="Инструкция 'pass' — это пустая операция; она ничего не делает, но позволяет синтаксически корректно оформлять пустые блоки.",
               option_rationales_en={
                   "It performs no action": "Correct. 'pass' is a placeholder that does nothing.",
                   "It stops Python": "Incorrect. It just skips to the next line.",
                   "It repeats the block": "Incorrect. That requires loop constructs.",
                   "It prints pass": "Incorrect. It produces no output."
               },
               option_rationales_ru={
                   "It performs no action": "Верно. 'pass' — это заглушка, которая ничего не делает.",
                   "It stops Python": "Неверно. Исполнение переходит на следующую строку.",
                   "It repeats the block": "Неверно. Для этого нужны конструкции цикла.",
                   "It prints pass": "Неверно. Она не выводит текст."
               }),
        ],
    },
    {
        "key": "match",
        "title_en": "Match",
        "title_ru": "Конструкция match",
        "description_en": "Selecting a case with match and case patterns.",
        "description_ru": "Выбор варианта с помощью match и шаблонов case.",
        "questions": [
            _q("beginner", "Which keyword starts pattern matching?", "Какое слово начинает сопоставление с образцом?", "match", ["switch", "choose", "select"],
               explanation_en="In Python 3.10+, 'match' starts a structural pattern matching block.",
               explanation_ru="В Python 3.10+ 'match' начинает блок сопоставления с образцом.",
               option_rationales_en={
                   "match": "Correct. 'match' tests a value against multiple patterns.",
                   "switch": "Incorrect. Python does not use 'switch' (used in C/Java).",
                   "choose": "Incorrect. This is not a Python keyword.",
                   "select": "Incorrect. This is not a Python keyword (used in SQL/Go)."
               },
               option_rationales_ru={
                   "match": "Верно. 'match' проверяет значение по нескольким шаблонам.",
                   "switch": "Неверно. Python не использует 'switch' (используется в C/Java).",
                   "choose": "Неверно. Это не ключевое слово Python.",
                   "select": "Неверно. Это не ключевое слово Python (используется в SQL/Go)."
               }),
            _q("intermediate", "Which keyword defines one match branch?", "Какое слово задаёт одну ветку match?", "case", ["when", "elif", "branch"],
               explanation_en="Inside a 'match' block, each pattern starts with 'case'.",
               explanation_ru="Внутри блока 'match' каждый шаблон начинается с 'case'.",
               option_rationales_en={
                   "case": "Correct. Each potential match branch starts with 'case'.",
                   "when": "Incorrect. 'when' can be used as a guard clause, but not to start the branch.",
                   "elif": "Incorrect. 'elif' is used with 'if'.",
                   "branch": "Incorrect. 'branch' is not a Python keyword."
               },
               option_rationales_ru={
                   "case": "Верно. Каждая потенциальная ветка начинается с 'case'.",
                   "when": "Неверно. 'when' используется для дополнительных условий, а не для старта ветки.",
                   "elif": "Неверно. 'elif' используется в конструкциях 'if'.",
                   "branch": "Неверно. 'branch' — не ключевое слово Python."
               }),
            _q("advanced", "Which pattern acts as the default case?", "Какой шаблон работает как вариант по умолчанию?", "_", ["*", "default", "else"],
               explanation_en="The underscore '_' is the wildcard pattern that matches anything not caught by previous cases.",
               explanation_ru="Подчёркивание '_' — это шаблон-маска, который совпадает с любым значением, не пойманным предыдущими 'case'.",
               option_rationales_en={
                   "_": "Correct. 'case _:' acts as the default fallback.",
                   "*": "Incorrect. '*' is not used as the default pattern.",
                   "default": "Incorrect. 'default' is used in switch statements in other languages.",
                   "else": "Incorrect. 'else' is used with 'if', not 'match'."
               },
               option_rationales_ru={
                   "_": "Верно. 'case _:' работает как запасной вариант.",
                   "*": "Неверно. '*' не используется как шаблон по умолчанию.",
                   "default": "Неверно. 'default' используется в операторах switch других языков.",
                   "else": "Неверно. 'else' используется с 'if', а не с 'match'."
               }),
        ],
    },
    {
        "key": "while",
        "title_en": "While Loops",
        "title_ru": "Циклы while",
        "description_en": "Repeating while a condition is true, break and continue.",
        "description_ru": "Повторение, пока условие истинно, break и continue.",
        "questions": [
            _q("beginner", "A while loop repeats while what is true?", "Цикл while повторяется, пока истинно что?", "Its condition", ["A file", "A comment", "A function name"],
               explanation_en="A while loop keeps running as long as its condition evaluates to True.",
               explanation_ru="Цикл while продолжает работу до тех пор, пока его условие оценивается как True.",
               option_rationales_en={
                   "Its condition": "Correct. The code runs repeatedly if the condition is True.",
                   "A file": "Incorrect. Files do not determine loop continuation directly.",
                   "A comment": "Incorrect. Comments are completely ignored by Python.",
                   "A function name": "Incorrect. Loop continuation is based on boolean logic."
               },
               option_rationales_ru={
                   "Its condition": "Верно. Код выполняется многократно, если условие истинно.",
                   "A file": "Неверно. Файлы не определяют напрямую продолжение цикла.",
                   "A comment": "Неверно. Комментарии полностью игнорируются Python.",
                   "A function name": "Неверно. Продолжение цикла зависит от логического выражения."
               }),
            _q("intermediate", "Which keyword exits a loop immediately?", "Какое слово немедленно завершает цикл?", "break", ["continue", "pass", "next"],
               explanation_en="The 'break' statement stops the loop completely and moves to the code after the loop.",
               explanation_ru="Инструкция 'break' полностью останавливает цикл и переходит к коду после него.",
               option_rationales_en={
                   "break": "Correct. It immediately breaks out of the loop.",
                   "continue": "Incorrect. It skips to the next iteration, but keeps looping.",
                   "pass": "Incorrect. It does nothing.",
                   "next": "Incorrect. It gets the next item from an iterator, but doesn't exit the loop."
               },
               option_rationales_ru={
                   "break": "Верно. Она немедленно прерывает выполнение цикла.",
                   "continue": "Неверно. Она переходит к следующей итерации, но продолжает цикл.",
                   "pass": "Неверно. Она ничего не делает.",
                   "next": "Неверно. Запрашивает следующий элемент у итератора, но не прерывает цикл."
               }),
            _q("advanced", "Which keyword skips to the next loop iteration?", "Какое слово переходит к следующей итерации?", "continue", ["break", "return", "stop"],
               explanation_en="The 'continue' statement stops the current iteration and jumps back to the top of the loop.",
               explanation_ru="Инструкция 'continue' останавливает текущую итерацию и прыгает обратно в начало цикла.",
               option_rationales_en={
                   "continue": "Correct. It skips the rest of the block and continues the loop.",
                   "break": "Incorrect. 'break' stops the loop entirely.",
                   "return": "Incorrect. 'return' exits the entire function.",
                   "stop": "Incorrect. 'stop' is not a Python keyword."
               },
               option_rationales_ru={
                   "continue": "Верно. Она пропускает остаток блока и продолжает цикл.",
                   "break": "Неверно. 'break' останавливает цикл полностью.",
                   "return": "Неверно. 'return' выходит из всей функции.",
                   "stop": "Неверно. 'stop' — не ключевое слово Python."
               }),
        ],
    },
    {
        "key": "for_range",
        "title_en": "For Loops and Range",
        "title_ru": "Циклы for и range",
        "description_en": "Looping over collections and generating number sequences.",
        "description_ru": "Перебор коллекций и создание последовательностей чисел.",
        "questions": [
            _q("beginner", "Which loop is commonly used to visit every list item?", "Какой цикл обычно перебирает все элементы списка?", "for", ["if", "try", "match"],
               explanation_en="The 'for' loop is the standard way to iterate over elements in a collection (like a list).",
               explanation_ru="Цикл 'for' — стандартный способ перебора элементов коллекции (например, списка).",
               option_rationales_en={
                   "for": "Correct. 'for item in list' iterates over each item.",
                   "if": "Incorrect. 'if' is a conditional statement.",
                   "try": "Incorrect. 'try' is used for error handling.",
                   "match": "Incorrect. 'match' is used for pattern matching."
               },
               option_rationales_ru={
                   "for": "Верно. Конструкция 'for item in list' перебирает каждый элемент.",
                   "if": "Неверно. 'if' — это условный оператор.",
                   "try": "Неверно. 'try' используется для обработки ошибок.",
                   "match": "Неверно. 'match' используется для сопоставления с образцом."
               }),
            _q("intermediate", "What numbers come from range(3)?", "Какие числа создаёт range(3)?", "0, 1, 2", ["1, 2, 3", "0, 1, 2, 3", "3 only"],
               explanation_en="range(N) generates numbers starting from 0 and stopping before N.",
               explanation_ru="range(N) создаёт числа, начиная с 0 и останавливаясь перед N.",
               option_rationales_en={
                   "0, 1, 2": "Correct. It starts at 0 and produces exactly 3 numbers.",
                   "1, 2, 3": "Incorrect. By default, range starts at 0, not 1.",
                   "0, 1, 2, 3": "Incorrect. It stops before the given number.",
                   "3 only": "Incorrect. range() produces a sequence of numbers."
               },
               option_rationales_ru={
                   "0, 1, 2": "Верно. Начинается с 0 и выдаёт ровно 3 числа.",
                   "1, 2, 3": "Неверно. По умолчанию range начинается с 0, а не с 1.",
                   "0, 1, 2, 3": "Неверно. Он останавливается перед указанным числом.",
                   "3 only": "Неверно. range() выдаёт последовательность чисел."
               }),
            _q("advanced", "What numbers come from range(2, 8, 2)?", "Какие числа создаёт range(2, 8, 2)?", "2, 4, 6", ["2, 4, 6, 8", "2, 3, 4, 5, 6, 7", "0, 2, 4, 6"],
               explanation_en="range(start, stop, step) begins at 2, increases by 2, and stops before 8.",
               explanation_ru="range(start, stop, step) начинается с 2, увеличивается на 2 и останавливается перед 8.",
               option_rationales_en={
                   "2, 4, 6": "Correct. Starts at 2, goes up by 2, and stops before 8.",
                   "2, 4, 6, 8": "Incorrect. It must stop before 8, not include it.",
                   "2, 3, 4, 5, 6, 7": "Incorrect. This is what range(2, 8) produces with a step of 1.",
                   "0, 2, 4, 6": "Incorrect. The sequence was specified to start at 2."
               },
               option_rationales_ru={
                   "2, 4, 6": "Верно. Начинается с 2, шагает по 2, останавливается перед 8.",
                   "2, 4, 6, 8": "Неверно. Диапазон должен остановиться перед 8, не включая его.",
                   "2, 3, 4, 5, 6, 7": "Неверно. Это результат range(2, 8) с шагом 1.",
                   "0, 2, 4, 6": "Неверно. Было указано, что старт с 2."
               }),
        ],
    },
    {
        "key": "functions",
        "title_en": "Functions",
        "title_ru": "Функции",
        "description_en": "Defining functions, parameters, return values and reusable code.",
        "description_ru": "Создание функций, параметры, возвращаемые значения и повторное использование кода.",
        "questions": [
            _q("beginner", "Which keyword defines a function?", "Какое слово создаёт функцию?", "def", ["func", "make", "return"],
               explanation_en="In Python, functions are defined using the 'def' keyword.",
               explanation_ru="В Python функции объявляются с помощью ключевого слова 'def'.",
               option_rationales_en={
                   "def": "Correct. 'def' stands for define.",
                   "func": "Incorrect. This keyword is used in Go or Swift, not Python.",
                   "make": "Incorrect. This is not a Python keyword.",
                   "return": "Incorrect. 'return' is used inside the function, not to define it."
               },
               option_rationales_ru={
                   "def": "Верно. Сокращение от define.",
                   "func": "Неверно. Это слово используется в Go или Swift.",
                   "make": "Неверно. В Python нет такого ключевого слова.",
                   "return": "Неверно. 'return' используется внутри функции."
               }),
            _q("intermediate", "Which keyword sends a value back from a function?", "Какое слово возвращает значение из функции?", "return", ["print", "yield", "break"],
               explanation_en="The 'return' statement exits the function and passes a value back to the caller.",
               explanation_ru="Инструкция 'return' завершает функцию и передаёт значение обратно вызывающему коду.",
               option_rationales_en={
                   "return": "Correct. It provides the function's final output to the caller.",
                   "print": "Incorrect. 'print' just displays text, it does not send data back.",
                   "yield": "Incorrect. 'yield' is used in generators to provide a series of values, not a single normal exit.",
                   "break": "Incorrect. 'break' is used to exit loops."
               },
               option_rationales_ru={
                   "return": "Верно. Она предоставляет результат работы функции вызывающему коду.",
                   "print": "Неверно. 'print' лишь выводит текст на экран.",
                   "yield": "Неверно. Используется в генераторах для выдачи последовательности значений.",
                   "break": "Неверно. 'break' используется для выхода из циклов."
               }),
            _q("advanced", "What is a parameter?", "Что такое параметр?", "A name in a function definition", ["The final printed value", "A Python file", "A loop condition"],
               explanation_en="Parameters are the variable names specified inside the parentheses of a function definition.",
               explanation_ru="Параметры — это имена переменных, указанные внутри круглых скобок при определении функции.",
               option_rationales_en={
                   "A name in a function definition": "Correct. Parameters act as placeholders for the arguments passed into the function.",
                   "The final printed value": "Incorrect. That is just output.",
                   "A Python file": "Incorrect. That is a module or script.",
                   "A loop condition": "Incorrect. Loop conditions are boolean expressions."
               },
               option_rationales_ru={
                   "A name in a function definition": "Верно. Параметры служат псевдонимами для аргументов, переданных функции.",
                   "The final printed value": "Неверно. Это просто вывод.",
                   "A Python file": "Неверно. Это модуль или скрипт.",
                   "A loop condition": "Неверно. Условия цикла — это логические выражения."
               }),
        ],
    },
    {
        "key": "arguments_scope",
        "title_en": "Arguments, *args, **kwargs and Scope",
        "title_ru": "Аргументы, *args, **kwargs и область видимости",
        "description_en": "Flexible arguments and where variables can be accessed.",
        "description_ru": "Гибкие аргументы и доступность переменных.",
        "questions": [
            _q("beginner", "A variable created inside a function is usually what?", "Переменная внутри функции обычно является какой?", "Local", ["Global", "Imported", "Constant"],
               explanation_en="Variables created inside a function are in the local scope and cannot be accessed from outside by default.",
               explanation_ru="Переменные, созданные внутри функции, находятся в локальной области видимости и по умолчанию недоступны снаружи.",
               option_rationales_en={
                   "Local": "Correct. Variables defined inside a function are local to that function.",
                   "Global": "Incorrect. Global variables are defined outside any function.",
                   "Imported": "Incorrect. Imported variables come from other modules.",
                   "Constant": "Incorrect. Constants are variables that are not meant to change, but scope is about visibility."
               },
               option_rationales_ru={
                   "Local": "Верно. Переменные внутри функции локальны для этой функции.",
                   "Global": "Неверно. Глобальные переменные определяются вне функций.",
                   "Imported": "Неверно. Импортированные переменные приходят из других модулей.",
                   "Constant": "Неверно. Константы — это переменные, которые не должны меняться, но область видимости — это про доступность."
               }),
            _q("intermediate", "What does *args collect?", "Что собирает *args?", "Extra positional arguments", ["Only keyword arguments", "Errors", "Modules"],
               explanation_en="The '*args' syntax in a function definition collects any extra positional arguments passed to the function into a tuple.",
               explanation_ru="Синтаксис '*args' в определении функции собирает все дополнительные позиционные аргументы в кортеж.",
               option_rationales_en={
                   "Extra positional arguments": "Correct. It gathers variable-length positional arguments into a tuple.",
                   "Only keyword arguments": "Incorrect. Keyword arguments are collected by **kwargs.",
                   "Errors": "Incorrect. Errors are caught using try-except.",
                   "Modules": "Incorrect. Modules are imported with the import statement."
               },
               option_rationales_ru={
                   "Extra positional arguments": "Верно. Собирает переменное число позиционных аргументов в кортеж.",
                   "Only keyword arguments": "Неверно. Именованные аргументы собираются через **kwargs.",
                   "Errors": "Неверно. Ошибки перехватываются через try-except.",
                   "Modules": "Неверно. Модули загружаются через import."
               }),
            _q("advanced", "What does **kwargs collect?", "Что собирает **kwargs?", "Extra keyword arguments", ["Only numbers", "Loop values", "Return statements"],
               explanation_en="The '**kwargs' syntax collects extra keyword arguments into a dictionary.",
               explanation_ru="Синтаксис '**kwargs' собирает дополнительные именованные аргументы в словарь.",
               option_rationales_en={
                   "Extra keyword arguments": "Correct. It collects named arguments into a dictionary.",
                   "Only numbers": "Incorrect. It collects arguments of any type.",
                   "Loop values": "Incorrect. It has nothing to do with loops.",
                   "Return statements": "Incorrect. Return statements send values back, they don't collect arguments."
               },
               option_rationales_ru={
                   "Extra keyword arguments": "Верно. Собирает именованные аргументы в словарь.",
                   "Only numbers": "Неверно. Собирает аргументы любого типа.",
                   "Loop values": "Неверно. К циклам это не имеет отношения.",
                   "Return statements": "Неверно. Инструкции return возвращают значения, а не собирают их."
               }),
        ],
    },
    {
        "key": "lambda_recursion",
        "title_en": "Lambda and Recursion",
        "title_ru": "Lambda и рекурсия",
        "description_en": "Small anonymous functions and functions that call themselves.",
        "description_ru": "Небольшие анонимные функции и функции, вызывающие сами себя.",
        "questions": [
            _q("beginner", "What creates a small anonymous function?", "Что создаёт небольшую анонимную функцию?", "lambda", ["class", "import", "while"],
               explanation_en="The 'lambda' keyword creates small, unnamed functions typically used for short operations.",
               explanation_ru="Ключевое слово 'lambda' создаёт небольшие безымянные функции для коротких операций.",
               option_rationales_en={
                   "lambda": "Correct. 'lambda' defines an anonymous function.",
                   "class": "Incorrect. 'class' defines an object blueprint.",
                   "import": "Incorrect. 'import' brings in modules.",
                   "while": "Incorrect. 'while' defines a loop."
               },
               option_rationales_ru={
                   "lambda": "Верно. 'lambda' создаёт анонимную функцию.",
                   "class": "Неверно. 'class' описывает структуру объекта.",
                   "import": "Неверно. 'import' загружает модули.",
                   "while": "Неверно. 'while' создаёт цикл."
               }),
            _q("intermediate", "What is recursion?", "Что такое рекурсия?", "A function calling itself", ["A list sorting itself", "A variable changing type", "A module import"],
               explanation_en="Recursion occurs when a function calls itself to solve a smaller piece of a problem.",
               explanation_ru="Рекурсия возникает, когда функция вызывает саму себя для решения меньшей части задачи.",
               option_rationales_en={
                   "A function calling itself": "Correct. Recursion is defined as a function calling itself.",
                   "A list sorting itself": "Incorrect. That is just an in-place sort.",
                   "A variable changing type": "Incorrect. That is type casting.",
                   "A module import": "Incorrect. That's how you bring in code."
               },
               option_rationales_ru={
                   "A function calling itself": "Верно. Рекурсия — это вызов функцией самой себя.",
                   "A list sorting itself": "Неверно. Это просто сортировка списка на месте.",
                   "A variable changing type": "Неверно. Это приведение типов.",
                   "A module import": "Неверно. Это загрузка кода."
               }),
            _q("advanced", "Why does recursion need a base case?", "Зачем рекурсии базовый случай?", "To stop the repeated calls", ["To print every result", "To create a class", "To import math"],
               explanation_en="Without a base case, a recursive function would call itself infinitely until the program crashes.",
               explanation_ru="Без базового случая рекурсивная функция будет вызывать себя бесконечно, пока программа не завершится с ошибкой.",
               option_rationales_en={
                   "To stop the repeated calls": "Correct. The base case stops the infinite loop of self-calling.",
                   "To print every result": "Incorrect. Printing is optional.",
                   "To create a class": "Incorrect. Recursion doesn't require classes.",
                   "To import math": "Incorrect. Math module is unrelated to the concept of recursion."
               },
               option_rationales_ru={
                   "To stop the repeated calls": "Верно. Базовый случай останавливает бесконечный цикл самовызовов.",
                   "To print every result": "Неверно. Вывод на экран не обязателен.",
                   "To create a class": "Неверно. Рекурсии не нужны классы.",
                   "To import math": "Неверно. Модуль math не связан с концепцией рекурсии."
               }),
        ],
    },
    {
        "key": "decorators_generators",
        "title_en": "Decorators and Generators",
        "title_ru": "Декораторы и генераторы",
        "description_en": "Wrapping function behavior and producing values with yield.",
        "description_ru": "Изменение поведения функций и создание значений с yield.",
        "questions": [
            _q("beginner", "Which keyword produces a generator value?", "Какое слово выдаёт значение генератора?", "yield", ["return only", "print", "send"],
               explanation_en="The 'yield' keyword pauses a function and returns a value, allowing it to be resumed later.",
               explanation_ru="Ключевое слово 'yield' приостанавливает функцию и возвращает значение, позволяя возобновить её позже.",
               option_rationales_en={
                   "yield": "Correct. It yields a value and pauses execution state.",
                   "return only": "Incorrect. 'return' terminates the function entirely.",
                   "print": "Incorrect. 'print' just displays output.",
                   "send": "Incorrect. 'send' is used to pass values into a generator, but 'yield' produces them."
               },
               option_rationales_ru={
                   "yield": "Верно. Выдаёт значение и сохраняет состояние функции.",
                   "return only": "Неверно. 'return' полностью завершает функцию.",
                   "print": "Неверно. 'print' только выводит текст.",
                   "send": "Неверно. 'send' отправляет значения в генератор, а 'yield' их выдаёт."
               }),
            _q("intermediate", "Which symbol commonly applies a decorator?", "Какой символ обычно применяет декоратор?", "@", ["#", "$", "&"],
               explanation_en="In Python, decorators are applied to functions using the '@' symbol followed by the decorator name.",
               explanation_ru="В Python декораторы применяются к функциям с помощью символа '@' и имени декоратора.",
               option_rationales_en={
                   "@": "Correct. '@decorator_name' is placed above the function definition.",
                   "#": "Incorrect. '#' is for comments.",
                   "$": "Incorrect. '$' is not used in Python syntax.",
                   "&": "Incorrect. '&' is the bitwise AND operator."
               },
               option_rationales_ru={
                   "@": "Верно. '@имя_декоратора' пишется над определением функции.",
                   "#": "Неверно. '#' используется для комментариев.",
                   "$": "Неверно. '$' не используется в синтаксисе Python.",
                   "&": "Неверно. '&' — это побитовое И."
               }),
            _q("advanced", "What is a key benefit of generators?", "Какое важное преимущество генераторов?", "They produce values lazily", ["They always sort values", "They replace every class", "They disable loops"],
               explanation_en="Generators produce items one at a time (lazily), which saves memory when working with large sequences.",
               explanation_ru="Генераторы выдают элементы по одному (лениво), что экономит память при работе с большими последовательностями.",
               option_rationales_en={
                   "They produce values lazily": "Correct. This means they only generate values when asked, saving memory.",
                   "They always sort values": "Incorrect. They do not sort.",
                   "They replace every class": "Incorrect. They don't replace classes.",
                   "They disable loops": "Incorrect. They are typically used inside loops."
               },
               option_rationales_ru={
                   "They produce values lazily": "Верно. Это означает, что значения генерируются только по запросу, экономя память.",
                   "They always sort values": "Неверно. Генераторы не сортируют данные.",
                   "They replace every class": "Неверно. Они не заменяют классы.",
                   "They disable loops": "Неверно. Обычно они используются внутри циклов."
               }),
        ],
    },
    {
        "key": "arrays_iterators",
        "title_en": "Arrays and Iterators",
        "title_ru": "Массивы и итераторы",
        "description_en": "Array-like lists, iterable objects, iter() and next().",
        "description_ru": "Списки как массивы, итерируемые объекты, iter() и next().",
        "questions": [
            _q("beginner", "Which built-in collection is commonly used as an array in basic Python?", "Какая встроенная коллекция обычно используется как массив в базовом Python?", "list", ["str", "bool", "None"],
               explanation_en="Python 'list' objects are dynamic arrays used to store ordered collections of items.",
               explanation_ru="Списки 'list' в Python — это динамические массивы для хранения упорядоченных коллекций.",
               option_rationales_en={
                   "list": "Correct. Lists are the default array-like structure.",
                   "str": "Incorrect. Strings store text.",
                   "bool": "Incorrect. Booleans represent True or False.",
                   "None": "Incorrect. None represents nothing."
               },
               option_rationales_ru={
                   "list": "Верно. Списки — структура по умолчанию, похожая на массивы.",
                   "str": "Неверно. Строки хранят текст.",
                   "bool": "Неверно. Булевые значения — это True или False.",
                   "None": "Неверно. None означает отсутствие значения."
               }),
            _q("intermediate", "Which function creates an iterator?", "Какая функция создаёт итератор?", "iter()", ["next()", "range()", "open()"],
               explanation_en="The 'iter()' function takes an iterable object (like a list) and returns an iterator.",
               explanation_ru="Функция 'iter()' принимает итерируемый объект (например, список) и возвращает итератор.",
               option_rationales_en={
                   "iter()": "Correct. iter(obj) returns an iterator.",
                   "next()": "Incorrect. next() fetches the next value from an already existing iterator.",
                   "range()": "Incorrect. range() generates a sequence of numbers.",
                   "open()": "Incorrect. open() is for reading/writing files."
               },
               option_rationales_ru={
                   "iter()": "Верно. iter(obj) возвращает итератор.",
                   "next()": "Неверно. next() запрашивает следующее значение у уже существующего итератора.",
                   "range()": "Неверно. range() создаёт последовательность чисел.",
                   "open()": "Неверно. open() используется для файлов."
               }),
            _q("advanced", "Which function requests the next iterator value?", "Какая функция запрашивает следующее значение итератора?", "next()", ["iter()", "step()", "move()"],
               explanation_en="The 'next()' function gets the next item from an iterator object.",
               explanation_ru="Функция 'next()' получает следующий элемент из объекта-итератора.",
               option_rationales_en={
                   "next()": "Correct. It fetches the next element from the iterator.",
                   "iter()": "Incorrect. iter() creates the iterator.",
                   "step()": "Incorrect. There is no step() built-in function.",
                   "move()": "Incorrect. There is no move() built-in function."
               },
               option_rationales_ru={
                   "next()": "Верно. Запрашивает следующий элемент.",
                   "iter()": "Неверно. iter() создаёт итератор.",
                   "step()": "Неверно. Нет встроенной функции step().",
                   "move()": "Неверно. Нет встроенной функции move()."
               }),
        ],
    },
    {
        "key": "modules_pip_venv",
        "title_en": "Modules, PIP and Virtual Environments",
        "title_ru": "Модули, PIP и виртуальные окружения",
        "description_en": "Importing code, installing packages and isolating projects.",
        "description_ru": "Импорт кода, установка пакетов и изоляция проектов.",
        "questions": [
            _q("beginner", "Which keyword loads a module?", "Какое слово загружает модуль?", "import", ["include", "load", "using"],
               explanation_en="The 'import' keyword is used to load code from a module into the current file.",
               explanation_ru="Ключевое слово 'import' загружает код из модуля в текущий файл.",
               option_rationales_en={
                   "import": "Correct. 'import module_name' loads the module.",
                   "include": "Incorrect. This is used in C/C++.",
                   "load": "Incorrect. This is not a Python keyword.",
                   "using": "Incorrect. This is used in C# or C++."
               },
               option_rationales_ru={
                   "import": "Верно. 'import имя_модуля' загружает модуль.",
                   "include": "Неверно. Используется в C/C++.",
                   "load": "Неверно. В Python нет такого ключевого слова.",
                   "using": "Неверно. Используется в C# или C++."
               }),
            _q("intermediate", "What is pip mainly used for?", "Для чего в основном используется pip?", "Installing Python packages", ["Writing comments", "Creating loops", "Drawing windows"],
               explanation_en="pip (Package Installer for Python) is used to install and manage third-party libraries.",
               explanation_ru="pip (Package Installer for Python) устанавливает и управляет сторонними библиотеками.",
               option_rationales_en={
                   "Installing Python packages": "Correct. It downloads and installs packages from PyPI.",
                   "Writing comments": "Incorrect. Comments use '#'.",
                   "Creating loops": "Incorrect. 'for' and 'while' create loops.",
                   "Drawing windows": "Incorrect. You need GUI libraries like Tkinter for that."
               },
               option_rationales_ru={
                   "Installing Python packages": "Верно. Скачивает и устанавливает пакеты из PyPI.",
                   "Writing comments": "Неверно. Комментарии пишутся через '#'.",
                   "Creating loops": "Неверно. Для этого служат 'for' и 'while'.",
                   "Drawing windows": "Неверно. Для этого нужны библиотеки вроде Tkinter."
               }),
            _q("advanced", "Why use a virtual environment?", "Зачем использовать виртуальное окружение?", "To isolate project dependencies", ["To speed up every loop", "To replace Python", "To hide source code"],
               explanation_en="Virtual environments keep dependencies required by different projects separate, avoiding version conflicts.",
               explanation_ru="Виртуальные окружения хранят зависимости разных проектов отдельно, избегая конфликтов версий.",
               option_rationales_en={
                   "To isolate project dependencies": "Correct. It prevents packages in one project from breaking another.",
                   "To speed up every loop": "Incorrect. It doesn't affect execution speed.",
                   "To replace Python": "Incorrect. It uses your installed Python.",
                   "To hide source code": "Incorrect. It provides no security or obfuscation."
               },
               option_rationales_ru={
                   "To isolate project dependencies": "Верно. Защищает пакеты одного проекта от конфликтов с другими.",
                   "To speed up every loop": "Неверно. Не влияет на скорость работы.",
                   "To replace Python": "Неверно. Использует уже установленный Python.",
                   "To hide source code": "Неверно. Не скрывает и не шифрует код."
               }),
        ],
    },
    {
        "key": "dates_math",
        "title_en": "Dates and Math",
        "title_ru": "Даты и математика",
        "description_en": "Working with datetime, math functions and numeric helpers.",
        "description_ru": "Работа с datetime, математическими функциями и числами.",
        "questions": [
            _q("beginner", "Which module provides many mathematical functions?", "Какой модуль содержит математические функции?", "math", ["json", "randomtext", "files"],
               explanation_en="The 'math' module contains functions like square root, sine, cosine, etc.",
               explanation_ru="Модуль 'math' содержит функции, такие как квадратный корень, синус, косинус и т.д.",
               option_rationales_en={
                   "math": "Correct. This is the standard math library.",
                   "json": "Incorrect. This is for parsing JSON data.",
                   "randomtext": "Incorrect. There is no such built-in module.",
                   "files": "Incorrect. File I/O does not use a module named files."
               },
               option_rationales_ru={
                   "math": "Верно. Это стандартная математическая библиотека.",
                   "json": "Неверно. Используется для работы с JSON.",
                   "randomtext": "Неверно. Такого встроенного модуля нет.",
                   "files": "Неверно. Работа с файлами не использует модуль с именем files."
               }),
            _q("intermediate", "What does abs(-7) return?", "Что вернёт abs(-7)?", "7", ["-7", "0", "49"],
               explanation_en="The 'abs()' function returns the absolute (positive) value of a number.",
               explanation_ru="Функция 'abs()' возвращает абсолютное (положительное) значение числа.",
               option_rationales_en={
                   "7": "Correct. It removes the negative sign.",
                   "-7": "Incorrect. That is the original value.",
                   "0": "Incorrect. abs() does not zero out the number.",
                   "49": "Incorrect. That would be the square."
               },
               option_rationales_ru={
                   "7": "Верно. Она убирает знак минуса.",
                   "-7": "Неверно. Это исходное значение.",
                   "0": "Неверно. abs() не обнуляет число.",
                   "49": "Неверно. Это был бы квадрат числа."
               }),
            _q("advanced", "Which datetime method gets the current local date and time?", "Какой метод datetime получает текущие локальные дату и время?", "datetime.now()", ["datetime.stop()", "date.time()", "now.datetime()"],
               explanation_en="The 'datetime.now()' method is the standard way to get the current timestamp.",
               explanation_ru="Метод 'datetime.now()' — стандартный способ получить текущую временную метку.",
               option_rationales_en={
                   "datetime.now()": "Correct. It returns the current local date and time.",
                   "datetime.stop()": "Incorrect. There is no stop() method.",
                   "date.time()": "Incorrect. These are separate classes.",
                   "now.datetime()": "Incorrect. Syntax is backward."
               },
               option_rationales_ru={
                   "datetime.now()": "Верно. Возвращает текущие дату и время.",
                   "datetime.stop()": "Неверно. Метода stop() нет.",
                   "date.time()": "Неверно. Это отдельные классы.",
                   "now.datetime()": "Неверно. Синтаксис перевёрнут."
               }),
        ],
    },
    {
        "key": "json",
        "title_en": "JSON",
        "title_ru": "JSON",
        "description_en": "Converting between JSON text and Python values.",
        "description_ru": "Преобразование между текстом JSON и значениями Python.",
        "questions": [
            _q("beginner", "What is JSON commonly used for?", "Для чего обычно используется JSON?", "Exchanging structured data", ["Drawing pictures", "Compiling Python", "Styling web pages"],
               explanation_en="JSON (JavaScript Object Notation) is a text format used to store and exchange data between systems.",
               explanation_ru="JSON (JavaScript Object Notation) — текстовый формат для хранения и обмена данными между системами.",
               option_rationales_en={
                   "Exchanging structured data": "Correct. It's a standard format for APIs and config files.",
                   "Drawing pictures": "Incorrect. It is just text.",
                   "Compiling Python": "Incorrect. Python uses its own compiler.",
                   "Styling web pages": "Incorrect. CSS is used for styling."
               },
               option_rationales_ru={
                   "Exchanging structured data": "Верно. Это стандартный формат для API и файлов конфигурации.",
                   "Drawing pictures": "Неверно. Это просто текст.",
                   "Compiling Python": "Неверно. Python использует собственный компилятор.",
                   "Styling web pages": "Неверно. Для стилизации используется CSS."
               }),
            _q("intermediate", "Which function reads JSON text into Python?", "Какая функция читает текст JSON в Python?", "json.loads()", ["json.dumps()", "json.open()", "json.reads()"],
               explanation_en="'json.loads()' parses a JSON string and converts it into a Python dictionary or list.",
               explanation_ru="'json.loads()' разбирает строку JSON и превращает её в словарь или список Python.",
               option_rationales_en={
                   "json.loads()": "Correct. The 's' stands for string (load string).",
                   "json.dumps()": "Incorrect. This converts Python to JSON string.",
                   "json.open()": "Incorrect. This function does not exist.",
                   "json.reads()": "Incorrect. This function does not exist."
               },
               option_rationales_ru={
                   "json.loads()": "Верно. Буква 's' означает string (загрузить строку).",
                   "json.dumps()": "Неверно. Превращает Python в строку JSON.",
                   "json.open()": "Неверно. Такой функции не существует.",
                   "json.reads()": "Неверно. Такой функции не существует."
               }),
            _q("advanced", "Which function converts a Python value to JSON text?", "Какая функция превращает значение Python в текст JSON?", "json.dumps()", ["json.loads()", "json.parse()", "json.text()"],
               explanation_en="'json.dumps()' takes a Python object and returns a JSON-formatted string.",
               explanation_ru="'json.dumps()' берёт объект Python и возвращает строку в формате JSON.",
               option_rationales_en={
                   "json.dumps()": "Correct. The 's' stands for string (dump string).",
                   "json.loads()": "Incorrect. This does the reverse.",
                   "json.parse()": "Incorrect. JavaScript uses JSON.parse(), Python uses loads().",
                   "json.text()": "Incorrect. This function does not exist."
               },
               option_rationales_ru={
                   "json.dumps()": "Верно. Буква 's' означает string (выгрузить строку).",
                   "json.loads()": "Неверно. Выполняет обратное действие.",
                   "json.parse()": "Неверно. JavaScript использует JSON.parse(), Python — loads().",
                   "json.text()": "Неверно. Такой функции не существует."
               }),
        ],
    },
    {
        "key": "regex",
        "title_en": "Regular Expressions",
        "title_ru": "Регулярные выражения",
        "description_en": "Searching and validating text patterns with re.",
        "description_ru": "Поиск и проверка шаблонов текста с помощью re.",
        "questions": [
            _q("beginner", "Which module supports regular expressions?", "Какой модуль поддерживает регулярные выражения?", "re", ["regexpy", "text", "find"],
               explanation_en="The built-in 're' module handles all regular expression operations in Python.",
               explanation_ru="Встроенный модуль 're' обрабатывает все операции с регулярными выражениями в Python.",
               option_rationales_en={
                   "re": "Correct. It stands for regular expressions.",
                   "regexpy": "Incorrect. There is no such built-in module.",
                   "text": "Incorrect. There is no standard module named text.",
                   "find": "Incorrect. String methods use find(), but it is not a module."
               },
               option_rationales_ru={
                   "re": "Верно. Это сокращение от regular expressions.",
                   "regexpy": "Неверно. Такого встроенного модуля нет.",
                   "text": "Неверно. Такого стандартного модуля нет.",
                   "find": "Неверно. Это строковый метод, а не модуль."
               }),
            _q("intermediate", "Which pattern matches a digit?", "Какой шаблон соответствует цифре?", "\\d", ["\\s", "\\w only letters", ".py"],
               explanation_en="In regular expressions, '\\d' is the shorthand for any digit [0-9].",
               explanation_ru="В регулярных выражениях '\\d' — это сокращение для любой цифры [0-9].",
               option_rationales_en={
                   "\\d": "Correct. It stands for digit.",
                   "\\s": "Incorrect. This matches whitespace.",
                   "\\w only letters": "Incorrect. \\w matches letters, numbers, and underscores.",
                   ".py": "Incorrect. This just matches the literal string '.py'."
               },
               option_rationales_ru={
                   "\\d": "Верно. Означает digit (цифра).",
                   "\\s": "Неверно. Соответствует пробельным символам.",
                   "\\w only letters": "Неверно. \\w соответствует буквам, цифрам и подчёркиваниям.",
                   ".py": "Неверно. Ищет точную строку '.py'."
               }),
            _q("advanced", "What does re.search() look for?", "Что ищет re.search()?", "A matching pattern anywhere in the text", ["Only at the final character", "Only Python keywords", "A file on disk"],
               explanation_en="Unlike re.match() which only checks the beginning of the string, re.search() scans the whole string for a match.",
               explanation_ru="В отличие от re.match(), который проверяет только начало строки, re.search() сканирует всю строку.",
               option_rationales_en={
                   "A matching pattern anywhere in the text": "Correct. It scans through the string looking for the first location where the pattern produces a match.",
                   "Only at the final character": "Incorrect. It searches the entire string.",
                   "Only Python keywords": "Incorrect. It searches for whatever pattern you define.",
                   "A file on disk": "Incorrect. It searches within a string in memory."
               },
               option_rationales_ru={
                   "A matching pattern anywhere in the text": "Верно. Сканирует строку в поисках первого места, где шаблон совпадёт.",
                   "Only at the final character": "Неверно. Ищет по всей строке.",
                   "Only Python keywords": "Неверно. Ищет то, что вы укажете в шаблоне.",
                   "A file on disk": "Неверно. Ищет внутри строки в памяти."
               }),
        ],
    },
    {
        "key": "exceptions",
        "title_en": "Try and Except",
        "title_ru": "Обработка ошибок try и except",
        "description_en": "Catching errors, else, finally and raising exceptions.",
        "description_ru": "Перехват ошибок, else, finally и создание исключений.",
        "questions": [
            _q("beginner", "Which block contains code that may fail?", "Какой блок содержит код, где возможна ошибка?", "try", ["except", "finally", "raise"],
               explanation_en="You put risky code inside a 'try' block so you can catch errors if they happen.",
               explanation_ru="Вы помещаете рискованный код в блок 'try', чтобы можно было перехватить ошибки.",
               option_rationales_en={
                   "try": "Correct. Python 'tries' to execute this code.",
                   "except": "Incorrect. This catches the error after it happens.",
                   "finally": "Incorrect. This runs at the end regardless of errors.",
                   "raise": "Incorrect. This causes an error on purpose."
               },
               option_rationales_ru={
                   "try": "Верно. Python «пытается» выполнить этот код.",
                   "except": "Неверно. Перехватывает ошибку после её появления.",
                   "finally": "Неверно. Выполняется в конце в любом случае.",
                   "raise": "Неверно. Вызывает ошибку намеренно."
               }),
            _q("intermediate", "Which block handles a matching error?", "Какой блок обрабатывает подходящую ошибку?", "except", ["else", "for", "match"],
               explanation_en="The 'except' block runs only if an exception is raised in the try block.",
               explanation_ru="Блок 'except' выполняется, только если в блоке try возникло исключение.",
               option_rationales_en={
                   "except": "Correct. You can specify which error type to catch.",
                   "else": "Incorrect. 'else' runs if NO error happened.",
                   "for": "Incorrect. 'for' is a loop.",
                   "match": "Incorrect. 'match' is used for pattern matching."
               },
               option_rationales_ru={
                   "except": "Верно. Вы можете указать тип ошибки для перехвата.",
                   "else": "Неверно. 'else' выполняется, если ошибок НЕ было.",
                   "for": "Неверно. 'for' — это цикл.",
                   "match": "Неверно. 'match' — это сопоставление с образцом."
               }),
            _q("advanced", "Which block runs whether an error happens or not?", "Какой блок выполняется независимо от ошибки?", "finally", ["except only", "elif", "yield"],
               explanation_en="The 'finally' block is used for cleanup actions and will always run, even if the program crashes.",
               explanation_ru="Блок 'finally' используется для действий по очистке и выполняется всегда, даже при сбое программы.",
               option_rationales_en={
                   "finally": "Correct. It always runs at the end.",
                   "except only": "Incorrect. 'except' only runs if an error occurs.",
                   "elif": "Incorrect. Used in if statements.",
                   "yield": "Incorrect. Used in generators."
               },
               option_rationales_ru={
                   "finally": "Верно. Всегда выполняется в самом конце.",
                   "except only": "Неверно. 'except' выполняется только при ошибке.",
                   "elif": "Неверно. Используется в условиях if.",
                   "yield": "Неверно. Используется в генераторах."
               }),
        ],
    },
    {
        "key": "formatting_none_input",
        "title_en": "Formatting, None and User Input",
        "title_ru": "Форматирование, None и ввод пользователя",
        "description_en": "f-strings, missing values and reading keyboard input.",
        "description_ru": "f-строки, отсутствие значения и ввод с клавиатуры.",
        "questions": [
            _q("beginner", "What does input() return?", "Что возвращает input()?", "A string", ["Always an integer", "A boolean", "Nothing"],
               explanation_en="No matter what the user types, input() always returns it as a string.",
               explanation_ru="Независимо от того, что вводит пользователь, input() всегда возвращает это как строку.",
               option_rationales_en={
                   "A string": "Correct. Even if the user types '42', it is returned as '42'.",
                   "Always an integer": "Incorrect. You must manually convert it using int().",
                   "A boolean": "Incorrect. You must evaluate the string.",
                   "Nothing": "Incorrect. It returns the user's input."
               },
               option_rationales_ru={
                   "A string": "Верно. Даже если ввести '42', вернётся строка '42'.",
                   "Always an integer": "Неверно. Нужно конвертировать вручную через int().",
                   "A boolean": "Неверно. Нужно оценивать строку.",
                   "Nothing": "Неверно. Функция возвращает введённые данные."
               }),
            _q("intermediate", "Which value means no value is present?", "Какое значение означает отсутствие значения?", "None", ["False only", "0 only", "empty"],
               explanation_en="In Python, 'None' is a special constant representing the absence of a value.",
               explanation_ru="В Python 'None' — это специальная константа, обозначающая отсутствие значения.",
               option_rationales_en={
                   "None": "Correct. It is Python's version of null.",
                   "False only": "Incorrect. False is a boolean value.",
                   "0 only": "Incorrect. 0 is a number, not the absence of value.",
                   "empty": "Incorrect. There is no 'empty' keyword in Python."
               },
               option_rationales_ru={
                   "None": "Верно. Это питоновская версия null.",
                   "False only": "Неверно. False — логическое значение.",
                   "0 only": "Неверно. 0 — это число.",
                   "empty": "Неверно. В Python нет слова 'empty'."
               }),
            _q("advanced", "Which is an f-string?", "Какая строка является f-строкой?", "f'Hi {name}'", ["'Hi {name}'", "format'Hi name'", "f(Hi name)"],
               explanation_en="F-strings start with an 'f' before the quote and allow variables inside curly braces {}.",
               explanation_ru="F-строки начинаются с буквы 'f' перед кавычкой и позволяют вставлять переменные в фигурных скобках {}.",
               option_rationales_en={
                   "f'Hi {name}'": "Correct. This evaluates the 'name' variable dynamically.",
                   "'Hi {name}'": "Incorrect. Without the 'f', it just prints the literal characters '{name}'.",
                   "format'Hi name'": "Incorrect. Invalid syntax.",
                   "f(Hi name)": "Incorrect. Invalid syntax."
               },
               option_rationales_ru={
                   "f'Hi {name}'": "Верно. Динамически подставляет значение переменной 'name'.",
                   "'Hi {name}'": "Неверно. Без 'f' это просто символы '{name}'.",
                   "format'Hi name'": "Неверно. Неправильный синтаксис.",
                   "f(Hi name)": "Неверно. Неправильный синтаксис."
               }),
        ],
    },
    {
        "key": "oop_basics",
        "title_en": "Classes, Objects, __init__ and self",
        "title_ru": "Классы, объекты, __init__ и self",
        "description_en": "Creating classes, instances, properties and methods.",
        "description_ru": "Создание классов, объектов, свойств и методов.",
        "questions": [
            _q("beginner", "Which keyword creates a class?", "Какое слово создаёт класс?", "class", ["object", "new", "def"],
               explanation_en="The 'class' keyword is used to define a new class in Python.",
               explanation_ru="Ключевое слово 'class' используется для определения нового класса в Python.",
               option_rationales_en={
                   "class": "Correct. It defines a new blueprint for objects.",
                   "object": "Incorrect. An object is an instance of a class.",
                   "new": "Incorrect. 'new' is used in Java/C++, not Python.",
                   "def": "Incorrect. 'def' creates a function."
               },
               option_rationales_ru={
                   "class": "Верно. Оно определяет новый чертёж для объектов.",
                   "object": "Неверно. Объект — это экземпляр класса.",
                   "new": "Неверно. 'new' используется в Java/C++, а не в Python.",
                   "def": "Неверно. 'def' создаёт функцию."
               }),
            _q("intermediate", "What is __init__ commonly used for?", "Для чего обычно используется __init__?", "Setting initial object data", ["Deleting every object", "Importing modules", "Starting a loop"],
               explanation_en="The '__init__' method is a constructor that initializes a newly created object's attributes.",
               explanation_ru="Метод '__init__' — это конструктор, который инициализирует атрибуты только что созданного объекта.",
               option_rationales_en={
                   "Setting initial object data": "Correct. It initializes the object's state.",
                   "Deleting every object": "Incorrect. The __del__ method handles deletion.",
                   "Importing modules": "Incorrect. 'import' is used for that.",
                   "Starting a loop": "Incorrect. Loops use 'for' or 'while'."
               },
               option_rationales_ru={
                   "Setting initial object data": "Верно. Инициализирует состояние объекта.",
                   "Deleting every object": "Неверно. За удаление отвечает метод __del__.",
                   "Importing modules": "Неверно. Для этого используется 'import'.",
                   "Starting a loop": "Неверно. Циклы используют 'for' или 'while'."
               }),
            _q("advanced", "What does self refer to inside an instance method?", "На что указывает self внутри метода объекта?", "The current object", ["The parent file", "Every class at once", "Python itself"],
               explanation_en="In Python, 'self' is the conventional name for the first parameter of an instance method, pointing to the specific instance calling the method.",
               explanation_ru="В Python 'self' — это общепринятое имя первого параметра метода объекта, указывающее на конкретный экземпляр, вызывающий этот метод.",
               option_rationales_en={
                   "The current object": "Correct. It gives the method access to the object's attributes.",
                   "The parent file": "Incorrect. It points to an instance, not a file.",
                   "Every class at once": "Incorrect. It points to one specific instance.",
                   "Python itself": "Incorrect. It represents the object."
               },
               option_rationales_ru={
                   "The current object": "Верно. Даёт методу доступ к атрибутам объекта.",
                   "The parent file": "Неверно. Указывает на экземпляр, а не на файл.",
                   "Every class at once": "Неверно. Указывает на один конкретный экземпляр.",
                   "Python itself": "Неверно. Представляет сам объект."
               }),
        ],
    },
    {
        "key": "oop_design",
        "title_en": "Inheritance, Polymorphism and Encapsulation",
        "title_ru": "Наследование, полиморфизм и инкапсуляция",
        "description_en": "Reusing classes, shared interfaces and protecting object details.",
        "description_ru": "Повторное использование классов, общий интерфейс и защита деталей объекта.",
        "questions": [
            _q("beginner", "What does inheritance let a child class do?", "Что наследование позволяет дочернему классу?", "Reuse behavior from a parent class", ["Delete Python", "Avoid all methods", "Become a list"],
               explanation_en="Inheritance allows a new class to take on the attributes and methods of an existing class.",
               explanation_ru="Наследование позволяет новому классу перенять атрибуты и методы существующего класса.",
               option_rationales_en={
                   "Reuse behavior from a parent class": "Correct. It promotes code reuse.",
                   "Delete Python": "Incorrect. It has no destructive capability.",
                   "Avoid all methods": "Incorrect. It actually inherits them.",
                   "Become a list": "Incorrect. You can inherit from list, but inheritance generally doesn't just 'become a list'."
               },
               option_rationales_ru={
                   "Reuse behavior from a parent class": "Верно. Способствует повторному использованию кода.",
                   "Delete Python": "Неверно. Не обладает разрушительной силой.",
                   "Avoid all methods": "Неверно. Наоборот, класс их наследует.",
                   "Become a list": "Неверно. Можно наследоваться от списка, но это не главная суть."
               }),
            _q("intermediate", "What is method overriding?", "Что такое переопределение метода?", "A child class provides its own version", ["A method runs twice", "A variable becomes global", "A file is renamed"],
               explanation_en="Overriding happens when a child class defines a method with the same name as one in its parent, replacing the parent's behavior.",
               explanation_ru="Переопределение происходит, когда дочерний класс определяет метод с тем же именем, что и у родительского, заменяя его поведение.",
               option_rationales_en={
                   "A child class provides its own version": "Correct. It 'overrides' the inherited behavior.",
                   "A method runs twice": "Incorrect. It just runs the new version once.",
                   "A variable becomes global": "Incorrect. This is unrelated to scope.",
                   "A file is renamed": "Incorrect. This is unrelated to file management."
               },
               option_rationales_ru={
                   "A child class provides its own version": "Верно. Он «переопределяет» унаследованное поведение.",
                   "A method runs twice": "Неверно. Выполняется только новая версия один раз.",
                   "A variable becomes global": "Неверно. Не связано с областью видимости.",
                   "A file is renamed": "Неверно. Не связано с файловой системой."
               }),
            _q("advanced", "What is encapsulation mainly about?", "В чём основная идея инкапсуляции?", "Controlling access to object details", ["Sorting every collection", "Replacing functions with loops", "Installing packages"],
               explanation_en="Encapsulation is the bundling of data and methods that operate on that data, often restricting direct access to some of the object's components.",
               explanation_ru="Инкапсуляция — это объединение данных и методов для работы с ними, часто с ограничением прямого доступа к некоторым компонентам объекта.",
               option_rationales_en={
                   "Controlling access to object details": "Correct. It hides internal state and requires all interaction to be performed through an object's methods.",
                   "Sorting every collection": "Incorrect. This is unrelated to algorithms.",
                   "Replacing functions with loops": "Incorrect. This is a coding stylistic choice.",
                   "Installing packages": "Incorrect. This is package management."
               },
               option_rationales_ru={
                   "Controlling access to object details": "Верно. Скрывает внутреннее состояние и требует взаимодействия через методы.",
                   "Sorting every collection": "Неверно. Не связано с алгоритмами.",
                   "Replacing functions with loops": "Неверно. Это стилистический выбор в коде.",
                   "Installing packages": "Неверно. Это управление пакетами."
               }),
        ],
    },
    {
        "key": "files",
        "title_en": "File Handling",
        "title_ru": "Работа с файлами",
        "description_en": "Opening, reading, writing, creating and deleting files.",
        "description_ru": "Открытие, чтение, запись, создание и удаление файлов.",
        "questions": [
            _q("beginner", "Which function opens a file?", "Какая функция открывает файл?", "open()", ["file()", "read()", "start()"],
               explanation_en="The built-in 'open()' function is used to open a file and return a file object.",
               explanation_ru="Встроенная функция 'open()' используется для открытия файла и возврата файлового объекта.",
               option_rationales_en={
                   "open()": "Correct. It is the standard way to access files.",
                   "file()": "Incorrect. Python 2 had this, but Python 3 only uses open().",
                   "read()": "Incorrect. This is a method called ON the file object.",
                   "start()": "Incorrect. There is no start() built-in function."
               },
               option_rationales_ru={
                   "open()": "Верно. Стандартный способ доступа к файлам.",
                   "file()": "Неверно. Было в Python 2, в Python 3 используется только open().",
                   "read()": "Неверно. Это метод, вызываемый У файлового объекта.",
                   "start()": "Неверно. Нет встроенной функции start()."
               }),
            _q("intermediate", "Which mode opens a file for reading?", "Какой режим открывает файл для чтения?", "'r'", ["'w'", "'a'", "'x'"],
               explanation_en="The 'r' mode stands for 'read', and it's the default mode when opening a file.",
               explanation_ru="Режим 'r' означает 'read' (чтение), это режим по умолчанию при открытии файла.",
               option_rationales_en={
                   "'r'": "Correct. It opens the file strictly for reading.",
                   "'w'": "Incorrect. 'w' is for writing (overwrites).",
                   "'a'": "Incorrect. 'a' is for appending.",
                   "'x'": "Incorrect. 'x' is for exclusive creation."
               },
               option_rationales_ru={
                   "'r'": "Верно. Открывает файл строго для чтения.",
                   "'w'": "Неверно. 'w' — для записи (перезаписывает).",
                   "'a'": "Неверно. 'a' — для добавления в конец.",
                   "'x'": "Неверно. 'x' — для эксклюзивного создания."
               }),
            _q("advanced", "Why is with open(...) useful?", "Почему удобно использовать with open(...)?", "It closes the file automatically", ["It makes every file public", "It converts files to JSON", "It prevents all errors"],
               explanation_en="Using 'with open()' creates a context manager that automatically closes the file when the block ends, even if errors occur.",
               explanation_ru="Конструкция 'with open()' создаёт менеджер контекста, который автоматически закрывает файл по завершении блока, даже при возникновении ошибок.",
               option_rationales_en={
                   "It closes the file automatically": "Correct. It guarantees cleanup of system resources.",
                   "It makes every file public": "Incorrect. File permissions are handled by the OS.",
                   "It converts files to JSON": "Incorrect. You need the json module for that.",
                   "It prevents all errors": "Incorrect. FileNotFounError can still happen, for example."
               },
               option_rationales_ru={
                   "It closes the file automatically": "Верно. Гарантирует освобождение системных ресурсов.",
                   "It makes every file public": "Неверно. Права доступа к файлам регулирует ОС.",
                   "It converts files to JSON": "Неверно. Для этого нужен модуль json.",
                   "It prevents all errors": "Неверно. Например, FileNotFoundError всё ещё возможна."
               }),
        ],
    },
]
