# Study record schema

Prepare a UTF-8 JSON object with this shape before calling `study_memory.py save`:

```json
{
  "schema_version": 1,
  "save_confirmed": true,
  "course": "BIO 101",
  "quiz": "Quiz 3",
  "topics": ["cell respiration", "ATP"],
  "summary": "The quiz focused on energy transfer during cellular respiration.",
  "source_url": "https://example.edu/courses/123/quizzes/456",
  "questions": [
    {
      "question": "Where is most ATP produced?",
      "answer": "The inner mitochondrial membrane",
      "why_correct": "The electron transport chain and ATP synthase are located there."
    }
  ],
  "notes": "Optional non-sensitive study note."
}
```

## Required fields

- `save_confirmed`: must be the JSON boolean `true`; the save command refuses any other value.
- `course`: confirmed class or course label.
- `quiz`: confirmed quiz, exam, assignment, survey, or form label.
- `topics`: non-empty array of confirmed topic strings.
- `summary`: brief study-oriented summary.
- `questions`: non-empty array. Every item must contain non-empty `question`, `answer`, and `why_correct` strings.

## Optional fields

- `schema_version`: defaults to `1`; no other version is currently accepted.
- `source_url`: visible page URL when it is useful and non-sensitive.
- `notes`: non-sensitive context useful for later study.
- `completed_at`: ISO 8601 timestamp. The save time is used when omitted.

The script adds `record_id` and `saved_at`. The `save` command writes a canonical JSON record and a human-readable Markdown record, then adds metadata to the local `index.json`.

For Google Drive, use `render --input <record.json> --output-dir <temporary-directory>`. It validates the same schema and creates a matching JSON/Markdown pair with one record ID and basename, but it does not create or modify a local study index. Upload both files and remove the temporary pair only after both Drive items are verified.

Do not include credentials, authentication codes, cookies, student IDs, signatures, payment data, hidden fields, raw page HTML, or unrelated personal information.
