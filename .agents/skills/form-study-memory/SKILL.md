---
name: form-study-memory
description: Save user-confirmed quiz or form answers and topics to a local cross-platform study library, retrieve records by course, quiz, or topic, and use them to prepare study summaries. Use after a form workflow when the user agrees to save, or when the user asks to recall or summarize previously saved study material. Never save without confirmation.
---

# Form Study Memory

Maintain a private, local study library from completed form and quiz work. Store only learning content useful for later review: course, quiz or assignment, topics, concise summary, and the final question/answer/reason table. Do not store passwords, authentication codes, cookies, student IDs, payment data, signatures, hidden page state, or unrelated personal information.

Use `scripts/study_memory.py`, resolved relative to this skill directory, for every save and lookup. It uses only the Python standard library and chooses a writable data directory on macOS, Windows, and Linux. Never write study records inside the installed plugin directory.

Read [references/record-schema.md](references/record-schema.md) when preparing a record for saving or when diagnosing malformed stored data.

## Storage location

The script resolves the study library in this order:

1. `FORMS_RESPONDER_MEMORY_DIR`, when the user configured one.
2. `PLUGIN_DATA/study-memory`, when Codex exposes a writable plugin data directory.
3. The operating system's per-user application-data directory:
   - macOS: `~/Library/Application Support/FormsResponder/StudyMemory`
   - Windows: `%LOCALAPPDATA%\FormsResponder\StudyMemory` with `%APPDATA%` or the user profile as fallbacks.
   - Linux: `$XDG_DATA_HOME/forms-responder/study-memory` or `~/.local/share/forms-responder/study-memory`.

Run `python <skill-directory>/scripts/study_memory.py root` to show the resolved path. Use `--root <path>` only when the user explicitly chooses another library location. An override may point to a synced folder, but do not assume synchronization is desired.

## Post-form save workflow

After the form is answered, internally double-checked, summarized, and left unsubmitted:

1. Infer the most likely **course or class**, **quiz or assignment**, and **topics** from trusted visible context such as the course breadcrumb, page title, assessment title, question content, and reviewed sources.
2. Do not save yet. Ask one short confirmation question after the required answer table, for example: “Save this under `BIO 101` → `Quiz 3` with topics `cell respiration` and `ATP`, or use a different class, quiz, or topic?”
3. Accept corrections naturally. If the user declines or does not answer, do not create or modify any study-memory file.
4. After explicit confirmation, create a record JSON object that follows the schema reference and sets `save_confirmed` to `true`.
5. Save it with `python <skill-directory>/scripts/study_memory.py save --input <record.json>`. Use an isolated temporary input file and remove that temporary file after a successful save; do not delete the saved library record.
6. Report the confirmed course, quiz, topics, record ID, and saved Markdown path.

Do not infer that a user wants saving merely because they previously saved another quiz. Confirmation is required for each completed form workflow.

## Finding the correct class or quiz

Search before assuming a destination already exists:

```text
python <skill-directory>/scripts/study_memory.py search --course "BIO 101" --json
python <skill-directory>/scripts/study_memory.py search --quiz "Quiz 3" --json
python <skill-directory>/scripts/study_memory.py search --topic "cell respiration" --json
python <skill-directory>/scripts/study_memory.py search --query "ATP" --json
```

Use multiple filters together when helpful. Matching is case-insensitive and searches record content, not browser state. If several classes or quizzes are plausible, show the smallest useful set of matches and ask the user which one they mean. Never silently merge records from similarly named courses.

## Building a later study summary

When the user asks for an exam review, topic summary, or recall of prior quizzes:

1. Identify the requested course, quiz, topic, or search terms from the request.
2. Retrieve full matching records with `python <skill-directory>/scripts/study_memory.py context` and the relevant filters. Use `--json` for structured output.
3. If the query is ambiguous, list matching courses or quizzes and ask the user to choose before combining them.
4. Build the study summary only from the retrieved records, clearly separating remembered quiz evidence from any new external research.
5. Organize the result around concepts, recurring mistakes or distinctions, and representative question-answer reasoning. Do not claim the saved answers are authoritative beyond the evidence recorded at the time.
6. Cite saved record IDs or quiz names in the summary so the user can trace the material.

Use `show <record-id> --format markdown` when the user asks to inspect one saved document.

## Safety and integrity

- Saving is an external write and always requires the explicit post-form confirmation described above.
- Lookup and summarization are read-only and do not require a new save confirmation.
- Never edit an existing record silently. A repeated quiz save creates a separate timestamped record so history remains recoverable.
- If the index is missing or malformed, stop and explain the problem; do not overwrite it with an empty index.
- Keep the form-submission boundary unchanged. Saving a study record never submits, finalizes, or changes the browser form.
