import json
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROUTER = REPO / "plugins" / "skill-autopilot" / "hooks" / "router.py"


def run_router(data_dir, payload=None, state=None, learned=None):
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    if state is not None:
        (data_dir / "state.json").write_text(
            state if isinstance(state, str) else json.dumps(state), encoding="utf-8")
    if learned is not None:
        (data_dir / "learned.json").write_text(json.dumps(learned), encoding="utf-8")
    start = time.time()
    proc = subprocess.run(
        [sys.executable, str(ROUTER), str(data_dir)],
        input=json.dumps(payload or {"session_id": "test0001", "prompt": "hi"}),
        capture_output=True, text=True, timeout=10)
    elapsed = time.time() - start
    return json.loads(proc.stdout), elapsed


def base_state(**config):
    state = {
        "schema": 1,
        "config": {"aggressiveness": "teaching", "language": "en",
                   "enable_plan_gate": True, "muted": False},
    }
    state["config"].update(config)
    return state


def context_of(output):
    return output.get("hookSpecificOutput", {}).get("additionalContext", "")


def write_index(data_dir, skills, budget=None):
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    (Path(data_dir) / "skills-index.json").write_text(
        json.dumps({"generated": "2026-01-01T00:00:00Z", "budget": budget or {}, "skills": skills}),
        encoding="utf-8")


class RouterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="autopilot-test-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_fresh_install_teaching_mode(self):
        out, elapsed = run_router(self.tmp)
        ctx = context_of(out)
        self.assertIn("[AUTOPILOT]", ctx)
        self.assertIn("EnterPlanMode", ctx)
        self.assertIn("BETTER-MOVE CHECK", ctx, "unlock track present in teaching mode")
        self.assertNotIn("never quote or mention", ctx, "secrecy framing must be gone")
        self.assertIn("honestly", ctx, "transparency-when-asked must be present")
        self.assertNotIn("observed behavior", ctx, "cold start must have no evidence digest")
        self.assertNotIn("#=SECTION", ctx, "section markers must not leak")
        self.assertLess(elapsed, 1.0)

    def test_token_budget(self):
        out, _ = run_router(self.tmp)
        # ceiling ~500 tokens (the capability checkpoint is the core value;
        # README's Honest-cost section advertises 300–500 accordingly)
        self.assertLess(len(context_of(out)), 2500)

    def test_muted_emits_nothing(self):
        out, _ = run_router(self.tmp, state=base_state(muted=True))
        self.assertEqual(out, {})

    def test_quiet_drops_unlock_keeps_core_and_safety(self):
        out, _ = run_router(self.tmp, state=base_state(aggressiveness="quiet"))
        ctx = context_of(out)
        self.assertIn("[AUTOPILOT]", ctx)
        self.assertIn("/rewind", ctx, "safety net must survive quiet mode")
        self.assertIn("DISCIPLINE", ctx, "core discipline must survive quiet mode")
        self.assertNotIn("BETTER-MOVE CHECK", ctx, "unlock track dropped in quiet mode")
        self.assertNotIn("MATERIALLY BETTER", ctx)

    def test_zh_language(self):
        out, _ = run_router(self.tmp, state=base_state(language="zh"))
        self.assertIn("计划模式", context_of(out))  # zh-only rendering of plan mode

    def test_plan_gate_off(self):
        out, _ = run_router(self.tmp, state=base_state(enable_plan_gate=False))
        self.assertNotIn("EnterPlanMode", context_of(out))

    def test_corrupt_state_self_heals(self):
        out, _ = run_router(self.tmp, state="{not valid json!!!")
        self.assertIn("[AUTOPILOT]", context_of(out))
        bad = list(self.tmp.glob("state.json.bad-*"))
        self.assertTrue(bad, "corrupt state should be preserved as .bad-*")

    def test_evidence_digest_appears(self):
        state = base_state()
        state["counters"] = {"commands": {"/clear": {"suggested": 2, "dismissed": 2, "last": "2026-06-10T00:00:00Z"}},
                             "skills": {}, "habits": {}}
        out, _ = run_router(self.tmp, state=state)
        ctx = context_of(out)
        self.assertIn("EVIDENCE", ctx)
        self.assertIn("/clear", ctx)
        self.assertIn("dismissed 2", ctx)

    def test_learned_rules_capped_at_five(self):
        learned = {"rules": [{"text": "rule %d" % i, "evidence": i, "status": "in_force"} for i in range(1, 8)]}
        out, _ = run_router(self.tmp, learned=learned)
        ctx = context_of(out)
        self.assertIn("LEARNED", ctx)
        self.assertEqual(sum(1 for line in ctx.splitlines() if line.startswith("- rule")), 5)
        self.assertIn("rule 7", ctx, "highest-evidence rules win")
        self.assertNotIn("rule 1 ", ctx)

    def test_canary_written(self):
        run_router(self.tmp, payload={"session_id": "canary99", "prompt": "x"})
        state = json.loads((self.tmp / "state.json").read_text())
        self.assertEqual(state["last_fired"]["session_id"], "canary99")

    def test_first_task_pending_injects_welcome(self):
        state = base_state()
        state["first_task_pending"] = True
        out, _ = run_router(self.tmp, state=state)
        self.assertIn("FIRST TASK ONLY", context_of(out),
                      "an armed first-task demo must inject the forced welcome menu")

    def test_no_welcome_in_steady_state(self):
        out, _ = run_router(self.tmp)
        self.assertNotIn("FIRST TASK ONLY", context_of(out),
                         "the forced welcome must never appear once the flag is clear")

    def test_unified_toolset_rule_present(self):
        # the always-on unified rule: skills + commands as ONE toolset (no code WHICH)
        out, _ = run_router(self.tmp)
        ctx = context_of(out)
        self.assertIn("ONE toolset", ctx, "the unified skills+commands rule must be present in teaching mode")
        self.assertIn("installed skills", ctx)
        self.assertNotIn("classify", ctx)

    def test_relevant_skill_surfaced(self):
        write_index(self.tmp, [
            {"name": "contract-risk-extraction", "description": "review contracts for risk", "parked": True},
            {"name": "algorithmic-art", "description": "generative art with p5", "parked": False}])
        ctx = context_of(run_router(self.tmp, payload={"session_id": "s", "prompt": "please review this contract for risks"})[0])
        self.assertIn("RELEVANT SKILL NAMES", ctx, "relevant skills must surface when the prompt overlaps")
        self.assertIn("contract-risk-extraction", ctx)
        self.assertNotIn("algorithmic-art", ctx, "an unrelated skill must not be surfaced")
        self.assertIn("MIGHT FIT", ctx, "the §skills rule must be present")

    def test_nothing_surfaced_when_irrelevant(self):
        write_index(self.tmp, [{"name": "contract-risk-extraction", "description": "review contracts", "parked": True}])
        ctx = context_of(run_router(self.tmp, payload={"session_id": "s", "prompt": "hello there friend"})[0])
        self.assertNotIn("RELEVANT SKILL NAMES", ctx, "no overlap → inject nothing (don't train blindness)")
        self.assertNotIn("MIGHT FIT", ctx)

    def test_surfaced_names_capped(self):
        write_index(self.tmp, [{"name": "contract-skill-%02d" % i, "description": "contract review risk", "parked": True}
                               for i in range(20)])
        ctx = context_of(run_router(self.tmp, payload={"session_id": "s", "prompt": "review this contract risk"})[0])
        line = [l for l in ctx.splitlines() if l.startswith("RELEVANT SKILL NAMES")][0]
        self.assertLessEqual(line.count("contract-skill-"), 8, "surfaced names are capped at SURFACE_MAX")

    def test_surfacing_dropped_in_quiet(self):
        write_index(self.tmp, [{"name": "contract-risk-extraction", "description": "review contracts", "parked": True}])
        ctx = context_of(run_router(self.tmp, state=base_state(aggressiveness="quiet"),
                                    payload={"session_id": "s", "prompt": "review this contract"})[0])
        self.assertNotIn("RELEVANT SKILL NAMES", ctx, "surfacing is dropped in quiet mode")

    def test_suppress_on_repeat(self):
        write_index(self.tmp, [{"name": "contract-risk-extraction", "description": "review contracts", "parked": True}])
        p = {"session_id": "s", "prompt": "review this contract for risk"}
        first = context_of(run_router(self.tmp, payload=p)[0])
        second = context_of(run_router(self.tmp, payload=p)[0])
        self.assertIn("contract-risk-extraction", first)
        self.assertNotIn("RELEVANT SKILL NAMES", second, "identical relevant slice must not re-inject next turn")

    def test_token_budget_with_surfacing(self):
        # Steady state with no relevant match stays < 2500 (test_token_budget). When
        # skills do surface, the payload (rule + <=8 names) adds a bounded amount.
        write_index(self.tmp, [{"name": "contract-skill-%02d" % i, "description": "contract review risk", "parked": True}
                               for i in range(20)])
        out, _ = run_router(self.tmp, payload={"session_id": "s", "prompt": "review this contract risk"})
        self.assertLess(len(context_of(out)), 3000, "surfacing payload must stay bounded")

    def test_garbage_stdin_still_outputs(self):
        proc = subprocess.run([sys.executable, str(ROUTER), str(self.tmp)],
                              input="not json at all", capture_output=True, text=True, timeout=10)
        self.assertEqual(proc.returncode, 0)
        json.loads(proc.stdout)


if __name__ == "__main__":
    unittest.main()
