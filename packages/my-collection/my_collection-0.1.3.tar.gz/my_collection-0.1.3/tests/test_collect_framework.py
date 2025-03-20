import pytest

import sys  # для роботи з помилками та виходом з програми

from unittest.mock import patch, mock_open  # контролює поведінку значення/ф-ії та відкриває файли

from src.my_collection.collect_framework import parse_arguments, get_input_text, read_file


@pytest.mark.parametrize("cli_args, expected", [
    # декоратор, що тестує одну і ту ф-ію з різними вхідними даними: імітує args командного рядка-> кортеж(рядок, файл)
    (["--string", "hello"], ("hello", None)),  # введено рядок
    (["--file", "test.txt"], (None, "test.txt")),  # введено файл
    (["--string", "hello", "--file", "test.txt"], (None, "test.txt")),  # пріоритет файлу
])
def test_parse_arguments(cli_args, expected):
    with patch("sys.argv", ["collect_framework.py"] + cli_args):
        # підміна sys.argv для імітації введих в терміналі команд (["collect_framework.py","--string","hello"])
        args = parse_arguments()  # виклик parse_arguments(), що читає args
        assert (args.string, args.file) == expected  # перевірка чи отриманий результат = expected


def test_get_input_text_string():  # перевірка на повернення рядку
    class Args:  # поводиться, як результат parse_arguments
        string = "hello"
        file = None
    assert get_input_text(Args()) == "hello"  # перевірка, що ф-ія повертає "hello"


def test_get_input_text_file():  # перевірка на повернення вмісту файлу
    class Args:
        string = None
        file = "text.txt"
    with patch("src.my_collection.collect_framework.read_file", return_value="file content"):
        # підміна read_file(), щоб замість читання реального файлу повертав "file content"
        assert get_input_text(Args()) == "file content"  # перевірка чи повертає "file content"


def test_get_input_text_no_args():  # перевірка, що без args буде помилка
    class Args:
        string = None
        file = None
    with patch("sys.stderr", new_callable=lambda: sys.stdout):
        # підміна sys.stderr, щоб тест не виводив помилку в стандартний потік
        with pytest.raises(SystemExit):  # перевірка, що ф-ія завершує програму при відсутності args
            get_input_text(Args())


def test_read_file_success():  # читка файлу
    mock_data = "mock file content"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        # підміна open(), щоб замість реального файлу повертався текст "mock file content"
        assert read_file("test.txt") == "mock file content"  # перевірка чи повертається "mock file content"


def test_read_file_not_found():  # перевірка, що при відсутності файлу буде error
    with patch("sys.stderr", new_callable=lambda: sys.stdout):
        # всі error,що йшли в stderr мають виводитись в stdout
        with pytest.raises(SystemExit):
            # перевірка, що read_file("non_existent.txt") викличе sys.exit(1), коли файл не знайдено
            read_file("non_existent.txt")
