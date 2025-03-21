"""
Package containing all tests for the package.

Modules:
    test_enums - tests all enumerations and functionality for enumerations.
    test_ingestion - tests the functionality of argument passing using default files.
    test_cli - tests the command line interface and the options that can be passed.
"""

__all__ = ["test_enums", "test_ingestion", "test_cli"]

from . import test_enums
from . import test_ingestion
from . import test_cli
