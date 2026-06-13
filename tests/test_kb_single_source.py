"""Guards the single-source-of-truth invariant: hooks derive command data from
the KB, never from a hard-coded subset. If anyone reintroduces a hand-picked
list that drifts from knowledge/commands.json, these tests go red."""
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PLUGIN = REPO / "plugins" / "command-autopilot"
HOOKS = PLUGIN / "hooks"
sys.path.insert(0, str(HOOKS))
import apcommon as ap  # noqa: E402


def kb_cmds():
    return [c["cmd"] for c in json.loads((PLUGIN / "knowledge" / "commands.json").read_text(encoding="utf-8"))["commands"]]


class SingleSourceTests(unittest.TestCase):
    def test_tracker_recognizes_every_kb_command(self):
        # build the regex exactly as tracker.py does, then assert full coverage
        import re
        names = sorted(ap.kb_command_names(str(PLUGIN)), key=len, reverse=True)
        rx = re.compile(r"/(" + "|".join(re.escape(n) for n in names) + r")\b")
        missing = [c for c in kb_cmds() if not rx.search("ran " + c + " just now")]
        self.assertEqual(missing, [], "tracker must recognize EVERY KB command; drift detected")

    def test_high_leverage_pool_is_kb_derived_not_hardcoded_six(self):
        pool = ap.kb_high_leverage(str(PLUGIN))
        kb_high = [c["cmd"] for c in json.loads((PLUGIN / "knowledge" / "commands.json").read_text(encoding="utf-8"))["commands"] if c.get("leverage") == "high"]
        self.assertEqual(set(pool), set(kb_high), "power-intro pool must equal the KB's leverage=high set")
        self.assertGreater(len(pool), 6, "pool must come from the KB, not the old hard-coded 6")

    def test_kb_helpers_fall_back_without_kb(self):
        # enhancement-only: a bad path must not raise, just return a usable minimum
        self.assertTrue(ap.kb_command_names("/nonexistent/path"))
        self.assertTrue(ap.kb_high_leverage("/nonexistent/path"))


if __name__ == "__main__":
    unittest.main()
