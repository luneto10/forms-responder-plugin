# Forms Responder Plugin

Forms Responder is a portable Codex plugin for carefully completing browser-based forms, surveys, quizzes, applications, and LMS pages.

It works sequentially through visible controls, reviews source material such as videos and readings, verifies every answer, and **never submits the form**. Final submission always remains with the user.

## Included skills

- `careful-form-responder`: completes and audits live browser forms without submitting.
- `form-source-reviewer`: reviews videos, audio, documents, slides, images, charts, and linked readings before answering source-dependent questions.

Consensus is optional. When installed separately, it may support outside scientific research only when the user or form instructions permit it. It never replaces required course or form source material.

## Requirements

- ChatGPT desktop with Codex, or Codex CLI.
- The Browser plugin or an equivalent supported browser-control surface.
- A signed-in browser session for any site that requires authentication.

## Install from GitHub

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

## Safety boundary

The plugin may fill or review a form when requested, but it must stop before any final action such as **Submit**, **Turn In**, **Send**, **Finish**, **Confirm**, or an equivalent control. It also stops for signatures, consent, payment authorization, legal attestations, CAPTCHA, and personal facts that only the user can provide.

## Repository structure

```text
.agents/plugins/marketplace.json
plugins/forms-responder/
├── .codex-plugin/plugin.json
└── skills/
    ├── careful-form-responder/
    └── form-source-reviewer/
```

## License

MIT
