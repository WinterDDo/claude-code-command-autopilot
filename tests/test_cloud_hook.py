"""The vendored cloud hook must keep the copilot present every turn:
dual-event (UserPromptSubmit + SessionStart), cloud-aware guard, valid output."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent / "plugins" / "command-autopilot"
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
        self.assertIn("CAPABILITY CHECKPOINT", d["hookSpecificOutput"]["additionalContext"])

    def test_cloud_sessionstart_event_stamped(self):
        d = json.loads(run(event="SessionStart", remote=True))
        self.assertEqual(d["hookSpecificOutput"]["hookEventName"], "SessionStart")

    def test_local_with_plugin_stays_silent(self):
        # this machine has the plugin installed; not remote -> guard exits silent
        if not (Path.home() / ".claude" / "plugins" / "cache" / "claude-code-command-autopilot").is_dir():
            self.skipTest("plugin not installed on this machine")
        self.assertEqual(run(event="UserPromptSubmit", remote=False).strip(), "")

    def test_local_without_plugin_injects(self):
        out = run(event="UserPromptSubmit", remote=False, home=self.nohome)
        self.assertIn("CAPABILITY CHECKPOINT", json.loads(out)["hookSpecificOutput"]["additionalContext"])

    def test_cloud_injects_even_if_a_plugin_cache_somehow_exists(self):
        # remote always wins over the local-plugin guard
        out = run(event="UserPromptSubmit", remote=True)  # real HOME may have the cache
        self.assertTrue(out.strip(), "cloud must inject regardless of local plugin cache")


NUDGE_SH = PLUGIN / "cloud" / "cloud-nudge.sh"


def run_nudge(payload, remote=True, home=None, tmpdir=None):
    env = dict(os.environ)
    if remote:
        env["CLAUDE_CODE_REMOTE"] = "true"
    else:
        env.pop("CLAUDE_CODE_REMOTE", None)
    if home:
        env["HOME"] = home
    if tmpdir:
        env["TMPDIR"] = tmpdir
    p = subprocess.run(["sh", str(NUDGE_SH)], input=json.dumps(payload),
                       capture_output=True, text=True, env=env, timeout=10)
    return p.stdout


class CloudNudgeTests(unittest.TestCase):
    """The vendored cloud Layer-2 nudge (pure sh): fires on subagent / plan-exit
    in cloud, gated to the real trigger tools, once per session, silent locally."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="autopilot-cloudnudge-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_cloud_agent_fires(self):
        d = json.loads(run_nudge({"tool_name": "Agent", "session_id": "c1"}, remote=True, tmpdir=self.tmp))
        self.assertEqual(d["hookSpecificOutput"]["hookEventName"], "PostToolUse")
        self.assertIn("fan-out", d["hookSpecificOutput"]["additionalContext"])

    def test_cloud_exitplanmode_fires(self):
        self.assertIn("fan-out", run_nudge({"tool_name": "ExitPlanMode", "session_id": "c2"}, remote=True, tmpdir=self.tmp))

    def test_cloud_non_trigger_silent(self):
        # broad matcher can catch the TaskCreate family — the script must gate it out
        self.assertEqual(run_nudge({"tool_name": "TaskCreate", "session_id": "c3"}, remote=True, tmpdir=self.tmp).strip(), "")

    def test_cloud_once_per_session(self):
        self.assertIn("fan-out", run_nudge({"tool_name": "Agent", "session_id": "dup"}, remote=True, tmpdir=self.tmp))
        self.assertEqual(run_nudge({"tool_name": "Agent", "session_id": "dup"}, remote=True, tmpdir=self.tmp).strip(),
                         "", "must nudge at most once per session")

    def test_local_with_plugin_stays_silent(self):
        if not (Path.home() / ".claude" / "plugins" / "cache" / "claude-code-command-autopilot").is_dir():
            self.skipTest("plugin not installed on this machine")
        self.assertEqual(run_nudge({"tool_name": "Agent", "session_id": "c4"}, remote=False, tmpdir=self.tmp).strip(), "")


if __name__ == "__main__":
    unittest.main()
