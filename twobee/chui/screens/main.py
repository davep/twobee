"""The main screen for the TwoBee application."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.screen     import Screen
from textual.containers import Horizontal, Vertical
from textual.widgets    import Header, Footer, Tree, Label
from textual.binding    import Binding

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

    #viewer {
        width: 1fr;
    }

    #info {
        height: 1;
        width: 100%;
        color: $text-muted;
        background: $primary-background;
        text-align: center;
    }

    #viewer:focus-within #info, #viewer:focus-within Bases .bases--label {
        text-style: bold;
        background: $panel-lighten-2;
    }

    Bases {
        width: 1fr;
        height: 1fr;
    }
    """

    BINDINGS = [
        Binding( "escape", "app.quit", "Exit" ),
        Binding( "ctrl+d", "app.toggle_dark", "Light/Dark" ),
    ]
    """The bindings for the main screen."""

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
            with Vertical( id="viewer" ):
                yield Label( "[i]None[/]", id="info" )
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
            self.query_one( "#info", Label ).update( event.node.data )
            self.query_one( Bases ).focus()

### main.py ends here
