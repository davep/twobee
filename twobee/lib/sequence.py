"""Code for reading and handling a DNA sequence in a 2bit file."""

##############################################################################
# Python imports.
from __future__  import annotations
from dataclasses import dataclass

##############################################################################
# Rich imports.
from rich.repr import Result

##############################################################################
# Local imports.
from .reader_protocol import TwoBitReaderInterface

##############################################################################
# Class that holds the start and end of a block.
@dataclass
class TwoBitBlock:

    start: int
    """The start location of the block (inclusive)."""
    end: int
    """The end location of the block (exclusive)."""
    size: int
    """The size of the block."""

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
        self._reader = reader
        self._name   = name
        self._offset = offset

        # Jump to the start of the sequence in the file.
        self._reader.goto( self._offset )

        # Get the size of the DNA in the sequence.
        self._dna_size = reader.read_long()

        # Get the N block data.
        self.n_blocks = self._load_blocks()

        # Get the mask block data.
        self.mask_blocks = self._load_blocks()

        # We should now be on the reserved long integer. It should always be
        # zero.
        assert self._reader.read_long() == 0

        # And. having go that far, we should be sat at the start of the
        # actual DNA data. Save where it is as we'll be needing to know
        # that.
        self._dna_start = self._reader.position()

    def _load_blocks( self ) -> tuple[ TwoBitBlock, ... ]:
        """Load the block data at the current location.

        Returns:
            A tuple of the blocks read.
        """
        counts = self._reader.read_long()
        starts = self._reader.read_long_array( counts )
        sizes  = self._reader.read_long_array( counts )
        return tuple( TwoBitBlock( start, start + size, size ) for start, size in zip( starts, sizes ) )

    def __rich_repr__( self ) -> Result:
        """Make the object look nice in Rich."""
        yield self._name
        yield "offset", self._offset
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
    def dna_size( self ) -> int:
        """The size of the DNA in the sequence."""
        return self._dna_size

    def __len__( self ) -> int:
        return self._dna_size

### sequence.py ends here
