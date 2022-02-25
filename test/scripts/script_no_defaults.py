from func_to_script import script


@script
def main(str_arg: str, int_arg: int, float_arg: float, bool_arg: bool):
    results = {
        "str_arg": str_arg,
        "int_arg": int_arg,
        "float_arg": float_arg,
        "bool_arg": bool_arg,
    }

    print(results)

    return results


if __name__ == "__main__":
    main()
