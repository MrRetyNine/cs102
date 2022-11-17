import typing as tp
import math


operations_order = {0: ("^y",), 1: ("/", "*"), 2: ("+", "-")}


def convert(number: int, base: int) -> int:
    """Перевод числа из десятичной системы в другую с основанием до 10"""
    res = 0
    n = 1
    while number > 0:
        res += (number % base) * n
        n *= 10
        number //= base
    return res


def check_int(number: float) -> tp.Union[None, int]:
    """Проверка, что вещественное число преобразуется в целочисленное без потерь"""
    if int(number) == number:
        return int(number)
    return None


def check_float(number: str) -> tp.Union[None, float]:
    """Проверка, что число вещественное"""
    try:
        value = float(number)
        return value
    except ValueError:
        return None


def check_input(value: str) -> float:
    """Проверка на ввод"""
    try:
        return float(value)
    except ValueError:
        return check_input(input("Повторите попытку > "))


def input_values(command: str) -> tuple[float, float] | tuple[float, None]:
    """Организация ввода одного или двух значений в зависимости от команды"""
    if command in ("+", "-", "*", "/", "#", "^y"):
        num_1 = check_input(input("Введите число 1 > "))
        num_2 = check_input(input("Введите число 2 > "))
        return num_1, num_2
    num = check_input(input("Введите число > "))
    return num, None


def calc(command: str, num_1: float, num_2=0.0) -> tp.Union[float, str]:  # type: ignore
    """Калькулятор операций"""
    match command:
        case "+":
            return num_1 + num_2
        case "-":
            return num_1 - num_2
        case "*":
            return num_1 * num_2
        case "/" if num_2 == 0:
            return "На о делить нельзя!"
        case "/":
            return num_1 / num_2
        case "#" if num_2 > 9:
            return "Основание СС не должно превышать 9!"
        case "#" if check_int(num_1) is None or check_int(num_2) is None:
            return "Число или основание степени не целочисленное!"
        case "#":
            return convert(int(num_1), int(num_2))
        case "^y":
            return num_1**num_2
        case "^2":
            return num_1**2
        case "sin":
            return math.sin(num_1)
        case "cos":
            return math.cos(num_1)
        case "tg":
            return math.tan(num_1)
        case "ln":
            return math.log(num_1)
        case "log":
            return math.log10(num_1)
        case _:
            return f"Неизвестная операция: {command!r}."


def parse_chain(chain: str):
    """Парсинг цепочки операторов до комбинации операторов и чисел"""
    chain = chain.replace(" ", "")
    chain = chain.replace("**", "^")
    new_chain = []
    if chain[0] == "-":
        cur_symbol = "-"
        chain = chain[1:]
    else:
        cur_symbol = ""
    for i, symbol in enumerate(chain):
        cur_symbol += symbol
        try:
            cur_symbol_f = float(cur_symbol)
            if i == len(chain) - 1:
                new_chain.append(cur_symbol_f)
        except ValueError:
            try:
                new_chain.append(float(cur_symbol[:-1]))
                if cur_symbol[-1] not in (set(operations_order[1]) | set(operations_order[2]) | {"^", "."}):
                    print("Incorrect input!")
                    return None
                new_chain.append(cur_symbol[-1])  # type: ignore
                cur_symbol = ""
            except ValueError:
                print("Incorrect input!")
                return None
    return new_chain


def calc_order(order, chain: tp.List[tp.Union[str, float]]):
    """Вычисление операций текущего порядка"""
    for j, operator in enumerate(order):
        if operator[0] == len(chain) - 2:
            chain[operator[0] - 1:] = [calc(operator[1], chain[operator[0] - 1], chain[operator[0] + 1])]
        else:
            if j != len(order) - 1:
                order[j + 1][0] -= (j + 1) * 2
            chain[operator[0] - 1: operator[0] + 2] = [
                calc(operator[1], chain[operator[0] - 1], chain[operator[0] + 1])
            ]
    return chain


def solve_chain_wt_brackets(chain):
    """
    Вычисление цепочки операторов без скобок
    >>> solve_chain_wt_brackets("2 ** 3 ** 2 - 4.6 * 3 + 3 - 5 / 2 * 4 + 3 ** 3")
    70.2
    """

    chain = parse_chain(chain)
    if chain:
        chain = ["^y" if str(elem) == "^" else elem for elem in chain]
        order_0 = [[i, elem] for i, elem in enumerate(chain) if elem in operations_order[0]]
        chain = calc_order(order_0, chain)
        order_1 = [[i, elem] for i, elem in enumerate(chain) if elem in operations_order[1]]
        chain = calc_order(order_1, chain)
        order_2 = [[i, elem] for i, elem in enumerate(chain) if elem in operations_order[2]]
        chain = calc_order(order_2, chain)
        return chain[0]
    return None


def solve_brackets(chain):
    """Вычисление цепочки операторов со скобками
    >>> solve_brackets("((2 ** 3 ** 2 - (4.6 * (3 + 3) - 5) / 2 * 4) + 3 ** 3)")
    45.8
    """
    if chain.rfind("(") == 0 and chain.find(")") == len(chain) - 1:
        return solve_chain_wt_brackets(chain[1:-1])

    ob = chain.rfind("(")
    cb = chain.find(")")
    chain = chain[:ob] + str(round(solve_chain_wt_brackets(chain[ob + 1: cb]), 2)) + chain[cb + 1:]
    return solve_brackets(chain)


def solve_chain(chain: str) -> tp.Union[float, str]:
    """Проверка и вычисление цепочки операторов"""
    if chain.count("(") + chain.count(")") == 0:
        return solve_chain_wt_brackets(chain)
    if chain.count("(") != chain.count(")") or "()" in chain:
        return "Невозможно выполнить!"
    chain = "(" + chain + ")"
    return solve_brackets(chain)


if __name__ == "__main__":
    while True:
        COMMAND = input("Введите оперцию > ")
        if COMMAND.isdigit() and int(COMMAND) == 0:
            break
        if len(COMMAND) <= 3:
            NUM_1, NUM_2 = input_values(COMMAND)
            print(calc(COMMAND, NUM_1, NUM_2))
        else:
            print(solve_chain(COMMAND))
