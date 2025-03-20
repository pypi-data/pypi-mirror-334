import os
from importlib import import_module

import yaml

__all__ = ['ConfigLoader', 'load_yaml', 'load_ctx_from_yaml']


def join_list(seq):
    result = []
    for i in seq:
        if isinstance(i, list):
            result.extend(i)
        else:
            result.append(i)
    return result


def join(loader, node):
    seq = loader.construct_sequence(node)
    return join_list(seq)


def chain2path(loader, node):
    seq = loader.construct_sequence(node)
    return os.path.join(*join_list(seq))


class ContextParser:

    def __init__(self, context_dict):
        self.context_dict = context_dict
        self.tmp_context_dict = {}

    def get_context(self):
        return self.context_dict

    def get_tmp_context(self):
        return self.tmp_context_dict

    def update_context(self, context_dict):
        self.context_dict.update(context_dict)

    def update_tmp_context(self, context_dict):
        self.tmp_context_dict.update(context_dict)

    def clear_context(self):
        self.context_dict.clear()

    def clear_tmp_context(self):
        self.tmp_context_dict.clear()

    def replace_context(self, context_dict):
        self.context_dict = context_dict

    def replace_tmp_context(self, context_dict):
        self.tmp_context_dict = context_dict

    def __call__(self, loader, node):
        key_name = loader.construct_yaml_str(node)
        if key_name in self.context_dict:
            return self.context_dict[key_name]
        return self.tmp_context_dict[key_name]


def import_loader(loader, node):
    """A loader for import things from module."""
    params = loader.construct_mapping(node, deep=True)  # get node mappings
    context = {}
    for m, attrs in params.items():
        module = import_module(name=m)  # load Python module
        for name, attr in attrs.items() if isinstance(attrs, dict) else zip(attrs, attrs):
            context[name] = getattr(module, attr)
    return context


def call_loader(loader, node):
    params = loader.construct_mapping(node, deep=True)  # get node mappings
    to_call = params.pop('call')
    return to_call(**params)


class ConfigLoader(yaml.Loader):

    context_tag = '!ctx'
    import_tag = '!ipt'
    call_tag = '!call'

    @classmethod
    def get_constructor(cls, tag):
        return cls.yaml_constructors[tag]

    @classmethod
    def update_context(cls, context_dict):
        cls.yaml_constructors[cls.context_tag].update_context(context_dict=context_dict)

    @classmethod
    def update_tmp_context(cls, context_dict):
        cls.yaml_constructors[cls.context_tag].update_tmp_context(context_dict=context_dict)

    @classmethod
    def replace_context(cls, context_dict):
        cls.yaml_constructors[cls.context_tag].replace_context(context_dict=context_dict)

    @classmethod
    def replace_tmp_context(cls, context_dict):
        cls.yaml_constructors[cls.context_tag].replace_tmp_context(context_dict=context_dict)


ConfigLoader.add_constructor(ConfigLoader.context_tag, constructor=ContextParser(context_dict={}))
ConfigLoader.add_constructor(ConfigLoader.import_tag, constructor=import_loader)
ConfigLoader.add_constructor(ConfigLoader.call_tag, constructor=call_loader)
ConfigLoader.add_constructor('!join', constructor=join)
ConfigLoader.add_constructor('!chain2path', constructor=chain2path)


def load_yaml(yaml_path, Loader=ConfigLoader, **kwargs):
    """
    Parse a YAML file and return its content as a dictionary.

    :param yaml_path: Path to the YAML file.
    :return: Dictionary containing the parsed content of the YAML file.
    """
    with open(yaml_path) as f:
        ctx = yaml.load(f, Loader=Loader, **kwargs)
    return ctx


def load_ctx_from_yaml(yaml_path, import_tag='import', temp=True, replace=True, **kwargs):
    """
    Load and manage context from a YAML file.

    :param yaml_path: Path to the YAML file.
    :param import_tag: The tag used in YAML for importing modules.
    :param temp: If True, updates the temporary context. Otherwise, updates the main context.
    :param replace: If True, replaces the current context with the new one. Otherwise, merges it.
    :param kwargs: Additional keyword arguments to pass to load_yaml.
    """
    ctx_config = load_yaml(yaml_path=yaml_path, Loader=ConfigLoader, **kwargs)
    attrs = ctx_config.pop(import_tag)
    ctx_config.update(attrs)
    if temp:
        if replace:
            ConfigLoader.replace_tmp_context(ctx_config)
        else:
            ConfigLoader.update_tmp_context(ctx_config)
    elif replace:
        ConfigLoader.replace_context(ctx_config)
    else:
        ConfigLoader.update_context(ctx_config)
