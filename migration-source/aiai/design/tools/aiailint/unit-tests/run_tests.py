#!/usr/bin/env python3
"""
Test runner for aiailint unit tests
"""

import unittest
import sys
from pathlib import Path

# Add src to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))


def run_all_tests():
    """Run all unit tests"""
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1


def run_specific_test(test_name):
    """Run a specific test"""
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    
    # Try to load the specific test
    try:
        suite = loader.loadTestsFromName(test_name)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return 0 if result.wasSuccessful() else 1
    except Exception as e:
        print(f"Error loading test '{test_name}': {e}")
        return 1


def list_available_tests():
    """List all available tests"""
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    print("Available tests:")
    for test in suite:
        if hasattr(test, '_tests'):
            for subtest in test._tests:
                if hasattr(subtest, '_tests'):
                    for case in subtest._tests:
                        print(f"  {case}")
                else:
                    print(f"  {subtest}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--list':
            list_available_tests()
        else:
            # Run specific test
            exit_code = run_specific_test(sys.argv[1])
            sys.exit(exit_code)
    else:
        # Run all tests
        exit_code = run_all_tests()
        sys.exit(exit_code) 