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
        
    # Make it behave like a dictionary
    def __iter__(self):
        return iter(self.__dict__)
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def items(self):
        return self.__dict__.items()
    
    def keys(self):
        return self.__dict__.keys()
    
    def values(self):
        return self.__dict__.values()
    
    def get(self, key, default=None):
        return self.__dict__.get(key, default)


def load_config_from_yaml(config_path):
    with open(config_path, "r") as stream:
        config_dict = yaml.safe_load(stream)
        config = Struct(**config_dict)
    return config
