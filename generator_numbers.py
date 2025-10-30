import re
from typing import Callable, Generator
import math

NUMBER_PATTERN = re.compile(r'(?:^| )([+-]?\d+(?:\.\d+)?)(?=(?: |$))')

def generator_numbers(text: str) -> Generator[float, None, None]:
    for m in NUMBER_PATTERN.finditer(text):
        yield float(m.group(1))

def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    return round(math.fsum(func(text)), 2)
