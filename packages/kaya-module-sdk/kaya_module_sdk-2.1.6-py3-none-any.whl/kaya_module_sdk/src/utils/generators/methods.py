# #import pysnooper

from functools import partial
from typing import get_type_hints, get_origin, Annotated, get_args


# #@pysnooper.snoop()
def kaya_io():
    def wrapper(cls):
        annotations = get_type_hints(cls, include_extras=True)
        # NOTE: Build the __init__ signature and method body
        parameter_lines, body_lines = build_class_structure(cls, annotations)
        # NOTE: Generate and attach the dynamic `__init__` method
        attach_init_method(cls, parameter_lines, body_lines)
        return cls

    return wrapper


# #@pysnooper.snoop()
def build_class_structure(cls, annotations):
    """
    Build the list of parameters and the initialization body for the class.
    """
    parameter_lines = []
    body_lines = []
    for field_name, field_type in annotations.items():
        # NOTE: Process fields with Annotated types only
        if get_origin(field_type) is not Annotated:
            continue
        if field_name in ["_errors", "_results"]:
            continue
        base_type = get_args(field_type)[0]
        add_getter_and_setter(cls, field_name, base_type)
        #       optional_type = Union[base_type, None]  # Optional[type]
        parameter_lines.append(build_parameter(field_name, base_type))
        body_lines.append(build_body_line(field_name))
    return parameter_lines, body_lines


# #@pysnooper.snoop()
def add_getter_and_setter(cls, field_name, base_type):
    """
    Dynamically create and attach getter and setter methods for a given field.
    """
    getter_func = partial(create_getter, field_name=field_name)
    setter_func = partial(create_setter, field_name=field_name)
    setattr(cls, field_name.lstrip("_"), getter_func())
    setattr(cls, f'set_{field_name.lstrip("_")}', setter_func())


# #@pysnooper.snoop()
def build_parameter(field_name, base_type):
    """
    Build a string representation of a parameter for the dynamic __init__ method.
    """
    return f"{field_name.strip('_')}: {base_type.__name__} | None = None"


# #@pysnooper.snoop()
def build_body_line(field_name):
    """
    Build a line of code for the __init__ method body to set instance attributes.
    """
    return f"if {field_name.strip('_')} is not None: self.set_{field_name.strip('_')}({field_name.strip('_')})"


# #@pysnooper.snoop()
def attach_init_method(cls, parameter_lines, body_lines):
    """
    Dynamically create and attach the __init__ method to the class.
    """
    init_code = f"""def __init__(self, {', '.join(parameter_lines)}):\n\
        super(type(self), self).__init__()\n\
        {'\n        '.join(body_lines)}"""
    namespace = {}
    exec(init_code, globals(), namespace)
    setattr(cls, "__init__", namespace["__init__"])


# NOTE: Placeholder functions for getter and setter creation
# #@pysnooper.snoop()
def create_getter(field_name):
    @property
    def getter(self):
        return getattr(self, field_name)

    return getter


# #@pysnooper.snoop()
def create_setter(field_name):
    def setter(self, value):
        setattr(self, field_name, value)

    return setter
