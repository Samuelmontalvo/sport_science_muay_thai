from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd


DEFAULT_INPUT = Path("data/processed/force_plate_metrics.csv")
DEFAULT_OUTPUT = Path("outputs/reports/qc_report.md")

RANGE_CHECKS = {
    "jump_height_cm": (0.0, 100.0),
    "peak_force_n": (0.0, 8000.0),
    "impulse_n_s": (0.0, 2000.0),
    "rfd_n_s": (0.0, 200000.0),
    "peak_power_w": (0.0, 20000.0),
    "body_mass_kg": (30.0, 200.0),
}

REQUIRED_COLUMNS = ["athlete_id", "timepoint", "test_type"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run basic QC checks on processed force-plate data."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Path to processed data file (.csv or .parquet).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path to QC report (markdown).",
    )
    return parser.parse_args()


def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    suffix = path.suffix.lower()
    if suffix in {".parquet", ".pq"}:
        return pd.read_parquet(path)
    if suffix in {".csv", ".txt"}:
        return pd.read_csv(path)
    raise ValueError(f"Unsupported file type: {suffix}")


def qc_missingness(df: pd.DataFrame) -> pd.Series:
    return df.isna().mean().sort_values(ascending=False)


def qc_duplicates(df: pd.DataFrame) -> int:
    return int(df.duplicated().sum())


def qc_range_checks(df: pd.DataFrame) -> dict[str, int]:
    out_of_range = {}
    for col, (min_val, max_val) in RANGE_CHECKS.items():
        if col not in df.columns:
            continue
        series = pd.to_numeric(df[col], errors="coerce")
        out_of_range[col] = int(((series < min_val) | (series > max_val)).sum())
    return out_of_range


def qc_required_columns(df: pd.DataFrame) -> list[str]:
    return [col for col in REQUIRED_COLUMNS if col not in df.columns]


def qc_timepoints(df: pd.DataFrame) -> dict[str, int]:
    if "timepoint" not in df.columns:
        return {}
    allowed = {"T0", "T1", 0, 1}
    return {
        "invalid_timepoint": int(~df["timepoint"].isin(allowed)).sum(),
    }


def write_report(
    output_path: Path,
    df: pd.DataFrame,
    missingness: pd.Series,
    duplicate_count: int,
    range_checks: dict[str, int],
    missing_columns: list[str],
    timepoint_flags: dict[str, int],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# QC report: {output_path.stem}",
        "",
        f"- Generated: {datetime.utcnow().isoformat()}Z",
        f"- Rows: {len(df):,}",
        f"- Columns: {len(df.columns):,}",
        f"- Duplicate rows: {duplicate_count:,}",
        "",
    ]

    if missing_columns:
        lines.append("## Missing required columns")
        lines.append(", ".join(missing_columns))
        lines.append("")

    lines.append("## Missingness (top 15)")
    lines.append("column | percent_missing")
    lines.append("--- | ---")
    for col, pct in missingness.head(15).items():
        lines.append(f"{col} | {pct:.3%}")
    lines.append("")

    if range_checks:
        lines.append("## Range checks")
        lines.append("metric | out_of_range_count")
        lines.append("--- | ---")
        for col, count in range_checks.items():
            lines.append(f"{col} | {count}")
        lines.append("")

    if timepoint_flags:
        lines.append("## Timepoint checks")
        for key, count in timepoint_flags.items():
            lines.append(f"- {key}: {count}")
        lines.append("")

    output_path.write_text("\n".join(lines))


def main() -> None:
    args = parse_args()
    df = load_data(args.input)
    missingness = qc_missingness(df)
    duplicate_count = qc_duplicates(df)
    range_checks = qc_range_checks(df)
    missing_columns = qc_required_columns(df)
    timepoint_flags = qc_timepoints(df)
    write_report(
        args.output,
        df,
        missingness,
        duplicate_count,
        range_checks,
        missing_columns,
        timepoint_flags,
    )


if __name__ == "__main__":
    main()
