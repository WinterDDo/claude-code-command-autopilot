import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SS = REPO / "plugins" / "command-autopilot" / "hooks" / "session-start.py"


def run_ss(data_dir, payload, state=None):
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    if state is not None:
        (data_dir / "state.json").write_text(json.dumps(state), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(SS), str(data_dir)],
                          input=json.dumps(payload), capture_output=True, text=True, timeout=10)
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    return out.get("hookSpecificOutput", {}).get("additionalContext", "")


def state_with_sessions(n, **extra):
    s = {"schema": 1,
         "config": {"aggressiveness": "teaching", "language": "en", "enable_plan_gate": True, "muted": False},
         "first_run_done": True,
         "sessions": {"s%d" % i: {"last_seen": "2026-06-13T00:00:00Z"} for i in range(n)}}
    s.update(extra)
    return s


class PowerIntroTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="autopilot-ss-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def read_state(self):
        return json.loads((self.tmp / "state.json").read_text())

    def test_power_intro_fires_on_second_session_when_unused(self):
        ctx = run_ss(self.tmp, {"session_id": "new"}, state=state_with_sessions(2))
        self.assertIn("never used these high-leverage commands", ctx)
        self.assertTrue(self.read_state().get("power_intro_done"))

    def test_power_intro_does_not_fire_first_session(self):
        # genuine first session: no prior sessions; touch_session adds this one → count 1
        ctx = run_ss(self.tmp, {"session_id": "new"}, state=state_with_sessions(0))
        self.assertNotIn("high-leverage commands", ctx)
        self.assertFalse(self.read_state().get("power_intro_done"))

    def test_power_intro_fires_only_once(self):
        run_ss(self.tmp, {"session_id": "a"}, state=state_with_sessions(2))
        # second run: flag already set -> no intro
        ctx2 = run_ss(self.tmp, {"session_id": "b"})
        self.assertNotIn("never used these high-leverage commands", ctx2)

    def test_power_intro_skips_already_used_commands(self):
        # mark EVERY KB high-leverage command as used (single source of truth)
        sys.path.insert(0, str(REPO / "plugins" / "command-autopilot" / "hooks"))
        import apcommon as ap
        high = ap.kb_high_leverage(str(REPO / "plugins" / "command-autopilot"))
        st = state_with_sessions(2)
        st["counters"] = {"commands": {c: {"self_used": 1} for c in high},
                          "skills": {}, "habits": {}}
        ctx = run_ss(self.tmp, {"session_id": "new"}, state=st)
        # all high-leverage commands used -> nothing to introduce
        self.assertNotIn("never used these high-leverage commands", ctx)


if __name__ == "__main__":
    unittest.main()
