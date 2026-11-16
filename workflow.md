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

*To be completed by my project partner after independently checking Copilot's claims against the dataset.*