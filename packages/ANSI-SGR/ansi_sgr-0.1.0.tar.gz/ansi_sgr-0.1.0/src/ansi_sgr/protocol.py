from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
from dataclasses import dataclass as _dataclass, asdict as _asdict

if _TYPE_CHECKING:
    from typing import Literal
    from protocolman import Stringable


@_dataclass
class ANSICodeBlockStyle:
    emoji: Stringable | None = "💻"
    title_styles: int | str | list[int | str] = "bold"
    title_color: int | str | tuple = (255, 255, 255)
    title_bg_color: int | str | tuple = (70, 0, 0)
    title_margin_top: int | None = None
    title_margin_bottom: int | None = None
    title_align: Literal["left", "right", "center"] = "left"
    code_margin_top: int | None = 1
    code_margin_bottom: int | None = 1
    line_num_styles: int | str | list[int | str] = "bold"
    line_num_color: int | str | tuple = (255, 255, 255)
    line_num_bg_color: int | str | tuple = (30, 30, 30)
    line_styles: int | str | list[int | str] = None
    line_color: int | str | tuple = (255, 255, 255)
    line_bg_color: int | str | tuple = (100, 0, 0)
    margin_left: int | None = 1
    margin_right: int | None = 1
    char_top: Stringable | None = ""
    char_bottom: Stringable | None = "━"
    char_left: Stringable | None = "┃"
    char_right: Stringable | None = "┃"
    char_top_left: Stringable | None = "┏"
    char_top_right: Stringable | None = "┓"
    char_bottom_left: Stringable | None = "┗"
    char_bottom_right: Stringable | None = "┛"
    line_width: int = 50

    @property
    def dict(self) -> dict:
        return _asdict(self)


@_dataclass
class ANSIAdmonitionStyle:
    emoji: Stringable | None = None
    title_styles: int | str | list[int | str] = "bold"
    title_color: int | str | tuple = (255, 255, 255)
    title_bg_color: int | str | tuple = (70, 0, 0)
    title_margin_top: int | None = None
    title_margin_bottom: int | None = None
    title_align: Literal["left", "right", "center"] = "left"
    text_styles: int | str | list[int | str] = None
    text_color: int | str | tuple = None
    text_bg_color: int | str | tuple = None
    text_margin_top: int | None = 1
    text_margin_bottom: int | None = 1
    text_align: Literal["left", "right", "center"] = "left"
    margin_left: int | None = 1
    margin_right: int | None = 1
    char_top: Stringable | None = None
    char_bottom: Stringable | None = "━"
    char_left: Stringable | None = "┃"
    char_right: Stringable | None = "┃"
    char_top_left: Stringable | None = "┏"
    char_top_right: Stringable | None = "┓"
    char_bottom_left: Stringable | None = "┗"
    char_bottom_right: Stringable | None = "┛"
    line_width: int = 50

    @property
    def dict(self) -> dict:
        return _asdict(self)


@_dataclass
class ANSIBlockStyle:
    text_styles: int | str | list[int | str] | None = None
    text_color: int | str | tuple[int, int, int] | None = None
    bg_color: int | str | tuple[int, int, int] = None
    char_top: str | None = None
    char_bottom: str | None = None
    char_left: str | None = None
    char_right: str | None = None
    margin_top: int | None = None
    margin_bottom: int | None = None
    margin_left: int | None = None
    margin_right: int | None = None
    line_width: int = 50

    @property
    def dict(self) -> dict:
        return _asdict(self)


@_dataclass
class ANSIInlineStyle:
    text_styles: int | str | list[int | str] | None = None
    text_color: int | str | tuple[int, int, int] | None = None
    bg_color: int | str | tuple[int, int, int] = None
    char_left: str | None = None
    char_right: str | None = None
    margin_left: int | None = None
    margin_right: int | None = None

    @property
    def dict(self) -> dict:
        return _asdict(self)

