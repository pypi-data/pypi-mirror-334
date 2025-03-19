"""
Absufyu: Utilities
------------------
Text table

Version: 5.2.0
Date updated: 13/03/2025 (dd/mm/yyyy)
"""

# Module level
# ---------------------------------------------------------------------------
__all__ = ["OneColumnTableMaker"]


# Library
# ---------------------------------------------------------------------------
import os
from collections.abc import Sequence
from enum import StrEnum
from textwrap import TextWrapper
from typing import Literal, Protocol, cast

from absfuyu.core import BaseClass


# Style
# ---------------------------------------------------------------------------
class BoxDrawingCharacter(Protocol):
    UPPER_LEFT_CORNER: str = ""
    UPPER_RIGHT_CORNER: str = ""
    HORIZONTAL: str = ""
    VERTICAL: str = ""
    LOWER_LEFT_CORNER: str = ""
    LOWER_RIGHT_CORNER: str = ""
    VERTICAL_RIGHT: str = ""
    VERTICAL_LEFT: str = ""
    CROSS: str = ""
    HORIZONTAL_UP: str = ""
    HORIZONTAL_DOWN: str = ""


class BoxDrawingCharacterNormal(StrEnum):
    """
    Box drawing characters - Normal

    Characters reference: https://en.wikipedia.org/wiki/Box-drawing_characters
    """

    UPPER_LEFT_CORNER = "\u250c"
    UPPER_RIGHT_CORNER = "\u2510"
    HORIZONTAL = "\u2500"
    VERTICAL = "\u2502"
    LOWER_LEFT_CORNER = "\u2514"
    LOWER_RIGHT_CORNER = "\u2518"
    VERTICAL_RIGHT = "\u251c"
    VERTICAL_LEFT = "\u2524"
    CROSS = "\u253c"
    HORIZONTAL_UP = "\u2534"
    HORIZONTAL_DOWN = "\u252c"


class BoxDrawingCharacterBold(StrEnum):
    """
    Box drawing characters - Bold

    Characters reference: https://en.wikipedia.org/wiki/Box-drawing_characters
    """

    UPPER_LEFT_CORNER = "\u250f"
    UPPER_RIGHT_CORNER = "\u2513"
    HORIZONTAL = "\u2501"
    VERTICAL = "\u2503"
    LOWER_LEFT_CORNER = "\u2517"
    LOWER_RIGHT_CORNER = "\u251b"
    VERTICAL_RIGHT = "\u2523"
    VERTICAL_LEFT = "\u252b"
    CROSS = "\u254b"
    HORIZONTAL_UP = "\u253b"
    HORIZONTAL_DOWN = "\u2533"


class BoxDrawingCharacterDashed(StrEnum):
    """
    Box drawing characters - Dashed

    Characters reference: https://en.wikipedia.org/wiki/Box-drawing_characters
    """

    UPPER_LEFT_CORNER = "\u250c"
    UPPER_RIGHT_CORNER = "\u2510"
    HORIZONTAL = "\u254c"
    VERTICAL = "\u254e"
    LOWER_LEFT_CORNER = "\u2514"
    LOWER_RIGHT_CORNER = "\u2518"
    VERTICAL_RIGHT = "\u251c"
    VERTICAL_LEFT = "\u2524"
    CROSS = "\u253c"
    HORIZONTAL_UP = "\u2534"
    HORIZONTAL_DOWN = "\u252c"


class BoxDrawingCharacterDouble(StrEnum):
    """
    Box drawing characters - Double

    Characters reference: https://en.wikipedia.org/wiki/Box-drawing_characters
    """

    UPPER_LEFT_CORNER = "\u2554"
    UPPER_RIGHT_CORNER = "\u2557"
    HORIZONTAL = "\u2550"
    VERTICAL = "\u2551"
    LOWER_LEFT_CORNER = "\u255a"
    LOWER_RIGHT_CORNER = "\u255d"
    VERTICAL_RIGHT = "\u2560"
    VERTICAL_LEFT = "\u2563"
    CROSS = "\u256c"
    HORIZONTAL_UP = "\u2569"
    HORIZONTAL_DOWN = "\u2566"


def get_box_drawing_character(
    style: Literal["normal", "bold", "dashed", "double"] = "normal",
) -> BoxDrawingCharacter:
    """
    Choose style for Box drawing characters.

    Parameters
    ----------
    style : Literal["normal", "bold", "dashed", "double"], optional
        Style for the table, by default ``"normal"``

    Returns
    -------
    BoxDrawingCharacter
        Box drawing characters in specified style.
    """

    if style.lower() == "normal":
        return cast(BoxDrawingCharacter, BoxDrawingCharacterNormal)
    elif style.lower() == "bold":
        return cast(BoxDrawingCharacter, BoxDrawingCharacterBold)
    elif style.lower() == "dashed":
        return cast(BoxDrawingCharacter, BoxDrawingCharacterDashed)
    elif style.lower() == "double":
        return cast(BoxDrawingCharacter, BoxDrawingCharacterDouble)
    else:
        return cast(BoxDrawingCharacter, BoxDrawingCharacterNormal)


# Class
# ---------------------------------------------------------------------------
class OneColumnTableMaker(BaseClass):
    """
    Table Maker instance

    Parameters
    ----------
    ncols : int | None, optional
        Length of the table (include content). Must be >= 5.
        Set to ``None`` to use maximum length,
        defaults to ``88`` when failed to use ``os.get_terminal_size()``.
        By default ``None``

    style : Literal["normal", "bold", "dashed", "double"], optional
        Style for the table, by default ``"normal"``
    """

    __slots__ = ("ncols", "_title", "_paragraphs", "_table_char", "_text_wrapper")

    def __init__(
        self,
        ncols: int | None = None,
        style: Literal["normal", "bold", "dashed", "double"] = "normal",
    ) -> None:
        """
        Table Maker instance

        Parameters
        ----------
        ncols : int | None, optional
            Length of the table (include content). Must be >= 5.
            Set to ``None`` to use maximum length,
            defaults to ``88`` when failed to use ``os.get_terminal_size()``.
            By default ``None``

        style : Literal["normal", "bold", "dashed", "double"], optional
            Style for the table, by default ``"normal"``
        """

        # Text length
        if ncols is None:
            try:
                self.ncols = os.get_terminal_size().columns
            except OSError:
                self.ncols = 88
        else:
            self.ncols = max(5, ncols)

        # Title & paragraph
        self._title = ""
        self._paragraphs: list[Sequence[str]] = []

        # Style
        self._table_char = get_box_drawing_character(style=style)

        # Text wrapper
        self._text_wrapper = TextWrapper(
            width=self.ncols - 4,
            initial_indent="",
            subsequent_indent="",
            tabsize=4,
            break_long_words=True,
        )

    def add_title(self, title: str) -> None:
        """
        Add title to Table

        Parameters
        ----------
        title : str
            Title to add.
            When ``len(title) > ncols``: title will not show
        """
        max_padding_length = self.ncols - 2
        if max_padding_length < (len(title) + 2) or len(title) < 1:
            _title = ""
        else:
            _title = f" {title} "

        line = (
            f"{self._table_char.UPPER_LEFT_CORNER}"
            f"{_title.center(max_padding_length, self._table_char.HORIZONTAL)}"
            f"{self._table_char.UPPER_RIGHT_CORNER}"
        )
        self._title = line

    def add_paragraph(self, paragraph: Sequence[str]) -> None:
        """
        Add paragraph into Table

        Parameters
        ----------
        paragraph : Sequence[str]
            An iterable of str
        """
        if isinstance(paragraph, str):
            self._paragraphs.append([paragraph])
        else:
            self._paragraphs.append(paragraph)

    def _make_line(self, option: Literal[0, 1, 2]) -> str:
        options = (
            (self._table_char.UPPER_LEFT_CORNER, self._table_char.UPPER_RIGHT_CORNER),
            (self._table_char.VERTICAL_RIGHT, self._table_char.VERTICAL_LEFT),
            (self._table_char.LOWER_LEFT_CORNER, self._table_char.LOWER_RIGHT_CORNER),
        )
        max_line_length = self.ncols - 2
        line = (
            f"{options[option][0]}"
            f"{''.ljust(max_line_length, self._table_char.HORIZONTAL)}"
            f"{options[option][1]}"
        )
        return line

    def _make_table(self) -> list[str] | None:
        # Check if empty
        if len(self._paragraphs) < 1:
            return None
        if len(self._paragraphs[0]) < 1:
            return None

        # Make table
        max_content_length = self.ncols - 4
        paragraph_length = len(self._paragraphs)

        # Line prep
        _first_line = self._make_line(0)
        _sep_line = self._make_line(1)
        _last_line = self._make_line(2)

        # Table
        table: list[str] = [_first_line] if self._title == "" else [self._title]
        for i, paragraph in enumerate(self._paragraphs, start=1):
            for line in paragraph:
                splitted_line = self._text_wrapper.wrap(line) if len(line) > 0 else [""]
                mod_lines: list[str] = [
                    f"{self._table_char.VERTICAL} "
                    f"{line.ljust(max_content_length, ' ')}"
                    f" {self._table_char.VERTICAL}"
                    for line in splitted_line
                ]
                table.extend(mod_lines)

            if i != paragraph_length:
                table.append(_sep_line)
            else:
                table.append(_last_line)
        return table

    def make_table(self) -> str:
        table = self._make_table()
        if table is None:
            return ""
        return "\n".join(table)
