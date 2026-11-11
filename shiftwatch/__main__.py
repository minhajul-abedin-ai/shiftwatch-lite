import argparse
import csv
import json
from .core import drift_report


def read_column(path, column):
    with open(path, newline='', encoding='utf-8') as f:
        rows = csv.DictReader(f)
        if column not in (rows.fieldnames or []):
            raise ValueError(f'Column {column!r} missing from {path}')
        return [float(row[column]) for row in rows]


def main():
    parser = argparse.ArgumentParser(description='Compare numeric CSV columns for distribution drift')
    parser.add_argument('reference_csv')
    parser.add_argument('current_csv')
    parser.add_argument('--column', required=True)
    parser.add_argument('--bins', type=int, default=10)
    args = parser.parse_args()
    print(json.dumps(drift_report(read_column(args.reference_csv,args.column),
                                  read_column(args.current_csv,args.column),args.bins), indent=2))

if __name__ == '__main__':
    main()
