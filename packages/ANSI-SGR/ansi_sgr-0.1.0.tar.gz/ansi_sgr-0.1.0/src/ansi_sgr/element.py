from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
import textwrap as _textwrap
import wcwidth as _wcwidth

import ansi_sgr as _sgr

if _TYPE_CHECKING:
    from typing import Literal
    from protocolman import Stringable


def code_block(
    code: Stringable,
    title: Stringable = "Code",
    emoji: Stringable | None = "💻",
    line_num: bool = True,
    line_num_start: int = 1,
    emphasize_lines: list[int] | None = None,
    title_styles: int | str | list[int | str] = "bold",
    title_color: int | str | tuple = (255, 255, 255),
    title_bg_color: int | str | tuple = (70, 0, 0),
    title_margin_top: int | None = None,
    title_margin_bottom: int | None = None,
    title_align: Literal["left", "right", "center"] = "left",
    code_margin_top: int | None = 1,
    code_margin_bottom: int | None = 1,
    line_num_styles: int | str | list[int | str] = "bold",
    line_num_color: int | str | tuple = (255, 255, 255),
    line_num_bg_color: int | str | tuple = (30, 30, 30),
    line_styles: int | str | list[int | str] = None,
    line_color: int | str | tuple = (255, 255, 255),
    line_bg_color: int | str | tuple = (100, 0, 0),
    margin_left: int | None = 1,
    margin_right: int | None = 1,
    char_top: Stringable | None = "",
    char_bottom: Stringable | None = "━",
    char_left: Stringable | None = "┃",
    char_right: Stringable | None = "┃",
    char_top_left: Stringable | None = "┏",
    char_top_right: Stringable | None = "┓",
    char_bottom_left: Stringable | None = "┗",
    char_bottom_right: Stringable | None = "┛",
    line_width: int = 50,
):
    title = str(title)
    code = str(code)
    code_lines = code.splitlines()
    if emoji:
        title = f"{emoji} {title}"
    title_section = block(
        text=title,
        text_styles=title_styles,
        text_color=title_color,
        bg_color=title_bg_color,
        char_top=char_top,
        char_bottom="",
        char_left=char_left,
        char_right=char_right,
        char_top_left=char_top_left,
        char_top_right=char_top_right,
        margin_top=title_margin_top,
        margin_bottom=title_margin_bottom,
        margin_left=margin_left,
        margin_right=margin_right,
        line_width=max(max(_wcwidth.wcswidth(line) for line in code_lines), line_width),
        align=title_align,
    )
    line_count = len(code_lines)
    number_width = len(str(line_num_start + line_count - 1))
    if margin_left is None:
        margin_left = margin_right or 0
    if margin_right is None:
        margin_right = margin_left or 0
    line_width_adjusted = max(max(_wcwidth.wcswidth(line) for line in code_lines), line_width)
    lines = _textwrap.fill(
        code,
        width=line_width_adjusted - ((number_width + 2) if line_num else 0),
        expand_tabs=True,
        tabsize=4,
        replace_whitespace=False,
        drop_whitespace=False,
    ).splitlines()
    if char_left is None:
        char_left = char_right or ""
    if char_right is None:
        char_right = char_left or ""
    if code_margin_top is None:
        code_margin_top = code_margin_bottom
    if code_margin_bottom is None:
        code_margin_bottom = code_margin_top
    formatted_lines = []
    for line_idx, line in enumerate(lines):
        screen_width = _wcwidth.wcswidth(line)
        char_width = len(line)
        extra_padding = char_width - screen_width
        width = line_width_adjusted + extra_padding - (number_width + 2 if line_num else 0)
        line = line.ljust(width)
        if emphasize_lines and line_idx + 1 in emphasize_lines:
            sequence = _sgr.create_sequence(line_styles, line_color, line_bg_color)
            line = _sgr.apply_sequence(line, sequence, reset=True)
        if line_num:
            sequence = _sgr.create_sequence(line_num_styles, line_num_color, line_num_bg_color)
            line_num_sgr = _sgr.apply_sequence(f"{line_num_start + line_idx:>{number_width}}", sequence, reset=True)
            line = f"{line_num_sgr}  {line}"
        if margin_left:
            line = " " * margin_left + line
        if margin_right:
            line = line + " " * margin_right
        formatted_lines.append(f"{char_left}{line}{char_right}")
    margin_line_content = " " * (line_width_adjusted + (margin_left or 0) + (margin_right or 0))
    if code_margin_top:
        formatted_lines = [f"{char_left}{margin_line_content}{char_right}"] * code_margin_top + formatted_lines
    if code_margin_bottom:
        formatted_lines = formatted_lines + [f"{char_left}{margin_line_content}{char_right}"] * code_margin_bottom
    if char_top is None:
        char_top = char_bottom or ""
    if char_bottom is None:
        char_bottom = char_top or ""
    if char_top:
        total_line_width = line_width_adjusted + margin_left + margin_right
        line_top = f"{char_top_left}{char_top * total_line_width}{char_top_right}"
        formatted_lines.insert(0, line_top)
    if char_bottom:
        total_line_width = line_width_adjusted + margin_left + margin_right
        line_bottom = f"{char_bottom_left}{char_bottom * total_line_width}{char_bottom_right}"
        formatted_lines.append(line_bottom)
    body_section = "\n".join(formatted_lines)
    return f"{title_section}\n{body_section}"


def admonition(
    title: Stringable,
    text: Stringable,
    emoji: Stringable | None = None,
    title_styles: int | str | list[int | str] = "bold",
    title_color: int | str | tuple = (255, 255, 255),
    title_bg_color: int | str | tuple = (70, 0, 0),
    title_margin_top: int | None = None,
    title_margin_bottom: int | None = None,
    title_align: Literal["left", "right", "center"] = "left",
    text_styles: int | str | list[int | str] = None,
    text_color: int | str | tuple = None,
    text_bg_color: int | str | tuple = None,
    text_margin_top: int | None = 1,
    text_margin_bottom: int | None = 1,
    text_align: Literal["left", "right", "center"] = "left",
    margin_left: int | None = 1,
    margin_right: int | None = 1,
    char_top: Stringable | None = "",
    char_bottom: Stringable | None = "━",
    char_left: Stringable | None = "┃",
    char_right: Stringable | None = "┃",
    char_top_left: Stringable | None = "┏",
    char_top_right: Stringable | None = "┓",
    char_bottom_left: Stringable | None = "┗",
    char_bottom_right: Stringable | None = "┛",
    line_width: int = 50,
):
    title = str(title)
    if emoji:
        title = f"{emoji} {title}"
    title_section = block(
        text=title,
        text_styles=title_styles,
        text_color=title_color,
        bg_color=title_bg_color,
        char_top=char_top,
        char_bottom="",
        char_left=char_left,
        char_right=char_right,
        char_top_left=char_top_left,
        char_top_right=char_top_right,
        margin_top=title_margin_top,
        margin_bottom=title_margin_bottom,
        margin_left=margin_left,
        margin_right=margin_right,
        line_width=max(max(_wcwidth.wcswidth(_sgr.remove_sequence(line)) for line in str(text).splitlines()), line_width),
        align=title_align,
    )
    body_section = block(
        text=text,
        text_styles=text_styles,
        text_color=text_color,
        bg_color=text_bg_color,
        char_top="",
        char_bottom=char_bottom,
        char_left=char_left,
        char_right=char_right,
        char_bottom_left=char_bottom_left,
        char_bottom_right=char_bottom_right,
        margin_top=text_margin_top,
        margin_bottom=text_margin_bottom,
        margin_left=margin_left,
        margin_right=margin_right,
        line_width=line_width,
        align=text_align,
    )
    return f"{title_section}\n{body_section}"


def block(
    text: Stringable,
    text_styles: int | str | list[int | str] = None,
    text_color: int | str | tuple = None,
    bg_color: int | str | tuple = None,
    char_top: Stringable | None = "━",
    char_bottom: Stringable | None = "━",
    char_left: Stringable | None = "┃",
    char_right: Stringable | None = "┃",
    char_top_left: Stringable | None = "┏",
    char_top_right: Stringable | None = "┓",
    char_bottom_left: Stringable | None = "┗",
    char_bottom_right: Stringable | None = "┛",
    margin_top: int | None = None,
    margin_bottom: int | None = None,
    margin_left: int | None = 1,
    margin_right: int | None = 1,
    line_width: int = 50,
    align: Literal["left", "right", "center"] = "left",
):
    if margin_left is None:
        margin_left = margin_right
    if margin_right is None:
        margin_right = margin_left
    if char_left is None:
        char_left = char_right or ""
    if char_right is None:
        char_right = char_left or ""
    if margin_top is None:
        margin_top = margin_bottom
    if margin_bottom is None:
        margin_bottom = margin_top
    lines = str(text).splitlines()
    max_line_width = max(max(_wcwidth.wcswidth(_sgr.remove_sequence(line)) for line in lines), line_width)
    if margin_top:
        lines = [" " * max_line_width] * margin_top + lines
    if margin_bottom:
        lines = lines + [" " * max_line_width] * margin_bottom
    formatted_lines = []
    for line in lines:
        line_sanitized = _sgr.remove_sequence(line)
        screen_width = _wcwidth.wcswidth(line_sanitized)
        char_width = len(line_sanitized)
        extra_padding = char_width - screen_width
        width = max_line_width + extra_padding + len(line) - len(line_sanitized)
        if align == "left":
            line = line.ljust(width)
        elif align == "right":
            line = line.rjust(width)
        else:
            line = line.center(width)
        formatted_lines.append(
            inline(
                line,
                text_styles=text_styles,
                text_color=text_color,
                bg_color=bg_color,
                char_left=char_left,
                char_right=char_right,
                margin_left=margin_left,
                margin_right=margin_right,
            )
        )
    if char_top is None:
        char_top = char_bottom or ""
    if char_bottom is None:
        char_bottom = char_top or ""
    if char_top:
        total_line_width = max_line_width + (margin_left or 0) + (margin_right or 0)
        line_top = f"{char_top_left}{char_top * total_line_width}{char_top_right}"
        formatted_lines.insert(0, line_top)
    if char_bottom:
        total_line_width = max_line_width + (margin_left or 0) + (margin_right or 0)
        line_bottom = f"{char_bottom_left}{char_bottom * total_line_width}{char_bottom_right}"
        formatted_lines.append(line_bottom)
    return "\n".join(formatted_lines)


def inline(
    text: Stringable,
    text_styles: int | str | list[int | str] = None,
    text_color: int | str | tuple = None,
    bg_color: int | str | tuple = None,
    char_left: Stringable | None = None,
    char_right: Stringable | None = None,
    margin_left: int | None = None,
    margin_right: int | None = None,
):
    sequence = _sgr.create_sequence(text_styles, text_color, bg_color)
    text = str(text)
    if char_left is None:
        char_left = char_right or ""
    if char_right is None:
        char_right = char_left or ""
    if margin_left is None:
        margin_left = margin_right
    if margin_right is None:
        margin_right = margin_left
    if margin_left:
        text = " " * margin_left + text
    if margin_right:
        text = text + " " * margin_right
    text_box = _sgr.apply_sequence(text, sequence, reset=True) if sequence != _sgr.reset_sequence() else text
    return f"{char_left}{text_box}{char_right}"
