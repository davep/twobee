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

        # Store off the key data.
        self._reader = reader
        self._name   = name
        self._offset = offset

        # Jump to the start of the sequence in the file.
        self._reader.goto( self._offset )

        # Get the size of the DNA in the sequence.
        self._dna_size = reader.read_long()

        # Get the N block data.
        self._n_block_counts = reader.read_long()
        self._n_block_starts = reader.read_long_array( self._n_block_counts )
        self._n_blick_sizes  = reader.read_long_array( self._n_block_counts )

        # Get the mask block data.
        self._mask_block_counts = reader.read_long()
        self._mask_block_starts = reader.read_long_array( self._mask_block_counts )
        self._mask_blick_sizes  = reader.read_long_array( self._mask_block_counts )

        # We should now be on the reserved long integer. It should always be
        # zero.
        assert self._reader.read_long() == 0

        # And. having go that far, we should be sat at the start of the
        # actual DNA data. Save where it is as we'll be needing to know
        # that.
        self._dna_start = self._reader.position()

    def __rich_repr__( self ) -> Result:
        """Make the object look nice in Rich."""
        yield self._name
        yield "offset", self._offset
        yield "dna_size", self._dna_size

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
