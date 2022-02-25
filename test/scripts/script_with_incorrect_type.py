from pathlib import Path

from func_to_script import script

DEFAULT_STR_ARG = "str_arg"
DEFAULT_INT_ARG = 42
DEFAULT_FLOAT_ARG = 42.0
DEFAULT_BOOL_ARG = False


@script
def fn_with_defaults(
    str_arg: Path = DEFAULT_STR_ARG,
    int_arg: int = DEFAULT_INT_ARG,
    float_arg: float = DEFAULT_FLOAT_ARG,
    bool_arg: bool = DEFAULT_BOOL_ARG,
):
    results = {
        "str_arg": str_arg,
        "int_arg": int_arg,
        "float_arg": float_arg,
        "bool_arg": bool_arg,
    }

    print(results)

    return results


if __name__ == "__main__":
    fn_with_defaults()
