from pathlib import Path
import yaml
import argparse

from .yaml_loader import load_yaml, load_ctx_from_yaml

__all__ = ["YamlArgParser"]


class YamlArgParser:
    """
    Parses arguments from YAML files and command line, combining them with default values.

    Attributes:
        default_name (str): Key in YAML for default values.
        help_name (str): Key in YAML for help documentation.
        defaults (dict): Default configurations from the default YAML file.
        args (dict): Final set of parsed arguments.
    """

    default_name = 'default'
    help_name = 'help'

    def __init__(self, parser=None, default_yaml=None):
        """
        Initializes the YamlArgParser with a path to a default configuration YAML file.

        :param parser: Existing argparse.ArgumentParser instance (optional).
        :param default_yaml: Path to the default configuration YAML file.
        """
        self.arg_parser = self._get_arg_parser(parser=parser, default_yaml=default_yaml)
        self.defaults = {}
        self.args = {}

    @classmethod
    def _get_arg_parser(cls, parser=None, default_yaml=None):
        """
        Creates and configures an argparse.ArgumentParser for parsing command-line arguments.

        :param parser: Existing argparse.ArgumentParser instance (optional).
        :param default_yaml: Default path to the configuration YAML file.
        :return: Configured argparse.ArgumentParser instance.
        """
        parser = parser or argparse.ArgumentParser()
        parser.add_argument("-d", type=str, default='configs', dest='cfg_dir',
                            help="Directory containing YAML config files.")
        parser.add_argument("-c", type=str, nargs='+', dest='cfg',
                            help="YAML config file names (can be multiple).")
        parser.add_argument("--doc", type=str, nargs='+',
                            help="Help documentation for specific arguments (multiple allowed).")
        parser.add_argument("--docs", action="store_true",
                            help="Print help documentation for all arguments.")
        parser.add_argument("--dc", type=str, default=default_yaml, dest='default_yaml',
                            help="Path to the default YAML configuration file.")
        parser.add_argument('-ctx', type=str, default=None, dest='ctx_yaml',
                            help="Path to the context YAML configuration file.")
        parser.add_argument('--strict', action="store_true",
                            help="Constraints user configuration defined in the default_yaml file.")
        return parser

    def add_argument(self, *args, **kwargs):
        """Adds an argument to the parser."""
        self.arg_parser.add_argument(*args, **kwargs)

    def parse_default(self, default_yaml):
        """
        Parses the default configuration YAML file and sets up initial arguments with their default values.

        :param default_yaml: Path to the default configuration YAML file.
        """
        self.defaults = load_yaml(default_yaml)
        self.args = {k: v.get(self.default_name) for k, v in self.defaults.items()}

    def update_from_dict(self, args, strict=True):
        """
        Updates the arguments dictionary with a new set of arguments provided as a dictionary.
        Validates that each key exists in the defaults if `strict` is True.

        :param args: Dictionary containing argument names and their values to be updated.
        :param strict: Boolean flag indicating whether to enforce existence of keys in defaults.
        """
        for k, v in args.items():
            if strict:
                assert k in self.args, f"Argument '{k}' not defined in the default configuration."
            if isinstance(v, dict) and self.default_name in v:
                self.args[k] = v[self.default_name]
            else:
                self.args[k] = v

    def update_from_yaml(self, yaml_path, strict=True):
        """
        Parses a YAML file and updates the arguments dictionary with its content.

        :param yaml_path: Path to the YAML file containing updated arguments.
        :param strict: Boolean flag indicating whether to enforce existence of keys in defaults.
        """
        args = load_yaml(yaml_path)
        self.update_from_dict(args, strict=strict)

    def parse_args_dict(self, yaml_paths=None, strict=True):
        """
        Updates the arguments dictionary from a list of YAML file paths.

        :param yaml_paths: List of paths to YAML files containing updated arguments.
        :return: The final set of parsed arguments as a dictionary.
        """
        if yaml_paths:
            for yaml_path in yaml_paths:
                self.update_from_yaml(yaml_path, strict=strict)
        return self.args

    def get_args(self):
        """
        Converts the arguments dictionary into an argparse Namespace object.

        :return: An argparse.Namespace object containing all the final set of parsed arguments.
        """
        return argparse.Namespace(**self.args)

    def parse_cmd_args(self):
        """Parses command-line arguments."""
        return self.arg_parser.parse_args()

    def parse_args(self, cmd_args):
        """
        Parses arguments from a list of YAML files and command-line inputs.

        :param cmd_args: Namespace containing command-line arguments.
        :return: Dictionary with the final set of parsed arguments.
        """
        ctx_yaml = cmd_args.ctx_yaml
        if ctx_yaml is not None:
            load_ctx_from_yaml(ctx_yaml)
        default_yaml = cmd_args.default_yaml
        if default_yaml is None:
            strict = False
        else:
            strict = cmd_args.strict
            self.parse_default(default_yaml=default_yaml)
            if cmd_args.docs:
                print(self.help())
            elif cmd_args.doc:
                for arg_name in cmd_args.doc:
                    print(self.help(arg_name))
        cfg_dir = Path(cmd_args.cfg_dir)
        yaml_paths = [cfg_dir / f'{name}.yaml' for name in cmd_args.cfg]
        return self.parse_args_dict(yaml_paths, strict=strict)

    def save_config(self, out_path):
        """
        Saves the current set of arguments to a YAML file at the specified path.

        :param out_path: Path where the output configuration YAML file will be saved.
        """
        with open(out_path, 'w') as f:
            yaml.safe_dump(self.args, f)

    def __getitem__(self, key):
        """Allows dictionary-like access to the arguments."""
        return self.args[key]

    def __setitem__(self, key, value):
        """Allows dictionary-like assignment to the arguments."""
        self.args[key] = value

    def help(self, arg_name=None):
        """
        Retrieves help documentation for a specific argument or all arguments.

        :param arg_name: Name of the argument to retrieve help documentation for (optional).
        :return: Help documentation for the specified argument or all arguments.
        """
        if arg_name:
            assert arg_name in self.defaults, f"Argument '{arg_name}' not defined in the configuration."
            return self.defaults[arg_name].get(self.help_name, 'No help available.')
        return '\n'.join([f'{k}: {v.get(self.help_name, "No help available.")}' for k, v in self.defaults.items()])
