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