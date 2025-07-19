# filepath: c:\TRABAJO\_TI-Informatica\Empresas\T-Systems\netbox-test\run_tests.py
#!/usr/bin/env python3
"""
Test runner for the NetBox API client project.

This script discovers and runs all tests in the project directory.
To run:
    python run_tests.py
"""

import unittest
import sys
import os


def run_tests():
    """Discover and run all tests in the project."""
    # Initialize the test loader
    loader = unittest.TestLoader()
    
    # Discover all tests in the current directory
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern="test_*.py")
    
    # Initialize the test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run the tests
    result = runner.run(suite)
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())