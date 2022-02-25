import argparse
import functools
import inspect
import sys
from types import SimpleNamespace


def extract_descriptions_from_docstring(docstring):
    descriptions = {}
    if docstring is not None:
        docstring = docstring.strip()

        first_param_index = docstring.find(":param")

        post_param_description = docstring[first_param_index:]

        lines = post_param_description.split("\n")
        for line in lines:
            line = line.strip()

            if ":param" in line:
                param_and_description = line.split(":param ")[1]
                split_description = param_and_description.split(":")
                description = "".join(split_description[1:]).strip()
                if description != "":
                    descriptions[split_description[0].strip()] = "".join(
                        split_description[1:]
                    ).strip()

    else:
        descriptions = {}

    return descriptions


def bool_checker(arg: str):
    return arg.lower() in ["true", "t", "yes", "1"]


def create_parser(func):
    docstring = func.__doc__
    parser = argparse.ArgumentParser(description=docstring)

    descriptions = extract_descriptions_from_docstring(docstring)

    for param_name, param in inspect.signature(func).parameters.items():

        desc = descriptions.get(param_name, None)

        param_type = param.annotation
        if param_type is inspect._empty:
            raise TypeError(
                f"Parameter {param_name} is missing a type hint. Please ensure that all argument types "
                "are explicitly specified"
            )
        else:
            if param_type not in {str, int, float, bool}:
                raise ValueError(
                    f"Parameter {param_name} has an incorrect type. The only types that are supported are str, int, float and bool"
                )
            # do type check
            if param_type == bool:
                param_type = bool_checker

        param_default = param.default
        if param_default is inspect._empty:
            has_default = False
            param_default = None
        else:
            has_default = True

        parser.add_argument(
            f"--{param_name}",
            help=desc,
            type=param_type,
            default=param_default,
            required=not has_default,
        )
    return parser


def merge(*ds):
    "Merge all dictionaries in `ds`"
    return {k: v for d in ds if d is not None for k, v in d.items()}


def script(func):
    script_info = SimpleNamespace(func=None)

    module = inspect.getmodule(inspect.currentframe().f_back)

    if not module:
        # called from a notebook
        return func

    @functools.wraps(func)
    def scripted_function(*args, **kwargs):
        mod = inspect.getmodule(inspect.currentframe().f_back)
        if not mod:
            return func(*args, **kwargs)
        if not script_info.func and mod.__name__ == "__main__":
            script_info.func = func.__name__
        if len(sys.argv) > 1 and sys.argv[1] == "":
            sys.argv.pop(1)
        p = create_parser(func)
        args = p.parse_args().__dict__
        args = merge(args, kwargs)
        return func(**args)

    if module.__name__ == "__main__":
        setattr(module, func.__name__, scripted_function)
        script_info.func = func.__name__
        return scripted_function
    else:
        return func
