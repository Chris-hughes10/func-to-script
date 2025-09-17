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

    # Dictionary-like interface methods
    def __iter__(self):
        """Allow iteration over keys like a dictionary."""
        return iter(self.__dict__)

    def __getitem__(self, key):
        """Allow bracket notation access like a dictionary."""
        return self.__dict__[key]

    def __contains__(self, key):
        """Support 'in' operator to check if key exists."""
        return key in self.__dict__

    def __len__(self):
        """Return the number of attributes."""
        return len(self.__dict__)

    def items(self):
        """Return key-value pairs like dict.items()."""
        return self.__dict__.items()

    def keys(self):
        """Return keys like dict.keys()."""
        return self.__dict__.keys()

    def values(self):
        """Return values like dict.values()."""
        return self.__dict__.values()

    def get(self, key, default=None):
        """Get value with optional default like dict.get()."""
        return self.__dict__.get(key, default)


def load_config_from_yaml(config_path):
    with open(config_path, "r") as stream:
        config_dict = yaml.safe_load(stream)
        config = Struct(**config_dict)
    return config
