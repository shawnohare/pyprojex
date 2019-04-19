import json
import sys
from pkg_resources import resource_string

# Load a package data file resource as a string. This
_conf = json.loads(resource_string(__name__, 'conf.json'))

# Load a data file specified in "package_data" setup option for this pkg.
_pkg_data = resource_string(__name__, 'data/pkg1.dat')

# Load a data file included in "data_files" setup option.
# FIXME
try:
    _sys_data = open(sys.prefix + '/data/data1.dat').read()
except Exception as exc:
    print('Sys data load error:', exc)
    _sys_data = 'System data: (In editable mode?) Unable to load data file: data/data1.dat'


def hello():
    print(_conf['greeting'])
    print(_pkg_data)
    print(_sys_data)


if __name__ == '__main__':
    hello()
