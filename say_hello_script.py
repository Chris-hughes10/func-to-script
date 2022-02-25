from func_to_script import script


@script
def say_hello(
    greeting: str = "Hello", name: str = "World", print_message: bool = True
):
    """
    A simple function to say hello

    :param greeting: the greeting to use
    :param name: the person to greet
    :param print_message: flag to indicate whether to print to the commandline
    """
    hello_str = f"{greeting}, {name}"

    if print_message:
        print(hello_str)

    return hello_str


if __name__ == "__main__":
    say_hello()
