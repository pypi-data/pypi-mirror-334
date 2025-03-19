# rich-string-builder
Text preprocessor for building strings for the [rich library](https://github.com/Textualize/rich)


## Background
This came about because I was annoyed at the way we needed to insert text into rich to make it reflect our intended
stylistic choices. Take the following example:

```python
console.print(
    f"Subnet: [{COLOR_PALETTE['GENERAL']['SUBHEADING']}]{netuid_}[/{COLOR_PALETTE['GENERAL']['SUBHEADING']}] "
    f"Stake:\n"
    f"  [blue]{current_stake}[/blue] "
    f":arrow_right: "[{COLOR_PALETTE['STAKE']['STAKE_AMOUNT']}]{new_stake}\n"
)
```

With this library, it's a bit more readable as:
```python
console.print(
    rs.str(
        "Subnet: ", rs.GENERAL.SUBHEADING(netuid_),
        " Stake:\n  ",
        rs.c.blue(current_stake),
        " :arrow_right: ", rs.STAKE.STAKE_AMOUNT(new_stake, "\n")
    )
)
```

The ideas are largely derived from Tailwind and other utility-style frameworks/libraries.

## Current State
Currently this is just proof of concept. I will likely add to this over time.


## Examples
See `examples` directory for examples of using this.

One of the fundamental aspects of this library is the ability to preload your own custom styles from a dictionary, like so:

```python
from rich.console import Console
from rich_string_builder.string_builder import RichStyles

console = Console()

my_styles = {
    "alert": "blink yellow",
    "headers": {
        "main": "bold",
        "sub": "#4196D6"
    }
}
rs = RichStyles(my_styles)
console.print(rs.custom.alert("WARNING!"))  # '[blink yellow]WARNING![/blink yellow]'
```

Though you are able to combine these styles ad-hoc:

```python
bright_blue = rs.Styles.bright + rs.Colors.blue
console.print(bright_blue("Coldkey"))  # '[bright blue]Coldkey[/bright blue]'
```

Say you have a complicated custom style, and you wish to only remove an element or two and reuse it:
```python
my_styles = {
    "foo": "blink bright yellow"
}
rs = RichStyles(my_styles)
console.print((rs.custom.foo - "blink")("Hello!"))  # '[bright yellow]Hello![/bright yellow]'
# or define a new type:
bar = rs.custom.foo - "blink"
console.print(bar("Hello!"))  # '[bright yellow]Hello![/bright yellow]'
```


## Who is this for?
I am personally colourblind. It's nice to have someone who is not colourblind define a colour palette, and I simply
build from this. While colourblind people are not the only intended users, I think it will help them (us) substantially
in terms of readability of the styles. 
It's also very helpful for keeping easier track of your styles and reusability.
