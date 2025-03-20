"""Work with ANSI SGR (Select Graphic Rendition) parameters.

References
----------
- https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
"""

from ansi_sgr.sgr import (
    format,
    create_sequence,
    create_sequence_from_code,
    apply_sequence,
    has_sequence,
    remove_sequence,
    reset_sequence,
    text_style_code,
    color_code,
)

from ansi_sgr import element, protocol
