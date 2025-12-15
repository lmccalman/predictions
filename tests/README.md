# Test Suite for Predictions Parser

## Overview

This directory contains comprehensive tests for the xlsx parser following a **Test-Driven Development (TDD)** approach. The tests were written *before* the implementation to define the expected behavior of the parser.

## Current Status

**Tests are currently SKIPPED** because the parser module (`predictions.parser.xlsx_parser`) has not been implemented yet. This is expected and intentional.

Once the parser implementation begins (Phase 2), these tests will:
1. Initially **FAIL** (as expected in TDD)
2. Gradually **PASS** as functionality is implemented
3. Provide confidence that the implementation meets requirements

## Test Structure

### Test Files

- `test_xlsx_parser.py` - Comprehensive test suite covering all parser functionality
- `create_fixtures.py` - Script to generate test fixture files
- `fixtures/` - Directory containing sample xlsx test files

### Test Fixtures

Two test fixture files are provided to represent the different year formats:

1. **test_2022.xlsx** - Represents 2022-2024 format
   - Main sheet with statements
   - Individual participant sheets
   - 3 participants: Alice, Bruce, Gaël
   - 3 statements with varied outcomes

2. **test_2025.xlsx** - Represents 2025 format
   - Statements sheet (combined format)
   - Individual participant sheets (simplified)
   - 4 participants: Alice, Bruce, David, Gaël
   - 3 statements with varied outcomes

### Test Coverage

The test suite covers all requirements from Phase 1 of the parser implementation plan:

#### Statement Extraction
- ✓ Extract statements from 2022-2024 format (Main sheet)
- ✓ Extract statements from 2025 format (Statements sheet)
- ✓ Handle column naming differences (ID vs Number, Proposer vs Name)
- ✓ Validate unique IDs within each year
- ✓ Correct year assignment

#### Prediction Extraction
- ✓ Extract predictions from 2022-2024 format (individual sheets)
- ✓ Extract predictions from 2025 format (individual sheets)
- ✓ Validate probability values in range [0.0, 1.0]
- ✓ Ensure all statement_id references are valid
- ✓ Verify each participant has predictions for all statements

#### Outcome Parsing
- ✓ Parse 2022-2024 format: 0 → False, 1 → True, NaN → None
- ✓ Parse 2025 format: 0 → False, 1 → True, "-" → None
- ✓ Use Optional[bool] type consistently

#### Participant Name Normalization
- ✓ Normalize Boof/Bruce
- ✓ Normalize Gael/Gaël variants
- ✓ Normalize Christine/Chris
- ✓ Case-insensitive normalization
- ✓ Preserve other names as-is

#### Multi-Year Aggregation
- ✓ Parse multiple xlsx files from directory
- ✓ Merge into single GameData object
- ✓ No duplicate statement IDs within same year
- ✓ Handle participants who didn't play in all years

#### JSON Export/Import
- ✓ Export to JSON format
- ✓ Valid JSON structure
- ✓ Round-trip data preservation
- ✓ Preserve field precision (especially probabilities)

#### Data Validation
- ✓ All predictions reference valid statements
- ✓ All outcomes reference valid statements
- ✓ Category consistency
- ✓ Proposer name normalization

## Running the Tests

### Current State (Before Implementation)
```bash
# Tests will be skipped
uv run pytest tests/test_xlsx_parser.py -v
```

Expected output:
```
============================== 1 skipped in 0.03s ==============================
```

### After Implementation Begins
```bash
# Run all tests
uv run pytest tests/test_xlsx_parser.py -v

# Run specific test class
uv run pytest tests/test_xlsx_parser.py::TestStatementExtraction2022Format -v

# Run specific test
uv run pytest tests/test_xlsx_parser.py::TestStatementExtraction2022Format::test_extract_statements_basic -v

# Run with output
uv run pytest tests/test_xlsx_parser.py -v -s
```

## Expected Test Progression

As the parser is implemented, tests should pass in this general order:

1. **Phase 2a: Statement Extraction**
   - TestStatementExtraction2022Format
   - TestStatementExtraction2025Format

2. **Phase 2b: Prediction Extraction**
   - TestPredictionExtraction

3. **Phase 2c: Outcome Parsing**
   - TestOutcomeParsing

4. **Phase 2d: Name Normalization**
   - TestParticipantNameNormalization

5. **Phase 2e: Integration**
   - TestYearAgnosticParser
   - TestMultiYearAggregation

6. **Phase 2f: Export**
   - TestJSONExportImport

7. **Phase 2g: Validation**
   - TestDataValidation
   - TestEdgeCases

## Regenerating Fixtures

If test fixtures need to be regenerated:

```bash
uv run python tests/create_fixtures.py
```

This will recreate:
- `tests/fixtures/test_2022.xlsx`
- `tests/fixtures/test_2025.xlsx`

## Next Steps

1. Implement `predictions/parser/xlsx_parser.py` module with:
   - Data classes (Statement, Prediction, Outcome, GameData)
   - Extraction functions
   - Normalization functions
   - Export functions

2. Run tests and fix failures iteratively

3. Add additional edge case tests as needed during implementation

4. Ensure all tests pass before moving to next phase

## Notes

- Tests use pytest fixtures for file paths
- Tests are organized by functionality in classes
- Each test is independent and can run in any order
- Test fixtures are minimal but cover all critical cases
- Tests follow TDD principles: written before implementation
