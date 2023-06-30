import os
import sys
import json
import math
import locale
import subprocess

from .info import __appname__
from .version import __version__



def get_locale_file():
    DIR_NAME = "locale"

    SEARCH_DIRS = [
        os.path.join(os.path.dirname(__file__), DIR_NAME),
    ]

    for directory in SEARCH_DIRS:
        if os.path.isdir(directory):
            return directory

    return None