# LEGO Unit Migration Journal

| Phase | Status | Commit SHA | Notes |
|-------|--------|------------|-------|
| P0 foundation | done | 3bb5d63–3250400 | fmt_qty, linters, journal |
| vol2 prose-units | done | 14fd7a535a | 14 files, 0 violations |
| Corpus equations | done | — | green |
| Corpus prose-units | done | 14fd7a535a | vol1 + vol2 |

## Chapters (14-step gate)

| Chapter | Step 11 LLM | Steps 8–10 | Sign-off | Commit |
|---------|-------------|------------|----------|--------|
| vol1/introduction | PASS | ✓ 27/27 | ✅ | 38108d00f2 |
| vol1/ml_systems | PASS | ✓ 37/37 | ✅ | 41a232b431 |
| vol1/ml_workflow | PASS | ✓ 10/10 | ✅ | 5b7c5bd738 |
| vol1/data_engineering | PASS | ✓ 32/32 | ✅ | 43c9567823 |
| vol1/nn_computation | PASS | ✓ 30/30 | ✅ | 3b6c7e60cf |
| vol1/nn_architectures | PASS | ✓ 34/34 | ✅ | d4553a442e |
| vol1/frameworks | PASS | ✓ 30/30 | ✅ | a67ffeb8cc |
| vol1/model_serving | PASS | ✓ 46/46 | ✅ | 2afd342f1f |
| vol1/training | 1 warn* | ✓ 49/49 | ⬜ | uncommitted WIP |
| vol1/data_selection | — | — | ⬜ | prose-units green |
| vol1/model_compression | — | — | ⬜ | prose-units green |
| vol1/hw_acceleration | — | — | ⬜ | prose-units green |
| vol1/benchmarking | — | — | ⬜ | prose-units green |
| vol1/ml_ops | — | — | ⬜ | prose-units green |
| vol1/responsible_engr | — | — | ⬜ | prose-units green |
| vol1/conclusion | — | — | ⬜ | prose-units green |
| vol1/appendix_* (5) | — | — | ⬜ | prose-units green |
| vol2 ch 01–23 | — | — | ⬜ | prose-units green (`14fd7a5`) |

\* `GPT2Compute` L524 — attention W_O / total FLOPs; blocks `--fail-on-warn` only.

**Signed off:** 8 / 44
**In flight:** vol1/training (commit pending)
**Next (book order):** training commit → vol1/data_selection

## Recent fixes

- **training:** fmt suffix sweep (49 cells); 80 GiB A100 / 32 GiB V100 nominal; batch-4 walkthrough vs batch-32 summary aligned
- **model_serving:** fallacy pitfall suffixes; CapacityPlanning × operator; 46/46
- **frameworks:** bandwidth/memory/TFLOP/s suffixes; 30/30
- **nn_architectures:** lighthouse + pitfall units; 34/34
- **nn_computation:** 12-class OUTPUT suffix migration; 30/30
