import argparse
from pathlib import Path
from typing import Dict

import pandas as pd


def clean_dataframe(df: pd.DataFrame, drop_duplicates: bool = True) -> pd.DataFrame:
    """Apply basic cleanup to a DataFrame."""
    cleaned = df.copy()
    cleaned = cleaned.dropna(how="all")
    cleaned = cleaned.dropna(axis=1, how="all")
    cleaned.columns = [str(col).strip() for col in cleaned.columns]
    if drop_duplicates:
        cleaned = cleaned.drop_duplicates()
    return cleaned


def process_excel_file(
    file_path: Path,
    output_dir: Path,
    drop_duplicates: bool = True,
    encoding: str = "utf-8-sig",
) -> Dict[str, Path]:
    """Read all sheets from one Excel file and export as CSV files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    workbook_name = file_path.stem
    sheet_map = pd.read_excel(file_path, sheet_name=None)
    outputs: Dict[str, Path] = {}

    for sheet_name, df in sheet_map.items():
        cleaned_df = clean_dataframe(df, drop_duplicates=drop_duplicates)
        safe_sheet_name = "".join(ch if ch.isalnum() or ch in ("_", "-") else "_" for ch in str(sheet_name))
        out_path = output_dir / f"{workbook_name}__{safe_sheet_name}.csv"
        cleaned_df.to_csv(out_path, index=False, encoding=encoding)
        outputs[str(sheet_name)] = out_path

    return outputs


def collect_excel_files(input_dir: Path) -> list[Path]:
    """Collect all Excel files from a directory."""
    files = []
    for ext in ("*.xlsx", "*.xls"):
        files.extend(input_dir.glob(ext))
    return sorted(files)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Batch process Excel files in datafiles directory.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory containing Excel files. Default: current datafiles directory.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "excel_output",
        help="Directory to save converted CSV files.",
    )
    parser.add_argument(
        "--keep-duplicates",
        action="store_true",
        help="Keep duplicate rows (default removes duplicates).",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    input_dir: Path = args.input_dir
    output_dir: Path = args.output_dir

    if not input_dir.exists() or not input_dir.is_dir():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    excel_files = collect_excel_files(input_dir)
    if not excel_files:
        print(f"No .xlsx or .xls files found in: {input_dir}")
        return

    print(f"Found {len(excel_files)} Excel file(s).")
    for excel_file in excel_files:
        print(f"\nProcessing: {excel_file.name}")
        exported = process_excel_file(
            excel_file,
            output_dir=output_dir,
            drop_duplicates=not args.keep_duplicates,
        )
        for sheet, out_file in exported.items():
            print(f"  - Sheet '{sheet}' -> {out_file}")

    print(f"\nDone. Output directory: {output_dir}")


if __name__ == "__main__":
    main()
