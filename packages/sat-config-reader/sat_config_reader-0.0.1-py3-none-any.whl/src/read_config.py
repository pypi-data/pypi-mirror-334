from configparser import ConfigParser
from typing import Union, Any
from os import path
from dataclasses import is_dataclass

BOOLEAN_TRUE_VALUES = [True, 'true', 'yes', 'on']
BOOLEAN_FALSE_VALUES = [False, 'false', 'no', 'off']
BOOLEAN_VALUES = BOOLEAN_TRUE_VALUES + BOOLEAN_FALSE_VALUES




def config_reader(items: Union[str, list], obj=None) -> dict[str, Any]:

    if obj is not None and type(obj) is not dict and not is_dataclass(obj):
        raise AttributeError("obj should be from type DICT or DATACLASS")

    obj = {} if obj is None else obj

    _list_items = []

    # is a single config file, we convert it to a list
    if type(items) is str:
        _list_items = list([items])

    if type(items) is list:
        _list_items = items

    # get the absolut path to the items
    abs_items = __get_abs_path(_list_items)

    # parses the config file
    config_parser = ConfigParser()
    config_parser.read(abs_items)

    config_dict = {}

    for section in config_parser.sections():
        config = config_parser.items(section)
        if type(obj) is dict:
            config_dict[section] = {__key(key): __cast_value(value) for key, value in config}

        if is_dataclass(obj):
            kwargs = {__key(key): __cast_value(value) for key, value in config}
            config_dict[section] = obj(**kwargs)

    return config_dict


def __get_abs_path(items: list[str]) -> list[str]:
    path_items = []
    for path_item in items:
        abs_path = path.abspath(path_item)
        if not path.exists(abs_path):
            raise FileNotFoundError(f"File {abs_path} not exists")

        path_items.append(abs_path)

    return path_items


def __key(value: str) -> str:
    return value.strip(" ").upper()


def __cast_value(value: str):
    value = value.strip(" ")

    # check is boolean
    if __is_bool_value(value):
        return True if value.lower() in BOOLEAN_TRUE_VALUES \
            else False if value.lower() in BOOLEAN_FALSE_VALUES \
            else value

    # check is number
    if __is_int_value(value):
        return int(value)

    # check is list value
    if __is_list_value(value):
        # nested list
        if value.startswith("\n") and value.__contains__("\n"):
            list_items = [
                __cast_value(i.strip(" "))
                for i in value.split("\n")
                if i not in ["\n", ""]
            ]
        else:
            list_items = [__cast_value(i.strip(" ")) for i in value.split(",")]

        return list_items

    # check is dict value
    if __is_dict_value(value):
        items: list[str] = value.strip("{ }").split(",")
        list_value = [item.strip(" ").split(":") for item in items]
        return {k.strip(" "): __cast_value(v.strip(" ")) for k, v in list_value}

    # values in quotation marks are strings
    if value.startswith("\"") and value.endswith("\""):
        return value[1:-1]

    return value


def __is_bool_value(value: str) -> bool:
    return True if value.lower() in BOOLEAN_VALUES else False


def __is_int_value(value: str) -> bool:
    if value[0] in ('-', '+'):
        is_int = value[1:].isdigit()
    else:
        is_int = value.isdigit()

    return True if is_int is True else False


def __is_list_value(value: str) -> bool:

    def is_flat(v):
        return True if not __is_dict_value(v) and v.__contains__(",") else False

    def is_nested(v):
        return True if v.startswith("\n") and v.__contains__("\n") else False

    is_list = False
    if is_flat(value) or is_nested(value):
        is_list = True

    return is_list


def __is_dict_value(value: str) -> bool:
    return True if value[0] == "{" else False
