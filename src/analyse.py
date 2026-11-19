from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd

from clean_co2 import EU27


START_YEAR = 2000
END_YEAR = 2024


def load_comparison_data(input_path: Path) -> pd.DataFrame:
    data = pd.read_csv(input_path)
    required_columns = {"country", "year", "co2_per_capita"}
    missing_columns = required_columns.difference(data.columns)
    if missing_columns:
        raise ValueError(
            "The cleaned dataset is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    comparison = data.loc[
        data["country"].isin(EU27) & data["year"].isin([START_YEAR, END_YEAR]),
        ["country", "year", "co2_per_capita"],
    ].copy()
    print(f"Rows after EU27 and comparison-year filter: {len(comparison)}")

    issues = []
    for country in EU27:
        for year in (START_YEAR, END_YEAR):
            rows = comparison.loc[
                (comparison["country"] == country) & (comparison["year"] == year),
                "co2_per_capita",
            ]
            if rows.empty:
                issues.append(f"{country} ({year}: comparison value is missing)")
            elif len(rows) > 1:
                issues.append(f"{country} ({year}: multiple comparison rows found)")
            elif pd.isna(rows.iloc[0]):
                issues.append(f"{country} ({year}: co2_per_capita is missing)")

    if issues:
        details = "\n".join(f" - {issue}" for issue in issues)
        raise ValueError(
            "Missing or invalid comparison-year data; no values were filled or "
            f"dropped:\n{details}"
        )

    return comparison.pivot(
        index="country",
        columns="year",
        values="co2_per_capita",
    ).loc[:, [START_YEAR, END_YEAR]]


def print_ranking(
    title: str,
    ranking: pd.DataFrame,
    reduction_column: str,
    reduction_label: str,
    reduction_precision: int,
) -> None:
    print(f"\n{title}")
    if ranking.empty:
        print("No countries qualify for this ranking.")
        return

    for position, row in enumerate(ranking.itertuples(index=False), start=1):
        reduction = f"{row.reduction:.{reduction_precision}f}"
        if reduction_column == "percentage_reduction":
            reduction_text = f"{reduction}%"
        else:
            reduction_text = f"{reduction} tonnes CO2 per person"
        print(
            f"{position}. {row.country}: "
            f"2000 = {row.value_2000:.3f} tonnes CO2 per person; "
            f"2024 = {row.value_2024:.3f} tonnes CO2 per person; "
            f"{reduction_label} = {reduction_text}"
        )


def save_chart(
    absolute_ranking: pd.DataFrame,
    percentage_ranking: pd.DataFrame,
    output_path: Path,
) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)
    chart_data = (
        (
            axes[0],
            absolute_ranking,
            "Largest absolute reductions",
            "Reduction (tonnes CO2 per person)",
            "#1f77b4",
        ),
        (
            axes[1],
            percentage_ranking,
            "Largest percentage reductions",
            "Reduction (%)",
            "#2ca02c",
        ),
    )

    for axis, ranking, title, x_label, color in chart_data:
        axis.set_title(title)
        axis.set_xlabel(x_label)
        axis.set_ylabel("Country")
        axis.set_axisbelow(True)
        axis.grid(axis="x", linestyle="--", alpha=0.4)
        if ranking.empty:
            axis.text(
                0.5,
                0.5,
                "No countries qualify",
                ha="center",
                va="center",
                transform=axis.transAxes,
            )
            continue

        bars = axis.barh(ranking["country"], ranking["reduction"], color=color)
        axis.invert_yaxis()
        for bar in bars:
            value = bar.get_width()
            axis.annotate(
                f"{value:.2f}",
                (value, bar.get_y() + bar.get_height() / 2),
                xytext=(4 if value >= 0 else -4, 0),
                textcoords="offset points",
                ha="left" if value >= 0 else "right",
                va="center",
            )

    figure.suptitle("EU27 CO2 per capita reductions, 2000-2024")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
    print(f"\nChart saved to: {output_path}")


def analyse(input_path: Path, chart_path: Path) -> None:
    values = load_comparison_data(input_path)
    absolute_reduction = values[START_YEAR] - values[END_YEAR]
    absolute_ranking = pd.DataFrame(
        {
            "country": values.index,
            "value_2000": values[START_YEAR].to_numpy(),
            "value_2024": values[END_YEAR].to_numpy(),
            "reduction": absolute_reduction.to_numpy(),
        }
    ).sort_values("reduction", ascending=False).head(3)
    print(f"Countries selected for absolute top-three ranking: {len(absolute_ranking)}")

    zero_baseline_countries = values.index[values[START_YEAR].eq(0)].tolist()
    if zero_baseline_countries:
        print(
            "\nPercentage reduction is undefined for countries with a zero "
            "2000 baseline; they are excluded from that ranking:"
        )
        for country in zero_baseline_countries:
            print(f" - {country} (2000 baseline = 0 tonnes CO2 per person)")

    percentage_eligible = values.loc[values[START_YEAR].ne(0)]
    print(
        "Rows eligible for percentage reduction after excluding zero baselines: "
        f"{len(percentage_eligible)}"
    )
    percentage_reduction = (
        (percentage_eligible[START_YEAR] - percentage_eligible[END_YEAR])
        / percentage_eligible[START_YEAR]
    ) * 100
    percentage_ranking = pd.DataFrame(
        {
            "country": percentage_eligible.index,
            "value_2000": percentage_eligible[START_YEAR].to_numpy(),
            "value_2024": percentage_eligible[END_YEAR].to_numpy(),
            "reduction": percentage_reduction.to_numpy(),
        }
    ).sort_values("reduction", ascending=False).head(3)
    print(
        "Countries selected for percentage top-three ranking: "
        f"{len(percentage_ranking)}"
    )

    print_ranking(
        "Top 3 EU27 countries by absolute CO2 per capita reduction (2000-2024):",
        absolute_ranking,
        "absolute_reduction",
        "Absolute reduction",
        3,
    )
    print_ranking(
        "Top 3 EU27 countries by percentage CO2 per capita reduction (2000-2024):",
        percentage_ranking,
        "percentage_reduction",
        "Percentage reduction",
        2,
    )
    save_chart(absolute_ranking, percentage_ranking, chart_path)


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent
    input_path = project_root / "data" / "processed" / "co2_eu.csv"
    chart_path = project_root / "figures" / "co2_eu_reductions.png"

    try:
        analyse(input_path, chart_path)
    except (OSError, KeyError, ValueError, pd.errors.ParserError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
