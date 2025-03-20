import pytest

from src.my_collection.unique_char import unique_char_count


@pytest.mark.parametrize("input_str, expected", [
    ("abbbccdf", 3),
    ("aabbcc", 0),
    ("abcdef", 6),
    ("aaaaaa", 0),
    ("tennessee", 1),
    ("xyz", 3),
])
def test_unique_char_count(input_str, expected):
    assert unique_char_count(input_str) == expected


# тести для валідації типів(нетипові випадки)
@pytest.mark.parametrize("invalid_input", [123, None, ["a", "b", "c"], {"a": 1}, 3.14])
def test_unique_char_count_invalid_type(invalid_input):
    with pytest.raises(TypeError, match="Expected input of type str"):
        unique_char_count(invalid_input)


# тести для перевірки роботи кеша
def test_cache_behavior():
    assert unique_char_count("abbbccdf") == 3  # перше виконання (обчислення)
    assert unique_char_count("abbbccdf") == 3  # повторне виконання з (кешу)

    assert unique_char_count("abbbccdf") == 3  # має обчислювати знову
