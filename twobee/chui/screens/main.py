"""The main screen for the TwoBee application."""

##############################################################################
# Textual imports.
from textual.app     import ComposeResult
from textual.screen  import Screen
from textual.widgets import Header, Footer

##############################################################################
class Main( Screen ):
    """The main screen for the TwoBee application."""

    def compose( self ) -> ComposeResult:
        """Compose the main screen of the application."""
        yield Header()
        yield Footer()

### main.py ends here
