from abc import ABC, abstractmethod


class ToStr(ABC):
    def __init__(self, data, indent, text_level=0, colorize=False):
        self._data = data
        self._indent = indent
        self._text_level = text_level
        self._colorize = colorize

    @abstractmethod
    def execute(self) -> str:
        pass

    @property
    def indent_space(self):
        return " " * (self._indent * self._text_level)

    def indenter(self, data: list, open_icon: str, close_icon: str) -> str:
        output_str = f"{self.indent_space}{open_icon}\n"

        for item in data:
            output_str += get_styled_text(item, self._indent, self._text_level + 1, self._colorize)
            if item != data[-1]:
                output_str += ","
            output_str += "\n"

        output_str += f"{self.indent_space}{close_icon}"

        return output_str


class TupleToStr(ToStr):
    def execute(self) -> str:
        return self.indenter(self._data, "(", ")")


class ListToStr(ToStr):
    def execute(self) -> str:
        return self.indenter(self._data, "[", "]")


class DictToStr(ToStr):
    def execute(self) -> str:
        return self.indenter(self._data, "{", "}")

    def indenter(self, data: dict, open_icon: str, close_icon: str) -> str:
        output_str = f"{self.indent_space}{open_icon}\n"

        for key, value in data.items():
            output_str += get_styled_text(key, self._indent, self._text_level + 1, self._colorize)
            output_str += ":\n"
            output_str += get_styled_text(value, self._indent, self._text_level + 2, self._colorize)
            if key != list(data.keys())[-1]:
                output_str += ","
            output_str += "\n"

        output_str += f"{self.indent_space}{close_icon}"

        return output_str


class SetToStr(ToStr):
    def execute(self) -> str:
        return self.indenter(list(self._data), "{", "}")


class IntToStr(ToStr):
    def execute(self) -> str:
        return f"{self.indent_space}{str(self._data)}"


class StringToStr(ToStr):
    def get_output_text(self):
        new_data = self._data.replace("\n", f"\n{self.indent_space}")
        return f"{self.indent_space}{new_data}"

    def execute(self) -> str:
        return self.get_output_text()


class FloatToStr(ToStr):
    def execute(self) -> str:
        return f"{self.indent_space}{str(self._data)}"


class AnotherToStr(ToStr):
    def execute(self) -> str:
        return f"{self.indent_space}{str(self._data)}"

datatypes = {
    list: ListToStr,
    tuple: TupleToStr,
    dict: DictToStr,
    set: SetToStr,
    str: StringToStr,
    float: FloatToStr,
    int: IntToStr,
}
default_type = AnotherToStr


def get_styled_text(text, indent, text_level=0, colorize=False):
    if colorize:
        from color_conversions import datatypes, default_type
    else:
        global datatypes
        global default_type

    return datatypes.get(type(text), default_type)(text, indent, text_level, colorize).execute()

