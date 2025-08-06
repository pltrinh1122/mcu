# Unit Tests for AIAI Design Tools

This directory contains unit tests for the tools in `aiai/design/tools/`.

## Structure

Each tool has its own self-contained test directory:

```
unit-tests/
├── script2manual/
│   ├── test_script2manual.py      # Main test file
│   ├── test_data/                 # Test input files
│   │   ├── sample_aiaiScript.yaml
│   │   ├── complex_aiaiScript.yaml
│   │   └── invalid_aiaiScript.yaml
│   └── test_outputs/              # Expected output files
│       └── expected_sample_manual.md
└── README.md                      # This file
```

## Running Tests

### Run all tests
```bash
cd aiai/design/tools/unit-tests/
python3 -m unittest discover -v
```

### Run specific tool tests
```bash
cd aiai/design/tools/unit-tests/script2manual/
python3 test_script2manual.py
```

### Run with coverage
```bash
cd aiai/design/tools/unit-tests/
python3 -m coverage run -m unittest discover
python3 -m coverage report
```

## Test Data

### Sample aiaiScript (`sample_aiaiScript.yaml`)
- Basic script with commands and validations
- Includes phase metadata
- Tests core functionality

### Complex aiaiScript (`complex_aiaiScript.yaml`)
- Nested script structure
- Conditional elements
- Multiple script types
- Tests advanced features

### Invalid aiaiScript (`invalid_aiaiScript.yaml`)
- Missing required fields
- Unknown element types
- Malformed structure
- Tests error handling

## Test Coverage

### script2manual.py Tests
- **File Loading**: Valid/invalid directories, YAML parsing
- **Phase Extraction**: Phase metadata detection and parsing
- **Command Extraction**: Simple and nested script structures
- **Content Generation**: Manual output format and structure
- **Error Handling**: Invalid inputs, missing fields, unknown types
- **Edge Cases**: Empty directories, malformed YAML, large files

## Adding New Tests

1. **Create test data**: Add sample files to `test_data/`
2. **Add test cases**: Extend the test class with new methods
3. **Update expected outputs**: Add expected results to `test_outputs/`
4. **Run tests**: Verify all tests pass

## Best Practices

- **Self-contained**: Each test should be independent
- **Realistic data**: Use realistic aiaiScript examples
- **Edge cases**: Test error conditions and boundary cases
- **Clear naming**: Use descriptive test method names
- **Documentation**: Comment complex test scenarios 