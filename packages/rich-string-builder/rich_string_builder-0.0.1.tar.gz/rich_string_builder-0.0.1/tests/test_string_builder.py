from rich_string_builder.string_builder import RichStyles
import pytest

C = RichStyles.Colors
S = RichStyles.Styles


@pytest.mark.parametrize(
    "expected,actual",
    [
        ("[blue]Hello[/blue]", RichStyles.Colors.blue("Hello")),
        ("[bold]Hello[/bold]", RichStyles.Styles.bold("Hello")),
        (
            "[blue][bold]Hello[/bold][/blue]",
            RichStyles.Colors.blue(RichStyles.Styles.bold("Hello")),
        ),
        (
            "[bold][blue]Hello, [/blue][black]World![/black][/bold]",
            RichStyles.Styles.bold(
                RichStyles.Colors.blue("Hello, "), RichStyles.Colors.black("World!")
            ),
        ),
        (
            "[bold][blue]Hello, [/blue][black]World![/black][/bold]",
            S.bold(C.blue("Hello, "), C.black("World!")),
        ),
        ("Hello, [dim]World![/dim]", RichStyles.String("Hello, ", S.dim("World!"))),
    ],
)
def test_string_builder(actual, expected):
    assert actual == expected


def test_custom_string_builder_single_layer_cd():
    single_layer_cd = {"general": "#4196D6"}
    rs = RichStyles(single_layer_cd)
    actual = rs.custom.general("Hello, World!")
    expected = "[#4196D6]Hello, World![/#4196D6]"
    assert actual == expected


def test_custom_string_builder_multiple_layer_cd():
    cd = {"general": {"header": "#4196D6"}}
    rs = RichStyles(cd)
    actual = rs.custom.general.header("Hello, World!")
    expected = "[#4196D6]Hello, World![/#4196D6]"
    assert actual == expected
