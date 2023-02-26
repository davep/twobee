"""Defines the application class for TwoBee."""

##############################################################################
# Python imports.
from __future__ import annotations
from argparse   import Namespace, ArgumentParser, ArgumentTypeError
from pathlib    import Path

##############################################################################
# Textual imports/
from textual     import __version__ as textual_version
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

    def __init__( self, cli_args: Namespace ) -> None:
        """Initialise the app."""
        super().__init__()
        self._args = cli_args

    def on_mount( self ) -> None:
        """Configure the application once the DOM is up and running."""
        self.push_screen( Main( self._args.file ) )

##############################################################################
def py_file( path: str ) -> Path:
    """Check that the file we're being asked to look at seems fine

    Args:
        path: The argument.

    Returns:
        The `Path` to the file if it looks okay.
    """
    candidate = Path( path )
    if not candidate.exists():
        raise ArgumentTypeError( f"{path} does not exist" )
    return candidate

##############################################################################
def get_args() -> Namespace:
    """Parse and return the command line arguments.

    Returns:
        The result of parsing the arguments.
    """

    # Create the parser object.
    parser = ArgumentParser(
        prog        = "twobee",
        description = "A simple terminal-based 2bit file viewer.",
        epilog      = f"v{__version__}"
    )

    # Add --version
    parser.add_argument(
        "-v", "--version",
        help    = "Show version information.",
        action  = "version",
        version = f"%(prog)s {__version__} (Textual v{textual_version})"
    )

    # The remainder is the file to view.
    parser.add_argument(
        "file",
        help    = "The 2bit file to view",
        type    = py_file,
        default = "."
    )

    # Finally, parse the command line.
    return parser.parse_args()

##############################################################################
def run() -> None:
    """Run the application."""
    TwoBeeApp( get_args() ).run()

### app.py ends here
