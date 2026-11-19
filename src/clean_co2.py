from pathlib import Path
import sys

import pandas as pd


EU27 = [
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
]

COLUMNS = ["country", "iso_code", "year", "population", "co2", "co2_per_capita"]
VALUE_COLUMNS = ["population", "co2", "co2_per_capita"]


def clean_co2(raw_path: Path, output_path: Path) -> pd.DataFrame:
    data = pd.read_csv(raw_path)

    data = data.loc[data["country"].isin(EU27)].copy()
    print(f"Rows after EU27 country filter: {len(data)}")

    data = data.loc[(data["year"] >= 2000) & (data["year"] <= 2024)].copy()
    print(f"Rows after year filter (2000-2024): {len(data)}")

    missing_counts = data[VALUE_COLUMNS].isna().sum()
    if missing_counts.any():
        counts = ", ".join(
            f"{column}={missing_counts[column]}" for column in VALUE_COLUMNS
        )
        total = int(missing_counts.sum())
        print(f"Missing values: {counts}; total={total}")
        raise ValueError(
            f"Missing values found in filtered data ({counts}; total={total}); "
            "no values were filled or dropped"
        )

    data = data.loc[:, COLUMNS]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)
    return data


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent
    raw_path = project_root / "data" / "raw" / "owid-co2-data.csv"
    output_path = project_root / "data" / "processed" / "co2_eu.csv"

    try:
        clean_co2(raw_path, output_path)
    except (OSError, KeyError, ValueError, pd.errors.ParserError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
