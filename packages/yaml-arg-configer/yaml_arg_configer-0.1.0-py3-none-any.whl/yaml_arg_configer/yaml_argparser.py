from pathlib import Path
import yaml
import argparse


__all__ = [
    "YamlArgParser",
    "get_arg_parser",
    "parse_args"
]


class YamlArgParser:
    """
    A class to parse arguments from YAML files and command line, combining them with default values.

    Attributes:
        default_name (str): The key used in the YAML files for default values.
        help_name (str): The key used in the YAML files for help documentation.
        default_yaml (str): Path to the default configuration YAML file.
        defaults (dict): Parsed default configurations from the default YAML file.
        args (dict): Dictionary to hold the final set of arguments.
    """

    default_name = 'default'
    help_name = 'help'

    def __init__(self, default_yaml):
        """
        Initialize the YamlArgParser with a path to a default configuration YAML file.

        Args:
            default_yaml (str): Path to the default configuration YAML file.
        """
        self.default_yaml = default_yaml
        self.parse_default()

    @classmethod
    def parse_yaml(cls, yaml_path):
        """
        Parse a YAML file and return its content as a dictionary.

        Args:
            yaml_path (str): The path to the YAML file.

        Returns:
            dict: The parsed content of the YAML file.
        """
        ctx = yaml.safe_load(Path(yaml_path).read_text())
        return ctx

    def parse_default(self):
        """
        Parse the default configuration YAML file and set up initial arguments with their default values.
        """
        self.defaults = self.parse_yaml(self.default_yaml)
        self.args = {}
        for k, v in self.defaults.items():
            self.args[k] = v.get(self.default_name, None)

    def update_from_dict(self, args):
        """
        Update the arguments dictionary with a new set of arguments provided as a dictionary.
        Validates that each key exists in the defaults.

        Args:
            args (dict): A dictionary containing argument names and their values to be updated.
        """
        for k, v in args.items():
            assert k in self.args, f'The arg {k} is not defined in the default config.'
            if isinstance(v, dict) and self.default_name in v:
                self.args[k] = v[self.default_name]
            else:
                self.args[k] = v

    def update_from_yaml(self, yaml_path):
        """
        Parse a YAML file and update the arguments dictionary with its content.

        Args:
            yaml_path (str): The path to the YAML file containing updated arguments.
        """
        args = self.parse_yaml(yaml_path)
        self.update_from_dict(args)

    def parse_args_dict(self, yaml_paths=None):
        """
        Update the arguments dictionary from a list of YAML file paths.

        Args:
            yaml_paths (list of str, optional): List of paths to YAML files containing updated arguments.
 Defaults to None.

        Returns:
            dict: The final set of parsed arguments.
        """
        if yaml_paths:
            for yaml_path in yaml_paths:
                self.update_from_yaml(yaml_path)
        return self.args

    def get_args_dict(self):
        return self.args

    def get_args(self):
        """
        Convert the arguments dictionary into an argparse Namespace object.

        Returns:
            argparse.Namespace: An object containing all the final set of parsed arguments.
        """
        return argparse.Namespace(**self.args)

    def parse_args(self, yaml_paths=None):
        """
        Parse arguments from a list of YAML files and return them as an argparse Namespace object.

        Args:
            yaml_paths (list of str, optional): List of paths to YAML files containing updated arguments.
 Defaults to None.

        Returns:
            argparse.Namespace: An object containing all the final set of parsed arguments.
        """
        self.parse_args_dict(yaml_paths=yaml_paths)
        return self.get_args()

    def save_config(self, out_path):
        """
        Save the current set of arguments to a YAML file at the specified path.

        Args:
            out_path (str): The path where the output configuration YAML file will be saved.
        """
        with open(out_path, 'w') as f:
            f.write(yaml.safe_dump(self.args))

    def __getitem__(self, key):
        """
        Allow dictionary-like access to the arguments.

        Args:
            key (str): The argument name to retrieve.

        Returns:
            any: The value of the specified argument.
        """
        return self.args[key]

    def __setitem__(self, key, value):
        """
        Allow dictionary-like assignment to the arguments.

        Args:
            key (str): The argument name to update.
            value (any): The new value for the specified argument.
        """
        self.args[key] = value

    def help(self, arg_name=None):
        """
        Retrieve help documentation for a specific argument or all arguments.

        Args:
            arg_name (str, optional): The name of the argument to retrieve help documentation for.
 If None, returns help for all arguments. Defaults to None.

        Returns:
            str: Help documentation for the specified argument or all arguments.
        """
        if arg_name:
            assert arg_name in self.defaults, f'The arg {arg_name} is not defined in the arg config.'
            return self.defaults[arg_name].get(self.help_name, 'None')
        return '\n'.join([f'{k}: {v.get(self.help_name, "None")}' for k, v in self.defaults.items()])


def get_arg_parser(default_yaml=None):
    """
    Create and configure an argparse.ArgumentParser for parsing command-line arguments.

    Args:
        default_yaml (str, optional): Default path to the configuration YAML file. Defaults to None.

    Returns:
        argparse.ArgumentParser: Configured argument parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", type=str, default='configs', dest='cfg_dir',
                        help="yaml config directory.")
    parser.add_argument("-c", type=str, nargs='+', dest='cfg',
                        help="yaml config name, can be multiple, split with space")
    parser.add_argument("--doc", type=str, nargs='+',
                        help="help doc for args, can be multiple, split with space.")
    parser.add_argument("--docs", action="store_true",
                        help="help doc for all args.")
    parser.add_argument("--default_yaml", type=str, default=default_yaml,
                        help="default yaml path")
    return parser


def parse_args(parser=None, default_yaml=None):
    """
    Parse command-line arguments and update configuration using specified YAML files.

    Args:
        parser (argparse.ArgumentParser, optional): A pre-configured argument parser. Defaults to None.
        default_yaml (str, optional): Default path to the configuration YAML file. Defaults to None.

    Returns:
        YamlArgParser: An instance of YamlArgParser with updated arguments.
    """
    if parser is None:
        parser = get_arg_parser(default_yaml=default_yaml)
    args = parser.parse_args()
    yaml_parser = YamlArgParser(default_yaml=args.default_yaml)
    if args.docs:
        print(yaml_parser.help())
    elif args.doc:
        for k in args.doc:
            print(yaml_parser.help(k))
    cfg_dir = Path(args.cfg_dir)
    yaml_parser.parse_args_dict([cfg_dir / f'{i}.yaml' for i in args.cfg])
    return yaml_parser
