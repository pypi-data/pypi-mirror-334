from mutationtracker.settings import Settings


def do_nothing(*_, **__):
    pass


def is_private_name(attribute_name: str) -> bool:
    return attribute_name.startswith("_")


def is_ignored_caller_module(caller_module: str) -> bool:
    if (
        caller_module is None
        or caller_module not in Settings.ignored_caller_module_names
    ):
        return False
    return True
