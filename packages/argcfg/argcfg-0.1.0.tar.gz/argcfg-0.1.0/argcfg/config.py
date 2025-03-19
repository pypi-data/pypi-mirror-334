# coding=utf-8

# from dataclasses import dataclass
import typing
from .parser_utils import parse_bool, parse_float_list, parse_int_list, parse_str_list


def add_args_by_config_class(parser, config_class, verbose=True):
    
    field_type_dict = typing.get_type_hints(config_class)

    for field_name, field_type in field_type_dict.items():
        arg_type = field_type

        if field_type == typing.List[str]:
            arg_type = parse_str_list
        elif field_type == typing.List[int]:
            arg_type = parse_int_list
        elif field_type == typing.List[float]:
            arg_type = parse_float_list
        elif field_type == bool:
            arg_type = parse_bool
        
        parser.add_argument("--{}".format(field_name), type=arg_type, required=False)

        if verbose:
            print("generate argument --{} with type {}".format(field_name, arg_type))
    
    return parser



def combine_args_into_config(config, args, verbose=False):
    for key, value in args.__dict__.items():
        if value is not None and hasattr(config, key):
            old_value = getattr(config, key)
            setattr(config, key, value)
            if verbose:
                print("set config.{} based on args.{}: {} => {}".format(key, key, old_value, value))

    return config