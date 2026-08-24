#!/usr/bin/env python3
"""Cross-platform local storage and lookup for Forms Responder study records."""

from __future__ import print_function

import argparse
import json
import os
import re
import sys
import tempfile
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


SCHEMA_VERSION = 1
INDEX_FILENAME = "index.json"


class MemoryErrorWithContext(Exception):
    """A user-facing storage or validation error."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_root() -> Path:
    override = os.environ.get("FORMS_RESPONDER_MEMORY_DIR")
    if override:
        return Path(os.path.expandvars(os.path.expanduser(override))).resolve()

    plugin_data = os.environ.get("PLUGIN_DATA")
    if plugin_data:
        return Path(os.path.expandvars(os.path.expanduser(plugin_data))).resolve() / "study-memory"

    if os.name == "nt":
        base = (
            os.environ.get("LOCALAPPDATA")
            or os.environ.get("APPDATA")
            or os.environ.get("USERPROFILE")
        )
        if not base:
            base = str(Path.home())
        return Path(base) / "FormsResponder" / "StudyMemory"

    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "FormsResponder" / "StudyMemory"

    xdg_data = os.environ.get("XDG_DATA_HOME")
    base = Path(xdg_data) if xdg_data else Path.home() / ".local" / "share"
    return base / "forms-responder" / "study-memory"


def resolve_root(value: Optional[str]) -> Path:
    if not value:
        return default_root()
    return Path(os.path.expandvars(os.path.expanduser(value))).resolve()


def slugify(value: str, fallback: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return slug[:80] or fallback


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=str(path.parent)
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(str(temporary_path), str(path))
    except Exception:
        try:
            temporary_path.unlink()
        except OSError:
            pass
        raise


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise MemoryErrorWithContext("File not found: {0}".format(path))
    except json.JSONDecodeError as exc:
        raise MemoryErrorWithContext("Malformed JSON in {0}: {1}".format(path, exc))
    except OSError as exc:
        raise MemoryErrorWithContext("Could not read {0}: {1}".format(path, exc))


def load_index(root: Path, allow_missing: bool) -> Dict[str, Any]:
    path = root / INDEX_FILENAME
    if not path.exists():
        if allow_missing:
            return {"schema_version": SCHEMA_VERSION, "records": []}
        raise MemoryErrorWithContext("Study-memory index does not exist at {0}".format(path))

    data = load_json(path)
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        raise MemoryErrorWithContext("Unsupported or malformed study-memory index at {0}".format(path))
    if not isinstance(data.get("records"), list):
        raise MemoryErrorWithContext("Study-memory index records must be an array at {0}".format(path))
    return data


def clean_required_string(data: Dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise MemoryErrorWithContext("Record field '{0}' must be a non-empty string".format(key))
    return value.strip()


def clean_optional_string(data: Dict[str, Any], key: str) -> str:
    value = data.get(key, "")
    if value is None:
        return ""
    if not isinstance(value, str):
        raise MemoryErrorWithContext("Record field '{0}' must be a string when present".format(key))
    return value.strip()


def validate_record(raw: Any) -> Dict[str, Any]:
    if not isinstance(raw, dict):
        raise MemoryErrorWithContext("Study record must be a JSON object")
    if raw.get("save_confirmed") is not True:
        raise MemoryErrorWithContext("Refusing to save: save_confirmed must be true")
    if raw.get("schema_version", SCHEMA_VERSION) != SCHEMA_VERSION:
        raise MemoryErrorWithContext("Unsupported study record schema_version")

    topics_raw = raw.get("topics")
    if not isinstance(topics_raw, list) or not topics_raw:
        raise MemoryErrorWithContext("Record field 'topics' must be a non-empty array")
    topics: List[str] = []
    topic_keys = set()
    for value in topics_raw:
        if not isinstance(value, str) or not value.strip():
            raise MemoryErrorWithContext("Every topic must be a non-empty string")
        cleaned = value.strip()
        if cleaned.casefold() not in topic_keys:
            topics.append(cleaned)
            topic_keys.add(cleaned.casefold())

    questions_raw = raw.get("questions")
    if not isinstance(questions_raw, list) or not questions_raw:
        raise MemoryErrorWithContext("Record field 'questions' must be a non-empty array")
    questions: List[Dict[str, str]] = []
    for position, item in enumerate(questions_raw, start=1):
        if not isinstance(item, dict):
            raise MemoryErrorWithContext("Question {0} must be an object".format(position))
        questions.append(
            {
                "question": clean_required_string(item, "question"),
                "answer": clean_required_string(item, "answer"),
                "why_correct": clean_required_string(item, "why_correct"),
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "course": clean_required_string(raw, "course"),
        "quiz": clean_required_string(raw, "quiz"),
        "topics": topics,
        "summary": clean_required_string(raw, "summary"),
        "source_url": clean_optional_string(raw, "source_url"),
        "notes": clean_optional_string(raw, "notes"),
        "completed_at": clean_optional_string(raw, "completed_at"),
        "questions": questions,
    }


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def render_markdown(record: Dict[str, Any]) -> str:
    lines = [
        "# {0}: {1}".format(record["course"], record["quiz"]),
        "",
        "- Record ID: `{0}`".format(record["record_id"]),
        "- Saved: {0}".format(record["saved_at"]),
        "- Completed: {0}".format(record["completed_at"] or "Not recorded"),
        "- Topics: {0}".format(", ".join(record["topics"])),
    ]
    if record["source_url"]:
        lines.append("- Source: {0}".format(record["source_url"]))
    lines.extend(["", "## Summary", "", record["summary"], "", "## Questions", ""])
    lines.extend(["| Question | Answer | Why this is correct |", "|---|---|---|"])
    for item in record["questions"]:
        lines.append(
            "| {0} | {1} | {2} |".format(
                markdown_cell(item["question"]),
                markdown_cell(item["answer"]),
                markdown_cell(item["why_correct"]),
            )
        )
    if record["notes"]:
        lines.extend(["", "## Notes", "", record["notes"]])
    lines.append("")
    return "\n".join(lines)


def save_record(root: Path, input_path: Path) -> Dict[str, Any]:
    validated = validate_record(load_json(input_path))
    saved_at = utc_now()
    record_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    validated["record_id"] = record_id
    validated["saved_at"] = saved_at
    if not validated["completed_at"]:
        validated["completed_at"] = saved_at

    course_slug = slugify(validated["course"], "course")
    quiz_slug = slugify(validated["quiz"], "quiz")
    relative_base = Path("records") / course_slug / quiz_slug / record_id
    json_path = root / relative_base.with_suffix(".json")
    markdown_path = root / relative_base.with_suffix(".md")

    index = load_index(root, allow_missing=True)
    atomic_write_text(json_path, json.dumps(validated, ensure_ascii=False, indent=2) + "\n")
    atomic_write_text(markdown_path, render_markdown(validated))

    entry = {
        "record_id": record_id,
        "course": validated["course"],
        "quiz": validated["quiz"],
        "topics": validated["topics"],
        "summary": validated["summary"],
        "completed_at": validated["completed_at"],
        "saved_at": saved_at,
        "json_path": json_path.relative_to(root).as_posix(),
        "markdown_path": markdown_path.relative_to(root).as_posix(),
    }
    index["records"].append(entry)
    index["records"].sort(key=lambda item: item.get("saved_at", ""), reverse=True)
    atomic_write_text(root / INDEX_FILENAME, json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    return {"record": entry, "root": str(root), "markdown_path": str(markdown_path)}


def contains(value: Any, needle: Optional[str]) -> bool:
    if not needle:
        return True
    if isinstance(value, list):
        value = " ".join(str(item) for item in value)
    return needle.casefold() in str(value).casefold()


def read_indexed_record(root: Path, entry: Dict[str, Any]) -> Dict[str, Any]:
    relative = entry.get("json_path")
    if not isinstance(relative, str) or not relative:
        raise MemoryErrorWithContext("Index entry {0} has no JSON path".format(entry.get("record_id", "unknown")))
    path = (root / relative).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        raise MemoryErrorWithContext("Index entry points outside the study-memory root")
    data = load_json(path)
    if not isinstance(data, dict):
        raise MemoryErrorWithContext("Stored record is not an object: {0}".format(path))
    return data


def find_records(root: Path, args: argparse.Namespace) -> List[Dict[str, Any]]:
    index = load_index(root, allow_missing=False)
    matches: List[Dict[str, Any]] = []
    for entry in index["records"]:
        if not contains(entry.get("course", ""), args.course):
            continue
        if not contains(entry.get("quiz", ""), args.quiz):
            continue
        if not contains(entry.get("topics", []), args.topic):
            continue
        record = read_indexed_record(root, entry)
        if args.query:
            searchable = json.dumps(record, ensure_ascii=False, sort_keys=True)
            if not contains(searchable, args.query):
                continue
        matches.append(record)
    matches.sort(key=lambda item: item.get("saved_at", ""), reverse=True)
    return matches[: args.limit]


def metadata_view(record: Dict[str, Any], root: Path) -> Dict[str, Any]:
    record_id = str(record.get("record_id", ""))
    course_slug = slugify(str(record.get("course", "")), "course")
    quiz_slug = slugify(str(record.get("quiz", "")), "quiz")
    markdown_path = root / "records" / course_slug / quiz_slug / (record_id + ".md")
    return {
        "record_id": record_id,
        "course": record.get("course", ""),
        "quiz": record.get("quiz", ""),
        "topics": record.get("topics", []),
        "summary": record.get("summary", ""),
        "saved_at": record.get("saved_at", ""),
        "markdown_path": str(markdown_path),
    }


def add_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--course", help="Case-insensitive course filter")
    parser.add_argument("--quiz", help="Case-insensitive quiz or assignment filter")
    parser.add_argument("--topic", help="Case-insensitive topic filter")
    parser.add_argument("--query", help="Case-insensitive full-record search")
    parser.add_argument("--limit", type=int, default=50, help="Maximum records to return")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="Override the study-memory root directory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("root", help="Print the resolved study-memory root")

    save_parser = subparsers.add_parser("save", help="Save a confirmed study record")
    save_parser.add_argument("--input", required=True, help="Path to a UTF-8 record JSON file")

    search_parser = subparsers.add_parser("search", help="Search saved record metadata")
    add_filters(search_parser)

    context_parser = subparsers.add_parser("context", help="Return full records for study synthesis")
    add_filters(context_parser)

    show_parser = subparsers.add_parser("show", help="Show one saved record")
    show_parser.add_argument("record_id")
    show_parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    return parser


def show_record(root: Path, record_id: str, output_format: str) -> str:
    index = load_index(root, allow_missing=False)
    for entry in index["records"]:
        if entry.get("record_id") != record_id:
            continue
        if output_format == "json":
            return json.dumps(read_indexed_record(root, entry), ensure_ascii=False, indent=2)
        relative = entry.get("markdown_path")
        if not isinstance(relative, str) or not relative:
            raise MemoryErrorWithContext("Record has no Markdown path")
        path = (root / relative).resolve()
        try:
            path.relative_to(root.resolve())
        except ValueError:
            raise MemoryErrorWithContext("Record points outside the study-memory root")
        try:
            return path.read_text(encoding="utf-8")
        except OSError as exc:
            raise MemoryErrorWithContext("Could not read {0}: {1}".format(path, exc))
    raise MemoryErrorWithContext("No study record found with ID {0}".format(record_id))


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = resolve_root(args.root)

    try:
        if args.command == "root":
            print(root)
            return 0
        if args.command == "save":
            result = save_record(root, Path(args.input).resolve())
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if args.command in ("search", "context"):
            if args.limit < 1:
                raise MemoryErrorWithContext("--limit must be at least 1")
            records = find_records(root, args)
            output = records if args.command == "context" else [metadata_view(item, root) for item in records]
            if args.json:
                print(json.dumps(output, ensure_ascii=False, indent=2))
            elif not output:
                print("No matching study records.")
            else:
                for item in output:
                    print(
                        "{0} | {1} | {2} | {3}".format(
                            item.get("record_id", ""),
                            item.get("course", ""),
                            item.get("quiz", ""),
                            ", ".join(item.get("topics", [])),
                        )
                    )
            return 0
        if args.command == "show":
            print(show_record(root, args.record_id, args.format))
            return 0
    except MemoryErrorWithContext as exc:
        print("Error: {0}".format(exc), file=sys.stderr)
        return 2
    except OSError as exc:
        print("Error: storage operation failed: {0}".format(exc), file=sys.stderr)
        return 2

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
