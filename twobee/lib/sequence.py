"""Code for reading and handling a DNA sequence in a 2bit file."""

##############################################################################
# Python imports.
from __future__ import annotations
from functools  import lru_cache
from re         import match

##############################################################################
# Rich imports.
from rich.repr import Result

##############################################################################
# Local imports.
from .bases           import TwoBitBases
from .block           import TwoBitBlock
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

        # Store off the key data.
        self.reader = reader
        self._name  = name

        # Jump to the start of the sequence in the file.
        self.reader.goto( offset )

        # Get the size of the DNA in the sequence.
        self._dna_size = self.reader.read_long()

        # Get the N block data.
        self.n_blocks = self._load_blocks()

        # Get the mask block data.
        self.mask_blocks = self._load_blocks()

        # We should now be on the reserved long integer. It should always be
        # zero.
        assert self.reader.read_long() == 0

        # And. having got that far, we should be sat at the start of the
        # actual DNA data. Save where it is as we'll be needing to know
        # that.
        self._dna_start = self.reader.position()

    def _load_blocks( self ) -> tuple[ TwoBitBlock, ... ]:
        """Load the block data at the current location.

        Returns:
            A tuple of the blocks read.
        """
        counts = self.reader.read_long()
        starts = self.reader.read_long_array( counts )
        sizes  = self.reader.read_long_array( counts )
        return tuple( TwoBitBlock( start, start + size, size ) for start, size in zip( starts, sizes ) )

    def __rich_repr__( self ) -> Result:
        """Make the object look nice in Rich."""
        yield self._name
        yield "dna_file_location", self.dna_file_location
        yield "dna_size", self._dna_size
        yield "len(n_blocks)", len( self.n_blocks )
        yield "len(mask_blocks)", len( self.mask_blocks )

    @property
    def name( self ) -> str:
        """The name of the sequence.

        Note:
            Generally this will be the chromosome name.
        """
        return self._name

    @property
    def dna_file_location( self ) -> int:
        """The location of the start of the DNA in the 2bit file."""
        return self._dna_start

    @property
    def dna_size( self ) -> int:
        """The size of the DNA in the sequence."""
        return self._dna_size

    def __len__( self ) -> int:
        return self._dna_size

    def bases( self, start: int, end: int ) -> TwoBitBases:
        """Get bases from the 2bit file.

        Args:
            start: The start location to get the bases from (inclusive).
            end: The end location to get the bases from (exclusive).

        Returns:
            The bases loaded between those locations.
        """

        # TODO: actually check and raise a library-bases exception.
        assert end > start
        return TwoBitBases( self, start, end )

    def __getitem__( self, location: int | slice | tuple[ int, int ] | str ) -> TwoBitBases:
        if isinstance( location, int ):
            return self.bases( location, location + 1 )
        if isinstance( location, slice ):
            return self.bases(
                0 if location.start is None else location.start,
                len( self ) if location.stop is None else location.stop
            )
        if isinstance( location, tuple ):
            return self.bases( *location )
        if isinstance( location, str ):
            hit = match( r"^(?P<start>\d+)(?::|\.\.)(?P<end>\d+)$", location )
            if hit is not None:
                return self[ ( int( hit[ "start" ] ), int( hit[ "end" ] )) ]
        return NotImplemented

    @lru_cache()
    def mask_blocks_intersecting( self, start: int, end: int ) -> tuple[ TwoBitBlock, ... ]:
        """Get all mask blocks that intersect the given range.

        Args:
            start: The start of the range to consider.
            end: The end of the range to consider.

        Returns:
            The mask blocks that intersect the given range.
        """
        return tuple(
            block for block in self.mask_blocks if not ( block.end < start or block.start > end )
        ) if self.reader.masking else ()

### sequence.py ends here
