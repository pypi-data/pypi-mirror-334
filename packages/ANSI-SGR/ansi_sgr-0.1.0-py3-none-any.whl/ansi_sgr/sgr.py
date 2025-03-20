from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
import re as _re

if _TYPE_CHECKING:
    from protocolman import Stringable


def format(
    text: Stringable,
    text_styles: int | str | list[int | str] = None,
    text_color: int | str | tuple = None,
    bg_color: int | str | tuple = None,
    reset: bool = True
):
    sequence = create_sequence(text_styles, text_color, bg_color)
    return apply_sequence(text, sequence, reset=reset)


def create_sequence(
    text_styles: int | str | list[int | str] = None,
    text_color: int | str | tuple = None,
    bg_color: int | str | tuple = None
):
    styles = []
    if text_styles:
        if isinstance(text_styles, (str, int)):
            text_styles = [text_styles]
        if not isinstance(text_styles, list):
            raise TypeError("styles must be a string, an integer, or a list of strings or integers")
        for text_style in text_styles:
            styles.append(text_style_code(text_style))
    if text_color:
        styles.append(color_code(text_color, bg=False))
    if bg_color:
        styles.append(color_code(bg_color, bg=True))
    if not styles:
        return reset_sequence()
    return create_sequence_from_code(styles)


def create_sequence_from_code(code: list[Stringable] | Stringable):
    if isinstance(code, (list, tuple)):
        code = ";".join([str(c) for c in code])
    return f"\033[{code}m"


def apply_sequence(text: Stringable, sequence: Stringable, per_line: bool = True, reset: bool = True):
    if per_line:
        lines = [f"{sequence}{line}{reset_sequence() if reset else ''}" for line in str(text).split("\n")]
        return "\n".join(lines)
    return f"{sequence}{text}{reset_sequence() if reset else ''}"


def remove_sequence(text: str):
    """Remove ANSI escape sequences from a string.

    Parameters
    ----------
    text

    Notes
    -----
    ANSI escape codes start with the \\033 (\\x1b) escape character,
    followed by '[', then zero or more numbers separated by ';', and ending with a letter.

    Regex Details:
    - [0-?]*: This part matches zero or more characters in the range between 0 and ?.
    This covers all the numbers and semicolons that might be present in the escape sequence.
    For example, in the code \\x1b[31;42m, 31 and 42 are matched by this part.
    - [ -/]*: This is a sequence of characters that might appear in some of the ANSI sequences.
    It's more of a catch-all for certain sequences and may not be strictly necessary for many common sequences.
    But it ensures we catch even those rare ANSI codes.
    - [@-~]: Finally, ANSI escape sequences end with a character from @ to ~:
    @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
    [ \\ ] ^ _ ` a b c d e f g h i j k l m n o p q r s t u v w x y z {.
    This part matches that ending character. This character typically indicates what action
    should be taken (e.g., change color, move cursor, clear screen, etc.).
    """
    return _re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]').sub('', text)


def has_sequence(text: str) -> bool:
    return bool(_re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]').search(text))


def reset_sequence():
    return create_sequence_from_code(0)


def text_style_code(text_style: Stringable | int) -> str:
    text_style_map = {
        'normal': '0',
        'bold': '1',
        'faint': '2',
        'italic': '3',
        'underline': '4',
        'blink': '5',
        'blink_fast': '6',
        'reverse': '7',
        'conceal': '8',
        'strike': '9',
    }
    if isinstance(text_style, int):
        if text_style not in range(10):
            raise ValueError(f"Invalid style code: {text_style}")
        return str(text_style)
    text_style = str(text_style)
    if text_style not in text_style:
        raise ValueError(f"Invalid style name: {text_style}")
    return text_style_map[text_style]


def color_code(color: int | Stringable | tuple[int, int, int], bg: bool = False):
    color_code_map = {
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37,
        'b_black': 90,
        'b_red': 91,
        'b_green': 92,
        'b_yellow': 93,
        'b_blue': 94,
        'b_magenta': 95,
        'b_cyan': 96,
        'b_white': 97,
    }

    int_range = (
        list(range(40, 48)) + list(range(100, 108)) if bg else
        list(range(30, 38)) + list(range(90, 98))
    )
    int_offset = 10 if bg else 0
    rgb_code = 48 if bg else 38
    if isinstance(color, int):
        if color not in int_range:
            raise ValueError(f"Invalid color code: {color}")
        return str(color)
    if isinstance(color, (tuple, list)):
        if len(color) != 3:
            raise ValueError(f"Invalid color tuple: {color}")
        if not all(isinstance(c, int) for c in color):
            raise ValueError(f"Invalid color tuple: {color}")
        if not all(c in range(256) for c in color):
            raise ValueError(f"Invalid color tuple: {color}")
        return f"{rgb_code};2;{';'.join([str(c) for c in color])}"
    color = str(color)
    if color not in color_code_map:
        raise ValueError(f"Invalid color name: {color}")
    return f"{color_code_map[color] + int_offset}"
