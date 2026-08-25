import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "plugins"
    / "forms-responder"
    / "skills"
    / "form-study-memory"
    / "scripts"
    / "study_memory.py"
)
SPEC = importlib.util.spec_from_file_location("study_memory", SCRIPT_PATH)
assert SPEC and SPEC.loader
study_memory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(study_memory)


class StudyMemoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def write_record(self, confirmed=True):
        path = self.base / ("confirmed.json" if confirmed else "unconfirmed.json")
        path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "save_confirmed": confirmed,
                    "course": "BIO: 101",
                    "quiz": "Quiz/3",
                    "topics": ["cell respiration", "ATP", "atp"],
                    "summary": "The quiz focused on cellular energy transfer.",
                    "questions": [
                        {
                            "question": "Where is most ATP produced?",
                            "answer": "The inner mitochondrial membrane",
                            "why_correct": "ATP synthase is located there.",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return path

    def test_render_creates_matching_pair_without_local_index(self):
        output = self.base / "upload"
        result = study_memory.render_record_pair(output, self.write_record())

        json_path = Path(result["json_path"])
        markdown_path = Path(result["markdown_path"])
        self.assertTrue(json_path.is_file())
        self.assertTrue(markdown_path.is_file())
        self.assertEqual(json_path.stem, markdown_path.stem)
        self.assertNotIn(":", json_path.name)
        self.assertNotIn("/", json_path.name)
        self.assertFalse((output / study_memory.INDEX_FILENAME).exists())

        record = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertEqual(record["record_id"], result["record_id"])
        self.assertEqual(record["topics"], ["cell respiration", "ATP"])
        self.assertNotIn("save_confirmed", record)
        markdown = markdown_path.read_text(encoding="utf-8")
        self.assertIn(result["record_id"], markdown)
        self.assertIn("| Question | Answer | Why this is correct |", markdown)

    def test_render_refuses_unconfirmed_record_without_outputs(self):
        output = self.base / "upload"
        with self.assertRaisesRegex(study_memory.MemoryErrorWithContext, "save_confirmed"):
            study_memory.render_record_pair(output, self.write_record(confirmed=False))
        self.assertFalse(output.exists())

    def test_local_save_still_creates_pair_and_index(self):
        root = self.base / "library"
        result = study_memory.save_record(root, self.write_record())
        entry = result["record"]

        self.assertTrue((root / entry["json_path"]).is_file())
        self.assertTrue((root / entry["markdown_path"]).is_file())
        index = json.loads((root / study_memory.INDEX_FILENAME).read_text(encoding="utf-8"))
        self.assertEqual(len(index["records"]), 1)
        self.assertEqual(index["records"][0]["record_id"], entry["record_id"])

    def test_rendered_pair_uses_collision_resistant_names(self):
        output = self.base / "upload"
        first = study_memory.render_record_pair(output, self.write_record())
        second = study_memory.render_record_pair(output, self.write_record())
        self.assertNotEqual(first["record_id"], second["record_id"])
        self.assertNotEqual(first["basename"], second["basename"])

    def test_render_command_returns_upload_paths(self):
        output = self.base / "upload"
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            status = study_memory.main(
                ["render", "--input", str(self.write_record()), "--output-dir", str(output)]
            )
        result = json.loads(stdout.getvalue())
        self.assertEqual(status, 0)
        self.assertTrue(Path(result["json_path"]).is_file())
        self.assertTrue(Path(result["markdown_path"]).is_file())


if __name__ == "__main__":
    unittest.main()
