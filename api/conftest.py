"""Make the `app` package importable when running pytest from the api/ directory.

Lets you run:  cd api && pytest tests/test_functional.py -v
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
