# tools_example.py — готовый пример реестра инструментов.
# Два инструмента: current_time (текущее время) и calc (безопасный
# калькулятор). Это образец, по которому вы пишете свой tools.py.
# Копировать не нужно: набирайте руками и сверяйтесь.

import ast
import operator
import time


# --- инструмент 1: текущее время ---------------------------------

def current_time():
    return time.strftime("%H:%M")


# --- инструмент 2: безопасный калькулятор ------------------------

# Разрешены только числа и знаки + - * /. Ничего другого ast не пустит.
_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

_ALLOWED = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Add, ast.Sub,
            ast.Mult, ast.Div, ast.Constant)


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("Неподдерживаемое выражение")


def calc(expression):
    tree = ast.parse(expression, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED):
            raise ValueError("Разрешены только числа и + - * /")
    return str(_eval(tree.body))


# --- схемы для модели ---------------------------------------------

ALL_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "current_time",
            "description": "Текущее время на компьютере в формате ЧЧ:ММ.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calc",
            "description": "Считает простое арифметическое выражение "
                           "из чисел и знаков + - * /.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Выражение, например '2 + 3 * 4'.",
                    },
                },
                "required": ["expression"],
            },
        },
    },
]


# --- dispatch: по имени инструмента зовём нужную функцию ----------

def dispatch(name, args):
    if name == "current_time":
        return current_time()
    if name == "calc":
        return calc(args.get("expression", ""))
    return "Инструмент не найден: " + name


# --- быстрая проверка без модели ---------------------------------

if __name__ == "__main__":
    print("время:", dispatch("current_time", {}))
    print("calc:", dispatch("calc", {"expression": "2 + 3 * 4"}))
