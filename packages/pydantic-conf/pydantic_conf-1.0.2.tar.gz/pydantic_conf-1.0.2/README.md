# pydantic-conf

## Overview

`pydantic-conf` is a Python library for managing application configuration using Pydantic. It supports 
loading configuration from environment variables and allows for custom startup actions.

## Installation

To install the package, use:

```sh
pip install pydantic-conf
```

## Usage

### Defining Configuration

Create a configuration class by inheriting from `EnvAppConfig`:

```python
from pydantic_conf.config import EnvAppConfig


class MyConfig(EnvAppConfig):
    app_name: str
    debug: bool = False
```

### Loading Configuration

Load the configuration using the `load` method:

```python
config = MyConfig.load()
print(config.app_name)
print(config.debug)
```

### Adding Startup Actions

Add startup actions by appending to the `STARTUP` list:

```python
def startup_action(config):
    print(f"Starting up with {config.app_name}")

MyConfig.STARTUP.append(startup_action)
config = MyConfig.load()
```

## License

This project is licensed under the MIT License.
