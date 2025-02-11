import yaml

class Struct:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.__dict__[key] = Struct(**value)
            else:
                self.__dict__[key] = value

    def __repr__(self):
        return str(self.__dict__)


def load_config_from_yaml(config_path):
    with open(config_path, "r") as stream:
        config_dict = yaml.safe_load(stream)
        config = Struct(**config_dict)
    return config
