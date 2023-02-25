"""Provides a 2bit file reader protocol."""

##############################################################################
# Python imports.
from __future__        import annotations
from typing_extensions import Protocol

##############################################################################
class TwoBitReaderInterface( Protocol ):

    @property
    def masking( self ) -> bool:
        ...

    def goto( self, position: int ) -> None:
        ...

    def position( self ) -> int:
        ...

    def read( self, size: int, position: int | None=None ) -> bytes:
        ...

    def read_long( self ) -> int:
        ...

    def read_long_array( self, count: int ) -> tuple[ int, ... ]:
        ...

### reader_protocol.py ends here
