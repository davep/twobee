"""The main screen for the TwoBee application."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual.app          import ComposeResult
from textual.screen       import Screen
from textual.containers   import Horizontal
from textual.widgets      import Header, Footer, Tree

##############################################################################
# Local imports.
from twobee    import TwoBitFileReader
from ..widgets import Bases

##############################################################################
class Main( Screen ):
    """The main screen for the TwoBee application."""

    DEFAULT_CSS = """
    Tree {
        width: 25%;
        min-width: 25;
        border-right: vkey $panel-lighten-2;
    }

    Bases {
        width: 1fr;
    }
    """

    def __init__( self, file: Path ) -> None:
        """Initialise the main screen."""
        super().__init__()
        self._file = file
        self._reader = TwoBitFileReader( str( file ), masking=False )

    def compose( self ) -> ComposeResult:
        """Compose the main screen of the application."""
        yield Header()
        with Horizontal():
            yield Tree[ str ]( str( self._file.stem ) )
            yield Bases()
        yield Footer()

    def on_mount( self ) -> None:
        """Populate the screen once the DOM is up and running."""
        file_map = self.query_one( Tree )
        for chromosome in self._reader:
            file_map.root.add_leaf( chromosome, data=chromosome )
        file_map.root.expand()
        file_map.focus()

    def on_tree_node_selected( self, event: Tree.NodeSelected ) -> None:
        """Response to a tree node being selected.

        Args:
            event: The selection event.
        """
        # The root has no data, chromosome nodes have the name of the
        # chromosome as their data, so test if we got a name...
        if isinstance( event.node.data, str ):
            # ...and update the base viewer to view that.
            self.query_one( Bases ).show( self._reader[ event.node.data ] )

### main.py ends here
