"""Tests for the EU CO2 report."""

import eu_report


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