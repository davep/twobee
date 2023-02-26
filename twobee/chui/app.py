"""Defines the application class for TwoBee."""

##############################################################################
# Textual imports/
from textual.app import App

##############################################################################
# Local imports.
from ..       import __version__
from .screens import Main

##############################################################################
class TwoBeeApp( App[ None ] ):
    """The TwoBee application class."""

    TITLE = "TwoBee"
    """The title for the application."""

    SUB_TITLE = f"A simple 2bit viewer for the terminal - v{__version__}"
    """The sub-title for the application."""

    def on_mount( self ) -> None:
        """Configure the application once the DOM is up and running."""
        self.push_screen( Main() )

##############################################################################
def run() -> None:
    """Run the application."""
    TwoBeeApp().run()

### app.py ends here
