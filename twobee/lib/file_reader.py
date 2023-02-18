"""Code for reading 2bit data from a local filesystem.."""

##############################################################################
# Local imports.
from .reader import TwoBitReader

##############################################################################
class TwoBitFileReader( TwoBitReader ):
    """Class for reading data from a local 2bit file."""

    def open( self ) -> None:
        """Open a file for reading."""
        self._file = open( self._uri, "rb" )

    def close( self ) -> None:
        """Close the file."""
        self._file.close()

    def read( self, size: int ) -> bytes:
        """Read a number of bytes from the 2bit file.

        Args:
            size: The number of bytes to read.

        Returns:
            The bytes read.
        """
        return self._file.read( size )

### file_reader.py ends here
