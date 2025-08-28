"""Top level package for catplist.

This project exposes a small CLI utility as well as a couple of helper
functions for working with Apple's binary plist files.  Historically the
package's ``__init__`` module was empty which meant ``from catplist import
catplist`` – the import style used throughout the tests and in the
documentation – failed with a ``ModuleNotFoundError``.  Exposing the CLI
and helper functions here makes importing behave as expected and mirrors
the behaviour of the original project.
"""

# Import the submodule so ``from catplist import catplist`` returns the module
# object (which itself exposes the ``catplist`` Click command).  This mirrors
# how the original project exposes its CLI entry point.
from . import catplist as catplist  # noqa: F401

# Re-export commonly used helpers at the package level for convenience.
from .catplist import BaseMetadataFile, read_ns_archiver, read_plist, unwrap

__all__ = ["catplist", "BaseMetadataFile", "read_ns_archiver", "read_plist", "unwrap"]
