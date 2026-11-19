# Bug hunt: eu_report.py

## Our review

We reviewed the script function by function with the slide "Review checklist for data code" and the official hints of the lab. We compared the numbers with the rows `European Union (27)` and `World` of the data.

| # | Function | Checklist row | What goes wrong | Evidence (command → number) |
|---|---|---|---|---|
| 1 | `eu_members` / `MEMBERS` | Join / names | "Czech Republic" is called "Czechia" in the file, so the merge drops it silently. The report still says "27 member states". | `eu['country'].nunique()` → 26; `cut -d, -f1 … \| sort -u \| grep -i czech` → only `Czechia` |
| 2 | `eu_members` | Missing values | `dropna` on `consumption_co2` removes rows for the whole report, although only the imports section needs them. The report ends in 2023 instead of 2024. | rows before/after `dropna`: 5022 → 884; latest year 2024 → 2023 |
| 3 | `per_person` | Aggregation | `.mean()` is an unweighted average of the countries: Malta counts as much as Germany. It should be total CO₂ / total population. | 1990: mean = 9.87 t; total CO₂ / total population = 9.05 t; OWID EU27 = 9.215 t |
| 4 | `world_share` | Aggregates | The denominator sums `co2` over all rows, also World, continents and income groups. It should be the row `World`. | 1990: sum of all rows = 154,667 Mt, `World` = 22,732 Mt; report 2.4 %, OWID `share_global_co2` = 17.0 % |
| 5 | `biggest_cuts` | Filters / off by one | `year > since` leaves out the base year. The comparison starts in 1991, the report says "since 1990". | first year in `period` = 1991 for every country |
| 6 | `chart` | Chart / units | The y-axis says "t" but the values are in Mt, and it starts at 2000 instead of 0. The drop looks much bigger. | report: 3,706 → 2,402 Mt (−35 %); visible bar height 1,706 → 402 (looks like −76 %) |


## Human vs. AI review

After completing and committing our manual bug hunt, we started a new GitHub Copilot session to independently review `eu_report.py`.

Copilot was instructed to check its suspicions against the raw CSV data and not to modify any files.

| Bug | Human review | Copilot review |
|---|---|---|
| Missing Czechia | Found | Found |
| Missing values remove valid rows | Found | Found |
| Unweighted per-capita average | Found | Found |
| Incorrect world-share denominator | Found | Found |
| Base year excluded from ranking | Found | Found |
| Misleading chart units and scale | Found | Found |

### Comparison

- Both reviews identified the same six bugs.
- Copilot confirmed its findings using calculations based on the raw CSV data.
- Copilot did not report any additional bugs.
- There were no false positives among the six reported findings.
- One numerical difference remains: the manual review reported an unweighted 1990 average of 9.87 t, while Copilot reported 10.095 t. The calculations may use different subsets of countries and rows, so this difference should be checked separately.

### Reflection

The manual review helped us understand how small data-handling decisions can affect the final results without causing a Python error.

Copilot was useful as an independent second review because it checked multiple calculations against the raw dataset.

However, we should not accept AI results without verification, especially when numerical results differ between reviews.

The original `eu_report.py` was not modified during the review.

## Human vs. AI review

After completing and committing our manual bug hunt, we started a new GitHub Copilot session to independently review `eu_report.py`.

Copilot was instructed to check its suspicions against the raw CSV data and not to modify any files.

| Bug | Human review | Copilot review |
|---|---|---|
| Missing Czechia | Found | Found |
| Missing values remove valid rows | Found | Found |
| Unweighted per-capita average | Found | Found |
| Incorrect world-share denominator | Found | Found |
| Base year excluded from ranking | Found | Found |
| Misleading chart units and scale | Found | Found |

### Comparison

- Both reviews identified the same six bugs.
- Copilot confirmed its findings using calculations based on the raw CSV data.
- Copilot did not report any additional bugs.
- There were no false positives among the six reported findings.
- One numerical difference remains: the manual review reported an unweighted 1990 average of 9.87 t, while Copilot reported 10.095 t. The calculations may use different subsets of countries and rows, so this difference should be checked separately.

### Reflection

The manual review helped us understand how small data-handling decisions can affect the final results without causing a Python error.

Copilot was useful as an independent second review because it checked multiple calculations against the raw dataset.

However, we should not accept AI results without verification, especially when numerical results differ between reviews.

The original `eu_report.py` was not modified during the review.

### Independent verification of an AI result

We independently checked one numerical result reported by Copilot against the original OWID dataset.

Copilot reported that the EU-27 share of global CO2 emissions in 1990 was 17.025%.

Using pandas, we checked the original `World` and `European Union (27)` rows for 1990:

- World CO2 emissions: 22,732.145 Mt
- EU-27 share of global CO2 emissions: 17.025%

The value reported by Copilot matches the original OWID data. Therefore, this numerical result was correct and did not reproduce the incorrect world-share calculation in `eu_report.py`.


## Conclusion

The error in `world_share` changed the report the most: the EU's share of world emissions in 1990 went from 2.4 % to 17.0 %, seven times higher, because the old denominator also counted World, continents and income groups. The most convincing wrong number in a presentation would have been the cut in CO₂ per person of −45.7 % in `report_before.txt`: it looks realistic and positive, so nobody would check it, but it came from an unweighted average and the wrong set of countries. Copilot was faster than us and found all six errors with numbers from the raw data. We noticed a new silent error after one of our fixes: after the `dropna` fix, the 2024 imports became −2,426 Mt, and we caught it with a test; we did not ask Copilot to review the fixed script, so we cannot say if it would have found it. We also learned that each test must fail first, otherwise it does not prove that it catches the error.