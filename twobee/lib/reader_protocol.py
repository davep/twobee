"""Provides a 2bit file reader protocol."""

##############################################################################
# Python imports.
from __future__        import annotations
from typing_extensions import Protocol

##############################################################################
class TwoBitReaderInterface( Protocol ):

    def read( self, size: int, position: int | None=None ) -> bytes:
        ...

### reader_protocol.py ends here
