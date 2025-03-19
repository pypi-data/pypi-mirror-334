from .conversions import *
from .colored_text import get_colored_message, CBlue, CMagenta, CGreen, COrange, CRed, CWhite

list_color = CBlue()
tuple_color = CMagenta()
dict_color = CMagenta()
set_color = CBlue()
str_color = CGreen()
float_color = CRed()
int_color = COrange()
another_color = CWhite()


class ColorListToStr(ListToStr):
    def execute(self) -> str:
        open_icon = get_colored_message("[", list_color)
        close_icon = get_colored_message("]", list_color)
        return self.indenter(self._data, open_icon, close_icon)


class ColorTupleToStr(TupleToStr):
    def execute(self) -> str:
        print(self._data)
        open_icon = get_colored_message("(", tuple_color)
        close_icon = get_colored_message(")", tuple_color)
        return self.indenter(self._data, open_icon, close_icon)


class ColorDictToStr(DictToStr):
    def execute(self) -> str:
        open_icon = get_colored_message("{", dict_color)
        close_icon = get_colored_message("}", dict_color)
        return self.indenter(self._data, open_icon, close_icon)


class ColorSetToStr(SetToStr):
    def execute(self) -> str:
        open_icon = get_colored_message("{", set_color)
        close_icon = get_colored_message("}", set_color)
        return self.indenter(list(self._data), open_icon, close_icon)


class ColorFloatToStr(FloatToStr):
    def execute(self) -> str:
        return f"{self.indent_space}{get_colored_message(str(self._data), float_color)}"


class ColorIntToStr(IntToStr):
    def execute(self) -> str:
        return f"{self.indent_space}{get_colored_message(str(self._data), int_color)}"


class ColorStringToStr(StringToStr):
    def execute(self) -> str:
        return get_colored_message(self.get_output_text(), str_color)


class ColorAnotherToStr(AnotherToStr):
    def execute(self) -> str:
        return f"{self.indent_space}{get_colored_message(str(self._data), another_color)}"


datatypes = {
    list: ColorListToStr,
    tuple: ColorTupleToStr,
    dict: ColorDictToStr,
    set: ColorSetToStr,
    str: ColorStringToStr,
    float: ColorFloatToStr,
    int: ColorIntToStr,
}
default_type = ColorAnotherToStr
