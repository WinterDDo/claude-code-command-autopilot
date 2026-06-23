import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
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
         # use a current timestamp: a hardcoded date silently rots once it ages past
         # the 7-day session-retention window and gets pruned (flaky over time).
         "sessions": {"s%d" % i: {"last_seen": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())} for i in range(n)}}
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

    def test_first_run_arms_first_task_demo(self):
        # genuine first run (no state file -> first_run_done False): arm the flag
        run_ss(self.tmp, {"session_id": "first"})
        st = self.read_state()
        self.assertTrue(st.get("first_task_pending"), "first run arms the one-time first-task demo")
        self.assertTrue(st.get("first_run_done"))

    def test_first_task_demo_not_armed_after_first_run(self):
        run_ss(self.tmp, {"session_id": "later"}, state=state_with_sessions(1))
        self.assertFalse(self.read_state().get("first_task_pending"),
                         "the demo arms only on the very first run")


def run_ss_home(data_dir, home, payload=None, state=None):
    """Run session-start with HOME+cwd pointed at a temp dir so scan_skills and
    read_skill_overrides see only our fixtures, never the real machine."""
    data_dir, home = Path(data_dir), Path(home)
    data_dir.mkdir(parents=True, exist_ok=True)
    if state is not None:
        (data_dir / "state.json").write_text(json.dumps(state), encoding="utf-8")
    env = {**os.environ, "HOME": str(home)}
    proc = subprocess.run([sys.executable, str(SS), str(data_dir)],
                          input=json.dumps(payload or {"session_id": "x"}),
                          capture_output=True, text=True, timeout=10, env=env, cwd=str(home))
    assert proc.returncode == 0, proc.stderr
    return json.loads((data_dir / "skills-index.json").read_text())


def make_skill(home, name, desc="does a useful thing for tests", dmi=False):
    d = Path(home) / ".claude" / "skills" / name
    d.mkdir(parents=True, exist_ok=True)
    fm = "---\nname: %s\ndescription: %s\n" % (name, desc)
    if dmi:
        fm += "disable-model-invocation: true\n"
    fm += "---\n\nbody text\n"
    (d / "SKILL.md").write_text(fm, encoding="utf-8")


def write_overrides(home, overrides):
    c = Path(home) / ".claude"
    c.mkdir(parents=True, exist_ok=True)
    (c / "settings.json").write_text(json.dumps({"skillOverrides": overrides}), encoding="utf-8")


class SkillIndexTests(unittest.TestCase):
    def setUp(self):
        self.data = Path(tempfile.mkdtemp(prefix="autopilot-data-"))
        self.home = Path(tempfile.mkdtemp(prefix="autopilot-home-"))

    def tearDown(self):
        shutil.rmtree(self.data, ignore_errors=True)
        shutil.rmtree(self.home, ignore_errors=True)

    def find(self, idx, name):
        return next(s for s in idx["skills"] if s["name"] == name)

    def test_skill_parked_by_override(self):
        make_skill(self.home, "alpha-skill")
        write_overrides(self.home, {"alpha-skill": "name-only"})
        s = self.find(run_ss_home(self.data, self.home), "alpha-skill")
        self.assertTrue(s["parked"])
        self.assertEqual(s["park_reason"], "override:name-only")

    def test_skill_parked_by_frontmatter(self):
        make_skill(self.home, "beta-skill", dmi=True)
        s = self.find(run_ss_home(self.data, self.home), "beta-skill")
        self.assertTrue(s["parked"])
        self.assertEqual(s["park_reason"], "frontmatter:disable-model-invocation")

    def test_override_on_beats_frontmatter(self):
        make_skill(self.home, "gamma-skill", dmi=True)
        write_overrides(self.home, {"gamma-skill": "on"})
        self.assertFalse(self.find(run_ss_home(self.data, self.home), "gamma-skill")["parked"])

    def test_active_skill_not_parked(self):
        make_skill(self.home, "delta-skill")
        s = self.find(run_ss_home(self.data, self.home), "delta-skill")
        self.assertFalse(s["parked"])
        self.assertNotIn("park_reason", s)

    def test_budget_block_written(self):
        make_skill(self.home, "alpha-skill")
        make_skill(self.home, "beta-skill", dmi=True)
        idx = run_ss_home(self.data, self.home)
        self.assertIn("budget", idx)
        self.assertEqual(idx["budget"]["parked_count"], 1)
        self.assertIn("over_budget", idx["budget"])

    def test_headsup_fires_once(self):
        make_skill(self.home, "alpha-skill")
        env = {**os.environ, "HOME": str(self.home)}

        def run():
            proc = subprocess.run([sys.executable, str(SS), str(self.data)],
                                  input=json.dumps({"session_id": "x"}),
                                  capture_output=True, text=True, timeout=10, env=env, cwd=str(self.home))
            assert proc.returncode == 0, proc.stderr
            return json.loads(proc.stdout).get("hookSpecificOutput", {}).get("additionalContext", "")

        first, second = run(), run()
        self.assertIn("Skills Autopilot is active", first, "heads-up fires on first run")
        self.assertNotIn("Skills Autopilot is active", second, "heads-up fires only once")


if __name__ == "__main__":
    unittest.main()
