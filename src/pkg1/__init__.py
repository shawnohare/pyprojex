from .main import hello
import pkg_resources
from pkg_resources import resource_string

__version__ = pkg_resources.get_distribution('pyprojex').version
