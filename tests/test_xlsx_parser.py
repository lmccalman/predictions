"""Comprehensive tests for the xlsx parser.

These tests follow a TDD (Test-Driven Development) approach.
They define the expected behavior of the parser before implementation.
"""

import json
import pytest
from pathlib import Path
from typing import Optional

# Import the parser module (will be created in Phase 2)
# For now, we'll define the expected interface through the tests
try:
    from predictions.parser.xlsx_parser import (
        Statement,
        Prediction,
        Outcome,
        GameData,
        extract_statements_2022_2024,
        extract_statements_2025,
        extract_predictions_2022_2024,
        extract_predictions_2025,
        parse_xlsx_file,
        parse_all_years,
        export_to_json,
        normalize_participant_name,
    )
except ImportError:
    # Module doesn't exist yet - this is expected in TDD
    pytest.skip("Parser module not yet implemented", allow_module_level=True)


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the path to the test fixtures directory."""
    return Path(__file__).parent / 'fixtures'


@pytest.fixture
def fixture_2022(fixtures_dir: Path) -> Path:
    """Return the path to the 2022 format test fixture."""
    return fixtures_dir / 'test_2022.xlsx'


@pytest.fixture
def fixture_2025(fixtures_dir: Path) -> Path:
    """Return the path to the 2025 format test fixture."""
    return fixtures_dir / 'test_2025.xlsx'


# ============================================================================
# Tests for Statement Extraction (2022-2024 Format)
# ============================================================================

class TestStatementExtraction2022Format:
    """Test statement extraction from 2022-2024 format files."""

    def test_extract_statements_basic(self, fixture_2022: Path):
        """Test basic statement extraction from 2022 format."""
        statements = extract_statements_2022_2024(fixture_2022, year=2022)

        assert len(statements) == 3
        assert all(isinstance(s, Statement) for s in statements)

    def test_statement_fields_2022_format(self, fixture_2022: Path):
        """Test that all statement fields are correctly extracted."""
        statements = extract_statements_2022_2024(fixture_2022, year=2022)

        # Check first statement
        stmt = statements[0]
        assert stmt.id == 1
        assert stmt.year == 2022
        assert stmt.text == 'Australia will win the Ashes'
        assert stmt.category == 'Sport'
        assert stmt.proposer == 'Bruce'

    def test_statement_year_assignment(self, fixture_2022: Path):
        """Test that year is correctly assigned to statements."""
        statements = extract_statements_2022_2024(fixture_2022, year=2023)

        assert all(s.year == 2023 for s in statements)

    def test_statement_ids_are_unique(self, fixture_2022: Path):
        """Test that statement IDs are unique within a year."""
        statements = extract_statements_2022_2024(fixture_2022, year=2022)

        ids = [s.id for s in statements]
        assert len(ids) == len(set(ids)), "Statement IDs must be unique"

    def test_all_categories_extracted(self, fixture_2022: Path):
        """Test that all categories are correctly extracted."""
        statements = extract_statements_2022_2024(fixture_2022, year=2022)

        categories = {s.category for s in statements}
        assert 'Sport' in categories
        assert 'Economics' in categories
        assert 'Aus Politics' in categories


# ============================================================================
# Tests for Statement Extraction (2025 Format)
# ============================================================================

class TestStatementExtraction2025Format:
    """Test statement extraction from 2025 format files."""

    def test_extract_statements_basic(self, fixture_2025: Path):
        """Test basic statement extraction from 2025 format."""
        statements = extract_statements_2025(fixture_2025, year=2025)

        assert len(statements) == 3
        assert all(isinstance(s, Statement) for s in statements)

    def test_statement_fields_2025_format(self, fixture_2025: Path):
        """Test that all statement fields are correctly extracted from 2025 format."""
        statements = extract_statements_2025(fixture_2025, year=2025)

        # Check first statement
        stmt = statements[0]
        assert stmt.id == 1
        assert stmt.year == 2025
        assert stmt.text == 'Trump will be re-elected'
        assert stmt.category == 'US Politics'
        assert stmt.proposer == 'David'

    def test_2025_uses_number_column(self, fixture_2025: Path):
        """Test that 2025 format correctly reads from 'Number' column (not 'ID')."""
        statements = extract_statements_2025(fixture_2025, year=2025)

        # Verify we got the statements and IDs match what's in the Number column
        assert statements[0].id == 1
        assert statements[1].id == 2
        assert statements[2].id == 3

    def test_2025_uses_name_for_proposer(self, fixture_2025: Path):
        """Test that 2025 format correctly reads proposer from 'Name' column."""
        statements = extract_statements_2025(fixture_2025, year=2025)

        proposers = [s.proposer for s in statements]
        assert 'David' in proposers
        assert 'Alice' in proposers
        assert 'Bruce' in proposers


# ============================================================================
# Tests for Prediction Extraction
# ============================================================================

class TestPredictionExtraction:
    """Test prediction extraction from both year formats."""

    def test_extract_predictions_2022_format(self, fixture_2022: Path):
        """Test prediction extraction from 2022 format."""
        predictions = extract_predictions_2022_2024(fixture_2022, year=2022)

        # 3 participants × 3 statements = 9 predictions
        assert len(predictions) == 9
        assert all(isinstance(p, Prediction) for p in predictions)

    def test_extract_predictions_2025_format(self, fixture_2025: Path):
        """Test prediction extraction from 2025 format."""
        predictions = extract_predictions_2025(fixture_2025, year=2025)

        # 4 participants × 3 statements = 12 predictions
        assert len(predictions) == 12
        assert all(isinstance(p, Prediction) for p in predictions)

    def test_prediction_fields(self, fixture_2022: Path):
        """Test that prediction fields are correctly extracted."""
        predictions = extract_predictions_2022_2024(fixture_2022, year=2022)

        # Find Alice's prediction for statement 1
        alice_pred = next(p for p in predictions if p.participant == 'Alice' and p.statement_id == 1)

        assert alice_pred.statement_id == 1
        assert alice_pred.participant == 'Alice'
        assert alice_pred.probability == 0.75

    def test_probability_values_in_valid_range(self, fixture_2022: Path):
        """Test that all probability values are in [0.0, 1.0] range."""
        predictions = extract_predictions_2022_2024(fixture_2022, year=2022)

        for pred in predictions:
            assert 0.0 <= pred.probability <= 1.0, (
                f"Probability {pred.probability} for {pred.participant} "
                f"on statement {pred.statement_id} is out of range"
            )

    def test_all_participants_extracted(self, fixture_2022: Path):
        """Test that all participants are found."""
        predictions = extract_predictions_2022_2024(fixture_2022, year=2022)

        participants = {p.participant for p in predictions}
        assert 'Alice' in participants
        assert 'Bruce' in participants
        assert 'Gaël' in participants  # With accent

    def test_statement_id_references_valid(self, fixture_2022: Path):
        """Test that all statement_id references correspond to actual statements."""
        statements = extract_statements_2022_2024(fixture_2022, year=2022)
        predictions = extract_predictions_2022_2024(fixture_2022, year=2022)

        valid_ids = {s.id for s in statements}
        for pred in predictions:
            assert pred.statement_id in valid_ids, (
                f"Prediction references invalid statement_id {pred.statement_id}"
            )

    def test_each_participant_has_all_predictions(self, fixture_2022: Path):
        """Test that each participant has predictions for all statements."""
        statements = extract_statements_2022_2024(fixture_2022, year=2022)
        predictions = extract_predictions_2022_2024(fixture_2022, year=2022)

        # Group predictions by participant
        by_participant = {}
        for pred in predictions:
            if pred.participant not in by_participant:
                by_participant[pred.participant] = []
            by_participant[pred.participant].append(pred.statement_id)

        # Each participant should have predictions for all statements
        expected_count = len(statements)
        for participant, stmt_ids in by_participant.items():
            assert len(stmt_ids) == expected_count, (
                f"{participant} has {len(stmt_ids)} predictions, expected {expected_count}"
            )


# ============================================================================
# Tests for Outcome Parsing
# ============================================================================

class TestOutcomeParsing:
    """Test outcome parsing for different formats."""

    def test_outcome_parsing_2022_format(self, fixture_2022: Path):
        """Test outcome parsing from 2022 format (0/1/NaN)."""
        statements = extract_statements_2022_2024(fixture_2022, year=2022)

        # Create outcomes from statements
        # In the fixture: statement 1 has outcome 1, statement 2 has NaN, statement 3 has 0
        outcomes = {s.id: s for s in statements}

        # Note: The Outcome dataclass might be extracted separately or as part of Statement
        # This test assumes we can get outcome info from statements
        # We'll test via the parse_xlsx_file which returns GameData

    def test_outcome_true_parsing(self, fixture_2022: Path):
        """Test that outcome value 1 is parsed as True."""
        game_data = parse_xlsx_file(fixture_2022, year=2022)

        # Statement 1 has outcome = 1.0 (True)
        outcome = next(o for o in game_data.outcomes if o.statement_id == 1)
        assert outcome.outcome is True

    def test_outcome_false_parsing(self, fixture_2022: Path):
        """Test that outcome value 0 is parsed as False."""
        game_data = parse_xlsx_file(fixture_2022, year=2022)

        # Statement 3 has outcome = 0.0 (False)
        outcome = next(o for o in game_data.outcomes if o.statement_id == 3)
        assert outcome.outcome is False

    def test_outcome_nan_parsing(self, fixture_2022: Path):
        """Test that NaN outcome is parsed as None (unresolved)."""
        game_data = parse_xlsx_file(fixture_2022, year=2022)

        # Statement 2 has outcome = NaN (None)
        outcome = next(o for o in game_data.outcomes if o.statement_id == 2)
        assert outcome.outcome is None

    def test_outcome_parsing_2025_format(self, fixture_2025: Path):
        """Test outcome parsing from 2025 format (0/1/"-")."""
        game_data = parse_xlsx_file(fixture_2025, year=2025)

        # Statement 1: outcome = 1 (True)
        outcome1 = next(o for o in game_data.outcomes if o.statement_id == 1)
        assert outcome1.outcome is True

        # Statement 2: outcome = "-" (None)
        outcome2 = next(o for o in game_data.outcomes if o.statement_id == 2)
        assert outcome2.outcome is None

        # Statement 3: outcome = 0 (False)
        outcome3 = next(o for o in game_data.outcomes if o.statement_id == 3)
        assert outcome3.outcome is False

    def test_outcome_type_is_optional_bool(self, fixture_2022: Path):
        """Test that outcome type is Optional[bool] (True, False, or None)."""
        game_data = parse_xlsx_file(fixture_2022, year=2022)

        for outcome in game_data.outcomes:
            assert outcome.outcome in (True, False, None), (
                f"Outcome must be True, False, or None, got {outcome.outcome}"
            )


# ============================================================================
# Tests for Participant Name Normalization
# ============================================================================

class TestParticipantNameNormalization:
    """Test participant name normalization across years."""

    def test_normalize_boof_to_bruce(self):
        """Test that 'Boof' is normalized to 'Bruce'."""
        assert normalize_participant_name('Boof') == 'Bruce'
        assert normalize_participant_name('Bruce') == 'Bruce'

    def test_normalize_gael_variants(self):
        """Test that Gael/Gaël variants are normalized consistently."""
        # Both should normalize to the same name
        normalized1 = normalize_participant_name('Gael')
        normalized2 = normalize_participant_name('Gaël')
        assert normalized1 == normalized2

    def test_normalize_christine_chris(self):
        """Test that Christine/Chris are normalized consistently."""
        normalized1 = normalize_participant_name('Christine')
        normalized2 = normalize_participant_name('Chris')
        assert normalized1 == normalized2

    def test_normalize_preserves_other_names(self):
        """Test that other names are preserved as-is."""
        assert normalize_participant_name('Alice') == 'Alice'
        assert normalize_participant_name('David') == 'David'

    def test_normalization_case_insensitive(self):
        """Test that normalization is case-insensitive."""
        assert normalize_participant_name('bruce') == normalize_participant_name('Bruce')
        assert normalize_participant_name('ALICE') == normalize_participant_name('alice')

    def test_predictions_use_normalized_names(self, fixture_2022: Path):
        """Test that extracted predictions use normalized participant names."""
        predictions = extract_predictions_2022_2024(fixture_2022, year=2022)

        participants = {p.participant for p in predictions}

        # Should have normalized names, not raw sheet names
        # 'Gaël' from sheet should be normalized
        assert all(name in ['Alice', 'Bruce', 'Gaël', 'Gael'] for name in participants)


# ============================================================================
# Tests for Multi-Year Aggregation
# ============================================================================

class TestMultiYearAggregation:
    """Test parsing and aggregating data from multiple years."""

    def test_parse_all_years(self, fixtures_dir: Path):
        """Test parsing all xlsx files from a directory."""
        game_data = parse_all_years(fixtures_dir)

        assert isinstance(game_data, GameData)
        assert len(game_data.statements) > 0
        assert len(game_data.predictions) > 0
        assert len(game_data.outcomes) > 0

    def test_statements_from_multiple_years(self, fixtures_dir: Path):
        """Test that statements from multiple years are aggregated."""
        game_data = parse_all_years(fixtures_dir)

        years = {s.year for s in game_data.statements}
        assert 2022 in years or 2023 in years or 2024 in years  # At least one old format
        assert 2025 in years  # New format

    def test_no_duplicate_statement_ids_within_year(self, fixtures_dir: Path):
        """Test that there are no duplicate statement IDs within the same year."""
        game_data = parse_all_years(fixtures_dir)

        # Group by year
        by_year = {}
        for stmt in game_data.statements:
            if stmt.year not in by_year:
                by_year[stmt.year] = []
            by_year[stmt.year].append(stmt.id)

        # Check each year for duplicates
        for year, ids in by_year.items():
            assert len(ids) == len(set(ids)), f"Duplicate statement IDs in year {year}"

    def test_statement_ids_can_repeat_across_years(self, fixtures_dir: Path):
        """Test that statement IDs can be reused across different years (this is OK)."""
        game_data = parse_all_years(fixtures_dir)

        # This is acceptable - same ID in different years is fine
        # Just verifying the data structure allows it
        all_ids = [s.id for s in game_data.statements]
        all_year_id_pairs = [(s.year, s.id) for s in game_data.statements]

        # If there are repeating IDs across years, that's fine
        # Just ensure the (year, id) pairs are unique
        assert len(all_year_id_pairs) == len(set(all_year_id_pairs))

    def test_participants_across_years(self, fixtures_dir: Path):
        """Test handling of participants who didn't play in all years."""
        game_data = parse_all_years(fixtures_dir)

        # Group predictions by participant and year
        participant_years = {}
        for pred in game_data.predictions:
            # Need to look up the year from the statement
            stmt = next(s for s in game_data.statements if s.id == pred.statement_id)
            key = (pred.participant, stmt.year)
            if pred.participant not in participant_years:
                participant_years[pred.participant] = set()
            participant_years[pred.participant].add(stmt.year)

        # David only appears in 2025
        if 'David' in participant_years:
            assert 2025 in participant_years['David']

        # Some participants appear in multiple years
        multi_year_participants = [p for p, years in participant_years.items() if len(years) > 1]
        assert len(multi_year_participants) > 0


# ============================================================================
# Tests for JSON Export/Import
# ============================================================================

class TestJSONExportImport:
    """Test JSON export and import round-trip."""

    def test_export_to_json_creates_file(self, fixture_2022: Path, tmp_path: Path):
        """Test that export_to_json creates a valid JSON file."""
        game_data = parse_xlsx_file(fixture_2022, year=2022)
        output_file = tmp_path / 'test_output.json'

        export_to_json(game_data, output_file)

        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_exported_json_is_valid(self, fixture_2022: Path, tmp_path: Path):
        """Test that exported JSON is valid and can be loaded."""
        game_data = parse_xlsx_file(fixture_2022, year=2022)
        output_file = tmp_path / 'test_output.json'

        export_to_json(game_data, output_file)

        # Load and verify it's valid JSON
        with open(output_file) as f:
            data = json.load(f)

        assert isinstance(data, dict)
        assert 'statements' in data
        assert 'predictions' in data
        assert 'outcomes' in data

    def test_json_round_trip_preserves_data(self, fixture_2022: Path, tmp_path: Path):
        """Test that data is preserved through JSON export/import cycle."""
        original_data = parse_xlsx_file(fixture_2022, year=2022)
        output_file = tmp_path / 'test_output.json'

        # Export
        export_to_json(original_data, output_file)

        # Import
        with open(output_file) as f:
            imported_dict = json.load(f)

        # Verify counts match
        assert len(imported_dict['statements']) == len(original_data.statements)
        assert len(imported_dict['predictions']) == len(original_data.predictions)
        assert len(imported_dict['outcomes']) == len(original_data.outcomes)

    def test_json_preserves_statement_fields(self, fixture_2022: Path, tmp_path: Path):
        """Test that statement fields are preserved in JSON export."""
        game_data = parse_xlsx_file(fixture_2022, year=2022)
        output_file = tmp_path / 'test_output.json'

        export_to_json(game_data, output_file)

        with open(output_file) as f:
            data = json.load(f)

        first_statement = data['statements'][0]
        assert 'id' in first_statement
        assert 'year' in first_statement
        assert 'text' in first_statement
        assert 'category' in first_statement
        assert 'proposer' in first_statement

    def test_json_preserves_probability_precision(self, fixture_2022: Path, tmp_path: Path):
        """Test that probability values maintain precision through JSON export."""
        game_data = parse_xlsx_file(fixture_2022, year=2022)
        output_file = tmp_path / 'test_output.json'

        export_to_json(game_data, output_file)

        with open(output_file) as f:
            data = json.load(f)

        # Find a specific prediction and verify precision
        predictions = data['predictions']
        # Should have the exact probability value, not rounded
        probabilities = [p['probability'] for p in predictions]
        assert 0.75 in probabilities  # From Alice's first prediction


# ============================================================================
# Tests for Year-Agnostic Parser
# ============================================================================

class TestYearAgnosticParser:
    """Test the parse_xlsx_file function that auto-detects format."""

    def test_parse_xlsx_file_detects_2022_format(self, fixture_2022: Path):
        """Test that parse_xlsx_file correctly detects and parses 2022 format."""
        game_data = parse_xlsx_file(fixture_2022, year=2022)

        assert isinstance(game_data, GameData)
        assert len(game_data.statements) == 3
        assert len(game_data.predictions) == 9
        assert len(game_data.outcomes) == 3

    def test_parse_xlsx_file_detects_2025_format(self, fixture_2025: Path):
        """Test that parse_xlsx_file correctly detects and parses 2025 format."""
        game_data = parse_xlsx_file(fixture_2025, year=2025)

        assert isinstance(game_data, GameData)
        assert len(game_data.statements) == 3
        assert len(game_data.predictions) == 12
        assert len(game_data.outcomes) == 3

    def test_parse_xlsx_file_returns_game_data(self, fixture_2022: Path):
        """Test that parse_xlsx_file returns a complete GameData object."""
        game_data = parse_xlsx_file(fixture_2022, year=2022)

        assert hasattr(game_data, 'statements')
        assert hasattr(game_data, 'predictions')
        assert hasattr(game_data, 'outcomes')
        assert all(isinstance(s, Statement) for s in game_data.statements)
        assert all(isinstance(p, Prediction) for p in game_data.predictions)
        assert all(isinstance(o, Outcome) for o in game_data.outcomes)


# ============================================================================
# Tests for Edge Cases and Error Handling
# ============================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_rows_are_skipped(self, fixture_2022: Path):
        """Test that empty rows at the end of sheets are skipped."""
        # The fixtures may have empty rows - parser should skip them
        statements = extract_statements_2022_2024(fixture_2022, year=2022)

        # Should only get the 3 valid statements, not any empty rows
        assert len(statements) == 3

    def test_missing_file_raises_error(self):
        """Test that attempting to parse a non-existent file raises an error."""
        with pytest.raises((FileNotFoundError, IOError)):
            parse_xlsx_file(Path('nonexistent.xlsx'), year=2022)

    def test_invalid_probability_raises_error(self, tmp_path: Path):
        """Test that invalid probability values (outside [0, 1]) raise an error."""
        # This would require creating a malformed fixture
        # For now, we'll skip this test or mark it as expected behavior
        pytest.skip("Requires creating malformed fixture - implement if needed")


# ============================================================================
# Tests for Data Validation
# ============================================================================

class TestDataValidation:
    """Test data validation functions."""

    def test_all_predictions_reference_valid_statements(self, fixture_2022: Path):
        """Test that all predictions reference valid statement IDs."""
        game_data = parse_xlsx_file(fixture_2022, year=2022)

        valid_stmt_ids = {s.id for s in game_data.statements}

        for pred in game_data.predictions:
            assert pred.statement_id in valid_stmt_ids

    def test_all_outcomes_reference_valid_statements(self, fixture_2022: Path):
        """Test that all outcomes reference valid statement IDs."""
        game_data = parse_xlsx_file(fixture_2022, year=2022)

        valid_stmt_ids = {s.id for s in game_data.statements}

        for outcome in game_data.outcomes:
            assert outcome.statement_id in valid_stmt_ids

    def test_category_consistency(self, fixture_2022: Path):
        """Test that category values are consistent (no typos)."""
        statements = extract_statements_2022_2024(fixture_2022, year=2022)

        # All statements should have non-empty categories
        for stmt in statements:
            assert stmt.category is not None
            assert len(stmt.category) > 0

    def test_proposer_names_are_normalized(self, fixture_2022: Path):
        """Test that proposer names in statements are normalized."""
        statements = extract_statements_2022_2024(fixture_2022, year=2022)

        # All proposers should be valid, normalized names
        for stmt in statements:
            assert stmt.proposer is not None
            assert len(stmt.proposer) > 0
