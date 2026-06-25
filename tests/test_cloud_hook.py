"""The vendored cloud hook must keep the copilot present every turn:
dual-event (UserPromptSubmit + SessionStart), cloud-aware guard, valid output."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent / "plugins" / "skill-autopilot"
SH = PLUGIN / "cloud" / "autopilot-cloud.sh"


def run(event="UserPromptSubmit", remote=False, home=None):
    env = dict(os.environ)
    if remote:
        env["CLAUDE_CODE_REMOTE"] = "true"
    else:
        env.pop("CLAUDE_CODE_REMOTE", None)
    if home:
        env["HOME"] = home
    p = subprocess.run(["sh", str(SH), event], capture_output=True, text=True, env=env, timeout=10)
    return p.stdout


class CloudHookTests(unittest.TestCase):
    def setUp(self):
        self.nohome = tempfile.mkdtemp(prefix="autopilot-nohome-")

    def tearDown(self):
        shutil.rmtree(self.nohome, ignore_errors=True)

    def test_cloud_injects_per_prompt_with_matching_event(self):
        out = run(event="UserPromptSubmit", remote=True)
        d = json.loads(out)
        self.assertEqual(d["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        ctx = d["hookSpecificOutput"]["additionalContext"]
        self.assertIn("BETTER-MOVE CHECK", ctx)
        self.assertIn("FIRST TASK ONLY", ctx, "cloud must carry the first-task demo (no local state to gate it)")

    def test_cloud_sessionstart_event_stamped(self):
        d = json.loads(run(event="SessionStart", remote=True))
        self.assertEqual(d["hookSpecificOutput"]["hookEventName"], "SessionStart")

    def test_local_with_plugin_stays_silent(self):
        # this machine has the plugin installed; not remote -> guard exits silent
        if not (Path.home() / ".claude" / "plugins" / "cache" / "claude-code-skill-autopilot").is_dir():
            self.skipTest("plugin not installed on this machine")
        self.assertEqual(run(event="UserPromptSubmit", remote=False).strip(), "")

    def test_local_without_plugin_injects(self):
        out = run(event="UserPromptSubmit", remote=False, home=self.nohome)
        self.assertIn("BETTER-MOVE CHECK", json.loads(out)["hookSpecificOutput"]["additionalContext"])

    def test_cloud_injects_even_if_a_plugin_cache_somehow_exists(self):
        # remote always wins over the local-plugin guard
        out = run(event="UserPromptSubmit", remote=True)  # real HOME may have the cache
        self.assertTrue(out.strip(), "cloud must inject regardless of local plugin cache")


if __name__ == "__main__":
    unittest.main()
