"""Implements a base reader class for reading from 2bit files."""

##############################################################################
# Python imports.
from __future__        import annotations
from abc               import ABC, abstractmethod
from struct            import unpack
from functools         import lru_cache
from typing            import Iterator
from typing_extensions import Final

##############################################################################
# Rich imports.
from rich.repr import Result

##############################################################################
# Local imports.
from .sequence import TwoBitSequence

##############################################################################
class TwoBitReader( ABC ):
    """Abstract base class for 2bit reader classes."""

    SIGNATURE: Final = 0x1a412743
    """The signature of a 2bit file."""

    VERSION: Final = 0
    """The valid version of a 2bit file."""

    _HEADER_SIZE: Final = 16
    """The size of a 2bit file header."""

    def __init__( self, uri: str, masking: bool=False ) -> None:
        """Initialise the reader.

        Args:
            uri: The URI to read the data from.
            masking: Should masking be taken into account?

        Note:

            The `masking` parameter is optional and is `False` by default.
        """
        self._uri     = uri
        self._masking = masking
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

    def __rich_repr__( self ) -> Result:
        """Make the object look nice in Rich."""
        yield self._uri
        yield "sequence_count", self._sequence_count

    @property
    def masking( self ) -> bool:
        """Should masking be taken into account?"""
        return self._masking

    @abstractmethod
    def open( self ) -> None:
        """Open the URI for reading."""

    @abstractmethod
    def close( self ) -> None:
        """Close the URI for reading."""

    @abstractmethod
    def goto( self, position: int ) -> None:
        """Go to a specific position within the file.

        Args:
            position: The position to go to in the file.
        """

    @abstractmethod
    def position( self ) -> int:
        """Get the current position within the 2bit file.

        Returns:
           The current position.
        """
        return NotImplemented

    @abstractmethod
    def read( self, size: int, position: int | None=None ) -> bytes:
        """Read a number of bytes from the 2bit file.

        Args:
            size: The number of bytes to read.
            position: The optional location to start reading from.

        Returns:
            The bytes read.
        """
        return NotImplemented

    def read_long( self ) -> int:
        """Read a long integer from the file.

        Returns:
            The long integer value read.

        Note:
            In this case a long integer is 4 bytes.
        """
        return int( unpack( f"{self._endianness}L", self.read( 4 ) )[ 0 ] )

    def read_long_array( self, count: int ) -> tuple[ int, ... ]:
        """Read an array of long integers from the file.

        Args:
            count: The count of long integers to read.

        Returns:
            A tuple of long integers read.
        """
        return unpack( f"{self._endianness}{'L' * count}", self.read( count * 4 ) )

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
            self._index[ name ], *_ = unpack(
                f"{self._endianness}L", raw_index[ offset: offset + 4 ]
            )
            offset += 4

    @property
    def sequences( self ) -> tuple[ str, ... ]:
        """The collection of sequences found in the 2bit file."""
        return tuple( self._index.keys() )

    def __iter__( self ) -> Iterator[ str ]:
        return iter( self.sequences )

    def __len__( self ) -> int:
        return self._sequence_count

    @lru_cache()
    def sequence( self, name: str ) -> TwoBitSequence:
        """Get a 2bit sequence given its name.

        Args:
            name: The name of the sequence to get.

        Returns:
            An object for reading the sequence.
        """
        # TODO: Validate the sequence name first and then throw an error if
        # it's not known.
        return TwoBitSequence( self, name, self._index[ name ] )

    def __getitem__( self, name: str ) -> TwoBitSequence:
        return self.sequence( name )

### reader.py ends here
