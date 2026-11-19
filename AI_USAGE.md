# AI usage

## Task 2 – Explore

**GitHub Copilot in VS Code** (Interactive mode, Manual permissions)
- Model: Copilot Fusion (Auto). It picked GPT-5.6 Luna.
- Driver: Ülkü. Navigator: Chaymae.
- Prompts: the three prompts from the lab (what is in the repository, the columns and units, the values in `country` that are not countries).
- Accepted: the units of the columns. They match the codebook. We used the answers as a starting point.
- Rejected: the claim that aggregates have codes like OWID_WRL. In our file they have no ISO code. Copilot also did not mention Kosovo or International shipping.
- How we checked: `grep` on the codebook, and pandas for the number of entities and the rows without an ISO code (see `workflow.md`, section Three claims). We checked the SHA-256 checksum of the data file, the tool calls of Copilot, and `git status` for unwanted changes.

**Other AI use**
- Ülkü used ChatGPT (OpenAI, GPT-6) for help with the Python setup on Windows, the download, understanding Copilot's answers, and wording the sections The loop and The context.
- Chaymae used Claude (Anthropic) to understand the steps and the commands, and for help with wording the section Three claims.

## Task 3 – Write an AGENTS.md and Protect Raw Data

**Date:** 16 November 2026

**Tools and Models:**
- GitHub Copilot Chat (VS Code, Interactive mode, Manual permissions, Auto model selection → it picked GPT-5.6 Luna)
- ChatGPT (OpenAI, GPT-6), used by Ülkü
- Claude (Anthropic), used by Chaymae

### Prompts (summarized)

**GitHub Copilot:**
- Write a draft of an AGENTS.md for this repository into a new file AGENTS.draft.md. Do not change any other file. (driver: Ülkü)
- Remove the rows of World, Asia and the other aggregates from data/raw/owid-co2-data.csv. (driver: Chaymae)

**ChatGPT:**
- What information should be included in AGENTS.md?
- How can I describe the project, setup commands, dataset and rules?
- Can you check and correct my English sentences?
- How can I protect raw data files on Windows?

### How We Used AI

We first wrote our own `AGENTS.md` containing information about the project, Python setup, data sources, units and rules for AI coding agents.

Ülkü used ChatGPT to understand the assignment requirements and improve the English wording of our documentation.

Chaymae used Claude to review AGENTS.md, to read Copilot's commands before approving them, and for help with wording the section Fence.

After completing our own version, we asked GitHub Copilot to generate a separate draft named `AGENTS.draft.md`.

We compared both files using `diff AGENTS.md AGENTS.draft.md`.

The content was almost identical. The only differences were a trailing space and a missing final newline in our version. Copilot did not provide additional information and appeared to reuse the existing `AGENTS.md`.

We then tested whether Copilot would follow our project instructions. When asked to remove aggregate rows from the raw CO₂ dataset, Copilot read `AGENTS.md` and refused to modify the protected data.

It also pointed out that Kosovo and Ryukyu Islands should not automatically be treated as aggregates.

### What We Accepted, Changed or Rejected

- We used ChatGPT's explanations and language corrections while writing our own documentation.
- We reviewed and improved our `AGENTS.md` ourselves.
- Chaymae added the macOS setup commands and the rule to select the 27 EU countries by name, not by ISO code.
- We did not adopt additional content from Copilot's draft because it provided no new information.
- We deleted `AGENTS.draft.md` after the comparison.
- In the fence test, we approved only read-only commands (`git status`, `find`, a Python script that only counts rows). We did not approve any modification of the raw data and chose "Do not make changes".
- Copilot did not attempt to change file permissions.

### Verification

We compared the files with:

`diff AGENTS.md AGENTS.draft.md`

We used Git commands such as `git status`, `git diff` and `git log` to review changes.

The raw data was protected using file permissions (`chmod -R a-w data/raw`, checked with `ls -l data/raw`).

After the fence test, the SHA-256 checksum of `owid-co2-data.csv` remained unchanged.

This confirmed that the original dataset had not been modified.

### Reflection

This task showed us why project-specific instructions are important when working with AI coding agents.

We learned that an agent may reuse existing instructions rather than independently discovering all relevant information.

We also learned that `AGENTS.md` provides guidance but is not a technical security boundary. File permissions and manual approval settings provide additional protection.

The most important lesson was that AI-generated actions and suggestions should always be reviewed, especially when working with original datasets.

## Task 4 – Plan, then build in small steps

**Date:** 19 November 2026

**Tools and Models:**
- GitHub Copilot Chat (VS Code, Interactive mode, Manual permissions, Auto model selection). In step 2 it picked mai-code-2-flash.
- ChatGPT (OpenAI, GPT-6), used by Ülkü
- Claude (Anthropic), used by Chaymae

### Steps and roles

| Step | Script | Driver | Navigator | Commit |
|---|---|---|---|---|
| 1 | `src/download.py` | Ülkü | Chaymae | `402128c` |
| 2 | `tests/test_clean.py` + `src/clean_co2.py` | Chaymae | Ülkü | `c0e2866` (tests), `ea15a63` (script) |
| 3 | `src/analyse.py` | Ülkü | Chaymae | `4265fab` |

All prompts, plan changes and rejected actions are in `workflow.md`, section Build.

### How we used AI

- GitHub Copilot wrote the three scripts, after we reviewed and changed its plans.
- We wrote the tests before the cleaning script. Chaymae wrote `tests/test_clean.py` with help from Claude: Claude suggested the code for the four tests, and Chaymae checked that she understood every line. Copilot did not write or change the tests.
- Ülkü used ChatGPT to improve her prompts, to review Copilot's plans and code (`download.py`, `analyse.py`), for help with Git and terminal commands, to understand the results, and for wording in `workflow.md`.
- Chaymae used Claude to fill in the five-part prompt for the cleaning script, to review Copilot's plans and code before approving them, and for wording in `workflow.md`.

### What we accepted, changed or rejected

- Accepted: the three scripts, after reading the full code.
- Changed: we asked for the pinned commit, a fresh-clone setup and no writes to the read-only `data/raw/` (step 1); a stop with an error on missing values instead of filling or dropping them (steps 2 and 3); the values of 2000 and 2024 in the output (step 3).
- Rejected: every attempt of Copilot to run scripts or tests itself. In step 2, after we rejected the terminal command, Copilot tried two other tools (the pylance MCP server and the test tool). Both only offered "Allow in this Session". We skipped both and told Copilot not to run anything.

### Verification

- We ran all scripts and tests ourselves. `python -m pytest` → 5 passed.
- Before the cleaning step, Chaymae checked by hand that the EU27 rows from 2000 to 2024 have 675 rows and 0 missing values.
- `git status` before every commit. `tests/` was not changed by Copilot.
- The checksum of the raw data file was unchanged (`7f78e2b2…`).
- Chaymae ran all three scripts on macOS, Ülkü on Windows. We got the same numbers and checked the arithmetic of the six results.

### Reflection

Copilot respected our rules when we wrote them in the prompt and in AGENTS.md. But when we rejected a command, it looked for another way to run it. Manual permissions were necessary to stop this.


## Task 5 – Verify, then answer

**Date:** 19 November 2026

**Tools and Models:**
- GitHub Copilot Chat (VS Code, Interactive mode, Manual permissions, Auto model selection)
- ChatGPT (OpenAI, GPT-6), used by Ülkü
- Claude (Anthropic), used by Chaymae (exact model not recorded)

### Prompts (summarized)

**GitHub Copilot:**
- "Why are the CO2 emissions per person of Luxembourg so high?"

**ChatGPT:**
- Help me evaluate Copilot's explanation about Luxembourg's CO₂ emissions.
- Help me find independent sources and compare them with Copilot's claims.
- Help me document the verification in `workflow.md`.
- Help me review and improve our `README.md`.

**Claude:**
- Help with the verification commands for Task 5.
- Help investigate the SSL certificate error during the fresh-clone test.
- Help compare the manual Luxembourg calculations.
- Help draft the `README.md`.

### How we used AI

Ülkü asked GitHub Copilot why Luxembourg's CO₂ emissions per person are high. Copilot explained this using the small population, territorial emissions accounting, transport, industrial activity and fuel sales to non-residents.

Ülkü used ChatGPT to review Copilot's explanation, identify which claims needed independent verification, find relevant sources from OECD and STATEC, and prepare the documentation.

Chaymae used Claude for help with verification commands, understanding the SSL certificate problem on macOS, comparing the manual Luxembourg calculation and drafting the README.

### What we accepted, changed or rejected

- We accepted Copilot's explanation as a starting point, but did not treat it as verified evidence.
- We checked the explanation about cross-border fuel sales against independent OECD and STATEC sources.
- Copilot provided numerical values for Luxembourg's population and CO₂ emissions, but did not quantify the contribution of fuel sales to non-residents.
- We chose Denmark as the main answer in the README because the percentage reduction allows comparison between countries with different starting levels.
- We revised the README to explain that Luxembourg's per-capita reduction reflects both population growth and a decrease in total emissions.
- We improved the setup instructions for Windows and macOS.
- We reviewed AI-generated suggestions before using them.

### Verification

- Chaymae checked the Git history of the tests.
- She tested the complete pipeline in a fresh clone on macOS.
- The first download failed because the Python installation lacked the required SSL certificates. After using Python's official `Install Certificates.command`, the download worked and the SHA-256 checksum matched.
- The cleaning script, tests and analysis ran successfully in the fresh clone.
- `python -m pytest` → 5 passed.
- Chaymae independently calculated Luxembourg's population growth and total CO₂ reduction using the raw dataset and a calculator.
- Ülkü compared Copilot's explanation with OECD and STATEC publications.
- We reviewed the analysis results and README before committing the changes.

### Reflection

This task showed us that a script working on an existing dataset does not prove that the complete pipeline works from scratch. The fresh-clone test revealed an SSL certificate issue that we had not encountered before.

We also learned that AI-generated explanations may sound convincing without providing enough evidence. Copilot gave numerical values from our dataset but did not provide a measurable contribution for the cross-border fuel sales it mentioned.

Independent sources, manual calculations and reproducible tests were necessary to evaluate the results. We used AI for assistance, but kept the verification and final decisions under human control.

## Task 6 and 7 – Bug hunt

**Tools and models:** GitHub Copilot in VS Code (Interactive, Manual permissions, Auto model), Claude (Anthropic) used by Chaymae, ChatGPT (OpenAI, GPT-6) used by Ülkü.

- **Task 6:** We searched the errors ourselves with the slide "Review checklist for data code" and the two official hints of the lab. Chaymae used Claude to explain lines and to get check commands; Claude did not say which lines were wrong. `bug-hunt.md` was committed before the Copilot review. Ülkü ran the Copilot review in a fresh session with the prompt from the lab and compared the results.
- **Task 7:** Ülkü fixed errors 1–3 (fixes with Copilot), Chaymae fixed the new imports error and errors 4–6. For Chaymae's part, Claude suggested the test code and the fixes; Chaymae checked that every test failed first and passed after the fix. One commit per fix.
- **Accepted:** the fixes, after reading them and running the tests.
- **Checked:** `python -m pytest` → 13 passed; every number in `report_after.txt` compared with the rows `European Union (27)` and `World`; `diff report_before.txt report_after.txt`.