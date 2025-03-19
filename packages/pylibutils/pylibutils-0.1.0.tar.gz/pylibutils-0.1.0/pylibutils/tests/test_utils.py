import string

import pytest

from pylibutils.utils import str_to_bool, generate_password, naive_utcnow
from pylibutils.constants import TRUTHFUL_STR, UNTRUTHFUL_STR, PUNCTUATION


def test_str_to_bool():
    for true_value in TRUTHFUL_STR:
        assert str_to_bool(true_value) is True

    for false_value in UNTRUTHFUL_STR:
        assert str_to_bool(false_value) is False

    with pytest.raises(ValueError):
        str_to_bool("UNRESOLVED_VALUE")


def test_generate_password_length():
    pwd1 = generate_password()
    assert len(pwd1) == 12

    pwd2 = generate_password(8)
    assert len(pwd2) == 8

    with pytest.raises(ValueError):
        generate_password(0)


def test_generate_password_all_characters():
    pwd = generate_password()
    pwd_set = set(pwd)
    assert pwd_set & set(PUNCTUATION)
    assert pwd_set & set(string.ascii_lowercase)
    assert pwd_set & set(string.ascii_uppercase)
    assert pwd_set & set(string.digits)


def test_generate_password_exclude_special_characters():
    pwd = generate_password(include_special_characters=False)
    pwd_set = set(pwd)
    assert pwd_set & set(string.ascii_lowercase)
    assert pwd_set & set(string.ascii_uppercase)
    assert pwd_set & set(string.digits)
    assert not (pwd_set & set(PUNCTUATION))
