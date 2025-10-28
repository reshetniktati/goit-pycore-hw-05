from typing import Callable, Dict

def caching_fibonacci() -> Callable[[int], int]:
    """
    Повертає функцію fibonacci(n), яка обчислює n-те число Фібоначчі,
    використовуючи кешування результатів у замиканні.

    Правила (за умовою):
      - якщо n <= 0 → повернути 0
      - якщо n == 1 → повернути 1
      - інакше F(n) = F(n-1) + F(n-2)
    """
    
    cache: Dict[int, int] = {0: 0, 1: 1}  # початкові значення

    def fibonacci(n: int) -> int:
        if not isinstance(n, int):
            raise TypeError("Аргумент n має бути цілим числом")
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]

        # рекурсивне обчислення з мемоізацією
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci
