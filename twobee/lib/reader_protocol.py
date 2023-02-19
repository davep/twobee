"""Provides a 2bit file reader protocol."""

##############################################################################
# Python imports.
from typing_extensions import Protocol

##############################################################################
class TwoBitReaderInterface( Protocol ):

    def read( self, size: int ) -> bytes:
        ...

### reader_protocol.py ends here
