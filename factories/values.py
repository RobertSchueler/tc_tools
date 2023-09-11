import random
from string import ascii_lowercase, ascii_uppercase, digits, punctuation


def positive_integer():
    return random.randint(0, 100)


def integer():
    return random.randint(-100, 100)


def full_string(
        allow_lowercase: bool = True,
        allow_uppercase: bool = True,
        allow_digits: bool = True,
        allow_punctuation: bool = True,
        minlen: int = 1,
        maxlen: int = 20
):
    alphabet: str = ""
    if allow_lowercase:
        alphabet += ascii_lowercase
    if allow_uppercase:
        alphabet += ascii_uppercase
    if allow_digits:
        alphabet += digits
    if allow_punctuation:
        alphabet += punctuation

    length: int = random.randint(minlen, maxlen)
    return "".join([random.choice(ascii_lowercase) for _ in range(length)])


def lowercase_string(minlen: int = 1, maxlen: int = 20):
    return full_string(True, False, False, False, minlen, maxlen)


def uppercase_string(minlen: int = 1, maxlen: int = 20):
    return full_string(False, True, False, False, minlen, maxlen)


def character_string(minlen: int = 1, maxlen: int = 20):
    return full_string(True, True, False, False, minlen, maxlen)


def verbatim_string(minlen: int = 1, maxlen: int = 20):
    return full_string(True, True, False, True, minlen, maxlen)


def digit_string(minlen: int = 1, maxlen: int = 20):
    return full_string(False, False, True, False, minlen, maxlen)


def no_digit_string(minlen: int = 1, maxlen: int = 20):
    return full_string(True, True, False, True, minlen, maxlen)


def boolean():
    return random.random() < 0.5


def any_type():
    return random.choice([integer, full_string, boolean])()


def list_of(generator, minlen: int = 1, maxlen: int = 10):
    def inner():
        length: int = random.randint(minlen, maxlen)
        return [generator() for _ in range(length)]
    return inner


def dict_of(key_generator, value_generator, minlen: int = 1, maxlen: int = 10):
    def inner():
        length: int = random.randint(minlen, maxlen)
        return {key_generator(): value_generator() for _ in range(length)}
    return inner


def dict_with_fixed_keys(keys, value_generator):
    def inner():
        return {key: value_generator() for key in keys}
    return inner


def concatenate_dicts(dict_generator, other_dict_generator):
    def inner():
        generated_dict: dict = dict_generator()
        generated_dict.update(other_dict_generator())
        return generated_dict
    return inner


def tuple_of(*generators):
    def inner():
        return (generator() for generator in generators)
    return inner
