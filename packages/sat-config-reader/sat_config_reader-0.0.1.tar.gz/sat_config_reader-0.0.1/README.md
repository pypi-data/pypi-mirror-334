# Python config file reader
[![coverage report](https://gitlab.com/markus2110-public/python/packages/config-reader/badges/develop/coverage.svg)](https://gitlab.com/markus2110-public/python/packages/config-reader/-/commits/develop)
[![pipeline status](https://gitlab.com/markus2110-public/python/packages/config-reader/badges/develop/pipeline.svg)](https://gitlab.com/markus2110-public/python/packages/config-reader/-/commits/develop) 


## Description
TBD

## Installation
```commandline
pip install sat_config_reader
```
or
```commandline
python -m pip install sat_config_reader
```

## Usage
`tests/mocks/config_1/my_defaults.ini`
```ini
[DEFAULT]
NAME = localhost
PORT = 8080
LOG_FILE = /tmp/logfile.log

[config1]
PORT = 12345
LOG_FILE = /tmp/config1.log

[config2]
NAME = remote_server
PORT = 80
LOG_FILE = /path/to/file.log
```
***
`main.py`   
#### Without dataclass, result will be a `dict[str, dict]`
```python
from src.read_config import config_reader

reader = config_reader("./tests/mocks/config_1/my_defaults.ini")
port = reader.get('config1').get('PORT')
assert 12345 == port
print(port)
```
#### with dataclass, result is a `dict[str, TypeMapping]`
```python
from dataclasses import dataclass
from src.read_config import config_reader

@dataclass
class TypeMapping:
    NAME: str
    PORT: int
    LOG_FILE: str

reader = config_reader("./tests/mocks/config_1/my_defaults.ini", TypeMapping)
config1: TypeMapping = reader.get('config1')
port = config1.PORT
assert 12345 == port
print(port)
```

*** 
## Example
TBD
