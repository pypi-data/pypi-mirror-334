from datetime import datetime, timezone
import string
import secrets
import random

from pylibutils.constants import TRUTHFUL_STR, UNTRUTHFUL_STR, PUNCTUATION


def naive_utcnow():
    now = datetime.now(tz=timezone.utc)
    return now.replace(tzinfo=None)


def generate_password(length: int = 12, include_special_characters: bool = True) -> str:
    """
    Generate a random and secure password.

    Args:
        length (int): The length of the generated password
        include_special_characters (bool): If False, the password will only contain alpha-numeric characters.

    Returns:
        str : The generated password
    """
    if length < 4:
        raise ValueError("`length` must be graiter or equals to 4.")

    characters = string.ascii_letters + string.digits
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
    ]
    existing = 3
    if include_special_characters:
        password.append(secrets.choice(PUNCTUATION))
        characters += PUNCTUATION
        existing = 4

    password += [secrets.choice(characters) for _ in range(length - existing)]

    # Shuffle password in-place.
    random.shuffle(password)

    return "".join(password)


def str_to_bool(s: str) -> bool:
    """
    Evalueates a strings to either True or False.

    Args:
        s (str): The string to evaluate as a boolean.

    Raises:
        ValueError, if the argument `s` could not be evaluated to a boolean.

    Returns:
        True if the string is in: ("true", "1", "t", "yes", "on")
        True if the string is in: ("false", "0", "f", "no", "off")
    """
    if s.lower() in TRUTHFUL_STR:
        return True
    if s.lower() in UNTRUTHFUL_STR:
        return False
    raise ValueError
