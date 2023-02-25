"""Provides the class for holding a collection of bases, read from a 2bit file."""


##############################################################################
# Python imports.
from __future__ import annotations

##############################################################################
# Rich imports.
from rich.repr import Result

##############################################################################
# Local imports.
from .sequence_protocol import TwoBitSequenceInterface

##############################################################################
# The bases, in the correct index ordering.
BASES = "TCAG"

##############################################################################
class TwoBitBases:
    """Holds bases read from a location in a 2bit file."""

    def __init__( self, sequence: TwoBitSequenceInterface, start: int, end: int ) -> None:
        """"""
        self._sequence = sequence
        self.start = start
        """The start location of the bases in the sequence (inclusive)."""
        self.end = end
        """The end location of the bases in the sequence (exclusive)."""
        self.bases = self._load()

    def __rich_repr__( self ) -> Result:
        """Make the object look nice in Rich."""
        yield self._sequence.name
        yield self.start
        yield self.end
        # TODO: pretty print and truncate.
        yield "bases", "".join( self.bases )

    def _load( self ) -> tuple[ str, ... ]:
        """Load a collection of bases from a 2bit file.

        Returns:
            The requested bases.
        """

        # Work out the byte range we'll be pulling out of the source.
        start_byte = self._sequence.dna_file_location + ( self.start // 4 )
        end_byte   = self._sequence.dna_file_location + ( self.end // 4 )

        # Now set the initial position; this is the base position we're
        # working in, which moves through the bytes in the range 2 bits at a
        # time.
        position = self.start

        # Bring various values into locals, simply to reduce the number of
        # attribute access calls in the loop below.
        start       = self.start
        end         = self.end
        masking     = self._sequence.reader.masking
        n_blocks    = self._sequence.n_blocks
        mask_blocks = self._sequence.mask_blocks

        # Now that we've figured all of the above out, let's load up enough
        # bytes to cover the range we're after.
        buffer = self._sequence.reader.read( ( end_byte - start_byte ) + 1, start_byte )

        # Where we'll build up the sequence.
        sequence = ""

        for byte in buffer:
            # For every bit-shift we'll be doing within the current byte...
            for shift in ( 6, 4, 2, 0 ):
                # If we're within the range we're interested in; don't
                # forget that we might be starting part way into the first
                # byte, and/or finishing part way through the end of the
                # final byte.
                if start <= position < end:
                    # If this position is within an N block, we just go with
                    # an N base.
                    if any( position in block for block in n_blocks ):
                        sequence += "N"
                    else:
                        # We're not looking at an N, so we decode the base
                        # instead.
                        base = BASES[ ( byte >> shift ) & 0b11 ]
                        # Handle masking if necessary.
                        if masking and any( position in block for block in mask_blocks ):
                            base = base.lower()
                        sequence += base

                # On to the next encoded base.
                position += 1

        # Having finished, let's turn the string of bases into a tuple of
        # individual bases.
        return tuple( sequence )

### bases.py ends here
