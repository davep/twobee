##############################################################################
# Python imports.
from dataclasses import dataclass

##############################################################################
@dataclass
class TwoBitBlock:
    """Holds the details of a block in a 2bit file."""

    start: int
    """The start location of the block (inclusive)."""
    end: int
    """The end location of the block (exclusive)."""
    size: int
    """The size of the block."""

    def __contains__( self, position: int ) -> bool:
        return self.start <= position < self.end

### block.py ends here
