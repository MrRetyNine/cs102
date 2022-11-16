import typing as tp
from math import cos
from math import log as ln
from math import log10, sin
from math import tan as tg

priors = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "s": 4, "c": 4, "t": 4, "l": 4, "n": 4, "g": 4}

info_logic = """Доступные операции: a+b, a-b, a/b (b != 0), a*b, a^b, a^2, sin(a), cos(a), tg(a), ctg(a), ln(a), 
log10(a), a#b - перевод целого неотрицательного числа a из десятичной системы счисления в b (2 <= b <= 36).
Если ввести в качестве операции (), то далее на вход будет ожидаться полноценное выражение. Подобный ввод
предусматривает все перечисленные выше операции, кроме #. Сами операции необходимо вводить без скобок, 
т.е. вводим sin, а не sin(). Для выхода из программы напечатайте 0 на запрос ввести операцию."""


def show_info() -> None:
    """Выводит общую информацию о калькуляторе"""
    print(info_logic)


def is_int(num: tp.Any) -> bool:
    """Проверка, что число целое"""
    try:
        if int(num) == num:
            return True
    except ValueError:
        ...
    return False


def is_float(num: tp.Any) -> bool:
    """Проверка, что число вещественное"""
    try:
        float(num)
    except ValueError:
        return False
    return True


def get_num(text: str) -> float:
    """Получение одного числа"""
    value = input(text)
    if is_float(value):
        return float(value)
    return get_num("Это не вещественное число, введите число > ")


def get_numbers(command: str) -> tuple[float, float]:
    """Получение чисел (одного или двух в зависимости от типа команды)"""
    if command in "+-*/^#":
        num1 = get_num("Введите число 1 > ")
        num2 = get_num("Введите число 2 > ")
    else:
        num1 = get_num("Введите число > ")
        num2 = 0.0
    return num1, num2


def convert(num1: int, num2: int) -> str:
    """Перевод целого положительного числа из 10 СС в другую с основанием от 2 до 36"""
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    while num1 > 0:
        res = digits[num1 % num2] + res
        num1 = num1 // num2
    return res if res != "" else 0


def calculate(command: str, num1: float, num2: float = 0.0) -> tp.Union[float, str]:
    """Сам калькулятор"""
    match command:
        case "+":
            return num1 + num2
        case "-":
            return num1 - num2
        case "*":
            return num1 * num2
        case "/":
            if num2 != 0:
                return num1 / num2
            return "На ноль делить нельзя!"
        case "^":
            return num1**num2
        case "#":
            if not is_int(num1) or not is_int(num2) or num1 < 0 or num2 < 0:
                return "Числа должны быть целыми неотрицательными!"
            if not (2 <= num2 <= 36):
                return "Основание CC должно быть в диапазоне [2, 36]"
            return convert(int(num1), int(num2))
        case "^2":
            return num1**2
        case ("s" | "sin"):
            return sin(num1)
        case ("c" | "cos"):
            return cos(num1)
        case ("t" | "tg"):
            return tg(num1)
        case ("g" | "ctg"):
            return 1 / tg(num1) if tg(num1) != 0 else "Котангенса не существует!"
        case ("l" | "log10"):
            if num1 > 0:
                return log10(num1)
            return "Логарифм должен браться от положительного числа!"
        case ("n" | "ln"):
            if num1 > 0:
                return ln(num1)
            return "Логарифм должен браться от положительного числа!"
        case _:
            return f"Неизвестный оператор: {command!r}."


def brackets_are_ok(string_eq):
    """Проверка, корректно ли стоят скобки в выражении"""
    brackets = 0
    for char in string_eq:
        if char == "(":
            brackets += 1
        elif char == ")":
            brackets -= 1
            if brackets < 0:
                ok = False
                break
    else:
        ok = not brackets
    return ok


def get_string_eq(given: tp.Optional[str] = None) -> str:
    """Получение выражения со скобочками или без"""
    string_eq = input("Введите выражение > ") if given is None else given
    if brackets_are_ok(string_eq):
        string_eq = (
            string_eq.replace(" ", "")
            .replace("ctg", "g")
            .replace("sin", "s")
            .replace("cos", "c")
            .replace("tg", "t")
            .replace("log10", "l")
            .replace("ln", "n")
        )
        if string_eq.find("#") != -1:
            return "Операция перевода в другую СС не поддерживается для опции ввода выражения целиком."
        return string_eq
    return "Скобки стоят неправильно!"


def solve(string_eq: str) -> tp.Union[float, str]:
    """Решение полноценного выражения"""
    if string_eq == "":
        return ""
    if is_float(string_eq):
        return float(string_eq)
    else:
        in_brackets = 0
        best_opt = 5
        found_outside_brackets = -1
        for i, char in enumerate(string_eq):
            if char == "(":
                in_brackets += 1
            elif char == ")":
                in_brackets -= 1
            elif char in "+-*/^sctlng":
                if in_brackets == 0 and priors[char] <= best_opt:
                    found_outside_brackets = i
                    best_opt = priors[char]
        if found_outside_brackets == -1:
            if string_eq[0] == "(" and string_eq[-1] == ")":
                return solve(string_eq[1:-1])
            return string_eq
        else:
            inner_1 = solve(string_eq[:found_outside_brackets])
            inner_2 = solve(string_eq[found_outside_brackets + 1 :])
            op = string_eq[found_outside_brackets]

            # хороший (нет) способ обхода майпаевских ограничений
            if inner_1 == "" and is_float(inner_2):
                return calculate(op, 0.0, float(inner_2)) if op == "-" else calculate(op, float(inner_2))
            if is_float(inner_1) and is_float(inner_2):
                return calculate(op, float(inner_1), float(inner_2))
            return inner_1 if inner_2.isspace() else inner_2


if __name__ == "__main__":
    show_info()
    while True:
        COMMAND = input("Введите оперцию > ")
        if COMMAND.isdigit() and int(COMMAND) == 0:
            break
        if COMMAND != "()":
            NUM1, NUM2 = get_numbers(COMMAND)
            ans = calculate(COMMAND, NUM1, NUM2)
        else:
            ans = solve(get_string_eq())
        print(int(ans) if is_int(ans) else ans)
