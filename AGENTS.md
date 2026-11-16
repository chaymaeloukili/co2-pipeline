## Projekt
### What is the goal of our CO₂ project?
The goal of this project is to analyse CO₂ emissions per person in the 27 EU member states from 2000 to 2024 and identify which country has achieved the largest reduction.

## Setup and Commands
### How can someone set up the Python environment and install the required packages for this project?
First, a virtual environment should be created. Then, the required Python libraries need to be installed. After that, the tests can be run to make sure everything works properly.
- Create virtual environment: `python -m venv .venv`
- Activate environment (Windows): `.venv\Scripts\activate.bat`
- Install packages: `python -m pip install -r requirements.txt`
- Run tests: `python -m pytest`
- Download data: `python src/download.py`
- Clean data: `python src/clean_co2.py`
- Analyse data: `python src/analyse.py`

## Data
The dataset `data/raw/owid-co2-data.csv` comes from Our World in Data and contains information about CO₂ emissions from different countries. 

Source : https://github.com/owid/co2-data

The dataset version is identified by the commit 382ee6c662b0ece26e111f263b44c029afad7787.

The codebook is located in data/raw/owid-co2-codebook.csv and explains the meaning and units of the dataset columns.

- `population`: Number of people.
- `co2`: Annual CO₂ emissions in million tonnes.
- `co2_per_capita`: Annual CO₂ emissions in tonnes per person.
- `co2` data is available until 2024, but not all columns cover the same years.

There are 36 entities without an ISO code. These include aggregates such as World, Africa, Asia and the European Union (27), but also Kosovo and international shipping and aviation.

Not every entity without an ISO code is an aggregate.

- Source: Our World in Data – CO₂ and Greenhouse Gas Emissions.
- Licence: CC BY 4.0.

## Rules
- The raw data in data/raw must not modified.
- Before installing packages, permission must be asked.
- The tests must not be modified or deleted.
- After every filtering row counts must be printed.
- Missing values must not be filled without explicitly reporting it.
- URLs must never be invented. If a URL is unknown, ask the user.