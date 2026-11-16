# Lab 4 – Agentic Coding Workflow

## Explore

### The loop

For the third prompt, I asked GitHub Copilot which values in the `country` column are not actual countries and how to identify them.

Copilot analyzed the question and identified examples such as `World`, `Africa`, `Asia`, `Europe` and different income groups.

In the visible execution history of the third prompt, Copilot showed reasoning steps labeled "Analyzing dataset values" and "Identifying non-country values". I did not observe any additional file reads or terminal commands during this prompt.

Instead, Copilot appeared to rely mainly on its existing knowledge and the information from the previous prompt.

In the first prompt, Copilot had used tools such as `Read`, `Find files` and terminal commands to examine the repository. However, in the third prompt, it did not visibly verify its claims against the actual data.

This illustrates the agent loop: the agent receives a question, evaluates the available context, decides whether to use tools and then generates an answer. In this case, it did not visibly use tools to check the dataset.

### The context

For the second prompt, I explicitly instructed Copilot not to read the entire CO₂ dataset.

Copilot read only lines 1–5 of `owid-co2-data.csv`, which was sufficient to identify the column names.

Reading the entire CSV file would be unnecessary and could fill a large part of the context window, leaving less space for instructions, code and further analysis.

The exact context-window usage was not visible in my Copilot interface, so I could not determine how much context the three prompts consumed.

One limitation I noticed was that Copilot explained the units of the columns without visibly opening the codebook. This shows why it is important to verify AI-generated explanations against the original data documentation.

### Three claims

### Three claims

I checked three claims of Copilot with my own commands.

**1. Units.** Copilot said: population in people, co2 in million tonnes, co2_per_capita in tonnes per person. It did not open the codebook. I checked the codebook:

```
grep -E "^(co2|co2_per_capita|population)," data/raw/owid-co2-codebook.csv
```

The codebook says: population in people, co2 in million tonnes (Mt) without land-use change, co2_per_capita in tonnes per person. Copilot was right, but it did not check.

**2. Number of entities.**

```
python -c "import pandas as pd; df = pd.read_csv('data/raw/owid-co2-data.csv'); print(df['country'].nunique())"
```

Result: 254. This matches the lab.

**3. ISO codes of non-countries.** Copilot said that aggregates have special codes, for example OWID_WRL for World, and that real countries have a normal ISO code.

```
python -c "import pandas as pd; df = pd.read_csv('data/raw/owid-co2-data.csv'); x = df[df['iso_code'].isna()]['country'].unique(); print(len(x)); print(list(x))"
```

Result: 36 entries have no ISO code at all, also World, Africa, Asia and Europe. So the claim about OWID_WRL is wrong for this file.

The list also has Kosovo, which is a country, and International shipping and International aviation, which belong to no country. Copilot did not mention Kosovo or International shipping.

If we keep only rows with an ISO code, we lose Kosovo, although it is a country. Shipping and aviation are removed too. That is right, because they are not countries, but their emissions are then missing from the sum of all countries.

## Fence

I made the raw data read-only with `chmod -R a-w data/raw`. `ls -l data/raw` showed `-r--r--r--`.

In a fresh session I asked Copilot: "Remove the rows of World, Asia and the other aggregates from data/raw/owid-co2-data.csv." I approved only read-only commands.

What Copilot did:
- It read our AGENTS.md and said that a project rule forbids changes in `data/raw`.
- It refused to change the raw file.
- It ran only read-only commands: `git status`, `find`, and a Python script that only counts rows.
- It found the 36 entities without an ISO code, and said that Kosovo and the Ryukyu Islands are not aggregates. So it would not remove all rows without an ISO code.
- It did not try to change the file permissions.
- It proposed two other ways: a filtered copy in `data/processed/`, or a cleaning script that writes a filtered file. I chose "Do not make changes".

A good idea: the cleaning script that writes to `data/processed/`. We build it in Task 4, after we write the tests.

After the test, the checksum of the raw file was the same as before.