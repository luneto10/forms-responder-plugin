# Google Drive study-memory workflow

Use this workflow only after the user explicitly names Google Drive for the save or lookup. Google Drive is an optional backend, not an automatic mirror of local memory.

## Availability check

Confirm that callable Google Drive tools are present before promising a Drive action. The workflow needs file or folder search, folder creation, file upload, metadata readback, and readable file fetch capabilities.

If the Google Drive plugin is unavailable, disabled, disconnected, or requests authentication:

1. Tell the user that Google Drive study memory cannot proceed until the Google Drive plugin is enabled and connected in Codex.
2. Preserve the completed form and internal ledger.
3. Do not fall back to local storage unless the user separately asks for a local save.
4. Resume the Drive save from the preserved record after the user enables or reconnects the plugin.

## Resolve the destination

1. If the user provides a Drive folder URL or ID, read its metadata and verify that it is a folder.
2. If the user names an existing folder, search Drive for that exact or closest folder name. When one clear match exists, use it. When several plausible matches exist, show their names or paths and ask which one to use.
3. If no matching folder exists, propose creating the folder name the user requested and include that in the save confirmation. When no name was supplied, propose `Forms Responder Study Memory`.
4. Create only the confirmed missing folder. A useful default layout is a root study-memory folder with one child folder per course. If the user identifies a course folder directly, save there without creating a duplicate nested course folder.
5. Preserve the folder's existing organization and sharing permissions.

## Create one Drive record

Use an append-only Markdown file so the record remains readable and searchable without a local index. Give it a collision-resistant name such as:

```text
2026-08-24 - BIO 101 - Quiz 3 - 20260824T235716Z-a1b2c3d4.md
```

The file content must include:

- course or class;
- quiz or assignment;
- record ID and save timestamp;
- topics;
- concise summary;
- the exact `Question | Answer | Why this is correct` table;
- optional non-sensitive notes or source URL.

Render the Markdown in an isolated temporary file, upload it to the resolved folder as `text/markdown`, and then verify the returned Drive item using metadata and readable-content fetch. Check its title, parent folder, and representative content. Report only the observed Drive URL and ID. Remove the temporary upload artifact after verification.

Do not run the local `save` command, create a local study index entry, or retain a persistent local copy for a Drive-backed record.

## Find and study Drive records

1. Search the confirmed memory folder or Drive using concise course, quiz, or topic terms. Prefer the naming convention for course and quiz matches.
2. Fetch readable content for plausible Markdown records before using them.
3. If similarly named courses or quizzes match, ask the user to disambiguate instead of combining them.
4. Build summaries only from fetched records. Cite each record by quiz name, record ID, or observed Drive link.
5. Do not mix local and Drive records unless the user explicitly asks to search both backends.

## Examples

- “Save this quiz to Google Drive in my `BIO 101` folder.”
- “Create `School/Forms Responder Memory` in Google Drive and save this there.”
- “Find my Google Drive study records about oxidative phosphorylation.”
- “Make an exam review from the quizzes in this Drive folder: `<folder URL>`.”
