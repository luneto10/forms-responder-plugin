# Forms Responder Plugin

Forms Responder is a portable Codex plugin for carefully completing browser-based forms, surveys, quizzes, applications, and LMS pages.

It works sequentially through visible controls, reviews source material such as videos and readings, verifies every answer, and **never submits the form**. Final submission always remains with the user.

## Included skills

- `careful-form-responder`: completes and audits live browser forms without submitting.
- `form-source-reviewer`: reviews videos, audio, documents, slides, images, charts, and linked readings before answering source-dependent questions.
- `form-study-memory`: saves user-confirmed quiz records locally, finds them by class, quiz, or topic, and retrieves them for exam study summaries.

Consensus is optional. When installed separately, it may support outside scientific research only when the user or form instructions permit it. It never replaces required course or form source material.

## Requirements

- ChatGPT desktop with Codex, or Codex CLI.
- The Browser plugin or an equivalent supported browser-control surface.
- A signed-in browser session for any site that requires authentication.
- Python 3 for the local study-memory helper (available in standard Codex desktop environments).

## Install from GitHub

This repository is public, so a friend can add it without access to your GitHub account.

Add this repository as a Codex marketplace:

```bash
codex plugin marketplace add luneto10/forms-responder-plugin --ref main
```

Then install the plugin:

```bash
codex plugin add forms-responder@forms-responder
```

Alternatively, restart the ChatGPT desktop app after adding the marketplace, open the Plugins Directory, select **Forms Responder**, and install **Forms Responder**.

Start a new chat or Codex task after installation so the bundled skills are loaded.

## Update on another computer

```bash
codex plugin marketplace upgrade forms-responder
codex plugin add forms-responder@forms-responder
```

Start a new task after reinstalling.

## Local study memory

After answering and double-checking a form, the plugin still leaves it unsubmitted and shows the required **Question / Answer / Why this is correct** table. It then infers a class, quiz or assignment, and topics and asks the user to confirm or correct those labels. Nothing is saved until the user explicitly agrees.

Each confirmed save creates an append-only JSON record, a human-readable Markdown document, and a searchable index. Later requests can find records case-insensitively by course, quiz, topic, or any text in the saved questions and answers, then use the retrieved records to prepare an exam study summary.

The default study-library location is:

- macOS: `~/Library/Application Support/FormsResponder/StudyMemory`
- Windows: `%LOCALAPPDATA%\FormsResponder\StudyMemory`
- Linux: `$XDG_DATA_HOME/forms-responder/study-memory` or `~/.local/share/forms-responder/study-memory`

Set `FORMS_RESPONDER_MEMORY_DIR` to use a different folder. A cloud-synced folder can make the same study library available on multiple computers, but the plugin never enables synchronization automatically.

## Safety boundary

The plugin may fill or review a form when requested, but it must stop before any final action such as **Submit**, **Turn In**, **Send**, **Finish**, **Confirm**, or an equivalent control. It also stops for signatures, consent, payment authorization, legal attestations, CAPTCHA, and personal facts that only the user can provide.

## Repository structure

```text
.agents/plugins/marketplace.json
plugins/forms-responder/
├── .codex-plugin/plugin.json
├── assets/
│   └── forms-responder-icon.png
└── skills/
    ├── careful-form-responder/
    ├── form-source-reviewer/
    └── form-study-memory/
```

## License

MIT
