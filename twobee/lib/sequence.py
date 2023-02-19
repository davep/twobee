"""Code for reading and handling a DNA sequence in a 2bit file."""

##############################################################################
# Rich imports.
from rich.repr import Result

##############################################################################
# Local imports.
from .reader_protocol import TwoBitReaderInterface

##############################################################################
class TwoBitSequence:
    """Class for reading a sequence from a 2bit file."""

    def __init__( self, reader: TwoBitReaderInterface, name: str, offset: int ):
        """Initialise the 2bit sequence object.

        Args:
            reader: The reader to load data from the file.
            name: The name of the sequence.
            offset: The initial offset of the sequence.
        """
        self._reader = reader
        self._name   = name
        self._offset = offset

    def __rich_repr__( self ) -> Result:
        """Make the object look nice in Rich."""
        yield self._name
        yield "offset", self._offset

    @property
    def name( self ) -> str:
        """The name of the sequence.

        Note:
            Generally this will be the chromosome name.
        """
        return self._name

### sequence.py ends here
