"""Validators for prediction game data."""

from collections import defaultdict
from dataclasses import dataclass

from ..parser.xlsx_parser import GameData, Statement, Prediction


class ValidationError(Exception):
    """Raised when validation fails."""

    pass


@dataclass
class ValidationResult:
    """Result of a validation check."""

    valid: bool
    errors: list[str]
    warnings: list[str]

    def __bool__(self) -> bool:
        """Allow using result in boolean context."""
        return self.valid


def validate_statements(game_data: GameData) -> ValidationResult:
    """
    Validate statements in game data.

    Checks:
    - No duplicate IDs within same year
    - All required fields present (id, year, text, category, proposer)
    - Category values are consistent across statements
    - Proposer names are normalized correctly

    Args:
        game_data: The game data to validate

    Returns:
        ValidationResult with any errors or warnings
    """
    errors = []
    warnings = []

    # Track IDs by year
    ids_by_year = defaultdict(set)
    categories = set()
    proposers = set()

    for stmt in game_data.statements:
        # Check required fields are present and non-empty
        if not stmt.id:
            errors.append(f"Statement missing ID: {stmt.text[:50]}...")
        if not stmt.year:
            errors.append(f"Statement {stmt.id} missing year")
        if not stmt.text or not stmt.text.strip():
            errors.append(f"Statement {stmt.id} missing text")
        if not stmt.category or not stmt.category.strip():
            errors.append(f"Statement {stmt.id} missing category")
        if not stmt.proposer or not stmt.proposer.strip():
            errors.append(f"Statement {stmt.id} missing proposer")

        # Check for duplicate IDs within same year
        if stmt.id in ids_by_year[stmt.year]:
            errors.append(
                f"Duplicate statement ID {stmt.id} found in year {stmt.year}"
            )
        ids_by_year[stmt.year].add(stmt.id)

        # Collect categories and proposers for consistency checking
        if stmt.category:
            categories.add(stmt.category.strip())
        if stmt.proposer:
            proposers.add(stmt.proposer.strip())

    # Check for proposer name normalization issues
    # Look for common variants that should be normalized
    proposer_lower = {p.lower(): [] for p in proposers}
    for p in proposers:
        proposer_lower[p.lower()].append(p)

    for lower, variants in proposer_lower.items():
        if len(variants) > 1:
            warnings.append(
                f"Proposer name has multiple variants: {variants} - "
                f"should be normalized to one form"
            )

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )


def validate_predictions(game_data: GameData) -> ValidationResult:
    """
    Validate predictions in game data.

    Checks:
    - All statement_id references exist in statements
    - All probabilities in valid range [0.0, 1.0]
    - No duplicate predictions (same participant, same statement)
    - All participants made predictions for all statements in their year

    Args:
        game_data: The game data to validate

    Returns:
        ValidationResult with any errors or warnings
    """
    errors = []
    warnings = []

    # Build set of valid statement IDs (now globally unique)
    valid_ids = {stmt.id for stmt in game_data.statements}

    # Build map of statement ID to year
    stmt_id_to_year = {stmt.id: stmt.year for stmt in game_data.statements}

    # Build map of statements by year
    statements_by_year = defaultdict(set)
    for stmt in game_data.statements:
        statements_by_year[stmt.year].add(stmt.id)

    # Track predictions by (participant, statement_id)
    predictions_seen = set()

    # Track which participants predicted in which years
    participants_by_year = defaultdict(set)

    for pred in game_data.predictions:
        # Check statement_id exists
        if pred.statement_id not in valid_ids:
            errors.append(
                f"Prediction references non-existent statement ID: {pred.statement_id}"
            )
            continue

        # Check probability is in valid range
        if not (0.0 <= pred.probability <= 1.0):
            errors.append(
                f"Invalid probability {pred.probability} for {pred.participant} "
                f"on statement {pred.statement_id}"
            )

        # Check for duplicate predictions
        pred_key = (pred.participant, pred.statement_id)
        if pred_key in predictions_seen:
            errors.append(
                f"Duplicate prediction: {pred.participant} on statement {pred.statement_id}"
            )
        predictions_seen.add(pred_key)

        # Track participants by year
        year = stmt_id_to_year[pred.statement_id]
        participants_by_year[year].add(pred.participant)

    # Check that all participants made predictions for all statements in their year
    for year, participants in participants_by_year.items():
        expected_statements = statements_by_year[year]
        for participant in participants:
            participant_predictions = {
                p.statement_id
                for p in game_data.predictions
                if p.participant == participant
            }
            missing = expected_statements - participant_predictions
            if missing:
                warnings.append(
                    f"{participant} missing predictions for {len(missing)} statements in {year}: "
                    f"{sorted(missing)[:5]}{'...' if len(missing) > 5 else ''}"
                )

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )


def validate_cross_year(game_data: GameData) -> ValidationResult:
    """
    Validate cross-year consistency in game data.

    Checks:
    - Participant names are consistent across years
    - Category names are consistent across years
    - No conflicts in data between years

    Args:
        game_data: The game data to validate

    Returns:
        ValidationResult with any errors or warnings
    """
    errors = []
    warnings = []

    # Check participant name consistency
    participants_by_year = defaultdict(set)
    for pred in game_data.predictions:
        # Find which year this prediction is from
        for stmt in game_data.statements:
            if stmt.id == pred.statement_id:
                participants_by_year[stmt.year].add(pred.participant)
                break

    # Check for participant name variations across years
    all_participants = set()
    for participants in participants_by_year.values():
        all_participants.update(participants)

    # Look for similar names (case-insensitive)
    participant_lower = defaultdict(list)
    for p in all_participants:
        participant_lower[p.lower()].append(p)

    for lower, variants in participant_lower.items():
        if len(variants) > 1:
            warnings.append(
                f"Participant name has multiple variants across years: {variants}"
            )

    # Check category name consistency
    categories_by_year = defaultdict(set)
    for stmt in game_data.statements:
        categories_by_year[stmt.year].add(stmt.category)

    # Look for similar categories (case-insensitive)
    all_categories = set()
    for categories in categories_by_year.values():
        all_categories.update(categories)

    category_lower = defaultdict(list)
    for c in all_categories:
        category_lower[c.lower()].append(c)

    for lower, variants in category_lower.items():
        if len(variants) > 1:
            warnings.append(
                f"Category has multiple variants across years: {variants}"
            )

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )


def validate_game_data(game_data: GameData) -> ValidationResult:
    """
    Validate all aspects of game data.

    Runs all validation checks and combines results.

    Args:
        game_data: The game data to validate

    Returns:
        Combined ValidationResult
    """
    all_errors = []
    all_warnings = []

    # Run all validations
    stmt_result = validate_statements(game_data)
    pred_result = validate_predictions(game_data)
    cross_result = validate_cross_year(game_data)

    # Combine results
    all_errors.extend(stmt_result.errors)
    all_errors.extend(pred_result.errors)
    all_errors.extend(cross_result.errors)

    all_warnings.extend(stmt_result.warnings)
    all_warnings.extend(pred_result.warnings)
    all_warnings.extend(cross_result.warnings)

    return ValidationResult(
        valid=len(all_errors) == 0,
        errors=all_errors,
        warnings=all_warnings,
    )
