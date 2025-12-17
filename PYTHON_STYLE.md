# Python Style Guide

This document defines the Python coding standards for this project, building on the global preferences and project-specific patterns.

## Core Principles

- **Clarity over cleverness**: Code should be self-documenting and immediately understandable
- **Functional over object-oriented**: Prefer simple functions and data structures over classes
- **YAGNI (You Ain't Gonna Need It)**: Implement only what's needed now
- **DRY (Don't Repeat Yourself)**: Reuse existing code where possible

## Code Structure

### Type Hints

Use type hints throughout:
- All function parameters and return types
- Use modern syntax: `list[str]` not `List[str]`
- Use `Optional[T]` for nullable types
- For complex types, use `from typing import` as needed

```python
def parse_outcome(value: Any) -> Optional[bool]:
    """Parse outcome value to Optional[bool]."""
    ...
```

### Data Structures

Prefer simple, immutable data structures:
- Use `@dataclass` for data containers
- Use `Enum` for fixed sets of values
- Use raw dictionaries/lists for transient data
- Avoid classes with methods unless necessary

```python
from dataclasses import dataclass
from enum import Enum

class SheetStructure(Enum):
    LEGACY = "legacy"
    CURRENT = "current"

@dataclass
class Statement:
    id: str
    year: int
    text: str
    category: str
    proposer: str
```

### Functions

- Small, focused functions with clear separation of concerns
- Descriptive names that indicate purpose
- Prefer multiple smaller functions over large monolithic ones
- Use functional patterns: map, filter, list comprehensions

```python
# Good: functional approach with list comprehension
statements = [create_statement(row, year) for row in rows]

# Avoid: imperative accumulation unless necessary
statements = []
for row in rows:
    statements.append(create_statement(row, year))
```

## Documentation

### Docstrings

Use docstrings for all public functions and classes:
- One-line summary for simple functions
- Multi-line format with Args/Returns/Raises for complex functions
- Use Australian spelling (visualisation, behaviour, etc.)

```python
def normalize_participant_name(name: str) -> str:
    """
    Normalise participant names to handle variations.

    Handles:
    - Bruce/Boof -> Bruce
    - Gaël/Gael/Gäel -> Gael
    - Christine/Chris -> Christine

    Args:
        name: The participant name to normalise

    Returns:
        The normalised participant name
    """
    ...
```

### Comments

- Write self-documenting code; use comments sparingly
- Only comment for non-obvious logic or business rules
- Prefer extracting complex logic to well-named functions

## Error Handling

Use asserts for fast, specific failures:
- Validate assumptions early
- Fail fast and explicitly
- Use `assert` for internal invariants
- Use `raise ValueError` for user input validation

```python
# Validate user input
if not (0.0 <= prob <= 1.0):
    raise ValueError(f"Probability must be in range [0.0, 1.0], got: {prob}")

# Internal invariants
assert len(statements) > 0, "Should have at least one statement"
```

## Configuration

Use configuration as code:
- Constants in a dedicated config module or at file top
- Use UPPER_CASE for module-level constants
- Import configuration globally

```python
# config.py
DEFAULT_PROBABILITY = 0.5
EXCLUDED_SHEETS = {"Main", "Summary", "Scores"}

# usage
from predictions.config import DEFAULT_PROBABILITY
```

## Tools and Formatting

- **ruff**: Automatic formatting (run before commits)
- **basedpyright**: Type checking and linting
- **pytest**: Unit tests
- Use `uv` for dependency management

Run checks:
```bash
uv run ruff format .
uv run ruff check .
uv run basedpyright
uv run pytest
```

## Australian Spelling

Use Australian spelling in:
- Comments
- Docstrings
- User-facing strings
- Variable names where appropriate

Examples: visualisation, normalise, behaviour, colour, centre

## Import Organisation

Group imports in order:
1. Standard library
2. Third-party packages
3. Local modules

Use absolute imports for project modules.

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd
import openpyxl

from predictions.validation import validate_probability
```
