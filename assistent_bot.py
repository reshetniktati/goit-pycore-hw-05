from typing import Dict, Tuple, Callable
from functools import wraps

def input_error(func: Callable) -> Callable:
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name."
        except ValueError:
            return "Give me name and phone please."
    return inner

def parse_input(user_input: str) -> Tuple[str, ...]:
    parts = user_input.split()
    return ("",) if not parts else (parts[0].lower(), *parts[1:])

@input_error
def add_contact(args, contacts: Dict[str, str]) -> str:
    name, phone = args  # ValueError якщо не рівно 2 аргументи
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts: Dict[str, str]) -> str:
    name, new_phone = args  # ValueError якщо не рівно 2
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = new_phone
    return "Contact updated."

@input_error
def show_phone(args, contacts: Dict[str, str]) -> str:
    name = args[0]            # IndexError якщо немає аргументів
    return contacts[name]     # KeyError якщо контакту немає

@input_error
def show_all(contacts: Dict[str, str]) -> str:
    return "No contacts." if not contacts else "\n".join(f"{n}: {p}" for n, p in contacts.items())
