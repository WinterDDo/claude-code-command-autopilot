#!/bin/sh
# Full local test suite: unit tests + dispatcher smoke tests.
set -e
cd "$(dirname "$0")/.."
HOOKS="plugins/command-autopilot/hooks"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

echo "== unit tests =="
python3 -m unittest discover -s tests -v

echo "== smoke: dispatcher with python =="
OUT=$(printf '{"session_id":"smoke001","prompt":"hi"}' | sh "$HOOKS/run.sh" router "$TMP/data")
echo "$OUT" | grep -q "AUTOPILOT" || { echo "FAIL: router smoke"; exit 1; }
echo ok

echo "== smoke: dispatcher without python (stateless fallback) =="
NOPY="$TMP/nopy-bin"
mkdir -p "$NOPY"
for tool in cat dirname sh grep; do
  if src=$(command -v "$tool"); then
    ln -s "$src" "$NOPY/$tool"
  fi
done
OUT=$(printf '{}' | PATH="$NOPY" sh "$HOOKS/run.sh" router "$TMP/data2")
echo "$OUT" | grep -q "Stateless mode" || { echo "FAIL: no-python fallback"; exit 1; }
echo ok

echo "== smoke: garbage stdin exits 0 =="
printf 'garbage' | sh "$HOOKS/run.sh" tracker-stop "$TMP/data3" > /dev/null
echo ok

echo "ALL TESTS PASSED"
