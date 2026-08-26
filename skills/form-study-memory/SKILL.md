---
name: form-study-memory
description: Save user-confirmed quiz or form answers to either a local cross-platform study library or an explicitly requested Google Drive folder, retrieve records by course, quiz, or topic, and prepare study summaries. Use after a form workflow when the user agrees to save, or when the user asks to recall or summarize saved study material. Never save without confirmation or use Google Drive unless the user names it.
---

# Form Study Memory

Maintain a private study library from completed form and quiz work. Store only learning content useful for later review: course, quiz or assignment, topics, concise summary, and the final question/answer/reason table. Do not store passwords, authentication codes, cookies, student IDs, payment data, signatures, hidden page state, or unrelated personal information.

Choose exactly one storage backend for each save:

- **Local** is the default when the user does not mention Google Drive. Use `scripts/study_memory.py`, resolved relative to this skill directory, for local saves and lookups.
- **Google Drive** is used only when the user explicitly says Google Drive or provides a Drive folder. Follow [references/google-drive-storage.md](references/google-drive-storage.md). Do not also run the local save command for that record.

Read [references/record-schema.md](references/record-schema.md) when preparing a record for saving or when diagnosing malformed stored data.

## Local storage

The script resolves the study library in this order:

1. `FORMS_RESPONDER_MEMORY_DIR`, when the user configured one.
2. `PLUGIN_DATA/study-memory`, when the current host exposes a writable plugin data directory.
3. The operating system's per-user application-data directory:
   - macOS: `~/Library/Application Support/FormsResponder/StudyMemory`
   - Windows: `%LOCALAPPDATA%\FormsResponder\StudyMemory` with `%APPDATA%` or the user profile as fallbacks.
   - Linux: `$XDG_DATA_HOME/forms-responder/study-memory` or `~/.local/share/forms-responder/study-memory`.

Run `python <skill-directory>/scripts/study_memory.py root` to show the resolved path. Use `--root <path>` only when the user explicitly chooses another library location. An override may point to a synced folder, but do not assume synchronization is desired.

## Post-form save workflow

After the form is answered, internally double-checked, summarized, and left unsubmitted:

1. Infer the most likely **course or class**, **quiz or assignment**, and **topics** from trusted visible context such as the course breadcrumb, page title, assessment title, question content, and reviewed sources.
2. Do not save yet. Ask one short confirmation question after the required answer table. Include the storage backend when Google Drive was explicitly requested, for example: “Save this in Google Drive under `BIO 101` → `Quiz 3`, with topics `cell respiration` and `ATP`, or change the folder, class, quiz, or topics?” Otherwise propose local storage.
3. Accept corrections naturally. If the user declines or does not answer, do not create or modify any study-memory file.
4. After explicit confirmation, create a record that follows the schema reference and sets `save_confirmed` to `true`.
5. If the confirmed backend is local, save it with `python <skill-directory>/scripts/study_memory.py save --input <record.json>`. Use an isolated temporary input file and remove that temporary file after a successful save.
6. If the confirmed backend is Google Drive, follow the Drive reference. Use the script's non-persistent `render` command to create a matching canonical JSON and readable Markdown pair, upload and verify both files, and then remove the temporary pair. Do not create a local library record or index entry.
7. Report the confirmed backend, course, quiz, topics, record ID, and the saved local paths or both verified Google Drive links.

Do not infer that a user wants saving merely because they previously saved another quiz. Confirmation is required for each completed form workflow.

## Finding the correct class or quiz locally

Search before assuming a destination already exists:

```text
python <skill-directory>/scripts/study_memory.py search --course "BIO 101" --json
python <skill-directory>/scripts/study_memory.py search --quiz "Quiz 3" --json
python <skill-directory>/scripts/study_memory.py search --topic "cell respiration" --json
python <skill-directory>/scripts/study_memory.py search --query "ATP" --json
```

Use multiple filters together when helpful. Matching is case-insensitive and searches record content, not browser state. If several classes or quizzes are plausible, show the smallest useful set of matches and ask the user which one they mean. Never silently merge records from similarly named courses.

For an explicitly requested Google Drive lookup, use the search and read workflow in the Drive reference instead of the local index. Prefer the canonical JSON record, use its Markdown companion for human-readable presentation, and treat a matching pair as one quiz. Do not combine local and Drive results unless the user explicitly asks for both.

## Building a later study summary

When the user asks for an exam review, topic summary, or recall of prior quizzes:

1. Identify the requested course, quiz, topic, or search terms from the request.
2. Retrieve full matching records from the backend the user named. Use `python <skill-directory>/scripts/study_memory.py context` with relevant filters for local memory, or follow the Drive reference for Google Drive.
3. If the query is ambiguous, list matching courses or quizzes and ask the user to choose before combining them.
4. Build the study summary only from the retrieved records, clearly separating remembered quiz evidence from any new external research.
5. Organize the result around concepts, recurring mistakes or distinctions, and representative question-answer reasoning. Do not claim the saved answers are authoritative beyond the evidence recorded at the time.
6. Cite saved record IDs or quiz names in the summary so the user can trace the material.

Use `show <record-id> --format markdown` when the user asks to inspect one saved document.

## Safety and integrity

- Saving is an external write and always requires the explicit post-form confirmation described above.
- Google Drive is never selected implicitly. If its tools are missing, unavailable, or disconnected, notify the user and stop the Drive save; do not silently create a local copy.
- Lookup and summarization are read-only and do not require a new save confirmation.
- Never edit an existing record silently. A repeated quiz save creates a separate timestamped record so history remains recoverable.
- If the index is missing or malformed, stop and explain the problem; do not overwrite it with an empty index.
- A Drive save uses a temporary JSON/Markdown upload pair. Remove both temporary files after both Drive uploads are verified. Do not retain a persistent local JSON, Markdown, or index entry for the same record.
- Keep the form-submission boundary unchanged. Saving a study record never submits, finalizes, or changes the browser form.
