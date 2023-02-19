"""Code for reading 2bit data from a local filesystem.."""

##############################################################################
# Python imports.
from __future__ import annotations

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

    def read( self, size: int, position: int | None=None ) -> bytes:
        """Read a number of bytes from the 2bit file.

        Args:
            size: The number of bytes to read.
            position: The optional location to start reading from.

        Returns:
            The bytes read.
        """
        if position is not None:
            self._file.seek( position )
        return self._file.read( size )

### file_reader.py ends here
