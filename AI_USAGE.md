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