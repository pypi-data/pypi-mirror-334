from typing import *
import logging
from random import *

from .config import langs, langCodes

DEBUG = True
log = logging.getLogger(__name__)


def getLang(lang):
    result = lang
    result = result if result in langs else 'fr'
    return result
def getLangCode(lang):
    return langCodes[getLang(lang)]