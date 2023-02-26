"""twobe - A Python-based 2bit file reader library and viewer tool."""

######################################################################
# Main information.
__author__     = "Dave Pearson"
__copyright__  = "Copyright 2023, Dave Pearson"
__credits__    = [ "Dave Pearson" ]
__maintainer__ = "Dave Pearson"
__email__      = "davep@davep.org"
__version__    = "0.0.1"
__licence__    = "GPLv3+"

##############################################################################
# Import things for easier access.
from .lib.file_reader import TwoBitFileReader

##############################################################################
# Define what importing * means.
__all__ = [
    "TwoBitFileReader"
]

### __init__.py ends here
