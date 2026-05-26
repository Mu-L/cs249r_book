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
| vol1/introduction | PASS | ✓ | ✅ | 38108d00f2 |
| vol1/ml_systems | PASS | ✓ 37/37 | ✅ | 41a232b431 |
| vol1/ml_workflow | PASS | ✓ | ✅ | 5b7c5bd738 |
| vol1/data_engineering | PASS | ✓ | ✅ | 43c9567823 |
| vol1/model_serving | PASS 46/46 | ✓ 46/46 | ✅ | (committing) |
| vol1/nn_computation | PASS 30/30 | ✓ 30/30 | ✅ | (committing) |
| vol1/nn_architectures | PASS 34/34 | ✓ 34/34 | ✅ | (committing) |
| vol1/frameworks | PASS 30/30 | ✓ 30/30 | ✅ | (committing) |
| vol1/training | WIP | — | ⬜ | LLM fixes in progress |
| vol1 ch 09–21 | pending | — | ⬜ | prose-units green |
| vol2 ch 01–23 | pending | — | ⬜ | prose-units green |

**Signed off:** 7 / 44 (training + vol1 ch 09–21 pending)
**Committed this session:** 4 chapters queued (nn_computation, nn_architectures, frameworks, model_serving)

## Recent fixes

- **model_serving:** BatchingSweetspot/Optimization/BudgetCalc coherence; OUTPUT suffix sweep
- **nn_computation:** 12-class OUTPUT suffix migration
- **nn_architectures:** lighthouse + pitfall units; 80 GB nominal A100
- **frameworks:** 17-class bandwidth/memory/TFLOP/s suffixes
