import random
from string import ascii_lowercase, ascii_uppercase, digits, punctuation


def integer(min_size=-100, max_size=100):
    def inner():
        return random.randint(min_size, max_size)

    return inner


def floating(min=-100, max=100):
    def inner():
        return random.random()*(max - min) - min

    return inner


def positive_integer(min_size=0, max_size=100):
    return integer(min_size, max_size)


def full_string(
        allow_lowercase: bool = True,
        allow_uppercase: bool = True,
        allow_digits: bool = True,
        allow_punctuation: bool = True,
        minlen: int = 1,
        maxlen: int = 20,
        forbidden_strings: list[str] = None,
        ending_with: str = ""
):
    if forbidden_strings is None:
        forbidden_strings = []
    alphabet: str = ""
    if allow_lowercase:
        alphabet += ascii_lowercase
    if allow_uppercase:
        alphabet += ascii_uppercase
    if allow_digits:
        alphabet += digits
    if allow_punctuation:
        alphabet += punctuation

    def inner() -> str:
        length: int = random.randint(minlen, maxlen)
        while True:
            candidate: str = "".join([random.choice(ascii_lowercase) for _ in range(length)])
            if candidate in forbidden_strings:
                continue
            return candidate + ending_with

    return inner


def lowercase_string(
        minlen: int = 1, maxlen: int = 20, forbidden_strings: list[str] = None,
        ending_with: str = ""
):
    return full_string(True, False, False, False, minlen, maxlen, forbidden_strings, ending_with)


def uppercase_string(minlen: int = 1, maxlen: int = 20, forbidden_strings=None):
    return full_string(False, True, False, False, minlen, maxlen, forbidden_strings)


def character_string(minlen: int = 1, maxlen: int = 20, forbidden_strings=None):
    return full_string(True, True, False, False, minlen, maxlen, forbidden_strings)


def verbatim_string(minlen: int = 1, maxlen: int = 20, forbidden_strings=None):
    return full_string(True, True, False, True, minlen, maxlen, forbidden_strings)


def digit_string(minlen: int = 1, maxlen: int = 20, forbidden_strings=None):
    return full_string(False, False, True, False, minlen, maxlen, forbidden_strings)


def no_digit_string(minlen: int = 1, maxlen: int = 20, forbidden_strings=None):
    return full_string(True, True, False, True, minlen, maxlen, forbidden_strings)


def boolean():
    def inner():
        return random.random() < 0.5
    return inner


def any_type():
    return random.choice([integer(), full_string(), boolean()])


def list_of(generator, minlen: int = 1, maxlen: int = 10):
    def inner():
        length: int = random.randint(minlen, maxlen)
        return [generator() for _ in range(length)]
    return inner


def dict_of(
        key_generator, value_generator, minlen: int = 1,maxlen: int = 10,
        fixed_values=None
):
    if fixed_values is None:
        fixed_values = {}
    def inner():
        length: int = random.randint(minlen, maxlen)
        generated_dict = {key_generator(): value_generator() for _ in range(length)}
        generated_dict.update(fixed_values)
        return generated_dict
    return inner


def dict_with_fixed_keys(keys, value_generator, fixed_values=None):
    if fixed_values is None:
        fixed_values = {}
    def inner():
        generated_dict = {key: value_generator() for key in keys}
        generated_dict.update(fixed_values)
        return generated_dict
    return inner


def dict_with_fixed_not_mandatory_keys(keys, value_generator, min_n_keys=0, max_n_keys=10, fixed_values=None):
    def inner():
        k: int = random.randint(min_n_keys, min(max_n_keys, len(keys)))
        subkeys = random.sample(keys, k)
        return dict_with_fixed_keys(subkeys, value_generator, fixed_values)()

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
