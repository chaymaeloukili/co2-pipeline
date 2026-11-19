# co2-pipeline

Which EU country has reduced its CO₂ emissions per person the most since 2000?

Lab 4 of the course Data Integration (TH Köln). Pair: Chaymae and Ülkü.

## Answer

We compare the 27 EU member states from 2000 to 2024. The answer depends on how you read "the most".

**Biggest cut in tonnes per person**

| | Country | 2000 | 2024 | Cut |
|---|---|---|---|---|
| 1 | Luxembourg | 19.953 t | 10.460 t | −9.493 t |
| 2 | Finland | 11.015 t | 5.301 t | −5.714 t |
| 3 | Ireland | 11.900 t | 6.339 t | −5.561 t |

**Biggest cut in percent**

| | Country | 2000 | 2024 | Cut |
|---|---|---|---|---|
| 1 | Denmark | 10.170 t | 4.746 t | −53.33 % |
| 2 | Finland | 11.015 t | 5.301 t | −51.87 % |
| 3 | Malta | 6.172 t | 3.204 t | −48.09 % |

![CO₂ per capita reductions in the EU27, 2000–2024](figures/co2_eu_reductions.png)

**Which answer we would present:** We would present Denmark, the biggest cut in percent. The cut in tonnes favours countries that started very high. Luxembourg's population grew by 54 % from 2000 to 2024, while its total CO₂ fell only by 19 %, so a large part of its cut per person comes from population growth, not from lower emissions. Finland is in the top 3 in both readings.

## How to run it

```
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python src/download.py             # downloads the pinned data into data/raw/
python src/clean_co2.py            # writes data/processed/co2_eu.csv
python -m pytest                   # 5 tests
python src/analyse.py              # prints the results and saves the chart in figures/
```

On macOS with Python from python.org, run `Install Certificates.command` once, or the download stops with an SSL error.

## Data and sources

- **Dataset:** CO₂ and Greenhouse Gas Emissions, by Our World in Data. Source: https://github.com/owid/co2-data, pinned to commit `382ee6c662b0ece26e111f263b44c029afad7787` (2 June 2026). Licence: CC BY 4.0.
- **Original sources of the columns we use** (from the column `source` of the codebook):
  - `co2`: Global Carbon Budget (2025), https://globalcarbonbudget.org/
  - `population`: Population based on various sources (2024), https://ourworldindata.org/population-sources
  - `co2_per_capita`: Global Carbon Budget (2025) and Population based on various sources (2024)

How we worked: see `workflow.md`. How we used AI: see `AI_USAGE.md`.