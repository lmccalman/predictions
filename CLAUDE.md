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

Current status: Data ingestion complete, frontend development in progress. Raw data in xlsx spreadsheets (`input/` directory, 2022-2025) is parsed into CSV format for analysis and the web frontend.

## Technology Stack

### Backend (Python)

- **uv**: Environment management
- **pytest**: Unit tests
- **ruff**: Automatic formatting
- **basedpyright**: Linting and static analysis
- **click**: Command-line argument processing
- **pandas/openpyxl**: Excel file parsing

### Frontend (JavaScript/Svelte)

- **Vite**: Build tool and dev server
- **Svelte 5**: UI framework
- **Observable Plot**: Data visualisation
- **Tailwind CSS**: Styling (v4)

## Coding Style

See style guides for detailed coding standards:
- **[PYTHON_STYLE.md](PYTHON_STYLE.md)**: Python coding standards
- **[JAVASCRIPT_STYLE.md](JAVASCRIPT_STYLE.md)**: JavaScript/Svelte coding standards

## Common Commands

### Backend Setup and Development

```bash
# Environment setup
uv sync              # Install dependencies
uv sync --dev        # Install with dev dependencies

# Running the application
uv run python main.py              # Run main script
uv run python -m predictions       # Run as module (when structured)

# Development tools
uv run ruff format .               # Format code
uv run ruff check .                # Lint code
uv run basedpyright                # Type checking
uv run pytest                      # Run all tests
uv run pytest path/to/test.py      # Run single test file
uv run pytest -k test_name         # Run specific test by name
```

### Frontend Development

```bash
cd predictions-frontend

# Install dependencies
npm install

# Development
npm run dev          # Start dev server (usually http://localhost:5173)
npm run build        # Build for production
npm run preview      # Preview production build
```

## Architecture

### Data Ingestion (Backend)

Located in `predictions/parser/`, the ingestion component reads xlsx files from `input/` directory and extracts:
1. **Statements**: True/false statements with categories, proposers, and IDs
2. **Predictions**: Probabilities (0.0-1.0) assigned by each family member
3. **Outcomes**: Actual results (True/False/Unresolved) for each statement

The parser handles multiple xlsx formats (2022-2024 legacy format and 2025+ current format) and exports to a denormalized CSV file where each row represents a statement with its outcome and all participants' predictions as columns.

Key files:
- `predictions/parser/xlsx_parser.py`: Main parsing logic
- `main.py`: CLI entry point for parsing

CSV Output Structure:
- Base columns: id, year, text, category, proposer, outcome, outcome_date
- Participant columns: One column per participant containing their probability prediction

### Scoring Algorithm

- Uses standardized log probability
- Formula: log(probability assigned to actual outcome) - log(0.5)
- Prior assumed to be 0.5 for all statements
- Scores update as events resolve throughout the year
- Final resolution on Christmas Eve

### Web Frontend

Located in `predictions-frontend/`, the frontend is built with:
- **Vite + Svelte 5**: Fast, reactive UI framework
- **Observable Plot**: Declarative data visualisation library for charts and graphs
- **Tailwind CSS v4**: Utility-first styling (use Tailwind classes, not CSS properties)

The frontend consumes CSV data from the backend parser and provides interactive visualisations for:
- Player performance over time
- Category analysis
- Comparative statistics
- Confidence calibration

Key structure:
- `src/App.svelte`: Main application component
- `src/lib/`: Reusable Svelte components
- `src/utils/`: JavaScript utility functions (future)
- Public data served from backend CSV output
