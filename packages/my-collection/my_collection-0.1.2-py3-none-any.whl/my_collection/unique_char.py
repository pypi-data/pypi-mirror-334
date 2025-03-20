from collections import Counter
# імпортує Counter з модуля collections для підрахунку кількості повторень кожного елемента

from functools import lru_cache
# імпортує lru_cache з модуля functools, щоб при повторному виклику з тим самим аргументом
# не потрібно було виконувати оьчислення ще раз


def unique_char_count(s):
    # підраховує кількість унікальних символів у рядку
    if not isinstance(s, str):
        # якщо s рядок - продовжить роботу, якщо ні - умова виконається і піде в raise TypeError(...)
        raise TypeError("Expected input of type str")
    # перевірка ще до кешування
    return _cached_unique_char_count(s)


@lru_cache(maxsize=None)
# додає кещування до ф-ії unique_char_count
# кеш може зберігати необмежену кількість результатів
def _cached_unique_char_count(s):
    # функція з кешуванням викликається тільки для рядків
    char_counts = Counter(s)
    return sum(1 for c in char_counts if char_counts[c] == 1)
# обчислення унікальних символів


if __name__ == "__main__":
    print(unique_char_count("abbbccdf"))
    # перевіряє чи виконується напряму і виводить результат тестового рядка
