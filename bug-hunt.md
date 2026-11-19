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