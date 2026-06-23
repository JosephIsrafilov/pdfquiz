from app.curriculum.python_core import _q


PYTHON_DEEP_TOPICS = [
    {
        "key": "mutability_copying",
        "title_en": "Mutability and Copying",
        "title_ru": "Изменяемость и копирование",
        "description_en": "How shared references, shallow copies and immutable values behave.",
        "description_ru": "Общие ссылки, поверхностные копии и неизменяемые значения.",
        "questions": [
            _q("beginner", "Which built-in collection is mutable?", "Какая встроенная коллекция изменяема?", "list", ["tuple", "str", "frozenset"],
               explanation_en="Lists can be modified after creation (items added, changed, or removed).",
               explanation_ru="Списки можно изменять после создания (добавлять, менять или удалять элементы).",
               option_rationales_en={
                   "list": "Correct. Lists are mutable.",
                   "tuple": "Incorrect. Tuples are immutable.",
                   "str": "Incorrect. Strings are immutable.",
                   "frozenset": "Incorrect. Frozensets are immutable sets."
               },
               option_rationales_ru={
                   "list": "Верно. Списки изменяемы.",
                   "tuple": "Неверно. Кортежи неизменяемы.",
                   "str": "Неверно. Строки неизменяемы.",
                   "frozenset": "Неверно. Frozenset - неизменяемое множество."
               }),
            _q("beginner", "If b = a for a list, what do a and b initially reference?", "Если для списка выполнить b = a, на что сначала указывают a и b?", "The same list", ["Two automatic copies", "Two tuples", "Nothing"],
               explanation_en="Assignment just copies the reference, so both point to the exact same list in memory.",
               explanation_ru="Присваивание копирует только ссылку, поэтому обе переменные указывают на один и тот же список в памяти.",
               option_rationales_en={
                   "The same list": "Correct. They refer to the same object.",
                   "Two automatic copies": "Incorrect. Python does not copy objects on assignment.",
                   "Two tuples": "Incorrect. Assignment doesn't change the type.",
                   "Nothing": "Incorrect. They point to the list."
               },
               option_rationales_ru={
                   "The same list": "Верно. Они ссылаются на один объект.",
                   "Two automatic copies": "Неверно. Python не копирует объекты при присваивании.",
                   "Two tuples": "Неверно. Тип не меняется.",
                   "Nothing": "Неверно. Они указывают на список."
               }),
            _q("intermediate", "Which expression makes a shallow copy of a list named items?", "Какое выражение создаёт поверхностную копию списка items?", "items.copy()", ["items = copy", "copy(items) without importing anything", "items.clone()"],
               explanation_en="The list method .copy() (or list(items) or items[:]) creates a shallow copy.",
               explanation_ru="Метод списка .copy() (или list(items) или items[:]) создаёт поверхностную копию.",
               option_rationales_en={
                   "items.copy()": "Correct. This is the standard method for a shallow copy.",
                   "items = copy": "Incorrect. 'copy' is not a built-in function like this.",
                   "copy(items) without importing anything": "Incorrect. 'copy' needs to be imported from the copy module.",
                   "items.clone()": "Incorrect. There is no .clone() method for lists."
               },
               option_rationales_ru={
                   "items.copy()": "Верно. Это стандартный метод для поверхностной копии.",
                   "items = copy": "Неверно. 'copy' не является встроенной функцией в таком виде.",
                   "copy(items) without importing anything": "Неверно. 'copy' нужно импортировать.",
                   "items.clone()": "Неверно. У списков нет метода .clone()."
               }),
            _q("intermediate", "Why can changing a nested list affect a shallow copy?", "Почему изменение вложенного списка может повлиять на поверхностную копию?", "Nested objects are still shared", ["Python deletes the copy", "Lists are always immutable", "copy() sorts the data"],
               explanation_en="A shallow copy creates a new outer list but keeps references to the same nested objects.",
               explanation_ru="Поверхностная копия создаёт новый внешний список, но сохраняет ссылки на те же вложенные объекты.",
               option_rationales_en={
                   "Nested objects are still shared": "Correct. The inner elements are references, not copies.",
                   "Python deletes the copy": "Incorrect. The copy is not deleted.",
                   "Lists are always immutable": "Incorrect. Lists are mutable.",
                   "copy() sorts the data": "Incorrect. Sorting is separate."
               },
               option_rationales_ru={
                   "Nested objects are still shared": "Верно. Внутренние элементы - это ссылки.",
                   "Python deletes the copy": "Неверно. Копия не удаляется.",
                   "Lists are always immutable": "Неверно. Списки изменяемы.",
                   "copy() sorts the data": "Неверно. Метод copy() не сортирует."
               }),
            _q("advanced", "Which module provides deepcopy()?", "Какой модуль содержит deepcopy()?", "copy", ["math", "json", "types"],
               explanation_en="The 'copy' module contains the deepcopy() function for fully copying nested structures.",
               explanation_ru="Модуль 'copy' содержит функцию deepcopy() для полного копирования вложенных структур.",
               option_rationales_en={
                   "copy": "Correct. Import copy, then use copy.deepcopy().",
                   "math": "Incorrect. Math handles numeric operations.",
                   "json": "Incorrect. JSON handles data serialization.",
                   "types": "Incorrect. Types is used for type checking."
               },
               option_rationales_ru={
                   "copy": "Верно. Модуль copy используется для deepcopy().",
                   "math": "Неверно. Модуль math для математики.",
                   "json": "Неверно. Модуль json для сериализации.",
                   "types": "Неверно. Модуль types для проверки типов."
               }),
        ],
    },
    {
        "key": "unpacking_comprehensions",
        "title_en": "Unpacking and Comprehensions",
        "title_ru": "Распаковка и включения",
        "description_en": "Compactly unpacking values and building collections from loops.",
        "description_ru": "Компактная распаковка значений и создание коллекций из циклов.",
        "questions": [
            _q("beginner", "After x, y = (4, 9), what is x?", "После x, y = (4, 9) чему равен x?", "4", ["9", "(4, 9)", "x"],
               explanation_en="Tuple unpacking assigns the first element to x and the second to y.",
               explanation_ru="Распаковка кортежа присваивает первый элемент x, а второй - y.",
               option_rationales_en={
                   "4": "Correct. x gets the first value.",
                   "9": "Incorrect. y gets 9.",
                   "(4, 9)": "Incorrect. The tuple is unpacked.",
                   "x": "Incorrect. It's evaluated to the value 4."
               },
               option_rationales_ru={
                   "4": "Верно. x получает первое значение.",
                   "9": "Неверно. y получает 9.",
                   "(4, 9)": "Неверно. Кортеж распаковывается.",
                   "x": "Неверно. Присваивается значение 4."
               }),
            _q("beginner", "What does a list comprehension create?", "Что создаёт списковое включение?", "A new list", ["A class", "A file", "An exception"],
               explanation_en="A list comprehension provides a concise way to create lists.",
               explanation_ru="Списковое включение - это краткий способ создания списков.",
               option_rationales_en={
                   "A new list": "Correct. List comprehensions yield new lists.",
                   "A class": "Incorrect. It does not define classes.",
                   "A file": "Incorrect. It has nothing to do with files.",
                   "An exception": "Incorrect. It is a valid expression."
               },
               option_rationales_ru={
                   "A new list": "Верно. Списковые включения создают новые списки.",
                   "A class": "Неверно. Они не создают классы.",
                   "A file": "Неверно. Они не работают с файлами.",
                   "An exception": "Неверно. Это корректное выражение."
               }),
            _q("intermediate", "What is [n for n in range(5) if n % 2 == 0]?", "Чему равно [n for n in range(5) if n % 2 == 0]?", "[0, 2, 4]", ["[1, 3, 5]", "[2, 4]", "[0, 1, 2, 3, 4]"],
               explanation_en="This filters range(5) to keep only the even numbers.",
               explanation_ru="Это фильтрует range(5), оставляя только чётные числа.",
               option_rationales_en={
                   "[0, 2, 4]": "Correct. 0, 2, and 4 are even.",
                   "[1, 3, 5]": "Incorrect. These are odd, and 5 is not in range(5).",
                   "[2, 4]": "Incorrect. 0 is also an even number.",
                   "[0, 1, 2, 3, 4]": "Incorrect. It includes the if condition."
               },
               option_rationales_ru={
                   "[0, 2, 4]": "Верно. 0, 2 и 4 - чётные.",
                   "[1, 3, 5]": "Неверно. Это нечётные, а 5 вне range(5).",
                   "[2, 4]": "Неверно. 0 тоже чётное число.",
                   "[0, 1, 2, 3, 4]": "Неверно. Не учтено условие if."
               }),
            _q("intermediate", "What does *rest collect in first, *rest = [1, 2, 3]?", "Что собирает *rest в first, *rest = [1, 2, 3]?", "[2, 3]", ["1", "[1, 2]", "3"],
               explanation_en="The starred expression collects all remaining items into a list.",
               explanation_ru="Выражение со звёздочкой собирает все оставшиеся элементы в список.",
               option_rationales_en={
                   "[2, 3]": "Correct. 'first' gets 1, '*rest' gets the rest as a list.",
                   "1": "Incorrect. 1 is assigned to 'first'.",
                   "[1, 2]": "Incorrect. It collects the end, not the beginning.",
                   "3": "Incorrect. It collects all remaining, not just the last."
               },
               option_rationales_ru={
                   "[2, 3]": "Верно. 'first' получает 1, а '*rest' - остальное.",
                   "1": "Неверно. 1 получает 'first'.",
                   "[1, 2]": "Неверно. Оно собирает конец, а не начало.",
                   "3": "Неверно. Оно собирает всё оставшееся, а не только последнее."
               }),
            _q("advanced", "Which expression creates a dictionary of n to n*n?", "Какое выражение создаёт словарь n и n*n?", "{n: n*n for n in range(3)}", ["[n: n*n for n in range(3)]", "{n*n for n in range(3)}", "dict(n*n)"],
               explanation_en="A dict comprehension uses curly braces and the key: value syntax.",
               explanation_ru="Словарное включение использует фигурные скобки и синтаксис ключ: значение.",
               option_rationales_en={
                   "{n: n*n for n in range(3)}": "Correct. This generates {0: 0, 1: 1, 2: 4}.",
                   "[n: n*n for n in range(3)]": "Incorrect. Square brackets are for list comprehensions.",
                   "{n*n for n in range(3)}": "Incorrect. This creates a set, not a dict.",
                   "dict(n*n)": "Incorrect. Invalid syntax."
               },
               option_rationales_ru={
                   "{n: n*n for n in range(3)}": "Верно. Это создаёт {0: 0, 1: 1, 2: 4}.",
                   "[n: n*n for n in range(3)]": "Неверно. Квадратные скобки - для списков.",
                   "{n*n for n in range(3)}": "Неверно. Это создаёт множество, а не словарь.",
                   "dict(n*n)": "Неверно. Неправильный синтаксис."
               }),
        ],
    },
    {
        "key": "builtins",
        "title_en": "Useful Built-in Functions",
        "title_ru": "Полезные встроенные функции",
        "description_en": "Using enumerate, zip, sorted, any, all, min, max and sum.",
        "description_ru": "Использование enumerate, zip, sorted, any, all, min, max и sum.",
        "questions": [
            _q("beginner", "Which function adds all numbers in a collection?", "Какая функция складывает все числа коллекции?", "sum()", ["all()", "zip()", "type()"],
               explanation_en="The built-in sum() function takes an iterable of numbers and returns their sum.",
               explanation_ru="Встроенная функция sum() принимает коллекцию чисел и возвращает их сумму.",
               option_rationales_en={
                   "sum()": "Correct. sum([1, 2, 3]) is 6.",
                   "all()": "Incorrect. all() checks if all elements are truthy.",
                   "zip()": "Incorrect. zip() pairs up elements.",
                   "type()": "Incorrect. type() gets the object's type."
               },
               option_rationales_ru={
                   "sum()": "Верно. sum([1, 2, 3]) равно 6.",
                   "all()": "Неверно. all() проверяет, что все элементы истинны.",
                   "zip()": "Неверно. zip() объединяет элементы в пары.",
                   "type()": "Неверно. type() возвращает тип."
               }),
            _q("beginner", "Which function finds the largest value?", "Какая функция находит наибольшее значение?", "max()", ["min()", "top()", "large()"],
               explanation_en="max() returns the largest item in an iterable or the largest of two or more arguments.",
               explanation_ru="max() возвращает наибольший элемент коллекции или наибольший из нескольких аргументов.",
               option_rationales_en={
                   "max()": "Correct. It finds the maximum.",
                   "min()": "Incorrect. min() finds the smallest.",
                   "top()": "Incorrect. Not a built-in Python function.",
                   "large()": "Incorrect. Not a built-in Python function."
               },
               option_rationales_ru={
                   "max()": "Верно. Находит максимум.",
                   "min()": "Неверно. min() находит минимум.",
                   "top()": "Неверно. Такой встроенной функции нет.",
                   "large()": "Неверно. Такой встроенной функции нет."
               }),
            _q("intermediate", "What does enumerate(items) provide during a loop?", "Что даёт enumerate(items) во время цикла?", "An index and an item", ["Two copies of each item", "Only sorted items", "A dictionary"],
               explanation_en="enumerate() yields pairs containing a count (from start, which defaults to 0) and the value obtained from iterating over the sequence.",
               explanation_ru="enumerate() выдаёт пары: счётчик (индекс) и само значение из последовательности.",
               option_rationales_en={
                   "An index and an item": "Correct. e.g., (0, 'a'), (1, 'b').",
                   "Two copies of each item": "Incorrect. It provides an index.",
                   "Only sorted items": "Incorrect. It does not sort.",
                   "A dictionary": "Incorrect. It yields tuples, not a dict."
               },
               option_rationales_ru={
                   "An index and an item": "Верно. Например, (0, 'a'), (1, 'b').",
                   "Two copies of each item": "Неверно. Оно выдаёт индекс.",
                   "Only sorted items": "Неверно. Оно не сортирует.",
                   "A dictionary": "Неверно. Выдаются кортежи, а не словарь."
               }),
            _q("intermediate", "What does zip(names, scores) combine?", "Что объединяет zip(names, scores)?", "Items from matching positions", ["Only the longest list", "All possible pairs", "Two strings"],
               explanation_en="zip() pairs the first item from each iterable, then the second item, and so on.",
               explanation_ru="zip() объединяет первые элементы каждой коллекции, затем вторые, и так далее.",
               option_rationales_en={
                   "Items from matching positions": "Correct. It pairs index 0 with index 0, 1 with 1.",
                   "Only the longest list": "Incorrect. It stops at the shortest list by default.",
                   "All possible pairs": "Incorrect. That would be itertools.product().",
                   "Two strings": "Incorrect. It works with any iterables."
               },
               option_rationales_ru={
                   "Items from matching positions": "Верно. Индекс 0 с индексом 0, и т.д.",
                   "Only the longest list": "Неверно. По умолчанию останавливается на самом коротком.",
                   "All possible pairs": "Неверно. Это декартово произведение (itertools.product).",
                   "Two strings": "Неверно. Работает с любыми итерируемыми объектами."
               }),
            _q("advanced", "When is all([True, True, False]) true?", "Когда all([True, True, False]) истинно?", "It is not true because one value is False", ["Always", "Only because the first value is True", "When the list is sorted"],
               explanation_en="all() returns True only if all elements of the iterable are true.",
               explanation_ru="all() возвращает True только если все элементы коллекции истинны.",
               option_rationales_en={
                   "It is not true because one value is False": "Correct. If any value is falsy, all() returns False.",
                   "Always": "Incorrect. It checks the values.",
                   "Only because the first value is True": "Incorrect. That describes any() loosely, but not all().",
                   "When the list is sorted": "Incorrect. Sorting is irrelevant."
               },
               option_rationales_ru={
                   "It is not true because one value is False": "Верно. Если есть хоть один ложный элемент, all() вернёт False.",
                   "Always": "Неверно. Зависит от значений.",
                   "Only because the first value is True": "Неверно. Это не так.",
                   "When the list is sorted": "Неверно. Сортировка не влияет."
               }),
        ],
    },
    {
        "key": "function_design",
        "title_en": "Function Design and Closures",
        "title_ru": "Проектирование функций и замыкания",
        "description_en": "Default arguments, keyword-only values, closures and pure functions.",
        "description_ru": "Аргументы по умолчанию, именованные аргументы, замыкания и чистые функции.",
        "questions": [
            _q("beginner", "What should one well-designed function usually do?", "Что обычно должна делать хорошо спроектированная функция?", "One clear job", ["Every task in the program", "Only print text", "Create a global variable"],
               explanation_en="A function should have a single responsibility (Single Responsibility Principle) making it easier to test and reuse.",
               explanation_ru="Функция должна выполнять одну задачу (принцип единственной ответственности), что упрощает тестирование и повторное использование.",
               option_rationales_en={
                   "One clear job": "Correct. Functions should be focused.",
                   "Every task in the program": "Incorrect. That creates a monolithic, unmaintainable function.",
                   "Only print text": "Incorrect. Functions often return values instead of printing.",
                   "Create a global variable": "Incorrect. Global variables should generally be avoided."
               },
               option_rationales_ru={
                   "One clear job": "Верно. Функции должны быть сфокусированы.",
                   "Every task in the program": "Неверно. Это делает функцию монолитной и сложной.",
                   "Only print text": "Неверно. Функции чаще возвращают значения, а не печатают их.",
                   "Create a global variable": "Неверно. Глобальных переменных лучше избегать."
               }),
            _q("beginner", "Why are return values useful?", "Почему полезны возвращаемые значения?", "Other code can reuse the result", ["They close Python", "They make every variable global", "They remove parameters"],
               explanation_en="Returning a value allows the calling code to store, manipulate, or pass the result to other functions.",
               explanation_ru="Возврат значения позволяет вызывающему коду сохранить результат, изменить его или передать другим функциям.",
               option_rationales_en={
                   "Other code can reuse the result": "Correct. This enables composition.",
                   "They close Python": "Incorrect. 'exit()' or 'sys.exit()' closes Python.",
                   "They make every variable global": "Incorrect. Variables remain local unless declared global.",
                   "They remove parameters": "Incorrect. Return values do not affect parameters."
               },
               option_rationales_ru={
                   "Other code can reuse the result": "Верно. Это позволяет комбинировать код.",
                   "They close Python": "Неверно. Python закрывают другие функции.",
                   "They make every variable global": "Неверно. Переменные остаются локальными.",
                   "They remove parameters": "Неверно. Возвращаемые значения не влияют на параметры."
               }),
            _q("intermediate", "Why should a list usually not be a mutable default argument?", "Почему список обычно не стоит использовать как изменяемый аргумент по умолчанию?", "The same list can be reused across calls", ["Lists cannot store values", "Defaults run after return", "Python converts it to a tuple"],
               explanation_en="Default arguments are evaluated once when the function is defined, so a mutable default like a list is shared between all calls.",
               explanation_ru="Аргументы по умолчанию вычисляются один раз при определении функции, поэтому изменяемый аргумент, такой как список, используется совместно при всех вызовах.",
               option_rationales_en={
                   "The same list can be reused across calls": "Correct. Modifications persist across calls.",
                   "Lists cannot store values": "Incorrect. Lists do store values.",
                   "Defaults run after return": "Incorrect. Defaults are evaluated at definition time.",
                   "Python converts it to a tuple": "Incorrect. It remains a list."
               },
               option_rationales_ru={
                   "The same list can be reused across calls": "Верно. Изменения сохраняются между вызовами.",
                   "Lists cannot store values": "Неверно. Списки могут хранить значения.",
                   "Defaults run after return": "Неверно. Аргументы вычисляются при создании функции.",
                   "Python converts it to a tuple": "Неверно. Он остаётся списком."
               }),
            _q("intermediate", "What is a closure?", "Что такое замыкание?", "A function that remembers values from an outer scope", ["A closed file", "A loop with break", "A private class"],
               explanation_en="A closure is an inner function that has access to variables in its enclosing scope, even after the outer function has returned.",
               explanation_ru="Замыкание - это внутренняя функция, которая имеет доступ к переменным из внешней области видимости, даже после того как внешняя функция завершила работу.",
               option_rationales_en={
                   "A function that remembers values from an outer scope": "Correct. It 'closes over' the variables.",
                   "A closed file": "Incorrect. This refers to file I/O.",
                   "A loop with break": "Incorrect. This is just flow control.",
                   "A private class": "Incorrect. Python doesn't have strict private classes."
               },
               option_rationales_ru={
                   "A function that remembers values from an outer scope": "Верно. Она 'замыкает' переменные.",
                   "A closed file": "Неверно. Это относится к вводу/выводу.",
                   "A loop with break": "Неверно. Это управление потоком.",
                   "A private class": "Неверно. Это не связано с замыканиями."
               }),
            _q("advanced", "What is a pure function?", "Что такое чистая функция?", "A function without hidden side effects for the same inputs", ["A function with no parameters", "A function that only prints", "A function inside a class"],
               explanation_en="A pure function always returns the same output for the same input and causes no observable side effects (like mutating globals or doing I/O).",
               explanation_ru="Чистая функция всегда возвращает одинаковый результат для одних и тех же входных данных и не вызывает побочных эффектов.",
               option_rationales_en={
                   "A function without hidden side effects for the same inputs": "Correct. This makes it highly predictable and testable.",
                   "A function with no parameters": "Incorrect. Pure functions usually take parameters.",
                   "A function that only prints": "Incorrect. Printing is actually a side effect.",
                   "A function inside a class": "Incorrect. That's a method."
               },
               option_rationales_ru={
                   "A function without hidden side effects for the same inputs": "Верно. Это делает её предсказуемой и тестируемой.",
                   "A function with no parameters": "Неверно. Обычно они принимают параметры.",
                   "A function that only prints": "Неверно. Вывод на экран - это побочный эффект.",
                   "A function inside a class": "Неверно. Это называется методом."
               }),
        ],
    },
    {
        "key": "advanced_oop",
        "title_en": "Advanced Object-Oriented Python",
        "title_ru": "Продвинутое объектно-ориентированное программирование",
        "description_en": "Properties, class methods, static methods and special methods.",
        "description_ru": "Свойства, методы класса, статические и специальные методы.",
        "questions": [
            _q("beginner", "Which special method creates a readable string for users?", "Какой специальный метод создаёт понятную строку для пользователя?", "__str__", ["__len__", "__add__", "__enter__"],
               explanation_en="The __str__ method returns a human-readable string representation of an object.",
               explanation_ru="Метод __str__ возвращает человекочитаемое строковое представление объекта.",
               option_rationales_en={
                   "__str__": "Correct. Used by print() and str().",
                   "__len__": "Incorrect. Returns the length.",
                   "__add__": "Incorrect. Implements addition.",
                   "__enter__": "Incorrect. Used in context managers."
               },
               option_rationales_ru={
                   "__str__": "Верно. Используется print() и str().",
                   "__len__": "Неверно. Возвращает длину.",
                   "__add__": "Неверно. Реализует сложение.",
                   "__enter__": "Неверно. Для контекстных менеджеров."
               }),
            _q("beginner", "What does @property allow?", "Что позволяет @property?", "Method logic accessed like an attribute", ["A class to become a list", "Every method to be static", "Imports inside objects"],
               explanation_en="The @property decorator allows you to define a method that can be accessed like a regular attribute.",
               explanation_ru="Декоратор @property позволяет определить метод, к которому можно обращаться как к обычному атрибуту.",
               option_rationales_en={
                   "Method logic accessed like an attribute": "Correct. E.g., obj.name instead of obj.name().",
                   "A class to become a list": "Incorrect. That requires implementing sequence methods.",
                   "Every method to be static": "Incorrect. That's what @staticmethod is for.",
                   "Imports inside objects": "Incorrect. Imports are independent of @property."
               },
               option_rationales_ru={
                   "Method logic accessed like an attribute": "Верно. Например, obj.name вместо obj.name().",
                   "A class to become a list": "Неверно. Для этого нужны методы последовательностей.",
                   "Every method to be static": "Неверно. Для этого есть @staticmethod.",
                   "Imports inside objects": "Неверно. Импорты не зависят от @property."
               }),
            _q("intermediate", "What is the first parameter of a class method usually called?", "Как обычно называется первый параметр метода класса?", "cls", ["self", "this", "class"],
               explanation_en="By convention, the first parameter of a class method (decorated with @classmethod) is named 'cls', representing the class itself.",
               explanation_ru="По соглашению, первый параметр метода класса (с декоратором @classmethod) называется 'cls' и представляет сам класс.",
               option_rationales_en={
                   "cls": "Correct. It refers to the class.",
                   "self": "Incorrect. 'self' is for instance methods.",
                   "this": "Incorrect. Used in Java/C++/JS, not Python.",
                   "class": "Incorrect. 'class' is a reserved keyword."
               },
               option_rationales_ru={
                   "cls": "Верно. Это ссылка на сам класс.",
                   "self": "Неверно. 'self' - для методов экземпляра.",
                   "this": "Неверно. Используется в других языках.",
                   "class": "Неверно. 'class' - зарезервированное слово."
               }),
            _q("intermediate", "When is @staticmethod suitable?", "Когда подходит @staticmethod?", "The behavior belongs to the class but needs no instance or class data", ["The method must change self", "The method creates every object", "The method must be recursive"],
               explanation_en="Static methods don't receive an implicit first argument (neither self nor cls) and behave like regular functions, but belong in the class's namespace.",
               explanation_ru="Статические методы не получают неявный первый аргумент (ни self, ни cls) и ведут себя как обычные функции внутри класса.",
               option_rationales_en={
                   "The behavior belongs to the class but needs no instance or class data": "Correct. It relies only on its parameters.",
                   "The method must change self": "Incorrect. Static methods don't have access to 'self'.",
                   "The method creates every object": "Incorrect. Class methods or __new__ create objects.",
                   "The method must be recursive": "Incorrect. Recursion has nothing to do with static methods."
               },
               option_rationales_ru={
                   "The behavior belongs to the class but needs no instance or class data": "Верно. Зависит только от своих аргументов.",
                   "The method must change self": "Неверно. У них нет доступа к 'self'.",
                   "The method creates every object": "Неверно. Для этого есть методы класса или __new__.",
                   "The method must be recursive": "Неверно. Рекурсия здесь ни при чём."
               }),
            _q("advanced", "Which special method can define len(obj)?", "Какой специальный метод может определить len(obj)?", "__len__", ["__size__", "__count__", "__str__"],
               explanation_en="Implementing __len__(self) allows the built-in len() function to work on instances of your class.",
               explanation_ru="Реализация __len__(self) позволяет использовать встроенную функцию len() для экземпляров вашего класса.",
               option_rationales_en={
                   "__len__": "Correct. Python calls this when len() is used.",
                   "__size__": "Incorrect. Not a standard Python magic method.",
                   "__count__": "Incorrect. Not a standard Python magic method.",
                   "__str__": "Incorrect. This is for string representation."
               },
               option_rationales_ru={
                   "__len__": "Верно. Python вызывает его при использовании len().",
                   "__size__": "Неверно. Это не стандартный магический метод.",
                   "__count__": "Неверно. Это не стандартный магический метод.",
                   "__str__": "Неверно. Это для строкового представления."
               }),
        ],
    },
    {
        "key": "dataclasses_typing",
        "title_en": "Dataclasses and Type Hints",
        "title_ru": "Dataclass и подсказки типов",
        "description_en": "Describing data objects and documenting expected value types.",
        "description_ru": "Описание объектов данных и ожидаемых типов значений.",
        "questions": [
            _q("beginner", "What do type hints mainly communicate?", "Что в основном сообщают подсказки типов?", "Expected value types", ["Guaranteed runtime speed", "File permissions", "Loop counts"],
               explanation_en="Type hints serve as documentation and help static analyzers check if variables hold the correct types.",
               explanation_ru="Подсказки типов служат документацией и помогают статическим анализаторам проверять правильность типов переменных.",
               option_rationales_en={
                   "Expected value types": "Correct. They show what types functions expect.",
                   "Guaranteed runtime speed": "Incorrect. Type hints don't affect performance in Python.",
                   "File permissions": "Incorrect. Irrelevant to type hints.",
                   "Loop counts": "Incorrect. Irrelevant to type hints."
               },
               option_rationales_ru={
                   "Expected value types": "Верно. Они показывают ожидаемые типы.",
                   "Guaranteed runtime speed": "Неверно. Они не влияют на скорость работы.",
                   "File permissions": "Неверно. Не связано с типами.",
                   "Loop counts": "Неверно. Не связано с типами."
               }),
            _q("beginner", "Do standard Python type hints normally block every wrong type at runtime?", "Обычные подсказки типов всегда блокируют неверный тип во время выполнения?", "No", ["Yes", "Only for strings", "Only in loops"],
               explanation_en="Type hints are not strictly enforced at runtime by default in Python; they are 'hints'.",
               explanation_ru="В Python подсказки типов по умолчанию не применяются строго во время выполнения; это лишь 'подсказки'.",
               option_rationales_en={
                   "No": "Correct. You need a tool like mypy to check them.",
                   "Yes": "Incorrect. Python runtime ignores them.",
                   "Only for strings": "Incorrect. They are ignored for all types.",
                   "Only in loops": "Incorrect. They are completely ignored by the interpreter."
               },
               option_rationales_ru={
                   "No": "Верно. Для проверки нужен инструмент вроде mypy.",
                   "Yes": "Неверно. Выполнение Python их игнорирует.",
                   "Only for strings": "Неверно. Игнорируются для всех типов.",
                   "Only in loops": "Неверно. Интерпретатор их полностью игнорирует."
               }),
            _q("intermediate", "Which decorator creates a data-focused class with generated methods?", "Какой декоратор создаёт класс данных с готовыми методами?", "@dataclass", ["@property", "@staticmethod", "@data"],
               explanation_en="The @dataclass decorator automatically adds generated special methods like __init__ and __repr__ to user-defined classes.",
               explanation_ru="Декоратор @dataclass автоматически добавляет сгенерированные специальные методы, такие как __init__ и __repr__.",
               option_rationales_en={
                   "@dataclass": "Correct. Found in the dataclasses module.",
                   "@property": "Incorrect. Used for getter methods.",
                   "@staticmethod": "Incorrect. Used for static methods.",
                   "@data": "Incorrect. There is no built-in @data decorator."
               },
               option_rationales_ru={
                   "@dataclass": "Верно. Находится в модуле dataclasses.",
                   "@property": "Неверно. Используется для геттеров.",
                   "@staticmethod": "Неверно. Для статических методов.",
                   "@data": "Неверно. Такого встроенного декоратора нет."
               }),
            _q("intermediate", "What does list[str] describe?", "Что описывает list[str]?", "A list expected to contain strings", ["A string converted to a list automatically", "A list named str", "A fixed-length tuple"],
               explanation_en="Using generics in type hints, list[str] specifies a list where every element should be a string.",
               explanation_ru="С использованием обобщений, list[str] указывает на список, каждый элемент которого должен быть строкой.",
               option_rationales_en={
                   "A list expected to contain strings": "Correct. This is the standard syntax for typed lists.",
                   "A string converted to a list automatically": "Incorrect. Type hints don't convert data.",
                   "A list named str": "Incorrect. 'str' is the type parameter.",
                   "A fixed-length tuple": "Incorrect. That would be tuple[type, ...]."
               },
               option_rationales_ru={
                   "A list expected to contain strings": "Верно. Это стандартный синтаксис типизированных списков.",
                   "A string converted to a list automatically": "Неверно. Подсказки типов не меняют данные.",
                   "A list named str": "Неверно. 'str' - это параметр типа.",
                   "A fixed-length tuple": "Неверно. Это был бы кортеж (tuple)."
               }),
            _q("advanced", "Which tool commonly checks type hints without running the program?", "Какой инструмент обычно проверяет подсказки типов без запуска программы?", "A static type checker", ["The print function", "A web browser", "The math module"],
               explanation_en="Tools like mypy, pyright, or pylance statically analyze Python code using type hints to catch bugs before execution.",
               explanation_ru="Инструменты вроде mypy, pyright или pylance статически анализируют код, используя подсказки типов, чтобы находить ошибки до запуска.",
               option_rationales_en={
                   "A static type checker": "Correct. Examples include mypy or pyright.",
                   "The print function": "Incorrect. print() just outputs data.",
                   "A web browser": "Incorrect. Browsers do not check Python code.",
                   "The math module": "Incorrect. Math handles numeric calculations."
               },
               option_rationales_ru={
                   "A static type checker": "Верно. Например, mypy или pyright.",
                   "The print function": "Неверно. print() просто выводит данные.",
                   "A web browser": "Неверно. Браузеры не проверяют код на Python.",
                   "The math module": "Неверно. Модуль math нужен для вычислений."
               }),
        ],
    },
    {
        "key": "paths_context",
        "title_en": "Paths and Context Managers",
        "title_ru": "Пути и контекстные менеджеры",
        "description_en": "Using pathlib and safely managing files or other resources.",
        "description_ru": "Использование pathlib и безопасное управление файлами и ресурсами.",
        "questions": [
            _q("beginner", "Which modern module works with filesystem paths?", "Какой современный модуль работает с путями файловой системы?", "pathlib", ["random", "decimal", "typing"],
               explanation_en="The pathlib module offers classes representing filesystem paths with semantics appropriate for different operating systems.",
               explanation_ru="Модуль pathlib предоставляет классы для работы с путями файловой системы с семантикой для разных ОС.",
               option_rationales_en={
                   "pathlib": "Correct. It provides an object-oriented approach to paths.",
                   "random": "Incorrect. Used for random number generation.",
                   "decimal": "Incorrect. Used for precise arithmetic.",
                   "typing": "Incorrect. Used for type hints."
               },
               option_rationales_ru={
                   "pathlib": "Верно. Объектно-ориентированный подход к путям.",
                   "random": "Неверно. Для генерации случайных чисел.",
                   "decimal": "Неверно. Для точной арифметики.",
                   "typing": "Неверно. Для подсказок типов."
               }),
            _q("beginner", "What keyword starts a context manager block?", "Какое слово начинает блок контекстного менеджера?", "with", ["using", "context", "open"],
               explanation_en="The 'with' statement simplifies exception handling by encapsulating common preparation and cleanup tasks.",
               explanation_ru="Оператор 'with' упрощает обработку исключений, объединяя подготовку и очистку ресурсов.",
               option_rationales_en={
                   "with": "Correct. Syntax is 'with context_manager() as variable:'.",
                   "using": "Incorrect. 'using' is from C#, not Python.",
                   "context": "Incorrect. Not a Python keyword.",
                   "open": "Incorrect. open() is a function often used *in* a with statement."
               },
               option_rationales_ru={
                   "with": "Верно. Синтаксис: 'with контекстный_менеджер() as переменная:'.",
                   "using": "Неверно. Это ключевое слово в C#.",
                   "context": "Неверно. Это не ключевое слово.",
                   "open": "Неверно. Это функция, часто используемая с with."
               }),
            _q("intermediate", "Why is Path('folder') / 'file.txt' useful?", "Почему удобно Path('folder') / 'file.txt'?", "It joins path parts clearly", ["It divides file contents", "It deletes the folder", "It opens the file automatically"],
               explanation_en="The division operator (/) is overloaded in pathlib to safely join path components across operating systems.",
               explanation_ru="Оператор деления (/) в pathlib переопределён для безопасного соединения путей независимо от ОС.",
               option_rationales_en={
                   "It joins path parts clearly": "Correct. It avoids manually dealing with os.path.join or slashes.",
                   "It divides file contents": "Incorrect. It operates on the path string, not contents.",
                   "It deletes the folder": "Incorrect. Creating a path doesn't delete anything.",
                   "It opens the file automatically": "Incorrect. You still need to call .open() or .read_text()."
               },
               option_rationales_ru={
                   "It joins path parts clearly": "Верно. Избавляет от необходимости использовать os.path.join.",
                   "It divides file contents": "Неверно. Оно не делит содержимое.",
                   "It deletes the folder": "Неверно. Это не удаляет файлы.",
                   "It opens the file automatically": "Неверно. Файл нужно открывать отдельно."
               }),
            _q("intermediate", "What does a context manager guarantee for a file?", "Что контекстный менеджер гарантирует для файла?", "Cleanup such as closing it", ["The file has no errors", "The file is always empty", "The filename is changed"],
               explanation_en="A context manager ensures its __exit__ block executes, safely closing the file even if an exception occurs.",
               explanation_ru="Контекстный менеджер гарантирует выполнение блока __exit__, безопасно закрывая файл даже при исключении.",
               option_rationales_en={
                   "Cleanup such as closing it": "Correct. This prevents resource leaks.",
                   "The file has no errors": "Incorrect. Reading/writing can still raise errors.",
                   "The file is always empty": "Incorrect. It doesn't modify the data unless asked to.",
                   "The filename is changed": "Incorrect. It doesn't rename files."
               },
               option_rationales_ru={
                   "Cleanup such as closing it": "Верно. Предотвращает утечки ресурсов.",
                   "The file has no errors": "Неверно. Ошибки ввода-вывода всё равно могут быть.",
                   "The file is always empty": "Неверно. Оно не очищает файл само по себе.",
                   "The filename is changed": "Неверно. Имя файла не меняется."
               }),
            _q("advanced", "Which methods define a custom context manager class?", "Какие методы определяют собственный класс контекстного менеджера?", "__enter__ and __exit__", ["__start__ and __stop__", "__open__ and __close__", "__init__ and __str__"],
               explanation_en="To support the 'with' statement, a class must implement both __enter__() and __exit__().",
               explanation_ru="Для поддержки 'with' класс должен реализовывать методы __enter__() и __exit__().",
               option_rationales_en={
                   "__enter__ and __exit__": "Correct. These are the magic methods for context managers.",
                   "__start__ and __stop__": "Incorrect. Not standard Python magic methods.",
                   "__open__ and __close__": "Incorrect. Those are conceptual, but not the Python method names.",
                   "__init__ and __str__": "Incorrect. These are for initialization and string representation."
               },
               option_rationales_ru={
                   "__enter__ and __exit__": "Верно. Это магические методы для контекстных менеджеров.",
                   "__start__ and __stop__": "Неверно. Таких стандартов нет.",
                   "__open__ and __close__": "Неверно. Это не магические методы.",
                   "__init__ and __str__": "Неверно. Это для создания объекта и его вывода."
               }),
        ],
    },
    {
        "key": "testing_debugging",
        "title_en": "Testing and Debugging",
        "title_ru": "Тестирование и отладка",
        "description_en": "Assertions, unit tests, tracebacks and systematic debugging.",
        "description_ru": "Утверждения, модульные тесты, traceback и системная отладка.",
        "questions": [
            _q("beginner", "What is a test meant to check?", "Что должен проверять тест?", "Whether code behaves as expected", ["Whether the screen is bright", "Whether Python is installed twice", "Whether variables have long names"],
               explanation_en="Tests are automated checks to verify that code correctly implements its intended behavior.",
               explanation_ru="Тесты - это автоматизированные проверки того, что код правильно реализует своё ожидаемое поведение.",
               option_rationales_en={
                   "Whether code behaves as expected": "Correct. Tests assert expected outcomes.",
                   "Whether the screen is bright": "Incorrect. Nonsense answer.",
                   "Whether Python is installed twice": "Incorrect. Nonsense answer.",
                   "Whether variables have long names": "Incorrect. Linting checks code style, not tests."
               },
               option_rationales_ru={
                   "Whether code behaves as expected": "Верно. Тесты проверяют логику кода.",
                   "Whether the screen is bright": "Неверно. Бессмысленный ответ.",
                   "Whether Python is installed twice": "Неверно. Бессмысленный ответ.",
                   "Whether variables have long names": "Неверно. Это проверяют линтеры, а не тесты."
               }),
            _q("beginner", "What information does a traceback provide?", "Какую информацию даёт traceback?", "Where and how an error happened", ["Only the final answer", "A list of installed games", "The computer password"],
               explanation_en="A traceback lists the sequence of function calls that led to an unhandled exception.",
               explanation_ru="Traceback (трассировка) показывает последовательность вызовов функций, приведших к необработанному исключению.",
               option_rationales_en={
                   "Where and how an error happened": "Correct. It shows the file, line, and sequence of calls.",
                   "Only the final answer": "Incorrect. It shows the whole path.",
                   "A list of installed games": "Incorrect. Nonsense answer.",
                   "The computer password": "Incorrect. It has no access to that."
               },
               option_rationales_ru={
                   "Where and how an error happened": "Верно. Показывает файл, строку и путь ошибки.",
                   "Only the final answer": "Неверно. Он показывает весь путь.",
                   "A list of installed games": "Неверно. Бессмысленный ответ.",
                   "The computer password": "Неверно. У него нет к этому доступа."
               }),
            _q("intermediate", "What happens when assert condition fails?", "Что происходит, если условие assert ложно?", "AssertionError is raised", ["The condition becomes true", "Python silently fixes it", "A file is created"],
               explanation_en="The assert statement checks a condition and raises an AssertionError if it evaluates to False.",
               explanation_ru="Инструкция assert проверяет условие и вызывает AssertionError, если оно ложно.",
               option_rationales_en={
                   "AssertionError is raised": "Correct. This typically fails a test.",
                   "The condition becomes true": "Incorrect. Assertions don't alter state.",
                   "Python silently fixes it": "Incorrect. Python throws an error.",
                   "A file is created": "Incorrect. No files are created."
               },
               option_rationales_ru={
                   "AssertionError is raised": "Верно. Обычно это означает провал теста.",
                   "The condition becomes true": "Неверно. Assert не меняет состояние.",
                   "Python silently fixes it": "Неверно. Возникает ошибка.",
                   "A file is created": "Неверно. Файлы не создаются."
               }),
            _q("intermediate", "Why should tests include edge cases?", "Почему тесты должны включать граничные случаи?", "Bugs often appear at unusual limits", ["Edge cases always run faster", "They replace normal cases", "They remove exceptions"],
               explanation_en="Edge cases (like empty lists, zeroes, negative numbers) are common sources of logic errors.",
               explanation_ru="Граничные случаи (пустые списки, нули, отрицательные числа) - частый источник логических ошибок.",
               option_rationales_en={
                   "Bugs often appear at unusual limits": "Correct. Boundary conditions are prone to bugs.",
                   "Edge cases always run faster": "Incorrect. Speed is not the goal.",
                   "They replace normal cases": "Incorrect. Both normal and edge cases should be tested.",
                   "They remove exceptions": "Incorrect. They often trigger hidden exceptions."
               },
               option_rationales_ru={
                   "Bugs often appear at unusual limits": "Верно. Граничные условия подвержены ошибкам.",
                   "Edge cases always run faster": "Неверно. Скорость тут ни при чём.",
                   "They replace normal cases": "Неверно. Тестировать нужно и то, и другое.",
                   "They remove exceptions": "Неверно. Они часто их вызывают."
               }),
            _q("advanced", "What makes a good unit test independent?", "Что делает хороший модульный тест независимым?", "It does not depend on another test running first", ["It uses no functions", "It prints every variable", "It must connect to the internet"],
               explanation_en="Tests should be runnable in any order, so each test must set up and clean up its own state.",
               explanation_ru="Тесты должны выполняться в любом порядке, поэтому каждый тест должен сам готовить и очищать своё состояние.",
               option_rationales_en={
                   "It does not depend on another test running first": "Correct. Isolation prevents cascading test failures.",
                   "It uses no functions": "Incorrect. Tests call functions.",
                   "It prints every variable": "Incorrect. Printing makes tests noisy, not independent.",
                   "It must connect to the internet": "Incorrect. Unit tests should generally avoid internet calls."
               },
               option_rationales_ru={
                   "It does not depend on another test running first": "Верно. Изоляция предотвращает каскадные ошибки.",
                   "It uses no functions": "Неверно. Тесты вызывают функции.",
                   "It prints every variable": "Неверно. Печать не влияет на независимость.",
                   "It must connect to the internet": "Неверно. Модульные тесты обычно работают локально."
               }),
        ],
    },
    {
        "key": "algorithms_complexity",
        "title_en": "Algorithms and Complexity",
        "title_ru": "Алгоритмы и сложность",
        "description_en": "Breaking down problems, searching, sorting and estimating work.",
        "description_ru": "Разбиение задач, поиск, сортировка и оценка количества работы.",
        "questions": [
            _q("beginner", "What is an algorithm?", "Что такое алгоритм?", "A step-by-step solution to a problem", ["A Python color theme", "A single variable", "A file extension"],
               explanation_en="An algorithm is a finite sequence of well-defined, computer-implementable instructions.",
               explanation_ru="Алгоритм - это конечная последовательность чётких инструкций для решения проблемы.",
               option_rationales_en={
                   "A step-by-step solution to a problem": "Correct. It is a logical recipe.",
                   "A Python color theme": "Incorrect. Nonsense answer.",
                   "A single variable": "Incorrect. Variables store data, they aren't instructions.",
                   "A file extension": "Incorrect. E.g. .py or .txt."
               },
               option_rationales_ru={
                   "A step-by-step solution to a problem": "Верно. Это логический рецепт.",
                   "A Python color theme": "Неверно. Бессмысленный ответ.",
                   "A single variable": "Неверно. Переменная просто хранит данные.",
                   "A file extension": "Неверно. Например, .py или .txt."
               }),
            _q("beginner", "What should happen before writing a complex program?", "Что стоит сделать перед написанием сложной программы?", "Break the problem into smaller steps", ["Add many global variables", "Avoid examples", "Write random loops"],
               explanation_en="Decomposition makes large problems manageable and reduces logical errors.",
               explanation_ru="Декомпозиция делает большие задачи решаемыми и уменьшает логические ошибки.",
               option_rationales_en={
                   "Break the problem into smaller steps": "Correct. Planning and decomposition are key.",
                   "Add many global variables": "Incorrect. This causes more bugs.",
                   "Avoid examples": "Incorrect. Examples help understand the problem.",
                   "Write random loops": "Incorrect. Code should be planned."
               },
               option_rationales_ru={
                   "Break the problem into smaller steps": "Верно. Планирование и декомпозиция важны.",
                   "Add many global variables": "Неверно. Это вызовет много багов.",
                   "Avoid examples": "Неверно. Примеры помогают понять задачу.",
                   "Write random loops": "Неверно. Код нужно планировать."
               }),
            _q("intermediate", "What does linear search do?", "Что делает линейный поиск?", "Checks items one by one", ["Always checks the middle item", "Sorts without comparisons", "Uses a database"],
               explanation_en="Linear search iterates through every element sequentially until the target is found.",
               explanation_ru="Линейный поиск перебирает каждый элемент по очереди, пока не найдёт цель.",
               option_rationales_en={
                   "Checks items one by one": "Correct. It operates in O(n) time.",
                   "Always checks the middle item": "Incorrect. That's binary search.",
                   "Sorts without comparisons": "Incorrect. Searching isn't sorting.",
                   "Uses a database": "Incorrect. It's a fundamental algorithm, not a technology."
               },
               option_rationales_ru={
                   "Checks items one by one": "Верно. Работает за время O(n).",
                   "Always checks the middle item": "Неверно. Это бинарный поиск.",
                   "Sorts without comparisons": "Неверно. Поиск - не сортировка.",
                   "Uses a database": "Неверно. Это базовый алгоритм."
               }),
            _q("intermediate", "What must usually be true before binary search?", "Что обычно должно быть верно перед бинарным поиском?", "The data is sorted", ["The data contains strings only", "The list is empty", "The values are random"],
               explanation_en="Binary search relies on the array being sorted to halve the search space at each step.",
               explanation_ru="Бинарный поиск работает, только если массив отсортирован, чтобы на каждом шаге отсекать половину вариантов.",
               option_rationales_en={
                   "The data is sorted": "Correct. Otherwise, it cannot reliably eliminate halves.",
                   "The data contains strings only": "Incorrect. It works on numbers or any sorted data.",
                   "The list is empty": "Incorrect. It works on populated lists.",
                   "The values are random": "Incorrect. Random order breaks binary search."
               },
               option_rationales_ru={
                   "The data is sorted": "Верно. Иначе он не сможет отсекать половины.",
                   "The data contains strings only": "Неверно. Работает с любыми сортируемыми данными.",
                   "The list is empty": "Неверно. Поиск по пустому списку не имеет смысла.",
                   "The values are random": "Неверно. Случайный порядок сломает алгоритм."
               }),
            _q("advanced", "What does O(n) commonly mean?", "Что обычно означает O(n)?", "Work grows roughly with the number of items", ["The program takes exactly n seconds", "No work is required", "The result is always a number"],
               explanation_en="Big O notation describes the upper bound of the algorithm's complexity; O(n) means linear time complexity.",
               explanation_ru="О-большое описывает верхнюю границу сложности алгоритма; O(n) означает линейную сложность.",
               option_rationales_en={
                   "Work grows roughly with the number of items": "Correct. It scales linearly with input size n.",
                   "The program takes exactly n seconds": "Incorrect. It measures operations, not exact seconds.",
                   "No work is required": "Incorrect. O(1) means constant work, but there is still work.",
                   "The result is always a number": "Incorrect. Output type is irrelevant to complexity."
               },
               option_rationales_ru={
                   "Work grows roughly with the number of items": "Верно. Время растёт пропорционально n.",
                   "The program takes exactly n seconds": "Неверно. Измеряются операции, а не секунды.",
                   "No work is required": "Неверно. Несвязанный ответ.",
                   "The result is always a number": "Неверно. Тип результата не связан со сложностью."
               }),
        ],
    },
    {
        "key": "async_concurrency",
        "title_en": "Async Programming Basics",
        "title_ru": "Основы асинхронного программирования",
        "description_en": "Coroutines, await and handling waiting tasks efficiently.",
        "description_ru": "Корутины, await и эффективная работа с задачами ожидания.",
        "questions": [
            _q("beginner", "Which keywords define an asynchronous function?", "Какие слова определяют асинхронную функцию?", "async def", ["await def", "async function", "parallel def"],
               explanation_en="'async def' declares an asynchronous coroutine in Python.",
               explanation_ru="'async def' объявляет асинхронную сопрограмму (корутину) в Python.",
               option_rationales_en={
                   "async def": "Correct. Syntax is: async def my_func():",
                   "await def": "Incorrect. await is used to call the function.",
                   "async function": "Incorrect. That's JavaScript syntax.",
                   "parallel def": "Incorrect. Python doesn't use the keyword 'parallel'."
               },
               option_rationales_ru={
                   "async def": "Верно. Синтаксис: async def my_func():",
                   "await def": "Неверно. await используется для вызова.",
                   "async function": "Неверно. Это синтаксис JavaScript.",
                   "parallel def": "Неверно. Нет такого ключевого слова."
               }),
            _q("beginner", "What kind of work benefits most from async programming?", "Какая работа чаще всего выигрывает от async?", "Tasks that spend time waiting for input or network data", ["Simple addition only", "Renaming variables", "Writing comments"],
               explanation_en="Async programming excels at I/O-bound tasks, allowing the program to do other things while waiting for the network or disk.",
               explanation_ru="Асинхронность отлично подходит для задач ввода-вывода (I/O bound), позволяя программе делать другие дела во время ожидания сети или диска.",
               option_rationales_en={
                   "Tasks that spend time waiting for input or network data": "Correct. This is I/O-bound concurrency.",
                   "Simple addition only": "Incorrect. CPU-bound math doesn't benefit from async.",
                   "Renaming variables": "Incorrect. Irrelevant to runtime.",
                   "Writing comments": "Incorrect. Irrelevant to runtime."
               },
               option_rationales_ru={
                   "Tasks that spend time waiting for input or network data": "Верно. Это конкурентность для задач ввода/вывода.",
                   "Simple addition only": "Неверно. Математика - это CPU-задачи.",
                   "Renaming variables": "Неверно. Никак не связано с работой кода.",
                   "Writing comments": "Неверно. Комментарии не выполняются."
               }),
            _q("intermediate", "What does await do?", "Что делает await?", "Pauses the coroutine until an awaitable is ready", ["Stops the whole computer", "Creates a class", "Converts data to JSON"],
               explanation_en="The 'await' keyword yields execution back to the event loop until the awaited operation completes.",
               explanation_ru="Ключевое слово 'await' возвращает выполнение циклу событий до завершения ожидаемой операции.",
               option_rationales_en={
                   "Pauses the coroutine until an awaitable is ready": "Correct. It suspends execution gracefully.",
                   "Stops the whole computer": "Incorrect. It's a software concurrency tool.",
                   "Creates a class": "Incorrect. Classes use the 'class' keyword.",
                   "Converts data to JSON": "Incorrect. That's json.loads()."
               },
               option_rationales_ru={
                   "Pauses the coroutine until an awaitable is ready": "Верно. Она мягко приостанавливает выполнение корутины.",
                   "Stops the whole computer": "Неверно. Это инструмент программирования.",
                   "Creates a class": "Неверно. Для этого нужно ключевое слово 'class'.",
                   "Converts data to JSON": "Неверно. Для этого есть модуль json."
               }),
            _q("intermediate", "Can await normally be used directly inside a regular def function?", "Можно ли обычно использовать await прямо внутри обычной функции def?", "No", ["Yes, anywhere", "Only in a list", "Only after print"],
               explanation_en="The 'await' keyword can only be used inside a function defined with 'async def' (a coroutine).",
               explanation_ru="Слово 'await' можно использовать только внутри функции, определённой через 'async def'.",
               option_rationales_en={
                   "No": "Correct. Doing so raises a SyntaxError.",
                   "Yes, anywhere": "Incorrect. It must be in an async context.",
                   "Only in a list": "Incorrect. Comprehensions can have async/await, but only inside coroutines.",
                   "Only after print": "Incorrect. Completely unrelated."
               },
               option_rationales_ru={
                   "No": "Верно. Иначе будет ошибка синтаксиса.",
                   "Yes, anywhere": "Неверно. Только в асинхронном контексте.",
                   "Only in a list": "Неверно. Это не имеет значения.",
                   "Only after print": "Неверно. Вывод не влияет."
               }),
            _q("advanced", "What is the event loop responsible for?", "За что отвечает цикл событий?", "Scheduling and resuming asynchronous tasks", ["Compiling CSS", "Creating database tables automatically", "Changing type hints"],
               explanation_en="The event loop is the core of an async application; it runs asynchronous tasks and callbacks, performs network I/O operations, and runs subprocesses.",
               explanation_ru="Цикл событий — ядро асинхронного приложения; он запускает задачи, обрабатывает сетевой I/O и управляет выполнением корутин.",
               option_rationales_en={
                   "Scheduling and resuming asynchronous tasks": "Correct. It manages the queue of awaitables.",
                   "Compiling CSS": "Incorrect. Nonsense answer.",
                   "Creating database tables automatically": "Incorrect. ORMs do this, not the event loop.",
                   "Changing type hints": "Incorrect. Type hints are static."
               },
               option_rationales_ru={
                   "Scheduling and resuming asynchronous tasks": "Верно. Он управляет очередью задач.",
                   "Compiling CSS": "Неверно. Бессмысленный ответ.",
                   "Creating database tables automatically": "Неверно. Этим занимаются ORM.",
                   "Changing type hints": "Неверно. Подсказки статические."
               }),
        ],
    },
]
