import argparse
import csv
import json
import math
from .core import drift_report


def read_column(path, column):
    """Read a finite numeric CSV column, including UTF-8 BOM-encoded files."""
    with open(path, newline='', encoding='utf-8-sig') as f:
        rows = csv.DictReader(f)
        if column not in (rows.fieldnames or []):
            raise ValueError(f'Column {column!r} missing from {path}')
        values = []
        for line_number, row in enumerate(rows, start=2):
            raw = row.get(column)
            if raw is None or not raw.strip():
                raise ValueError(f'Missing value in {column!r} at {path}:{line_number}')
            try:
                value = float(raw)
            except ValueError as exc:
                raise ValueError(
                    f'Non-numeric value in {column!r} at {path}:{line_number}: {raw!r}'
                ) from exc
            if not math.isfinite(value):
                raise ValueError(f'Non-finite value in {column!r} at {path}:{line_number}')
            values.append(value)
        return values


def main():
    parser = argparse.ArgumentParser(description='Compare numeric CSV columns for distribution drift')
    parser.add_argument('reference_csv')
    parser.add_argument('current_csv')
    parser.add_argument('--column', required=True)
    parser.add_argument('--bins', type=int, default=10)
    args = parser.parse_args()
    try:
        report = drift_report(
            read_column(args.reference_csv, args.column),
            read_column(args.current_csv, args.column),
            args.bins,
        )
    except (OSError, ValueError, csv.Error) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
