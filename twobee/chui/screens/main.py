"""The main screen for the TwoBee application."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.screen     import Screen
from textual.containers import Horizontal
from textual.widgets    import Header, Footer, Tree, Static

##############################################################################
# Local imports.
from twobee import TwoBitFileReader

##############################################################################
class Main( Screen ):
    """The main screen for the TwoBee application."""

    DEFAULT_CSS = """
    Tree {
        width: 25%;
        border-right: vkey $panel-lighten-2;
    }
    """

    def __init__( self, file: Path ) -> None:
        """Initialise the main screen."""
        super().__init__()
        self._file = file
        self._reader = TwoBitFileReader( str( file ) )

    def compose( self ) -> ComposeResult:
        """Compose the main screen of the application."""
        yield Header()
        with Horizontal():
            yield Tree[ str ]( str( self._file.stem ) )
            yield Static( "TODO: data goes here" )
        yield Footer()

    def on_mount( self ) -> None:
        """Populate the screen once the DOM is up and running."""
        file_map = self.query_one( Tree )
        for chromosome in self._reader:
            file_map.root.add_leaf( chromosome, data=chromosome )
        file_map.root.expand()
        file_map.focus()

### main.py ends here
