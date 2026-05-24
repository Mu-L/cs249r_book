#!/usr/bin/env bash
# Render each vol1 inline-python chapter and scan HTML for spurious .0
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"
BUILD_DIR="book/quarto/_build/html-vol1/contents/vol1"
ARCHIVE_DIR="book/quarto/_build/html-audit/vol1"
mkdir -p "$ARCHIVE_DIR"
CHAPTERS=(
  introduction/introduction
  ml_systems/ml_systems
  ml_workflow/ml_workflow
  data_engineering/data_engineering
  nn_computation/nn_computation
  nn_architectures/nn_architectures
  frameworks/frameworks
  training/training
  data_selection/data_selection
  model_compression/model_compression
  hw_acceleration/hw_acceleration
  benchmarking/benchmarking
  model_serving/model_serving
  ml_ops/ml_ops
  responsible_engr/responsible_engr
  conclusion/conclusion
  backmatter/appendix_algorithm
  backmatter/appendix_assumptions
  backmatter/appendix_dam
  backmatter/appendix_data
  backmatter/appendix_machine
)
echo "VOL1 HTML RENDER + AUDIT"
echo "========================"
FAIL=0
for ch in "${CHAPTERS[@]}"; do
  name="${ch##*/}"
  printf "%-28s " "$name"
  if ! ./book/binder build html --vol1 "vol1/${name}" --skip-hygiene --skip-validate >/tmp/render_${name}.log 2>&1; then
    echo "BUILD FAIL (see /tmp/render_${name}.log)"
    FAIL=$((FAIL + 1))
    continue
  fi
  html="${BUILD_DIR}/${ch}.html"
  archive="${ARCHIVE_DIR}/${name}.html"
  if [[ ! -f "$html" ]]; then
    echo "HTML MISSING"
    FAIL=$((FAIL + 1))
    continue
  fi
  cp "$html" "$archive"
  result=$(python3 scripts/audit_html.py "$archive" 2>&1 || true)
  if [[ "$result" == "CLEAN" ]]; then
    echo "OK + CLEAN"
  else
    echo "OK + HTML FLAGS"
    echo "$result" | head -5
    FAIL=$((FAIL + 1))
  fi
done
echo "========================"
echo "Failed: $FAIL / ${#CHAPTERS[@]}"
exit $(( FAIL > 0 ? 1 : 0 ))
