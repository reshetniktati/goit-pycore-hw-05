"""
Завдання 4: Консольний бот-асистент (CLI) з обробкою помилок через декоратор
"""
from typing import Dict, Tuple, Callable
from functools import wraps


def input_error(func: Callable) -> Callable:
    """
    Декоратор, який перехоплює типові помилки вводу користувача
    і повертає дружні повідомлення замість винятків.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except IndexError:
            # Напр.: не вказали ім'я для команди phone
            return "Enter user name."
        except ValueError as e:
            # Якщо хендлер підняв ValueError із конкретним текстом — повернемо його,
            # інакше — дефолтне повідомлення.
            msg = str(e).strip()
            return msg if msg else "Give me name and phone please."
    return inner


def parse_input(user_input: str) -> Tuple[str, ...]:
    """
    Розбиває введений рядок на команду та аргументи.
    Повертає кортеж: (command, *args)
    """
    parts = user_input.split()
    if not parts:
        return ("",)
    cmd, *args = parts
    cmd = cmd.strip().lower()
    return (cmd, *args)


@input_error
def add_contact(args, contacts: Dict[str, str]) -> str:
    """
    Додає контакт: add <name> <phone>
    Піднімає ValueError, якщо не передано рівно 2 аргументи.
    """
    if len(args) != 2:
        # конкретне повідомлення для декоратора
        raise ValueError("Give me name and phone please.")
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts: Dict[str, str]) -> str:
    """
    Змінює телефон контакту: change <name> <new_phone>
    - ValueError, якщо не 2 аргументи
    - KeyError, якщо контакту не існує
    """
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, new_phone = args
    if name not in contacts:
        # Декоратор перетворить KeyError -> "Contact not found."
        raise KeyError(name)
    contacts[name] = new_phone
    return "Contact updated."


@input_error
def show_phone(args, contacts: Dict[str, str]) -> str:
    """
    Показує телефон: phone <name>
    - IndexError, якщо не передали ім'я
    - KeyError, якщо контакту не існує
    """
    if len(args) < 1:
        # Декоратор поверне "Enter user name."
        raise IndexError("name is required")
    name = args[0]
    if name not in contacts:
        raise KeyError(name)
    return contacts[name]


@input_error
def show_all(contacts: Dict[str, str]) -> str:
    """
    Показує всі контакти. Помилок вводу не очікується.
    """
    if not contacts:
        return "No contacts."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def help_text() -> str:
    return (
        "Commands:\n"
        "  hello                       -> How can I help you?\n"
        "  add <name> <phone>          -> Add a contact\n"
        "  change <name> <new_phone>   -> Change phone\n"
        "  phone <name>                -> Show phone by name\n"
        "  all                         -> Show all contacts\n"
        "  close | exit                -> Quit\n"
    )


def main() -> None:
    contacts: Dict[str, str] = {}
    print("Welcome to the assistant bot!")
    print("Type 'help' to see available commands.")
    while True:
        user_input = input("Enter a command: ").strip()
        command, *args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "help":
            print(help_text())
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        elif command == "":
            # порожній ввід — просто продовжуємо цикл
            continue
        else:
            print("Invalid command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
