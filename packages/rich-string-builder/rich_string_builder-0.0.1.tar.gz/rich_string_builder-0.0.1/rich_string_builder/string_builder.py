from typing import Union, Optional


class _ApplyStyle:
    def __init__(self, style=None):
        self.style = style

    def __call__(self, *strings):
        return self.apply_style(*strings)

    def __repr__(self):
        return f"_ApplyStyle<{self.style}>"

    def __str__(self):
        return self.style

    def __add__(self, other):
        if not isinstance(other, (str, _ApplyStyle)):
            raise TypeError
        elif isinstance(other, _ApplyStyle):
            return _ApplyStyle(f"{self.style} {other.style}")
        else:
            return _ApplyStyle(f"{self.style} {other}")

    def __sub__(self, other):
        if not isinstance(other, (str, _ApplyStyle)):
            raise TypeError
        elif isinstance(other, _ApplyStyle):
            return _ApplyStyle(self.style.replace(other.style, "").strip())
        else:
            return _ApplyStyle(self.style.replace(other, "").strip())

    def apply_style(self, *strings):
        braces = "{}" * len(strings)
        if self.style is not None:
            return f"[{self.style}]" + braces.format(*strings) + f"[/{self.style}]"
        else:
            return braces.format(*strings)


class _StyleBuilder:
    def __str__(self):
        return str(
            {
                attr: str(getattr(self, attr))
                for attr in dir(self)
                if not attr.startswith("_")
            }
        )

    def __repr__(self):
        return f"_StyleBuilder<{self.__str__()}>"


class RichStyles:
    String = _ApplyStyle()

    class Styles:
        dim = _ApplyStyle("dim")
        bright = _ApplyStyle("bright")
        bold = _ApplyStyle("bold")
        strong = _ApplyStyle("strong")
        code = _ApplyStyle("code")
        italic = _ApplyStyle("italic")
        emphasize = _ApplyStyle("emphasize")
        underline = _ApplyStyle("underline")
        blink = _ApplyStyle("blink")
        blink2 = _ApplyStyle("blink2")

    class Colors:
        black = _ApplyStyle("black")
        red = _ApplyStyle("red")
        green = _ApplyStyle("green")
        yellow = _ApplyStyle("yellow")
        magenta = _ApplyStyle("magenta")
        cyan = _ApplyStyle("cyan")
        white = _ApplyStyle("white")
        blue = _ApplyStyle("blue")

    def __init__(
        self, custom_definitions: Optional[dict[str, Union[str, dict]]] = None
    ):
        self.custom = (
            self._objectify(custom_definitions) if custom_definitions else None
        )
        self.s = self.Styles
        self.c = self.Colors
        self.str = self.String

    @staticmethod
    def _objectify(custom_definition: dict[str, Union[str, dict]]):
        def _create_object(value_: Union[str, dict]):
            if isinstance(value_, str):
                return _ApplyStyle(value_)
            elif isinstance(value_, dict):
                inner_object = _StyleBuilder()
                for inner_key_, inner_value_ in value_.items():
                    setattr(inner_object, inner_key_, _create_object(inner_value_))
                return inner_object
            else:
                raise TypeError(
                    f"Unexpected type {type(value_)} {value_}. "
                    f"Dictionary must only consist of strings or inner dictionaries."
                )

        custom = _StyleBuilder()
        for key, value in custom_definition.items():
            setattr(custom, key, _create_object(value))
        return custom
