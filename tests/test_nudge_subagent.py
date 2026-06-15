"""The PostToolUse(Agent) moment-nudge: fires once per session when a subagent is
spawned, stays silent on non-subagent tools and in quiet/mute, records an event."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NUDGE = REPO / "plugins" / "command-autopilot" / "hooks" / "nudge_subagent.py"


def run(data_dir, payload, state=None):
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    if state is not None:
        (data_dir / "state.json").write_text(json.dumps(state), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(NUDGE), str(data_dir)],
                          input=json.dumps(payload), capture_output=True, text=True, timeout=10)
    return proc.stdout


def base_state(**config):
    state = {"schema": 1, "config": {"aggressiveness": "teaching", "language": "en",
                                     "enable_plan_gate": True, "muted": False}}
    state["config"].update(config)
    return state


def ctx(out):
    if not out.strip():
        return ""
    return json.loads(out).get("hookSpecificOutput", {}).get("additionalContext", "")


class NudgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="autopilot-nudge-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_agent_tool_fires_nudge(self):
        out = run(self.tmp, {"tool_name": "Agent", "session_id": "s1"})
        d = json.loads(out)
        self.assertEqual(d["hookSpecificOutput"]["hookEventName"], "PostToolUse")
        c = d["hookSpecificOutput"]["additionalContext"]
        self.assertIn("fan-out", c)
        self.assertIn("/fork", c)

    def test_task_alias_also_fires(self):
        # the matcher is broad (Agent|Task) for version differences; both are subagents
        self.assertIn("fan-out", ctx(run(self.tmp, {"tool_name": "Task", "session_id": "s1"})))

    def test_exit_plan_mode_fires_nudge(self):
        # plan-mode exit is the second trigger: the model just planned a multi-step
        # task and is about to execute it — fire even if no subagent was ever used
        d = json.loads(run(self.tmp, {"tool_name": "ExitPlanMode", "session_id": "s1"}))
        self.assertEqual(d["hookSpecificOutput"]["hookEventName"], "PostToolUse")
        self.assertIn("fan-out", d["hookSpecificOutput"]["additionalContext"])

    def test_non_subagent_tool_is_silent(self):
        # broad matcher can catch the TaskCreate/TaskList family — script must gate it out
        self.assertEqual(run(self.tmp, {"tool_name": "TaskCreate", "session_id": "s1"}).strip(), "")
        self.assertEqual(run(self.tmp, {"tool_name": "Edit", "session_id": "s1"}).strip(), "")

    def test_once_per_session(self):
        first = run(self.tmp, {"tool_name": "Agent", "session_id": "same"})
        self.assertIn("fan-out", ctx(first))
        second = run(self.tmp, {"tool_name": "Agent", "session_id": "same"})
        self.assertEqual(second.strip(), "", "must nudge at most once per session")

    def test_new_session_fires_again(self):
        run(self.tmp, {"tool_name": "Agent", "session_id": "sessA"})
        out = run(self.tmp, {"tool_name": "Agent", "session_id": "sessB"})
        self.assertIn("fan-out", ctx(out), "a different session gets its own nudge")

    def test_quiet_mode_silent(self):
        out = run(self.tmp, {"tool_name": "Agent", "session_id": "s1"}, state=base_state(aggressiveness="quiet"))
        self.assertEqual(out.strip(), "", "unlock track is off in quiet mode")

    def test_muted_silent(self):
        out = run(self.tmp, {"tool_name": "Agent", "session_id": "s1"}, state=base_state(muted=True))
        self.assertEqual(out.strip(), "")

    def test_records_event(self):
        run(self.tmp, {"tool_name": "Agent", "session_id": "s1"})
        events = (self.tmp / "events.jsonl").read_text(encoding="utf-8")
        self.assertIn("leverage_nudge", events)

    def test_garbage_stdin_exits_clean(self):
        proc = subprocess.run([sys.executable, str(NUDGE), str(self.tmp)],
                              input="not json", capture_output=True, text=True, timeout=10)
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
