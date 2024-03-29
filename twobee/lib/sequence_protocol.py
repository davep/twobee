"""Provides a 2bit sequence protocol."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from typing_extensions import Protocol

##############################################################################
# Local imports.
from .block import TwoBitBlock
from .reader_protocol import TwoBitReaderInterface


##############################################################################
class TwoBitSequenceInterface(Protocol):
    """Interface of a 2bit sequence."""

    reader: TwoBitReaderInterface
    n_blocks: tuple[TwoBitBlock, ...]
    mask_blocks: tuple[TwoBitBlock, ...]

    # pylint: disable=missing-docstring

    @property
    def name(self) -> str:
        ...

    @property
    def dna_file_location(self) -> int:
        ...

    @property
    def dna_size(self) -> int:
        ...

    def mask_blocks_intersecting(self, start: int, end: int) -> tuple[TwoBitBlock, ...]:
        ...


### reader_protocol.py ends here
