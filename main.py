#!/usr/bin/env python3
"""Main script for parsing prediction game data from xlsx files."""

from pathlib import Path

import click

from predictions.parser import export_to_arrow, export_to_csv, parse_all_years


@click.command()
@click.option(
    "--input-dir",
    "-i",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default="input",
    help="Directory containing xlsx files",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default="output/game_data.csv",
    help="Output CSV file path",
)
@click.option(
    "--arrow-output",
    "-a",
    type=click.Path(path_type=Path),
    default="predictions-frontend/public/game_data.arrow",
    help="Output Arrow file path for frontend",
)
def main(input_dir: Path, output: Path, arrow_output: Path):
    """Parse prediction game xlsx files and export to CSV and Arrow formats."""
    click.echo(f"Reading xlsx files from: {input_dir}")

    try:
        # Parse all years from the input directory
        game_data = parse_all_years(input_dir)

        # Report what was parsed
        click.echo(f"✓ Parsed {len(game_data.statements)} statements")
        click.echo(f"✓ Parsed {len(game_data.predictions)} predictions")
        click.echo(f"✓ Parsed {len(game_data.outcomes)} outcomes")

        # Create output directory if it doesn't exist
        output.parent.mkdir(parents=True, exist_ok=True)

        # Export to CSV
        export_to_csv(game_data, output)
        click.echo(f"✓ Exported data to: {output}")

        # Export to Arrow
        export_to_arrow(game_data, arrow_output)
        click.echo(f"✓ Exported data to: {arrow_output}")

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
