"""twobe - A Python-based 2bit file reader library and viewer tool."""

######################################################################
# Main information.
__author__ = "Dave Pearson"
__copyright__ = "Copyright 2023-2024, Dave Pearson"
__credits__ = ["Dave Pearson"]
__maintainer__ = "Dave Pearson"
__email__ = "davep@davep.org"
__version__ = "0.0.2"
__licence__ = "GPLv3+"

##############################################################################
# Import things for easier access.
from .lib.bases import TwoBitBases
from .lib.file_reader import TwoBitFileReader
from .lib.reader import (
    InvalidSignature,
    InvalidVersion,
    TwoBitError,
    TwoBitReader,
    UnknownSequence,
)
from .lib.sequence import TwoBitSequence

##############################################################################
# Define what importing * means.
__all__ = [
    "TwoBitReader",
    "TwoBitError",
    "InvalidSignature",
    "InvalidVersion",
    "UnknownSequence",
    "TwoBitFileReader",
    "TwoBitSequence",
    "TwoBitBases",
]

### __init__.py ends here
