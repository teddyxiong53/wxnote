import sys
import gettext
import os.path

try:
    import wx
except ImportError as error:
    print error
    sys.exit(1)

__packagename__ = "wxnote"

# For package use
from .version import __version__
from .info import (
    __author__,
    __appname__,
    __contact__,
    __license__,
    __projecturl__,
    __licensefull__,
    __description__,
    __descriptionfull__,
)
gettext.install(__packagename__)

