"""Create test fixture xlsx files for testing the parser."""

import pandas as pd
from pathlib import Path


def create_2022_format_fixture(output_path: Path) -> None:
    """Create a minimal 2022-2024 format xlsx file for testing.

    Structure:
    - Main sheet: ID, Prediction, Category, Proposer, Clarifications, Outcome, etc.
    - Individual sheets: ID, Prediction, Category, Probability, Rationale, [other participant columns]
    """
    # Main sheet with statements and outcomes
    main_data = pd.DataFrame({
        'ID': [1, 2, 3],
        'Prediction': [
            'Australia will win the Ashes',
            'Bitcoin will reach $100k',
            'Labor will win the election'
        ],
        'Category': ['Sport', 'Economics', 'Aus Politics'],
        'Proposer': ['Bruce', 'Gael', 'Christine'],
        'Clarifications': ['', 'By end of year', ''],
        'Outcome': [1.0, float('nan'), 0.0],  # 1=True, NaN=None, 0=False
        'Outcome comments': ['Won 3-2', '', 'Coalition won'],
        'Outcome supporting link': ['', '', '']
    })

    # Alice's predictions sheet
    alice_data = pd.DataFrame({
        'ID': [1, 2, 3],
        'Prediction': [
            'Australia will win the Ashes',
            'Bitcoin will reach $100k',
            'Labor will win the election'
        ],
        'Category': ['Sport', 'Economics', 'Aus Politics'],
        'Probability': [0.75, 0.3, 0.6],
        'Rationale': ['Strong team', 'Too volatile', 'Polls look good'],
        'Bruce': [0.0, -0.2, 0.1],  # Deltas vs other participants (not needed for parsing)
        'Gael': [0.1, 0.0, -0.05]
    })

    # Bruce's predictions sheet
    bruce_data = pd.DataFrame({
        'ID': [1, 2, 3],
        'Prediction': [
            'Australia will win the Ashes',
            'Bitcoin will reach $100k',
            'Labor will win the election'
        ],
        'Category': ['Sport', 'Economics', 'Aus Politics'],
        'Probability': [0.65, 0.5, 0.45],
        'Rationale': ['Good chance', 'Could go either way', 'Uncertain'],
        'Alice': [0.1, -0.2, 0.15],
        'Gael': [0.0, 0.0, 0.05]
    })

    # Gaël's predictions sheet (with accent)
    gael_data = pd.DataFrame({
        'ID': [1, 2, 3],
        'Prediction': [
            'Australia will win the Ashes',
            'Bitcoin will reach $100k',
            'Labor will win the election'
        ],
        'Category': ['Sport', 'Economics', 'Aus Politics'],
        'Probability': [0.55, 0.5, 0.5],
        'Rationale': ['Maybe', '50/50', 'No idea'],
        'Alice': [-0.2, -0.2, 0.1],
        'Bruce': [0.1, 0.0, -0.05]
    })

    # Summary sheet (should be ignored)
    summary_data = pd.DataFrame({
        'Participant': ['Alice', 'Bruce', 'Gaël'],
        'Score': [10.5, 8.3, 9.1],
        'Rank': [1, 3, 2]
    })

    # Write to Excel with multiple sheets
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        main_data.to_excel(writer, sheet_name='Main', index=False)
        alice_data.to_excel(writer, sheet_name='Alice', index=False)
        bruce_data.to_excel(writer, sheet_name='Bruce', index=False)
        gael_data.to_excel(writer, sheet_name='Gaël', index=False)
        summary_data.to_excel(writer, sheet_name='Summary', index=False)

    print(f"Created 2022 format fixture: {output_path}")


def create_2025_format_fixture(output_path: Path) -> None:
    """Create a minimal 2025 format xlsx file for testing.

    Structure:
    - Statements sheet: Number, Name (proposer), Prediction, Category, Outcome, [participant probability columns]
    - Individual sheets: Name (proposer), Prediction, Category, Probability (no ID!)
    """
    # Statements sheet with combined data
    statements_data = pd.DataFrame({
        'Number': [1, 2, 3],
        'Name': ['David', 'Alice', 'Bruce'],
        'Prediction': [
            'Trump will be re-elected',
            'AI will pass the Turing test',
            'Mars mission will launch'
        ],
        'Category': ['US Politics', 'Technology', 'Space'],
        'Outcome': [1, '-', 0],  # 1=True, "-"=None, 0=False
        'Alice': [0.8, 0.2, 0.3],
        'Bruce': [0.7, 0.4, 0.25],
        'David': [0.9, 0.1, 0.5],
        'Gaël': [0.75, 0.3, 0.4],
        # Analysis columns (should be ignored)
        'Analysis 1': ['', '', ''],
        'Analysis 2': [0, 0, 0]
    })

    # Alice's predictions sheet (simpler format, no ID)
    alice_data = pd.DataFrame({
        'Name': ['David', 'Alice', 'Bruce'],
        'Prediction': [
            'Trump will be re-elected',
            'AI will pass the Turing test',
            'Mars mission will launch'
        ],
        'Category': ['US Politics', 'Technology', 'Space'],
        'Probability': [0.8, 0.2, 0.3]
    })

    # Bruce's predictions sheet
    bruce_data = pd.DataFrame({
        'Name': ['David', 'Alice', 'Bruce'],
        'Prediction': [
            'Trump will be re-elected',
            'AI will pass the Turing test',
            'Mars mission will launch'
        ],
        'Category': ['US Politics', 'Technology', 'Space'],
        'Probability': [0.7, 0.4, 0.25]
    })

    # David's predictions sheet (new participant in 2025)
    david_data = pd.DataFrame({
        'Name': ['David', 'Alice', 'Bruce'],
        'Prediction': [
            'Trump will be re-elected',
            'AI will pass the Turing test',
            'Mars mission will launch'
        ],
        'Category': ['US Politics', 'Technology', 'Space'],
        'Probability': [0.9, 0.1, 0.5]
    })

    # Gaël's predictions sheet
    gael_data = pd.DataFrame({
        'Name': ['David', 'Alice', 'Bruce'],
        'Prediction': [
            'Trump will be re-elected',
            'AI will pass the Turing test',
            'Mars mission will launch'
        ],
        'Category': ['US Politics', 'Technology', 'Space'],
        'Probability': [0.75, 0.3, 0.4]
    })

    # Summary sheet (should be ignored)
    summary_data = pd.DataFrame({
        'Status': ['Resolved', 'Pending', 'Total'],
        'Count': [1, 2, 3]
    })

    # Write to Excel with multiple sheets
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        statements_data.to_excel(writer, sheet_name='Statements', index=False)
        alice_data.to_excel(writer, sheet_name='Alice', index=False)
        bruce_data.to_excel(writer, sheet_name='Bruce', index=False)
        david_data.to_excel(writer, sheet_name='David', index=False)
        gael_data.to_excel(writer, sheet_name='Gaël', index=False)
        summary_data.to_excel(writer, sheet_name='Summary', index=False)

    print(f"Created 2025 format fixture: {output_path}")


def main() -> None:
    """Create all test fixtures."""
    fixtures_dir = Path('tests/fixtures')
    fixtures_dir.mkdir(parents=True, exist_ok=True)

    create_2022_format_fixture(fixtures_dir / 'test_2022.xlsx')
    create_2025_format_fixture(fixtures_dir / 'test_2025.xlsx')

    print("\nAll fixtures created successfully!")


if __name__ == '__main__':
    main()
