# Forms Responder capabilities and examples

Use the sections relevant to the user's help question. Do not overwhelm a user who asked about only one feature.

## Typical form session

1. The user opens the form in the connected browser and asks Forms Responder to help.
2. The responder reads the complete prompt and all answer options before interacting.
3. When a question cites a video, reading, image, chart, slide deck, or document, the source reviewer inspects the actual source before answering.
4. The responder interacts with one visible control at a time and confirms the visible result.
5. It preserves the question, answer, reason, and interaction status in an internal conversation ledger.
6. It performs two review passes from that ledger. It returns to the UI only for a specific discrepancy.
7. It leaves the final action untouched and presents the answer table.
8. It may propose a class, quiz, and topics for study memory, but it saves only after confirmation.

## Example completion handoff

```text
| Question | Answer | Why this is correct |
|---|---|---|
| Where does glycolysis occur? | Cytoplasm | Glycolysis occurs in the cytosol. |
| What is the final electron acceptor? | Oxygen | Oxygen accepts electrons at the end of the transport chain. |

Nothing was submitted. The Submit button remains for you.

Save this locally under BIO 101 → Quiz 3 with topics cellular respiration and ATP,
or change the class, quiz, topics, or storage choice?
```

## Prompt examples

### Answer or review a form

- “Complete this form carefully and stop before Submit.”
- “Review the answers already entered, explain any corrections, and do not submit.”
- “Answer this Canvas quiz. Use the linked reading as evidence.”

### Source-dependent questions

- “Watch the required video before answering the questions.”
- “Read the attached PDF and use only that source for the quiz.”
- “Inspect the chart carefully and explain why each selected answer is correct.”

### Intermediate user action

- “When the page requires my personal choice, wait for me and resume when the next section appears.”

### Local study memory

- “Save this locally under CHEM 101, Chapter 4 Quiz.”
- “Find my local quizzes about covalent bonds.”
- “Make an exam review from my saved CHEM 101 records.”

### Google Drive study memory

- “Save this quiz to Google Drive in my BIO 101 folder. Do not keep a local copy.”
- “Use this Google Drive folder for the matching JSON and Markdown study record: `<folder URL>`.”
- “Find my Forms Responder records in Google Drive about ATP.”
- “Create a study guide from the quizzes in my Google Drive `PSYC 101` folder.”

## Storage comparison

| Choice | Activation | Saved artifacts | Lookup | Duplicate behavior |
|---|---|---|---|---|
| Local | Default when Drive is not named | Markdown, JSON, local index | Local course, quiz, topic, or text search | Local only |
| Google Drive | User explicitly says Google Drive | Matching JSON and Markdown files in the confirmed Drive folder | JSON-first Drive lookup with Markdown fallback | No persistent local copy |

## Troubleshooting

- **No browser capability:** Explain that a supported browser-control plugin or surface is required for live form interaction.
- **Google Drive unavailable:** Tell the user to install, enable, or connect a callable Google Drive integration in the current host. Preserve the unsaved record and do not fall back to local storage without permission.
- **Several folders have the same name:** Ask the user to choose using folder links or paths.
- **The form asks for a signature, consent, personal experience, or CAPTCHA:** Leave it for the user.
- **The user asks whether the form was submitted:** State the observed status accurately; Forms Responder is designed to leave submission untouched.
- **A source cannot be reviewed:** Say what could not be accessed and do not pretend its content was reviewed.

## Optional plugins

- A callable Google Drive connector enables explicit cloud study-memory storage and retrieval.
- Consensus or an equivalent research connector may support outside scientific research when outside research is allowed. It never replaces required course material or a source the form specifically requires.
