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

Current status: Data ingestion complete, frontend development in progress. Raw data in xlsx spreadsheets (`input/` directory, 2022-2025) is parsed into both CSV and Apache Arrow formats for analysis and the web frontend.

## Technology Stack

### Backend (Python)

- **uv**: Environment management
- **pytest**: Unit tests
- **ruff**: Automatic formatting
- **basedpyright**: Linting and static analysis
- **click**: Command-line argument processing
- **pandas/openpyxl**: Excel file parsing
- **pyarrow**: Apache Arrow format export

### Frontend (JavaScript/Svelte)

- **Vite**: Build tool and dev server
- **Svelte 5**: UI framework
- **Observable Plot**: Data visualisation
- **arquero**: Data manipulation and querying (loads Apache Arrow files)
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
uv run python main.py              # Run main script (exports to CSV and Arrow)
uv run python main.py -o output/custom.csv -a frontend/custom.arrow  # Custom output paths
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

# Data encryption (after exporting Arrow data)
npm run encrypt "password"   # Encrypts public/game_data.arrow → public/game_data.encrypted
```

## Architecture

### Data Ingestion (Backend)

Located in `predictions/parser/`, the ingestion component reads xlsx files from `input/` directory and extracts:
1. **Statements**: True/false statements with categories, proposers, and IDs
2. **Predictions**: Probabilities (0.0-1.0) assigned by each family member
3. **Outcomes**: Actual results (True/False/Unresolved) for each statement

The parser handles multiple xlsx formats (2022-2024 legacy format and 2025+ current format) and exports to both CSV and Apache Arrow formats. Both exports use a denormalized structure where each row represents a statement with its outcome and all participants' predictions as columns.

Key files:
- `predictions/parser/xlsx_parser.py`: Main parsing logic (includes `export_to_csv` and `export_to_arrow` functions)
- `main.py`: CLI entry point for parsing

Output Structure (both CSV and Arrow):
- Base columns: id, year, text, category, proposer, outcome, outcome_date
- Participant columns: One column per participant containing their probability prediction
- CSV output: `output/game_data.csv`
- Arrow output: `predictions-frontend/public/game_data.arrow` (Feather V2 format, compatible with arquero)

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
- **arquero**: Data manipulation library for loading and querying Apache Arrow data
- **Tailwind CSS v4**: Utility-first styling (use Tailwind classes, not CSS properties)

The frontend consumes Apache Arrow data from the backend parser (via arquero) and provides interactive visualisations for:
- Player performance over time
- Category analysis
- Comparative statistics
- Confidence calibration

Key structure:
- `src/App.svelte`: Main application component
- `src/lib/`: Reusable Svelte components and shared stores
- `src/views/`: Tab view components
- `src/utils/`: JavaScript utility functions
- `public/game_data.encrypted`: Encrypted Arrow data file (decrypted client-side)

#### Password Protection and Data Encryption

The frontend uses client-side encryption to protect game data even when publicly hosted.

**Authentication flow**:
1. User enters password in `PasswordGate.svelte`
2. Password is verified against stored PBKDF2 hash (`authStore.svelte.js`)
3. On success, password is used to decrypt the Arrow data (`gameDataStore.svelte.js`)
4. Decrypted data is loaded into arquero for the app to use

**Key files**:
- `src/lib/authStore.svelte.js`: Password verification and storage (password kept in memory only)
- `src/lib/PasswordGate.svelte`: Login UI component
- `src/utils/crypto.js`: AES-GCM decryption using Web Crypto API
- `encrypt-data.js`: Node.js script to encrypt Arrow file at build time
- `generate-password-hash.html`: Browser tool to generate password hash for authStore

**Setting up a new password**:
1. Open `generate-password-hash.html` in a browser
2. Enter the password and copy the generated salt/hash
3. Update `PASSWORD_HASH` in `src/lib/authStore.svelte.js`
4. Run `npm run encrypt "password"` to encrypt the data file

**Technical details**:
- Encryption: AES-256-GCM (authenticated encryption)
- Key derivation: PBKDF2 with SHA-256, 100,000 iterations
- File format: 16-byte salt + 12-byte IV + ciphertext (includes 16-byte auth tag)

#### Data Loading Architecture

**Store**: `src/lib/gameDataStore.svelte.js`
- Exports `loadData(password)` function to fetch and decrypt data
- Exports: `gameData` (arquero table), `years` (sorted array), `dataReady` (promise)
- Exports player configuration: `players` array and `playerColors` array
- Data is loaded after successful password verification in PasswordGate

**Usage Pattern in Components**:
```javascript
import { dataReady, gameData, years, players, playerColors } from '../lib/gameDataStore.svelte.js'

let loading = $state(true)
let error = $state(null)

// Wait for data to be ready (already decrypted by PasswordGate)
$effect(() => {
  dataReady.then(() => {
    loading = false
  }).catch(e => {
    error = e.message
    loading = false
  })
})

// Use gameData and years directly after loading
// const filtered = gameData.filter(...)
```

#### Utility Functions

**Scoring**: `src/utils/scoring.js`
- `calculateScore(prediction, outcome)`: Core scoring formula, returns `log(p_assigned) - log(0.5)`
- `calculateTotalScore(rows, player)`: Sum scores for a player across an array of statement rows
- `formatScore(score)`: Format score for display with +/- sign (e.g., "+1.23", "-0.45")
- `formatProbability(value)`: Format probability as percentage (e.g., "75%")
