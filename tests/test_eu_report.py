"""Tests for the EU CO2 report."""

import matplotlib

matplotlib.use("Agg")  # draw charts without opening a window

import pandas as pd
import pytest

import eu_report
import eu_report as r


@pytest.fixture(scope="module")
def df():
    return r.load()


@pytest.fixture(scope="module")
def owid_eu(df):
    """Our World in Data's own row for the 27 member states."""
    return df[df["country"] == "European Union (27)"].set_index("year")


def test_report_runs():
    r.main()


def test_eu_members_includes_all_27_countries():
    """The EU dataset must contain all 27 member states."""
    df = eu_report.load()
    eu = eu_report.eu_members(df)

    assert eu["country"].nunique() == 27


def test_eu_members_includes_2024():
    """EU data should include the latest year, 2024."""
    df = eu_report.load()
    eu = eu_report.eu_members(df)

    assert eu["year"].max() == 2024


def test_per_person_is_population_weighted():
    """EU CO2 per person must use total emissions and population."""
    df = eu_report.load()
    eu = eu_report.eu_members(df)

    data_1990 = eu[eu["year"] == 1990]

    expected = (
        data_1990["co2"].sum() * 1_000_000
        / data_1990["population"].sum()
    )

    actual = eu_report.per_person(eu).loc[1990]

    assert abs(actual - expected) < 0.01


def test_missing_consumption_is_not_zero(df):
    totals = r.eu_totals(r.eu_members(df))
    assert pd.isna(totals.loc[2024, "consumption_co2"])  # no data for 2024, so not 0