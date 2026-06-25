# Pre-PR Checklist

Copy this checklist to project root as `PR_CHECKLIST.md` (don't commit) to track Pre-PR verification.

## Usage

1. Copy to project root: `cp references/pre-pr-checklist.md ../PR_CHECKLIST.md`
2. Check each item before creating PR
3. Mark completed items with [x]
4. Don't create PR until all [ ] become [x]

---

# Pre-PR Checklist for Issue #NUMBER

## Research (Phase 5.5 Step 1)

- [ ] Read `CONTRIBUTING.md` / `AGENTS.md`
- [ ] Study 3 recent merged PRs (note format, required sections)
- [ ] Check PR template (`.github/PULL_REQUEST_TEMPLATE.md`)
- [ ] Search for duplicate PRs/Issues (use `gh issue list --search` and `gh pr list --search`)

## Code Completeness (Phase 5.5 Step 2)

### 2.1 All Paths Synced

- [ ] Searched for all prompt/contract locations: `grep -r "EXISTING_FIELD" src/`
- [ ] Updated ALL paths (non-agent, agent, multi-agent)
- [ ] Tested ALL paths

**Example** (from daily_stock_analysis):
- ✅ `src/analyzer.py` updated
- ✅ `src/agent/executor.py` updated
- ✅ `src/agent/agents/decision_agent.py` updated

### 2.2 Schema Defined

- [ ] New fields have Pydantic models in `schemas/report_schema.py`
- [ ] Fields are `Optional` for backward compatibility
- [ ] Added `model_validator` to handle edge cases:
  - [ ] String values (convert to number)
  - [ ] Negative values (clamp to 0)
  - [ ] None values (handle gracefully)
  - [ ] Sum constraints (normalize to 100 if needed)

### 2.3 Prompt Updated

- [ ] LLM prompt includes new fields with constraints
- [ ] Added "必须输出" (must output) directive
- [ ] Added detailed field descriptions (what it means, examples)

### 2.4 Display/Notification Updated

- [ ] Default report mode (`notification.py`) shows new fields
- [ ] Render mode (`templates/report_markdown.j2`) shows new fields
- [ ] Added helper functions to handle None values (avoid "None%" display)

### 2.5 i18n Updated

- [ ] Internationalization labels added (`report_language.py`)
- [ ] Both Chinese and English labels added

## Testing (Phase 5.5 Step 3)

- [ ] Unit tests added (`tests/test_FEATURE.py`)
- [ ] Tests cover:
  - [ ] Schema validation (valid/invalid inputs)
  - [ ] Field normalization (string to number, negative to 0)
  - [ ] Edge cases (None, empty, boundary values)
  - [ ] Display logic (None values, formatting)
  - [ ] i18n labels (Chinese/English)
- [ ] All tests pass: `pytest tests/test_FEATURE.py -v`

## Documentation (Phase 5.5 Step 4)

- [ ] `docs/CHANGELOG.md` updated (add entry under `[Unreleased]`)
- [ ] Follow project's changelog format (e.g., `[新功能] #NUMBER 描述`)
- [ ] Code comments added for complex logic

## Compatibility Statement (Phase 5.5 Step 5)

- [ ] PR description includes "兼容性说明" section
- [ ] Explicitly state "无 model/provider/Base URL/默认配置变更" (or list changes)
- [ ] If changes exist, provide migration guide

## CI (Phase 5.5 Step 6)

- [ ] Run project's CI script: `./scripts/ci_gate.sh` (or equivalent)
- [ ] All checks passed ✅
- [ ] Test count: M tests passed
- [ ] No new warnings or errors

## PR Description (Phase 7)

- [ ] Follow project template (from Phase 5.5 Step 1)
- [ ] All sections filled:
  - [ ] 概述 (Overview)
  - [ ] 解决的问题 (Problems solved)
  - [ ] 主要改动 (Major changes)
  - [ ] 测试 (Testing)
  - [ ] CI 检查 (CI results)
  - [ ] 兼容性说明 (Compatibility statement)
  - [ ] Checklist
  - [ ] 后续优化建议 (Future improvements)
  - [ ] 相关 Issue (Related issues)
- [ ] Reference issue: "Closes #NUMBER"

## Final Check

- [ ] No merge conflicts: `git pull upstream main`
- [ ] All commits signed off (if required)
- [ ] Branch up to date with main
- [ ] PR title follows project convention (e.g., "feat: 添加... (Issue #NUMBER)")
- [ ] PR description preview looks correct (no formatting errors)

---

## Notes

- Don't create PR until ALL items are checked
- If any item is not applicable, mark as "N/A" and explain why
- After creating PR, don't close this checklist - use it to verify fixes when reviewer raises blockers
