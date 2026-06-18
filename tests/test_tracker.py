import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TRACKER = REPO / "plugins" / "command-autopilot" / "hooks" / "tracker.py"


def run_tracker(data_dir, payload, submode):
    proc = subprocess.run(
        [sys.executable, str(TRACKER), str(data_dir), submode],
        input=json.dumps(payload), capture_output=True, text=True, timeout=10)
    assert proc.returncode == 0, proc.stderr
    return proc


TRANSCRIPT_LINES = [
    {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "EnterPlanMode", "input": {}}]}},
    {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "AskUserQuestion",
        "input": {"questions": [{"question": "topic switch", "options": [{"label": "/clear fresh start"}, {"label": "continue here"}]}]}}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result",
        "content": "Your questions have been answered: choice=\"/clear fresh start\""}]}},
    {"type": "assistant", "message": {"content": [{"type": "text", "text": "Done. Tip: /btw keeps side questions out of history."}]}},
    {"type": "user", "message": {"content": "I pressed Esc twice and used /rewind, worked great"}},
]


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="autopilot-test-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def state(self):
        return json.loads((self.tmp / "state.json").read_text())

    def test_skill_invocation_recorded(self):
        run_tracker(self.tmp, {"session_id": "s1", "tool_input": {"skill": "pdf"}}, "skill")
        state = self.state()
        self.assertEqual(state["counters"]["skills"]["pdf"]["invoked"], 1)
        events = (self.tmp / "events.jsonl").read_text()
        self.assertIn("skill_invoked", events)
        self.assertEqual(state["milestones"].get("first_skill_auto_used"), "pending")

    def test_stop_scan_full_pipeline(self):
        transcript = self.tmp / "transcript.jsonl"
        transcript.write_text("\n".join(json.dumps(l) for l in TRANSCRIPT_LINES), encoding="utf-8")
        run_tracker(self.tmp, {"session_id": "s2", "transcript_path": str(transcript)}, "stop")
        state = self.state()
        cmds = state["counters"]["commands"]
        self.assertEqual(cmds["/clear"]["suggested"], 1)
        self.assertEqual(cmds["/clear"]["accepted"], 1)
        self.assertNotIn("self_used", cmds["/clear"],
                         "tool_result content must never count as user self-use")
        self.assertEqual(cmds["/rewind"]["self_used"], 1)
        # prose markers must NOT be counted as teaching: the fixture's
        # "Tip: /btw ..." assistant line must produce no habit tip event.
        self.assertNotIn("btw", state["counters"].get("habits", {}),
                         "discussing a command in prose must never count as a habit tip")
        self.assertEqual(state["milestones"].get("first_auto_plan_mode"), "pending")
        events = (self.tmp / "events.jsonl").read_text()
        self.assertIn("value_auto_plan_mode", events)
        self.assertIn("suggestion_accepted", events)

    def test_new_answer_phrasing_counts_as_accepted(self):
        lines = [
            TRANSCRIPT_LINES[1],
            {"type": "user", "message": {"content": [{"type": "tool_result",
                "content": "User has answered your questions: choice=\"/clear fresh start\""}]}},
        ]
        transcript = self.tmp / "transcript.jsonl"
        transcript.write_text("\n".join(json.dumps(l) for l in lines), encoding="utf-8")
        run_tracker(self.tmp, {"session_id": "s5", "transcript_path": str(transcript)}, "stop")
        self.assertEqual(self.state()["counters"]["commands"]["/clear"]["accepted"], 1)

    def test_stop_scan_is_incremental(self):
        transcript = self.tmp / "transcript.jsonl"
        transcript.write_text("\n".join(json.dumps(l) for l in TRANSCRIPT_LINES), encoding="utf-8")
        payload = {"session_id": "s3", "transcript_path": str(transcript)}
        run_tracker(self.tmp, payload, "stop")
        run_tracker(self.tmp, payload, "stop")  # second run, no new bytes
        self.assertEqual(self.state()["counters"]["commands"]["/clear"]["suggested"], 1,
                         "re-running on an unchanged transcript must not double count")
        # append new content: only the appended part is scanned
        with open(transcript, "a", encoding="utf-8") as fh:
            fh.write("\n" + json.dumps({"type": "user", "message": {"content": "I ran /compact just now"}}))
        run_tracker(self.tmp, payload, "stop")
        state = self.state()
        self.assertEqual(state["counters"]["commands"]["/compact"]["self_used"], 1)
        self.assertEqual(state["counters"]["commands"]["/clear"]["suggested"], 1,
                         "appended-bytes rescan must not recount old content")

    def test_first_task_demo_disarmed_when_menu_fires(self):
        transcript = self.tmp / "transcript.jsonl"
        transcript.write_text("\n".join(json.dumps(l) for l in TRANSCRIPT_LINES), encoding="utf-8")
        (self.tmp / "state.json").write_text(json.dumps({
            "schema": 1,
            "config": {"aggressiveness": "teaching", "language": "en",
                       "enable_plan_gate": True, "muted": False},
            "first_task_pending": True}), encoding="utf-8")
        run_tracker(self.tmp, {"session_id": "s9", "transcript_path": str(transcript)}, "stop")
        self.assertFalse(self.state().get("first_task_pending"),
                         "a fired menu (suggestion_made) must disarm the one-time first-task demo")

    def test_missing_transcript_is_silent(self):
        run_tracker(self.tmp, {"session_id": "s4", "transcript_path": "/nonexistent/x.jsonl"}, "stop")
        self.assertTrue((self.tmp / "state.json").exists())


if __name__ == "__main__":
    unittest.main()
