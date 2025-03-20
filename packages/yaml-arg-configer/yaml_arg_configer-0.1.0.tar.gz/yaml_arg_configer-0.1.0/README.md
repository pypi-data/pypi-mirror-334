# YAML Argument Parser

## Overview

The `YamlArgParser` class simplifies the process of parsing command-line arguments and configurations from YAML files, combining default values with those specified via the command line or additional YAML files.

## Features

- **Default Configuration**: Load default settings from a YAML file.
- **Command-Line Override**: Override default settings using command-line arguments.
- **Multiple Configurations**: Support for multiple YAML configuration files.
- **Help Documentation**: Generate help documentation for each configuration option.

## Installation

This library is not available via PyPI, so include it manually in your project by copying the `yaml_argparser.py` file into your project directory and importing it as needed.

## Configuration

### 1. Default Configuration YAML File

Create a default configuration file (e.g., `defaults.yaml`) with settings:

```yaml
arg1:
  default: ~ # Set arg1 default value to None
  help: "Help documentation for arg1"
arg2:
  default: ~ # Set arg2 default value to None
  help: "Help documentation for arg2"
```

### 2. User Configuration YAML Files

Create user configuration files (e.g., `config1.yaml`):

```yaml
arg1: value1 # Set arg1 value to value1
```

And additional configurations (e.g., `config2.yaml`):

```yaml
arg2: value2 # Set arg2 value to value2
```

### 3. Command-Line Arguments

Use the `parse_args` function to parse command-line arguments:

```python
from yaml_argparse import parse_args

yaml_parser = parse_args(default_yaml='defaults.yaml')
```

## Command-Line Usage

Run your script with configuration options:

```bash
python my_script.py -d configs -c config1 config2
```

- `-d`, `--cfg_dir`: Directory containing configuration files.
- `-c`, `--cfg`: Names of configuration files to use (without `.yaml` extension).
- `--doc`: Get help documentation for a specific argument.
- `--docs`: Print help documentation for all arguments.

## Accessing Configurations

Retrieve parsed configurations using:

```python
print(yaml_parser.get_args_dict())
print(yaml_parser.get_args())
```

## Saving Configurations

Save current configurations to a YAML file:

```python
yaml_parser.save_config('output_config.yaml')
```

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. Ensure that any new features or bug fixes include appropriate tests.

## License

This project is licensed under the MIT License.
