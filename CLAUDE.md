# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a family prediction game analyzer and publisher. Each year, family members propose true/false statements that can be evaluated by December 24th. Members assign probabilities to all statements, and scoring uses standardized log probability (log of probability mass assigned to actual outcome minus log of prior 0.5).

The goal is to create an interactive website for exploring game progress and statistics, including:
- Performance over time for individuals
- Performance on different categories
- Confidence levels of different people
- Comparative analyses between players
- Performance on own predictions vs. others' predictions

Current status: Initial planning phases. Raw data is in xlsx spreadsheets in `input/` directory (2022-2025) that need ingestion into consistent data format.

## Technology Stack

- **uv**: Environment management
- **pytest**: Unit tests
- **ruff**: Automatic formatting
- **basedpyright**: Linting and static analysis
- **click**: Command-line argument processing

## Common Commands

### Environment Setup
```bash
uv sync              # Install dependencies
uv sync --dev        # Install with dev dependencies
```

### Running the Application
```bash
uv run python main.py              # Run main script
uv run python -m predictions       # Run as module (when structured)
```

### Development Tools
```bash
uv run ruff format .               # Format code
uv run ruff check .                # Lint code
uv run basedpyright                # Type checking
uv run pytest                      # Run all tests
uv run pytest path/to/test.py      # Run single test file
uv run pytest -k test_name         # Run specific test by name
```

## Architecture

### Data Ingestion (Current Focus)

The ingestion component is a Python script that reads xlsx files from `input/` directory and extracts:
1. Questions (true/false statements with categories)
2. Predictions (probabilities assigned by each family member)
3. Results (actual outcomes resolved by judging date)

Output: Consistent data format suitable for web hosting and interactive analysis

### Scoring Algorithm

- Uses standardized log probability
- Formula: log(probability assigned to actual outcome) - log(0.5)
- Prior assumed to be 0.5 for all statements
- Scores update as events resolve throughout the year
- Final resolution on Christmas Eve

### Web Frontend (Future)

Technology not yet decided. Will host interactive analyses and statistics for family access.
