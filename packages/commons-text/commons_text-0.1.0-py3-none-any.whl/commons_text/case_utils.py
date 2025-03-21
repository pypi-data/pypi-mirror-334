import re


def str_to_camel_case(s: str, capitalize_first_letter: bool = False, delimiter: str = "_"):
    components = s.split(delimiter)
    if capitalize_first_letter:
        components = [x.capitalize() for x in components]
    return components[0] + "".join(x.title() for x in components[1:])


def str_to_snake_case(s: str, capitalize_first_letter: bool = False, delimiter: str = "_"):
    ss = re.sub("(.)([A-Z][a-z]+)", rf"\1{delimiter}\2", s)
    result = re.sub("([a-z0-9])([A-Z])", rf"\1{delimiter}\2", ss).lower()
    if capitalize_first_letter:
        return delimiter.join([part.capitalize() for part in result.split(delimiter)])
    return result


def object_to_camel_case(
        data: object,
        capitalize_first_letter: bool = False,
        delimiter: str = "_"
):
    if isinstance(data, dict):
        return {
            str_to_camel_case(k, capitalize_first_letter, delimiter): object_to_camel_case(
                v,
                capitalize_first_letter,
                delimiter
            )
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [object_to_camel_case(v, capitalize_first_letter, delimiter) for v in data]
    return data


def object_to_snake_case(
        data: object,
        capitalize_first_letter: bool = False,
        delimiter: str = "_"
):
    if isinstance(data, dict):
        return {
            str_to_snake_case(k, capitalize_first_letter, delimiter): object_to_snake_case(
                v,
                capitalize_first_letter,
                delimiter
            )
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [object_to_snake_case(v, capitalize_first_letter, delimiter) for v in data]
    return data
