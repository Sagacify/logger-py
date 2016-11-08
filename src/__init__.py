"""
Logging configuration utils.

Contains saga formatter and function to create a logger.
"""
from .__about__ import (
    __author__, __copyright__, __email__, __license__, __summary__,
    __title__, __uri__, __version__
)
from .formatter import SagaFormatter
from .creator import get_logger

__all__ = [
    'SagaFormatter', 'get_logger', '__author__', '__copyright__', '__email__',
    '__license__', '__summary__', '__title__', '__uri__', '__version__']
