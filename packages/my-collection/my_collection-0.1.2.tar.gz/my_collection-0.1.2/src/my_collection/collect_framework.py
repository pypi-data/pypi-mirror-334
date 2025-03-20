import argparse  # для обробки аргументів командного рядку

import sys  # для виводу помилок і завершення програми

from src.my_collection.unique_char import unique_char_count  # імпорт функції


def read_file(file_path):  # зчитує вміст файлу та повертає його як рядок
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # відкриває файл для читання, utf-8 для корректної роботи з символами
            return f.read().strip()
        # читає файл і видаляє зайві пробіли на початку та в кінці
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        # вивід помилки в stderr
        sys.exit(1)
        # завершення програми з кодом 1 (помилка)
    except OSError:
        print(f"Error: Cannot read file '{file_path}'.", file=sys.stderr)
        sys.exit(1)
        # якщо є проблема з читанням файлу - теж завершення програми


def parse_arguments():  # парсить аргументи командного рядка та повертає їх
    parser = argparse.ArgumentParser()
    # створює парсер аргументів
    parser.add_argument("--string", type=str, help="Input string to process")
    # додає аргумент, який очікує текстовий рядок
    parser.add_argument("--file", type=str, help="Path to a text file to process")
    # додає аргумент, який очікує шлях до файлу
    args = parser.parse_args()
    # зчитує аргументи

    if args.file:  # пріоритет файлу, якщо він є - ігнор string
        return argparse.Namespace(string=None, file=args.file)
    return args  # повертає args у якому збережені передані аргументи


def get_input_text(args):  # отримує вхідні дані для обробки
    if args.file:
        return read_file(args.file)  # зчитує файл і повертає його як текст
    elif args.string:
        return args.string  # повертає рядок без змін
    else:
        print("Error: Either --string or --file must be provided.", file=sys.stderr)
        sys.exit(1)  # якщо жоден аргумент не передано - виводить помилку


def main():
    args = parse_arguments()  # отримує аргументи командного рядку
    input_text = get_input_text(args)  # отримує текст для обробки
    result = unique_char_count(input_text)  # рахує унікальні символи в тексті
    print(f"Unique character count: {result}")


if __name__ == "__main__":  # перевіряє чи запущено код напряму, а не імпортовано як модуль
    main()
