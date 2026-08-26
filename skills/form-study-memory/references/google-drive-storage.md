# Google Drive study-memory workflow

Use this workflow only after the user explicitly names Google Drive for the save or lookup. Google Drive is an optional backend, not an automatic mirror of local memory.

## Availability check

Confirm that callable Google Drive tools are present before promising a Drive action. The workflow needs file or folder search, folder creation, file upload, metadata readback, and readable file fetch capabilities.

If the Google Drive connector or callable Drive integration is unavailable, disabled, disconnected, or requests authentication:

1. Tell the user that Google Drive study memory cannot proceed until a Google Drive connector or equivalent callable Drive tool is enabled and connected in the current host.
2. Preserve the completed form and internal ledger.
3. Do not fall back to local storage unless the user separately asks for a local save.
4. Resume the Drive save from the preserved record after the user enables or reconnects the plugin.

## Resolve the destination

1. If the user provides a Drive folder URL or ID, read its metadata and verify that it is a folder.
2. If the user names an existing folder, search Drive for that exact or closest folder name. When one clear match exists, use it. When several plausible matches exist, show their names or paths and ask which one to use.
3. If no matching folder exists, propose creating the folder name the user requested and include that in the save confirmation. When no name was supplied, propose `Forms Responder Study Memory`.
4. Create only the confirmed missing folder. A useful default layout is a root study-memory folder with one child folder per course. If the user identifies a course folder directly, save there without creating a duplicate nested course folder.
5. Preserve the folder's existing organization and sharing permissions.

## Create one paired Drive record

Store two append-only files with the same generated basename and record ID:

```text
2026-08-24 - BIO 101 - Quiz 3 - 20260824T235716Z-a1b2c3d4.json
2026-08-24 - BIO 101 - Quiz 3 - 20260824T235716Z-a1b2c3d4.md
```

The JSON file is the canonical machine-readable record. The Markdown file is the human-readable companion. Both must represent the same:

- course or class;
- quiz or assignment;
- record ID and save timestamp;
- topics;
- concise summary;
- the exact `Question | Answer | Why this is correct` table;
- optional non-sensitive notes or source URL.

Create the pair with the skill's deterministic helper:

```text
python <skill-directory>/scripts/study_memory.py render \
  --input <record.json> \
  --output-dir <temporary-directory>
```

The command validates confirmation and schema, creates one record ID and timestamp, renders both formats, and does not update the local study index.

Upload the generated `.json` as `application/json` and `.md` as `text/markdown` to the same resolved Drive folder. Verify both returned items using metadata and readable-content fetch:

- filenames share the exact basename;
- both parent IDs match the confirmed folder;
- JSON parses and contains the returned record ID, course, quiz, topics, and questions;
- Markdown contains the same record ID and the exact `Question | Answer | Why this is correct` table.

Treat the save as complete only after both files pass verification. If one succeeds and the other fails, report the partial state and retry only the missing file; never upload another copy of the verified companion. If the missing upload still fails, leave the verified Drive item intact, report its observed link, and ask the user whether to retry later or remove the partial record.

After both uploads are verified, remove both temporary artifacts. Do not run the local `save` command, create a local study index entry, or retain persistent local copies for a Drive-backed record. Report both observed Drive links and IDs.

## Find and study Drive records

1. Search the confirmed memory folder or Drive using concise course, quiz, topic, or record-ID terms. Prefer the shared filename convention for course and quiz matches.
2. Group `.json` and `.md` files by their common basename or record ID. Count a pair as one study record, not two.
3. Fetch and parse the JSON companion first. Validate its schema version and required fields before using it as study context.
4. Use the Markdown companion for user-facing inspection or links. Confirm its record ID matches the JSON.
5. For legacy Markdown-only records, fetch the Markdown and use it as a supported fallback. Do not require retroactive JSON creation unless the user requests migration.
6. If JSON is malformed but Markdown is valid, disclose the malformed companion and use Markdown only when its content is sufficiently complete; do not silently treat malformed JSON as authoritative.
7. If similarly named courses or quizzes match, ask the user to disambiguate instead of combining them.
8. Build summaries only from fetched records. Cite each logical record once by quiz name, record ID, and observed Drive link when useful.
9. Do not mix local and Drive records unless the user explicitly asks to search both backends.

## Examples

- “Save this quiz to Google Drive in my `BIO 101` folder.”
- “Create `School/Forms Responder Memory` in Google Drive and save this there.”
- “Find my Google Drive study records about oxidative phosphorylation.”
- “Make an exam review from the quizzes in this Drive folder: `<folder URL>`.”
