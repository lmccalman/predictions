# Data Parser Implementation Plan

## Overview
Create a Python script to parse xlsx files from the `input/` directory and extract only the raw prediction data, ignoring all analysis and scoring. The parser must handle variations in spreadsheet structure across years (2022-2025).

## Data Structure Analysis

### 2022-2024 Structure
- **Main sheet**: Contains core statement data
  - Columns: ID, Prediction, Category, Proposer, Clarifications, Outcome, Outcome comments, Outcome supporting link
  - ~102 rows of statements
  - Outcomes: 0 = False, 1 = True, NaN = None (unresolved) → parsed as Optional[bool]
- **Individual sheets** (one per participant): Contains probabilities
  - Columns: ID, Prediction, Category, Probability (0.0 to 1.0), Rationale, [all participant names as columns]
  - Each participant has their own sheet with their probability in a dedicated column
- **Summary sheet**: Contains analysis/scoring → **IGNORE**
- **Scores sheet**: Contains progress tracking → **IGNORE**

### 2025 Structure
- **Statements sheet**: Combined statement and outcome data
  - Columns: Number, Name (proposer), Prediction, Category, Outcome, [participant probabilities], [analysis columns]
  - ~59 rows of statements
  - Outcome: 1 = True, 0 = False, "-" = None (unresolved) → parsed as Optional[bool]
- **Individual sheets** (one per participant): Simplified probability data
  - Columns: Name (proposer), Prediction, Category, Probability
  - Cleaner structure with just the essentials
- **Summary sheet**: Progress tracking only → **IGNORE**

### Key Differences Between Years
1. **Column naming**: "ID" (2022-2024) vs "Number" (2025)
2. **Proposer field**: "Proposer" (2022-2024) vs "Name" (2025)
3. **Outcome encoding**: Numeric only (2022-2024) vs numeric/string "-" (2025)
4. **Individual sheet structure**: Complex with all participants' deltas (2022-2024) vs simple with just own probability (2025)
5. **Participant names**: Vary by year (Bruce/Boof, Gael/Gaël, Christine/Chris, new participants David in 2025)

## Proposed Data Structure

### Python Data Model

```python
@dataclass
class Statement:
    """A prediction statement"""
    id: int  # Statement ID/number
    year: int  # Year of the prediction game
    text: str  # The prediction text
    category: str  # Category (e.g., "Aus Politics", "Sport")
    proposer: str  # Person who proposed this statement

@dataclass
class Prediction:
    """A person's probability assignment to a statement"""
    statement_id: int  # Reference to statement
    participant: str  # Name of person making prediction
    probability: float  # Probability assigned (0.0 to 1.0)

@dataclass
class Outcome:
    """The outcome of a prediction statement"""
    statement_id: int  # Reference to statement
    outcome: Optional[bool]  # True, False, or None if unresolved
    date: Optional[date]  # The date that the outcome was resolved

@dataclass
class GameData:
    """Complete data for all years"""
    statements: list[Statement]
    predictions: list[Prediction]
    outcomes: list[Outcome]
```


## Implementation Steps

### Phase 1: Test-Driven Development Setup

#### Step 1: Write comprehensive pytest tests (TDD approach)
**These tests will initially fail but should pass when the plan is complete.**

- [ ] Create test file `tests/test_xlsx_parser.py`
- [ ] Test statement extraction for each year format (2022-2024 vs 2025):
  - Test extraction of all fields (id, text, category, proposer)
  - Test correct year assignment
  - Test validation of duplicate IDs
- [ ] Test prediction extraction for each year format:
  - Test extraction from individual participant sheets
  - Test probability values are in valid range [0.0, 1.0]
  - Test statement_id references are valid
- [ ] Test outcome parsing for all formats:
  - 2022-2024: Test 0 → False, 1 → True, NaN → None
  - 2025: Test 0 → False, 1 → True, "-" → None
  - Test Optional[bool] datatype is correctly used
- [ ] Test participant name normalization:
  - Test handling of Boof/Bruce, Gael/Gaël variants
  - Test consistency across years
- [ ] Test multi-year aggregation:
  - Test parsing all xlsx files from input directory
  - Test merging into single GameData object
  - Test no duplicate statement IDs within same year
- [ ] Test JSON export/import round-trip:
  - Test dataclasses serialize correctly
  - Test data integrity after export/import
- [ ] Create test fixtures:
  - Sample xlsx files with known data for each year format
  - Expected output data structures
  - Edge cases (missing data, invalid formats)

### Phase 2: Data Extraction

#### Step 2: Create core parser module (`src/parser/xlsx_parser.py`)
- [ ] Define data classes (Statement, Prediction, Outcome, GameData)
- [ ] Create utility functions for:
  - Detecting year/structure from sheet names and columns
  - Normalizing participant names (handle Boof/Bruce, Gael/Gaël variants)
  - Parsing outcomes (handle 0/1/NaN/"-" variations to Optional[bool])
  - Validating probability values (0.0-1.0 range)

#### Step 3: Implement statement extraction
- [ ] Create `extract_statements_2022_2024(filepath, year)` function
  - Read "Main" sheet
  - Extract: ID, Prediction, Category, Proposer
  - Parse Outcome column (handle NaN → None for Optional[bool])
  - Validate: all required fields present, IDs are unique
- [ ] Create `extract_statements_2025(filepath, year)` function
  - Read "Statements" sheet
  - Extract: Number → id, Name → proposer, Prediction, Category
  - Parse Outcome column (handle "-" → None, 0 → False, 1 → True for Optional[bool])
  - Validate: all required fields present, IDs are unique

#### Step 4: Implement prediction extraction
- [ ] Create `extract_predictions_2022_2024(filepath, year)` function
  - For each participant sheet (exclude "Main", "Summary", "Scores"):
    - Extract participant name from sheet name
    - Read ID and Probability columns
    - Create Prediction objects for each row
  - Normalize participant names across years
  - Validate: probabilities in [0.0, 1.0], IDs match statements
- [ ] Create `extract_predictions_2025(filepath, year)` function
  - For each participant sheet (exclude "Statements", "Summary"):
    - Extract participant name from sheet name
    - Match predictions to statements by text (no ID in individual sheets)
    - Read Probability column
    - Create Prediction objects
  - Validate: probabilities in [0.0, 1.0], statement matching successful

#### Step 5: Implement year-agnostic parser
- [ ] Create `parse_xlsx_file(filepath)` function
  - Auto-detect structure (check for "Main" vs "Statements" sheet)
  - Route to appropriate extraction functions
  - Return GameData object for that year

#### Step 6: Implement multi-year aggregation
- [ ] Create `parse_all_years(input_dir)` function
  - Find all .xlsx files in directory
  - Parse each file
  - Merge into single GameData object
  - Validate: no duplicate statement IDs within same year
  - Handle: participants who didn't play in all years

### Phase 3: Data Validation & Quality

#### Step 7: Add comprehensive validation
- [ ] Statement validation:
  - No duplicate IDs within same year
  - All required fields present
  - Category values are consistent
  - Proposer names are normalized
- [ ] Prediction validation:
  - All statement IDs exist
  - All probabilities in valid range
  - No duplicate predictions (same person, same statement)
  - All participants made predictions for all statements in their year
- [ ] Cross-year validation:
  - Participant name consistency
  - Category name consistency

#### Step 8: Add data quality reporting
- [ ] Create `generate_summary_report(game_data)` function
  - Count statements per year
  - Count predictions per year
  - List participants per year
  - Report missing predictions (if any)
  - Report data quality issues

### Phase 4: Output & CLI

#### Step 9: Implement data export
- [ ] Create `export_to_json(game_data, output_path)` function
  - Convert dataclasses to JSON-serializable dicts
  - Write formatted JSON (indent=2 for readability)
  - Include metadata (export timestamp, parser version)

#### Step 10: Create CLI script (`main.py` or `parse_data.py`)
- [ ] Add command-line interface using Click:
  ```bash
  uv run python parse_data.py --input input/ --output data/predictions.json
  uv run python parse_data.py --input input/ --validate-only
  uv run python parse_data.py --input input/ --summary
  ```
- [ ] Options:
  - `--input`: Input directory (default: `input/`)
  - `--output`: Output JSON file (default: `data/predictions.json`)
  - `--validate-only`: Run validation without exporting
  - `--summary`: Print summary report
  - `--verbose`: Detailed logging

### Phase 5: Documentation

#### Step 11: Documentation
- [ ] Add docstrings to all functions
- [ ] Create README section on data parsing
- [ ] Document data structure and JSON format
- [ ] Add examples of common queries on parsed data

## Technical Considerations

### Dependencies
- `pandas`: Excel file reading and data manipulation
- `click`: CLI argument parsing
- `pathlib`: Cross-platform path handling
- Standard library: `dataclasses`, `json`, `typing`

### Error Handling
- Graceful handling of:
  - Missing files
  - Malformed Excel files
  - Missing expected sheets/columns
  - Invalid data types
  - Encoding issues with special characters (Gaël, etc.)

### Performance
- Parser should complete all 4 years in < 5 seconds
- Memory efficient: don't load all sheets simultaneously
- Consider caching parsed data if re-parsing is frequent

### Data Integrity
- **Critical**: Preserve exact prediction text (no normalization/cleaning)
- **Critical**: Preserve exact probability values (no rounding)
- **Critical**: Correctly map all predictions to statements
- Maintain participant name consistency within each year
- Handle missing data transparently (None/null)

## Known Data Quirks to Handle

1. **Participant name variations**:
   - Bruce vs Boof (appears to be same person)
   - Gaël vs Gael (encoding variations)
   - Christine vs Chris (likely same person)
   - New participants in 2025 (David)

2. **Column name variations**:
   - Different probability column headers across years
   - Unnamed columns with analysis data

3. **Outcome encoding**:
   - 2022-2024: 0 → False, 1 → True, NaN → None
   - 2025: 0 → False, 1 → True, "-" → None
   - Must use Optional[bool] datatype consistently: True, False, or None

4. **Statement matching in 2025**:
   - Individual sheets lack IDs
   - Must match by prediction text
   - Text must match exactly (whitespace, punctuation)

5. **Empty rows**:
   - Both formats have empty rows at end of sheets
   - Skip rows where ID/Number is NaN

## Success Criteria

- [ ] Parser successfully extracts all statements from all 4 years
- [ ] Parser successfully extracts all predictions from all 4 years
- [ ] No data loss: manual spot-check against original Excel files
- [ ] JSON output is valid and human-readable
- [ ] Validation catches malformed data
- [ ] CLI is user-friendly with helpful error messages
- [ ] Code is well-tested and documented
- [ ] Can re-run parser on updated Excel files without code changes

## Future Enhancements (Out of Scope for Initial Implementation)

- Support for additional metadata (clarifications, outcome comments, links)
- Database export (SQLite/PostgreSQL)
- Data anonymization for public sharing
- Incremental parsing (only parse changed files)
- Web API for querying parsed data
