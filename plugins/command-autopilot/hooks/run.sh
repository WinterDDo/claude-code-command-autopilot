#!/bin/sh
# Dispatcher: run.sh <mode> <data_dir>
# Finds a Python interpreter; without one, degrades to the static core rules.
MODE="$1"
DATA="$2"
DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)

case "$MODE" in
  router)        SCRIPT="router.py";        SUB="" ;;
  session-start) SCRIPT="session-start.py"; SUB="" ;;
  tracker-stop)  SCRIPT="tracker.py";       SUB="stop" ;;
  tracker-skill) SCRIPT="tracker.py";       SUB="skill" ;;
  *) exit 0 ;;
esac

# Probe that the interpreter actually runs Python 3: Windows ships fake
# python3/python store aliases that print an error and exit nonzero, and some
# Linux distros still alias python to Python 2 (which can't parse our scripts).
for PY in python3 python; do
  if command -v "$PY" >/dev/null 2>&1 && "$PY" -c 'import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)' >/dev/null 2>&1; then
    if [ -n "$SUB" ]; then
      exec "$PY" "$DIR/$SCRIPT" "$DATA" "$SUB"
    else
      exec "$PY" "$DIR/$SCRIPT" "$DATA"
    fi
  fi
done
if command -v py >/dev/null 2>&1 && py -3 -c 'import sys' >/dev/null 2>&1; then
  if [ -n "$SUB" ]; then
    exec py -3 "$DIR/$SCRIPT" "$DATA" "$SUB"
  else
    exec py -3 "$DIR/$SCRIPT" "$DATA"
  fi
fi

# No Python: stateless degradation. Core rules still reach the model.
if [ "$MODE" = "router" ]; then
  cat "$DIR/fallback-context.json"
fi
exit 0
