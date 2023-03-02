"""A widget for browsing bases within a chromosome in a 2bit file."""

##############################################################################
# Python imports.
from __future__ import annotations
from math       import ceil

##############################################################################
# Rich imports.
from rich.segment import Segment

##############################################################################
# Textual imports.
from textual.scroll_view import ScrollView
from textual.strip       import Strip
from textual.geometry    import Size

##############################################################################
# Local imports.
from twobee.lib.sequence import TwoBitSequence

##############################################################################
class Bases( ScrollView, can_focus=True ):
    """A widget for browsing bases within a sequence (chromosome)."""

    COMPONENT_CLASSES = {
        "bases--no-data",
        "bases--label",
        "bases--t",
        "bases--c",
        "bases--a",
        "bases--g",
        "bases--n",
        "bases--T",
        "bases--C",
        "bases--A",
        "bases--G",
        "bases--N"
    }

    DEFAULT_CSS = """
    Bases {
        background: $panel;
        /* Currently I can only make this work always showing the scrollbars. */
        overflow-y: scroll;
    }

    Bases > .bases--no-data {
        color: $panel-lighten-2;
    }

    Bases > .bases--label {
        color: $text-muted;
        background: $primary-background;
    }

    /* Thymine. */

    Bases > .bases--t, Bases > .bases--T {
        color: #bbbb00;
    }

    App.-light-mode Bases > .bases--t, App.-light-mode Bases > .bases--T {
        color: #969600;
    }

    /* Cytosine. */

    Bases > .bases--c, Bases > .bases--C {
        color: #ff0000;
    }

    App.-light-mode Bases > .bases--c, App.-light-mode Bases > .bases--C {
        color: #bb0000;
    }

    /* Adenine. */

    Bases > .bases--a, Bases > .bases--A {
        color: #8dd4e8;
    }

    App.-light-mode Bases > .bases--a, App.-light-mode Bases > .bases--A {
        color: #4b5cc4;
    }

    /* Guanine. */

    Bases > .bases--g, Bases > .bases--G {
        color: #00c000;
    }

    /* Any/unknown. */

    Bases > .bases--n, Bases > .bases--N {
        color: $text-disabled;
    }
    """

    NO_DATA = "."
    """The character to use to show there's no data at all."""

    def __init__( self ) -> None:
        """Initialise the widget.

        Args:
            reader: The reader object to read data from the 2bit file.
        """
        super().__init__()
        self._sequence: TwoBitSequence | None = None
        self._label_size                      = 0

    @property
    def _width( self ) -> int:
        """The width of the data."""
        return self.size.width - ( self._label_size + self.scrollbar_size_vertical )

    def show( self, sequence: TwoBitSequence ):
        """Show the given sequence's bases.

        Args:
            sequence: The sequence to show.
        """
        self._sequence    = sequence
        self._label_size  = len( f"{sequence.dna_size:>,} " )
        self.virtual_size = Size( self._width, ceil( self._sequence.dna_size // self._width ) + 1 )
        self.scroll_to( 0, 0, animate=False )

    @property
    def _empty_line( self ) -> Strip:
        """An empty line for the display."""
        return Strip( [
            Segment(
                self.NO_DATA * self.size.width,
                style=self.get_component_rich_style( "bases--no-data" )
            )
        ] )

    def render_line( self, y: int ) -> Strip:
        """Render a line in the display.

        Args:
            y: The line to render.

        Returns:
            A `Strip` that is the line to render.
        """

        # Only try and show something if we're actually viewing a sequence.
        if self._sequence is not None:

            # Calculate the starting base in the view.
            start = self._width * ( self.scroll_offset.y + y )

            # If that places us within the bases in the current sequence...
            if start < self._sequence.dna_size:
                return Strip( [
                    Segment(
                        f"{start:>{self._label_size-1},} ",
                        style=self.get_component_rich_style( "bases--label" )
                    ),
                    *[
                        Segment( base, style=self.get_component_rich_style( f"bases--{base}" ) )
                        for base in self._sequence[ start:start + self._width ]
                    ]
                ] )

        # We're past the end, or there's nothing to show, so just show an
        # empty line.
        return self._empty_line

### bases.py ends here
