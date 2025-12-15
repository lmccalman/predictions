"""Explore the structure of xlsx files in the input/ directory."""

import pandas as pd
from pathlib import Path


def explore_xlsx_file(filepath: Path) -> None:
    """Display structure and sample data from an xlsx file."""
    print(f"\n{'='*80}")
    print(f"FILE: {filepath.name}")
    print(f"{'='*80}")

    # Load the Excel file
    excel_file = pd.ExcelFile(filepath)

    print(f"\nSheets: {excel_file.sheet_names}")

    # Examine each sheet
    for sheet_name in excel_file.sheet_names:
        print(f"\n{'-'*80}")
        print(f"Sheet: {sheet_name}")
        print(f"{'-'*80}")

        df = pd.read_excel(filepath, sheet_name=sheet_name)

        print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
        print(f"\nColumns: {list(df.columns)}")

        print("\nFirst few rows:")
        print(df.head(10).to_string())

        print("\nData types:")
        print(df.dtypes.to_string())

        # Show some basic statistics
        print("\nBasic info:")
        print(f"  - Non-null counts per column:")
        for col in df.columns:
            non_null = df[col].notna().sum()
            print(f"    {col}: {non_null}/{len(df)}")


def main() -> None:
    """Explore all xlsx files in the input/ directory."""
    input_dir = Path("input")

    if not input_dir.exists():
        print(f"Error: {input_dir} directory not found")
        return

    xlsx_files = sorted(input_dir.glob("*.xlsx"))

    if not xlsx_files:
        print(f"No xlsx files found in {input_dir}")
        return

    print(f"Found {len(xlsx_files)} xlsx files")

    for filepath in xlsx_files:
        explore_xlsx_file(filepath)

    print(f"\n{'='*80}")
    print("Exploration complete!")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
