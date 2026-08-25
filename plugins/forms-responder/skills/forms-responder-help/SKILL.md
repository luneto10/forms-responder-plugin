---
name: forms-responder-help
description: Explain Forms Responder capabilities, safety boundaries, local and Google Drive study memory, installation requirements, and realistic usage examples. Use when a new or existing user asks what the plugin does, how to use it, what to ask, where answers are saved, or requests help or examples. Do not operate a live form from a help-only request.
---

# Forms Responder Help

Give a friendly, accurate orientation tailored to the user's question. Explain the relevant capability first, then provide one or two copyable prompts. Do not imply that a browser, Google Drive, Consensus, or another optional plugin is installed unless its capability is visible in the current environment.

Read [references/capabilities-and-examples.md](references/capabilities-and-examples.md) when the user asks for a complete overview, onboarding guide, examples, storage comparison, or troubleshooting help.

## Core explanation

Forms Responder can:

- work through browser forms, surveys, quizzes, applications, and LMS pages sequentially;
- review required videos, audio, readings, images, charts, presentations, and documents before answering;
- maintain an internal answer ledger and perform two memory-based review passes;
- pause for an intermediate user-controlled click and resume from the checkpoint;
- leave every final submission action to the user;
- produce the exact `Question | Answer | Why this is correct` summary table;
- optionally save confirmed study records locally or, only when explicitly requested, to Google Drive;
- retrieve saved records for later exam reviews.

Make the non-submission boundary prominent. Explain that the plugin does not guess personal facts, sign, consent, attest, solve CAPTCHAs, authorize payment, or press the final submission control.

## Storage explanation

- Local memory is the default when Google Drive is not named. It stores Markdown, JSON, and a searchable index in the user's application-data directory.
- Google Drive is a separate, explicit backend. The user must say Google Drive and identify or approve a destination folder. A successful Drive save creates the study document there and does not keep another persistent local copy.
- If Google Drive capability is not available or connected, state that clearly and tell the user to enable/connect the Google Drive plugin. Never claim the save succeeded and never silently switch to local storage.

## Help-only boundary

A help request explains behavior; it does not authorize opening a form, filling fields, creating folders, saving records, installing plugins, or changing settings. Perform those actions only when the user separately requests them.

When asked for a quick start, offer this prompt:

> Open the quiz in my browser, answer it carefully using any required sources, double-check from memory, and stop before submission.

When asked for Google Drive usage, offer this prompt:

> After the quiz is complete, ask me to confirm the class, quiz, topics, and Google Drive folder. Save it to Drive only after I confirm, and do not keep a local copy.
