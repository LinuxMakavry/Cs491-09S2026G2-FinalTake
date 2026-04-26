# conftest.py — tells pytest to add the server/ directory to sys.path
# so that 'from app import create_app' resolves correctly in CI
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

"""
SOURCES / REFERENCES:
- pytest conftest.py documentation: root-level conftest for path configuration
  https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-files
- Python sys.path documentation
  https://docs.python.org/3/library/sys.html#sys.path
"""