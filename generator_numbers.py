import re
from typing import Callable, Generator

NUMBER_PATTERN = re.compile(r"(?<=\s)[+-]?\d+(?:\.\d+)?(?=\s)")

def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Повертає генератор дійсних чисел із тексту.
    За умовою числа чітко відокремлені пробілами з обох боків.
    Приклади збігів: ' 100 ', ' -12.5 ', ' +0.75 '.
    """
    for m in NUMBER_PATTERN.finditer(f" {text} "):  # обгортка пробілами спрощує краї рядка
        yield float(m.group())


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Обчислює суму всіх чисел, які повертає генератор `func(text)`.
    Повертає суму, заокруглену до 2 знаків після коми.
    """
    # Використовуємо вбудовану суму; для підвищеної точності можна замінити на math.fsum
    total = sum(func(text))
    return round(total, 2)
