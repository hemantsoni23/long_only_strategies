"""Run the current CSM Value regression tests.

The previous script encoded superseded timing, split-adjustment and accounting
assumptions. Historical versions are available in version control.
"""
from pathlib import Path
import sys
import unittest

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).parent / 'tests'))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
