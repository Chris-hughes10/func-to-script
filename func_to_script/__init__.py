from func_to_script.core import script
from func_to_script.config_loader import load_config_from_yaml

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("func-to-script")
except PackageNotFoundError:
    # Package is not installed
    __version__ = "0.0.0.dev0"
