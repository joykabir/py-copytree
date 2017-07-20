"""
Version
"""
import os
import sys

# pylint: disable=invalid-name

version = '0.0.1'

sys.modules['src'].__path__[0] = os.path.dirname(os.path.abspath(__file__))
