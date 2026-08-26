# Forms Responder

Forms Responder is a portable Agent Skills package for Codex, Claude Code, Gemini CLI, and Grok Build. It provides careful assistance with browser forms, surveys, quizzes, applications, and LMS pages. It works through visible controls in order, reviews required source material, double-checks its work from an internal answer ledger, and always leaves final submission to the user.

It can also turn confirmed quiz work into a searchable study library. Records may be stored locally on macOS, Windows, or Linux, or saved only to an explicitly requested Google Drive folder.

> **Submission boundary:** Forms Responder never clicks **Submit**, **Turn In**, **Send**, **Finish**, **Confirm**, **Purchase**, **Sign**, or an equivalent final action. The user always submits.

## Highlights

| Capability | Behavior |
|---|---|
| Careful form interaction | Reads the full prompt and every option, then works sequentially through ordinary visible controls. |
| Source-grounded answers | Reviews required videos, audio, readings, PDFs, images, charts, and presentations before answering. |
| Internal double-check | Maintains an answer ledger and performs two review passes from conversation memory instead of jumping around the UI. |
| Human checkpoints | Waits when an intermediate step requires the user's own click or choice, then resumes from the preserved page state. |
| Safe handoff | Leaves the form open and reports every answer in a `Question / Answer / Why this is correct` table. |
| Local study memory | Saves confirmed Markdown and JSON records plus a searchable local index. |
| Google Drive study memory | Saves a canonical JSON record and matching readable Markdown companion to the chosen Drive folder without persistent local copies. |
| Study-guide retrieval | Finds saved material by class, quiz, topic, or question content and turns it into an exam review. |
| Built-in help | Explains the plugin to new users and provides copyable example prompts. |

## Included skills

- `careful-form-responder` — completes or audits live browser forms without submitting.
- `form-source-reviewer` — reviews the actual media, document, chart, or linked reading required by a question.
- `form-study-memory` — saves and retrieves user-confirmed study records locally or in explicitly requested Google Drive storage.
- `forms-responder-help` — explains capabilities, safety boundaries, storage options, troubleshooting, and example prompts.

Skills are selected automatically from natural-language requests. Slash commands are not normally required.

## Platform compatibility

The instructions, references, and Python study-memory helper are shared across all supported hosts. Each host receives its native package manifest, while generated skill copies are checked against the canonical plugin skills so their behavior cannot drift silently.

| Host | Native packaging | Skill behavior | Extra capability needed for live forms |
|---|---|---|---|
| Codex | `.codex-plugin/plugin.json` and Codex marketplace | Full | Browser plugin or supported browser-control surface |
| Claude Code | `.claude-plugin/plugin.json` and Claude marketplace | Full | Chrome integration, computer-use surface, or trusted browser MCP/tool |
| Gemini CLI | `gemini-extension.json` with extension skills | Full | Browser-capable extension or trusted MCP/tool |
| Grok Build | Reads the Claude-compatible plugin natively | Full | Grok browser/computer surface or trusted MCP/tool |

“Full” means the same safety rules, sequential workflow, internal audit, handoff table, and study-memory logic. Installing instructions cannot create a browser, media player, signed-in session, or Google Drive connector that the host does not expose. If a required tool is missing, Forms Responder reports the missing prerequisite and does not pretend that it operated the page or saved to Drive.

## How a form session works

```text
User requests help with the open form
                ↓
Read the full question and all options
                ↓
Review required video/document/source
                ↓
Interact with one visible control at a time
                ↓
Confirm the visible result and update the internal ledger
                ↓
Perform two memory-based audit passes
                ↓
Leave final submission untouched
                ↓
Show Question / Answer / Why this is correct
                ↓
Offer an optional, separately confirmed study-memory save
```

If the responder finds a specific inconsistency during its audit, it returns only to that question. It does not restart a full UI review merely for reassurance.

The responder never guesses personal experiences, consent, signatures, attestations, payment authorization, authentication information, or CAPTCHA answers.

## Example session

Ask:

> Answer this Canvas quiz carefully. Watch any required video, double-check every answer from memory, and stop before submission.

The final handoff uses this format:

| Question | Answer | Why this is correct |
|---|---|---|
| Where does glycolysis occur? | Cytoplasm | Glycolysis occurs in the cytosol. |
| What is the final electron acceptor? | Oxygen | Oxygen accepts electrons at the end of the electron transport chain. |

It then states that nothing was submitted and may ask:

> Save this locally under `BIO 101` → `Quiz 3`, with topics `cellular respiration` and `ATP`, or change the storage, class, quiz, or topics?

No study record is written until the user confirms.

## Study-memory storage choices

Each save uses exactly one backend.

| Backend | When selected | Persistent files | Best for |
|---|---|---|---|
| Local | Default when the user does not mention Google Drive | Markdown, JSON, and `index.json` | Private per-computer storage and fast structured lookup |
| Google Drive | Only when the user explicitly says Google Drive or supplies a Drive folder | Matching JSON and Markdown files in the confirmed Drive folder | Structured cross-computer lookup plus a readable document, without a local duplicate |

Local and Google Drive records are not combined unless the user explicitly asks to search both.

## Local study memory

The local helper uses Python's standard library and stores records outside the installed plugin so an update does not erase them.

Default locations:

| Operating system | Study-library location |
|---|---|
| macOS | `~/Library/Application Support/FormsResponder/StudyMemory` |
| Windows | `%LOCALAPPDATA%\FormsResponder\StudyMemory` |
| Linux | `$XDG_DATA_HOME/forms-responder/study-memory` or `~/.local/share/forms-responder/study-memory` |

Local records are append-only and organized by course and quiz:

```text
StudyMemory/
├── index.json
└── records/
    └── bio-101/
        └── quiz-3/
            ├── 20260824T235716Z-a1b2c3d4.json
            └── 20260824T235716Z-a1b2c3d4.md
```

Advanced users can set `FORMS_RESPONDER_MEMORY_DIR` to choose another local or filesystem-synchronized directory. This is different from the Google Drive connector workflow below.

## Use Google Drive instead of local memory

Google Drive is optional and must be explicitly requested. Installing Forms Responder does not automatically install or connect Google Drive.

### 1. Enable Google Drive in the current host

1. Install or enable a Google Drive connector for Codex, Claude, Gemini, or Grok.
2. Connect the Google account that owns the destination folder.
3. Confirm that the integration can search files, create folders, upload files, and read back metadata and content.
4. Start a new task or session if the host requires a restart to expose newly installed tools.

If Google Drive is missing, disabled, disconnected, or awaiting authentication, Forms Responder must notify the user. It does not silently save locally instead.

### 2. Choose or create the Drive folder

You can provide an existing folder name or URL:

> Save this quiz to Google Drive in my `BIO 101` folder. Do not keep a local copy.

Or ask Forms Responder to create a dedicated library:

> Use Google Drive for this study memory. Find or create a folder named `Forms Responder Study Memory`, organize records by class, and save this quiz there only after I confirm the class, quiz, topics, and folder.

Forms Responder searches before creating anything. If several folders have similar names, it asks which one you mean. If no folder exists, it includes the proposed new folder in the confirmation before creating it.

### 3. Confirm the save

A typical confirmation is:

> Save to Google Drive → `Forms Responder Study Memory/BIO 101` as `Quiz 3`, with topics `ATP`, `glycolysis`, and `oxidative phosphorylation`?

After confirmation, the plugin:

1. resolves or creates the approved folder;
2. validates the record and creates one collision-resistant record ID;
3. renders a canonical `.json` file and matching readable `.md` file with the same basename;
4. uploads both files to the confirmed Drive folder;
5. verifies both titles, parent folders, record IDs, and representative content;
6. returns both observed Google Drive links and the shared record ID;
7. removes both temporary upload artifacts;
8. skips the local save command and local index entirely.

Example Drive layout:

```text
Forms Responder Study Memory/
└── BIO 101/
    ├── 2026-08-24 - BIO 101 - Quiz 3 - 20260824T235716Z-a1b2c3d4.json
    └── 2026-08-24 - BIO 101 - Quiz 3 - 20260824T235716Z-a1b2c3d4.md
```

The JSON file is authoritative for structured lookup. The Markdown companion is optimized for reading. Forms Responder groups them by basename or record ID and counts them as one quiz.

Because Drive selection must be explicit, mention **Google Drive** again in a new task. This avoids accidentally sending school content to the cloud based on an old conversation preference.

### 4. Retrieve Drive records later

Examples:

- “Find my Forms Responder records in Google Drive about cellular respiration.”
- “Make an exam review from the quizzes in my Google Drive `BIO 101` folder.”
- “Use only the study records in this Drive folder: `<folder URL>`.”
- “Search both my local and Google Drive records for ATP.”

Drive lookup searches for likely pairs, reads and validates JSON first, uses Markdown for human-readable presentation, disambiguates similarly named classes, and cites each logical quiz once. Older Markdown-only records remain supported as a fallback.

## Moving existing local records to Google Drive

Existing local records are not uploaded automatically. To migrate them, ask explicitly:

> Move my local Forms Responder study records for `BIO 101` to this Google Drive folder: `<folder URL>`. Verify every upload before asking whether I want the local originals removed.

Upload verification and deletion are separate steps. Local originals should remain until the user explicitly approves their removal after checking the Drive copies.

## Built-in help

New users can ask naturally:

- “What can Forms Responder do?”
- “Show me examples of how to use this plugin.”
- “Explain local versus Google Drive study memory.”
- “Why did the plugin stop before Submit?”
- “How do I make a study guide from old quizzes?”

The help skill explains behavior only. A help question by itself does not authorize browser interaction, folder creation, saving, installation, or setting changes.

## Optional integrations

- **Google Drive:** enables explicitly requested Drive storage and retrieval when the current host exposes the required operations.
- **Consensus or an equivalent research connector:** may support outside scientific research when the user or form instructions permit it. It never replaces required course material or a specifically assigned source.

## Runtime requirements

- Codex, Claude Code, Gemini CLI, or Grok Build with Agent Skills support.
- A compatible browser/computer-control surface for live form work.
- A signed-in browser session for sites requiring authentication.
- Python 3 only when using the local study-memory backend.
- A callable Google Drive integration plus a connected Google account only when using the Drive backend.

## Install from the public GitHub repository

The repository is public. Friends do not need access to the owner's GitHub account. Installation syntax differs by host.

### Codex

```bash
codex plugin marketplace add luneto10/forms-responder-plugin --ref main
codex plugin add forms-responder@forms-responder
```

Start a new Codex task after installation so the bundled skills load.

In the Codex UI, after the marketplace has been added, restart Codex, open **Plugins Directory**, choose **Forms Responder**, and click **Install**. Start a new task afterward.

### Claude Code

Run these as shell commands, or use the corresponding `/plugin` commands inside Claude Code:

```bash
claude plugin marketplace add luneto10/forms-responder-plugin
claude plugin install forms-responder@forms-responder
```

Claude plugin skills use namespaced commands such as `/forms-responder:careful-form-responder`, but natural-language activation also works. Claude Desktop can browse configured marketplaces from **+ → Plugins**.

### Gemini CLI

```bash
gemini extensions install https://github.com/luneto10/forms-responder-plugin --auto-update
```

Restart Gemini CLI after installation. The root `gemini-extension.json` and `skills/` directory make the repository directly installable as one extension.

### Grok Build

Grok Build reads Claude Code plugins and marketplaces directly. If the Claude plugin is already installed, Grok can discover it without a second package format. For a local test or a Grok-only installation, clone the repository and load the shared plugin directory:

```bash
grok --plugin-dir ./plugins/forms-responder
```

For persistent use, place that plugin directory under `~/.grok/plugins/forms-responder` on macOS/Linux or `%USERPROFILE%\.grok\plugins\forms-responder` on Windows, then enable it from Grok's extensions UI.

## Update an existing installation

Installed plugin content is cached. A GitHub push does not replace the currently loaded copy inside an existing task.

```bash
codex plugin marketplace upgrade forms-responder
codex plugin add forms-responder@forms-responder
```

Then start a new task. In the UI, use **Update** if shown; otherwise reinstall Forms Responder after refreshing the marketplace.

Claude Code users run `claude plugin marketplace update forms-responder` and then `claude plugin update forms-responder@forms-responder`. Gemini users who did not enable `--auto-update` run `gemini extensions update forms-responder`. Grok users relying on the Claude installation receive the Claude-updated package; local-directory users pull the repository again and restart Grok.

## Repository structure

```text
.agents/plugins/marketplace.json
.claude-plugin/marketplace.json
gemini-extension.json
skills/                         # generated Gemini extension skills
plugins/forms-responder/
├── .codex-plugin/plugin.json
├── .claude-plugin/plugin.json
├── assets/
│   └── forms-responder-icon.png
└── skills/
    ├── careful-form-responder/
    ├── form-source-reviewer/
    ├── form-study-memory/
    │   ├── references/
    │   │   ├── google-drive-storage.md
    │   │   └── record-schema.md
    │   └── scripts/
    │       └── study_memory.py
    └── forms-responder-help/
        └── references/
            ├── capabilities-and-examples.md
            └── platform-compatibility.md
scripts/
└── sync_skill_packages.py
```

## Development validation

The package includes Codex, Claude, and Gemini manifest validation; portable skill-structure and mirror-drift checks; Python syntax; confirmed-save, refusal, search, retrieval, paired JSON/Markdown rendering, shared-ID, collision-resistance, no-index rendering, and local-save regression checks. A real Drive write is verified using Drive metadata and readable-content readback for both uploaded companions.

After changing a canonical skill under `plugins/forms-responder/skills`, regenerate and verify the cross-platform copies:

```bash
python3 scripts/sync_skill_packages.py sync
python3 scripts/sync_skill_packages.py check
```

## License

MIT
