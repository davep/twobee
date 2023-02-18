"""Implements a base reader class for reading from 2bit files."""

##############################################################################
# Python imports.
from __future__        import annotations
from abc               import ABC, abstractmethod
from typing_extensions import Final
from struct            import unpack

##############################################################################
class TwoBitReader( ABC ):
    """Abstract base class for 2bit reader classes."""

    SIGNATURE: Final = 0x1a412743
    """The signature of a 2bit file."""

    VERSION: Final = 0
    """The valid version of a 2bit file."""

    _HEADER_SIZE: Final = 16
    """The size of a 2bit file header."""

    def __init__( self, uri: str ) -> None:
        """Initialise the reader.

        Args:
            uri: The URI to read the data from.
        """
        self._uri = uri
        self.open()

        # Start out not knowing what endianness the data is in.
        self._endianness = ""

        # Start out assuming there are no sequences.
        self._sequence_count = 0

        # Start out with an empty index.
        self._index: dict[ str, int ] = {}

        # Read the header.
        self._read_header()

        # Read the index.
        self._read_index()

    @abstractmethod
    def open( self ) -> None:
        """Open the URI for reading."""
        raise NotImplemented

    @abstractmethod
    def close( self ) -> None:
        """Close the URI for reading."""
        raise NotImplemented

    @abstractmethod
    def read( self, size: int ) -> bytes:
        """Read a number of bytes from the 2bit file.

        Returns:
            The bytes read.
        """
        raise NotImplemented

    def _read_header( self ) -> None:
        """Read the header of the 2bit file."""

        # Read in the header.
        header = self.read( self._HEADER_SIZE )

        # Now test it to figure out what endianness we want to be using.
        for candidate in "<>":
            signature, version, self._sequence_count, _ = unpack( f"{candidate}IIII", header )
            if signature == self.SIGNATURE:
                self._endianness = candidate
                break
        else:
            # Looks like the signature wasn't valid.
            raise Exception     # TODO

        # 2bit files only have one recognised version; if we're not looking
        # at it...
        if version != self.VERSION:
            # ...throw an error.
            raise Exception     # TODO

    def _read_index( self ) -> None:
        """Read the index of the 2bit file."""

        # An index entry is 1 byte for the name length, length number of
        # bytes for the name, and then 4 bytes for the offset to the actual
        # data. This means each record is variable in length. Because we
        # might be reading from a slow source, let's load up the maximum
        # buffer.
        raw_index = self.read( ( 1 + 255 + 4 ) * self._sequence_count )

        offset = 0
        for _ in range( self._sequence_count ):
            name_length = raw_index[ offset ]
            offset += 1
            name = raw_index[ offset: offset + name_length ].decode()
            offset += name_length
            self._index[ name ], _ = unpack( f"{self._endianness}L", raw_index[ offset: offset + 4 ] )
            offset += 4

### reader.py ends here
