# func-to-script: Quickly turn a function into a command-line script

`func-to-script` is a lightweight and convenient tool which can be used to turn a Python function into a command line
 script, with minimal boilerplate!

As `func-to-script` is a thin wrapper around `argparse`, it is incredibly lightweight with minimal dependencies
(only PyYAML for configuration file support).

`func-to-script` is designed to be used in simple cases, so offers a streamlined feature set.
For more complex scenarios, it is recommended to use `argparse` directly.

## Installation

`func-to-script` can be installed from pip using the following command:
```
pip install func-to-script
```

## Usage

To get started, all that you need to do is add the `script` decorator to the function that you wish to convert,
 as demonstrated below:
 
```
# say_hello_script.py

from func_to_script import script

@script
def say_hello(
    greeting: str = "Hello", name: str = "World", print_message: bool = True
):
    """
    A simple function to say hello

    :param greeting: the greeting to use
    :param name: the person to greet
    :param print_message: flag to indicate whether to print to the command line
    """
    hello_str = f"{greeting}, {name}"

    if print_message:
        print(hello_str)

    return hello_str


if __name__ == "__main__":
    say_hello()

```

We can now call this like so:
```
python say_hello_script.py --greeting hi --print_message False
```

As `func-to-script` uses regular Python type hints and default value syntax, no additional changes are required! 
If a docstring is provided, `func-to-script` will also attempt to parse this to provide descriptions of the 
required parameters to display when using:
```
python say_hello_script.py -h
```

The script decorator does not affect normal function usage, so decorated functions can still be imported and 
called elsewhere:

```
from say_hello_script import say_hello


def main():
    say_hello(print_message=True)


if __name__ == "__main__":
    main()

```

### Using YAML Configuration Files
For more complex applications, configuration can be loaded from YAML files. 
`func-to-script` provides a simple way to convert YAML configs into accessible Python objects:

```python
# config.yaml
data:
  num_classes: 80
  max_instances: 65
  image_size: 640

# train_script.py
from func_to_script import load_config_from_yaml, script

@script
def train(
    config_file: str = "config.yaml",
):
    """
    Train a model using parameters from a config file
    :param config_file: path to YAML configuration file
    """
    config = load_config_from_yaml(config_file)

    # Access config values using dot notation
    print(config.data.num_classes)  # prints: 80

    # Or use dictionary-style access
    print(config["data"]["num_classes"])  # prints: 80

    # Mix both styles as needed
    print(config.data["max_instances"])  # prints: 65

    # Use .get() for safe access with defaults
    batch_size = config.get("training", {}).get("batch_size", 32)
```

We can now call this like so:
```
python train_script.py --config_file my_config.yaml
```

### Constraints
 
- Only four types are supported for script level arguments: `str`, `int`, `float`, `bool`
- When calling a function as a script, arguments must be given as keyword arguments; positional
 arguments are not supported by design, to promote clarity.
- To be able to parse documentation, docstrings must be written in 
[sphinx format](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html). If this is not the case, 
the docstring will be ignored.


## Aren't there a bunch of libraries that do this already

There are, and most of those contain more functionality than is contained here! However, most of these tend to require
interacting with custom objects or adding additional boilerplate; `func-to-script` is able to avoid this for simple
use cases.
