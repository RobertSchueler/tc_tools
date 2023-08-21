SEPARATOR = ":"


def parse_configuration_file(options_file_path: str) -> str:
    options_dict: dict = {}
    with open(options_file_path, "r", encoding="utf-8") as file:
        for line in file:
            if SEPARATOR not in line:
                continue
            key, *option_tup = line.split(SEPARATOR)
            option: str = SEPARATOR.join(option_tup)
            options_dict[key] = option
    return options_dict["inkscape_path"]

