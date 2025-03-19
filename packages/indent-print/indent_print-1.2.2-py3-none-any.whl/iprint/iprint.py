import sys
import inspect
from .conversions import get_styled_text


def iprint(*text, sep=", ", end="\n", indent=4, file=sys.stdout):
    out_put = ""
    for item in text:
        out_put += get_styled_text(item, indent)
        if item != text[-1]:
            out_put += sep
    file.write(out_put + end)


def cprint(*text, sep=" ", end="\n", indent=4):
    out_put = ""
    for item in text:
        out_put += get_styled_text(item, indent, colorize=True)
        if item != text[-1]:
            out_put += sep
    sys.stdout.write(out_put + end)


def status_print(instance, *, end="\n", indent=4, file=sys.stdout, colorize=False, show_dunder_attr=False):
    document = instance.__doc__
    try:
        size = instance.__sizeof__()
    except TypeError:
        size = sys.getsizeof (instance)
    try:
        instance_variables = dict(instance.__dict__)
    except AttributeError:
        instance_variables = {}

    class_variables = {}
    methods = {}
    class_methods = {}
    static_methods = {}
    properties = {}
    other_members = {}

    for name, attr in vars(instance.__class__).items():
        if isinstance(attr, staticmethod):
            static_methods[name] = attr
        elif isinstance(attr, classmethod):
            class_methods[name] = attr
        elif isinstance(attr, property):
            properties[name] = attr
        elif not name.startswith('__') and not name.endswith('__'):
            if inspect.ismethod(attr) or inspect.isfunction(attr) or inspect.ismethoddescriptor(attr):
                methods[name] = attr
            else:
                class_variables[name] = attr
        else:
            if name != "__doc__":
                other_members[name] = attr

    data = {
        "document": document,
        "size": size,
        "instance_variables": instance_variables,
        "class_variables": class_variables,
        "methods": methods,
        "class_methods": class_methods,
        "static_methods": static_methods,
        "properties": properties,
        "other_members": other_members if show_dunder_attr else "'off'",
    }

    if colorize:
        if file != sys.stdout:
            raise RuntimeError("can't write colorized in file")
        cprint(data, end=end, indent=indent)
    else:
        iprint(data, end=end, indent=indent, file=file)


if __name__ == "__main__":
    # Example:
    class AnotherData:
        """document of test class"""
        class_variable = "class_variable_value"

        def __init__(self, data):
            self.instance_variable = data

        def instance_method(self):
            pass

        @classmethod
        def class_method(cls):
            pass

        @staticmethod
        def static_method():
            pass

        @property
        def property_variable(self):
            return "property_variable_value"


    string_data = "my name is matin"
    int_data = 20
    float_data = 1.55
    another_data = AnotherData("instance_variable_value")
    dict_data = {"author": "matin ahmadi", "github": "https://github.com/matinprogrammer"}
    set_data = {1, 2, 3}
    tuple_data = (1, 2)
    list_data = [string_data, int_data, float_data, another_data, dict_data, set_data, tuple_data,  [[["test list"]]]]

    print("result of mprint: ")
    iprint(list_data)

    print("\nresult of cprint: ")
    cprint(list_data)

    print("\nresult of status_print: ")
    status_print(another_data, show_dunder_attr=True, colorize=True)
