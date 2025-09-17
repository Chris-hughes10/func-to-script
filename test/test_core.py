import ast
import subprocess

from pytest import mark

from func_to_script.core import extract_descriptions_from_docstring
from test.scripts.script_with_defaults import (
    DEFAULT_STR_ARG,
    DEFAULT_INT_ARG,
    DEFAULT_FLOAT_ARG,
    DEFAULT_BOOL_ARG,
    fn_with_defaults,
)


def execute_command(command):
    # Run commands from the test directory so scripts/ is accessible
    import os
    test_dir = os.path.dirname(__file__)
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=test_dir).stdout.decode("utf-8")
    output_dict = ast.literal_eval(output)
    return output_dict


def test_can_get_output_from_script():
    result = execute_command(
        "python scripts/script_no_defaults.py --str_arg test --int_arg 42 --float_arg 42 --bool_arg False"
    )
    print(result)
    pass


@mark.parametrize(
    ("str_arg", "int_arg", "float_arg", "bool_arg"),
    [("test", 42, 42.0, False), ("test2", 21, 50.0, True)],
)
def test_can_call_script(str_arg, int_arg, float_arg, bool_arg):
    result = execute_command(
        f"python scripts/script_no_defaults.py --str_arg {str_arg}"
        f" --int_arg {int_arg} --float_arg {float_arg} --bool_arg {bool_arg}"
    )

    assert result["str_arg"] == str_arg
    assert result["int_arg"] == int_arg
    assert result["float_arg"] == float_arg
    assert result["bool_arg"] == bool_arg


def test_can_call_script_with_defaults():
    result = execute_command(f"python scripts/script_with_defaults.py")

    assert result["str_arg"] == DEFAULT_STR_ARG
    assert result["int_arg"] == DEFAULT_INT_ARG
    assert result["float_arg"] == DEFAULT_FLOAT_ARG
    assert result["bool_arg"] == DEFAULT_BOOL_ARG


def test_can_override_script_with_defaults():
    str_arg = "override_str"
    int_arg = 24
    float_arg = 12.0
    bool_arg = True

    result = execute_command(
        f"python scripts/script_with_defaults.py --str_arg {str_arg} "
        f"--int_arg {int_arg} --float_arg {float_arg} --bool_arg {bool_arg}"
    )

    assert result["str_arg"] == str_arg
    assert result["int_arg"] == int_arg
    assert result["float_arg"] == float_arg
    assert result["bool_arg"] == bool_arg


def test_can_override_some_args_script_with_defaults():
    str_arg = "override_str"
    bool_arg = True

    result = execute_command(
        f"python scripts/script_with_defaults.py --str_arg {str_arg} "
        f" --bool_arg {bool_arg}"
    )

    assert result["str_arg"] == str_arg
    assert result["int_arg"] == DEFAULT_INT_ARG
    assert result["float_arg"] == DEFAULT_FLOAT_ARG
    assert result["bool_arg"] == bool_arg


def test_can_call_as_function():
    result = fn_with_defaults()

    assert result["str_arg"] == DEFAULT_STR_ARG
    assert result["int_arg"] == DEFAULT_INT_ARG
    assert result["float_arg"] == DEFAULT_FLOAT_ARG
    assert result["bool_arg"] == DEFAULT_BOOL_ARG


def test_can_override_arguments_as_function():
    override_str = "override_str"
    override_int = 2
    override_float = 4.0
    override_bool = True

    result = fn_with_defaults(override_str, override_int, override_float, override_bool)

    assert result["str_arg"] == override_str
    assert result["int_arg"] == override_int
    assert result["float_arg"] == override_float
    assert result["bool_arg"] == override_bool


def test_can_override_arguments_as_function_kwargs():
    override_str = "override_str"
    override_int = 2
    override_float = 4.0
    override_bool = True

    result = fn_with_defaults(
        str_arg=override_str,
        int_arg=override_int,
        float_arg=override_float,
        bool_arg=override_bool,
    )

    assert result["str_arg"] == override_str
    assert result["int_arg"] == override_int
    assert result["float_arg"] == override_float
    assert result["bool_arg"] == override_bool


def test_no_type_hint_raises_exception():
    import os
    test_dir = os.path.dirname(__file__)
    command = f"python scripts/script_with_missing_types.py"

    output = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=test_dir
    ).stderr.decode("utf-8")

    assert "TypeError" in output


def test_invalid_type_raises_exception():
    import os
    test_dir = os.path.dirname(__file__)
    command = f"python scripts/script_with_incorrect_type.py"

    output = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=test_dir
    ).stderr.decode("utf-8")

    assert "ValueError" in output


def test_can_extract_docstring():
    def fn_with_docstring(arg_1: str, arg_2: int):
        """
        A short description of what this function does. You can call this function like so:

            result = fn_with_docstring('hello', 3)

        :param arg_1: a string argument
        :param arg_2: an integer argument

        :return a note on what is returned

        Additional details are after the params

        """
        pass

    docstring = fn_with_docstring.__doc__
    descriptions = extract_descriptions_from_docstring(docstring)

    assert descriptions == {
        "arg_1": "a string argument",
        "arg_2": "an integer argument",
    }


def test_can_extract_docstring_with_no_params():
    def fn_with_docstring(arg_1: str, arg_2: int):
        """
        A short description of what this function does. Figure out the arguments yourself

        """
        pass

    docstring = fn_with_docstring.__doc__
    descriptions = extract_descriptions_from_docstring(docstring)

    assert descriptions == {}


def test_can_extract_docstring_with_no_param_descriptions():
    def fn_with_docstring(arg_1: str, arg_2: int):
        """
        A short description of what this function does.

        :param arg_1
        :param arg_2

        """
        pass

    docstring = fn_with_docstring.__doc__
    descriptions = extract_descriptions_from_docstring(docstring)

    assert descriptions == {}
