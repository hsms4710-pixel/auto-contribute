---
name: pr-contribute
description: Open-source PR contribution workflow. Use when user wants to contribute to open-source projects, submit PRs, or find contributable issues. Enforces code verification, local CI checks, and user approval before PR submission. Includes pre-PR checklist, research standards, and common pitfalls.
agent_created: true
---

# PR Contribute Skill

Automate open-source contributions with verification and approval gates.

## Core Principles

1. **🚨 User must manually test** - Unit tests passing ≠ verification complete. User must test in real environment.
2. **🚨 Check for existing PRs/Issues** - Before starting, search if issue already has PRs. Skip if exists.
3. **🚨 Research project PR standards** - Study recent merged PRs, read CONTRIBUTING.md, check PR template.
4. **🚨 Local CI first** - Run format, lint, typecheck, tests before pushing.
5. **🚨 Human approval required** - Never auto-submit PR. Generate review materials and wait for approval.
6. **🚨 If no issue exists** - Submit issue first, then implement.

---

## Phase 1: Discover Contribution Opportunities

### Search Sources (2 sources, no more)

**Source 1: GitHub Trending**
```
Fetch: https://github.com/trending
Extract: All repository links (no time limit)
Priority: Recent projects (2025-11 onwards)
```

**Source 2: Self-Explore (NO keyword restrictions)**
- GitHub Explore: https://github.com/explore (AI applications, AI tools categories)
- Forums: Reddit (r/MachineLearning, r/LocalLLaMA, r/Python), Hacker News, Twitter
- Search method: Browse freely, no fixed keywords
- Scope: AI applications, AI tools, developer tools

### Search Execution
1. Fetch GitHub Trending page → Extract all project links
2. Self-explore GitHub Explore + forums → Collect interesting projects
3. Combine results (aim for 10+ candidates)
4. For each candidate:
   - Check open issues (priority: `good first issue`, bugs, feature requests)
   - If no suitable issues, clone project → Use it → Find bugs/improvements
5. Output: Top 3 candidate issues/improvements with analysis

### ❌ Avoid
- Limiting search keywords (let exploration be free)
- Only searching popular projects (already have many contributors)
- Hardcoding specific project names

---

## Phase 2: Analyze Contribution Opportunity

### Case A: Has Corresponding Issue

1. Read issue description + **ALL comments** (using `mcp__github__issue_read` with `method: "get_comments"`)
2. Check issue comments for:
   - Someone claimed it? → Skip
   - Already has PR? → Check PR status, skip if open/merged
3. Check for existing PRs (`mcp__github__search_pull_requests`)
4. Output: Issue analysis + feasibility assessment

### Case B: No Corresponding Issue

1. Found a bug or needed feature during self-exploration
2. **🚨 First submit an issue** describing the problem/enhancement
3. Wait for maintainer response (or implement immediately if trivial)
4. Then proceed to Phase 3 (implementation)

---

## Phase 3: Present Implementation Plan (Approval Gate)

Generate plan in **Chinese** with:
- Issue summary (or self-discovered problem)
- Proposed solution
- Files to modify
- Verification steps
- Risk assessment

**🚨 WAIT for user approval** (explicit "Approved" or "批准") before proceeding.

---

## Phase 4: Implement and Verify

1. Set up dev environment (clone, install deps)
2. Create feature branch
3. Implement changes
4. **🚨 Request user to manually test**
   - For GUI: Launch app, test the fix
   - For CLI: Run command, verify output
   - For library: Write test script
5. Record test results (screenshots if needed)

---

## Phase 5: Local CI Checks

Run project's CI commands (check `.github/workflows/` for config):
```bash
# Common commands (adjust per project)
npm run format && npm run lint && npm run typecheck && npm run test
# or
pytest && mypy . && ruff check .
```

Fix any issues found.

---

## Phase 5.5: Pre-PR Checklist (CRITICAL)

**🚨 MUST complete before creating PR. Skipping any item will cause reviewer blockers.**

### Step 1: Research Project PR Standards

**Why**: Every project has different PR standards. Must study before creating PR.

1. **Read project documentation**:
   - `CONTRIBUTING.md` - Contribution guidelines
   - `AGENTS.md` - Agent/AI contribution guidelines (if exists)
   - `docs/CHANGELOG.md` - Changelog format and [Unreleased] section
   - `README.md` - General project info

2. **Study recent merged PRs** (at least 3):
   ```bash
   # Using GitHub API
   curl -H "Authorization: token $GITHUB_TOKEN" \
     "https://api.github.com/repos/OWNER/REPO/pulls?state=closed&per_page=10" \
     | jq '.[] | select(.merged_at != null) | {number, title, body}'
   ```
   - Note the PR description format
   - Note required sections (Overview, Testing, Checklist, etc.)
   - Note how they reference issues

3. **Check PR template**:
   - Look for `.github/PULL_REQUEST_TEMPLATE.md` or `.github/pull_request_template.md`
   - If exists, use it as the PR description template

**Deliverable**: Create PR description following project template.

### Step 2: Verify Code Completeness

**Why**: Incomplete implementation causes reviewer blockers.

#### 2.1 All Paths Synced

**Pitfall** (from daily_stock_analysis Issue #1742):
- Project has multiple analysis paths (non-agent, agent, multi-agent)
- Only updated non-agent path (`src/analyzer.py`)
- Agent path (`src/agent/executor.py`, `src/agent/agents/decision_agent.py`) not updated
- Result: Feature works in one path but not others

**Solution**:
```bash
# Search for all prompt/contract locations
grep -r "EXISTING_FIELD" src/
# Example: grep -r "phase_decision" src/
```
- Update ALL paths
- Test ALL paths

#### 2.2 Schema Defined

- [ ] New fields have Pydantic models (or equivalent) in `schemas/`
- [ ] Fields are `Optional` for backward compatibility
- [ ] Added `model_validator` (or equivalent) to handle edge cases:
  - String values (convert to number)
  - Negative values (clamp to 0)
  - None values (handle gracefully)
  - Sum constraints (normalize to 100 if needed)

#### 2.3 Prompt Updated

- [ ] LLM prompt includes new fields with constraints
- [ ] Added "必须输出" (must output) directive
- [ ] Added detailed field descriptions (what it means, examples)

#### 2.4 Display/Notification Updated

- [ ] Default report mode (e.g., `notification.py`) shows new fields
- [ ] Render mode (e.g., Jinja2 template) shows new fields
- [ ] Added helper functions to handle None values (avoid "None%" display)

#### 2.5 i18n Updated

- [ ] Internationalization labels added (e.g., `report_language.py`)
- [ ] Both Chinese and English labels added

### Step 3: Add Tests

**Why**: CI success ≠ regression coverage. Must add tests for new code.

**Pitfall** (from daily_stock_analysis Issue #1742):
- PR had no test files
- Only had real API test example in PR description
- Reviewer flagged as "[验证缺口]"

**Solution**:
```bash
# Create test file
touch tests/test_NEW_FEATURE.py
```

Add tests for:
- Schema validation (valid/invalid inputs, edge cases)
- Field normalization (string to number, negative to 0, sum normalization)
- Display logic (None values, formatting)
- i18n labels (Chinese/English)

Run tests:
```bash
pytest tests/test_NEW_FEATURE.py -v
```

### Step 4: Update Documentation

**Why**: Project docs must reflect code changes.

**Pitfall** (from daily_stock_analysis Issue #1742):
- Modified user-visible report structure
- No `docs/CHANGELOG.md` update
- Reviewer flagged as "[Process blocker]"

**Solution**:
1. Read `docs/CHANGELOG.md` format
2. Add entry under `[Unreleased]` section:
   ```markdown
   ## [Unreleased]
   
   - [新功能] #NUMBER 新增 FEATURE_NAME 功能
   - [改进] 详细描述
   ```

### Step 5: Prepare Compatibility Statement

**Why**: Reviewer needs to know if PR breaks existing functionality.

**Pitfall** (from daily_stock_analysis Issue #1742):
- PR description didn't mention model/API/config changes
- Reviewer assumed breaking changes
- Flagged as "[Process blocker]"

**Solution**:
Add "兼容性说明" section to PR description:
```markdown
## 模型/API/配置兼容性说明

**本 PR 无以下变更**:
- ❌ 无 provider 变更
- ❌ 无 model 变更
- ❌ 无 Base URL 变更
- ❌ 无默认模型变更
- ❌ 无配置迁移变更

本 PR 仅添加可选字段，不影响现有功能。
```

If changes exist, provide migration guide.

### Step 6: Run CI Script

**Why**: Project may have custom CI script.

```bash
# Check if project has CI script
ls ./scripts/ci_gate.sh ./scripts/ci.sh ./scripts/test.sh 2>/dev/null

# Run if exists
./scripts/ci_gate.sh  # or equivalent

# If no CI script, run standard checks
pytest
flake8 src/
mypy src/
```

**Deliverable**: CI output (✅ passed or ❌ failed with errors)

---

## Phase 6: Generate Review Materials

Create `.PR_REVIEW.md` in **Chinese** with:
- Contribution summary
- Implementation details
- Files modified
- Verification results (including **user manual test**)
- Local CI results
- **Pre-PR checklist results** (all items verified)
- Risk assessment

Present to user and request approval.

---

## Phase 7: Submit PR (After Approval)

### If Has Issue

1. **Prepare PR description** (follow project template from Phase 5.5 Step 1):

   **Standard sections** (adjust per project):
   ```markdown
   ## 概述
   Brief description of what this PR does.
   
   ## 解决的问题
   - Problem 1
   - Problem 2
   
   ## 主要改动
   ### 1. Data Model (src/schemas/xxx.py)
   - Changes
   
   ### 2. Prompt Updates (src/analyzer.py)
   - Changes
   
   ### 3. Agent Path Sync (src/agent/executor.py)
   - Changes
   
   ### 4. Display (src/notification.py, templates/xxx.j2)
   - Changes
   
   ## 测试
   ### Real API Test
   - Test results
   
   ### Unit Tests
   - Test file: tests/test_xxx.py
   - Results: ✅ N tests passed
   
   ### CI Check
   - ✅ CI script passed
   - ✅ M tests passed
   
   ## 模型/API/配置兼容性说明
   **本 PR 无以下变更**:
   - ❌ 无 provider 变更
   - ❌ 无 model 变更
   (or list changes if any)
   
   ## Checklist
   - [x] Code verified
   - [x] All paths synced
   - [x] Field validation added
   - [x] Docs updated
   - [x] Tests added
   - [x] CI passed
   
   ## 后续优化建议
   1. Suggestion 1
   2. Suggestion 2
   
   ## 相关 Issue
   Closes #XXX
   ```

2. Push branch to fork
3. Create PR with description above
4. **🚨 DO NOT write "cannot test locally"** - instead, describe actual verification steps
5. If cannot test, submit as **Draft PR**

### If No Issue (Self-Discovered)

1. First submit issue (if not already submitted)
2. Then create PR referencing the issue
3. If issue not needed (trivial fix), submit PR directly with clear description

---

## Phase 8: Handle Reviewer Feedback

**When reviewer raises blockers, DON'T panic. This is normal.**

### Step 1: Categorize Feedback

- **[Correctness blocker]**: Logic error, must fix
  - Example: "Agent path not synced"
  - Action: Fix immediately
  
- **[Process blocker]**: Missing docs/tests, must fix
  - Example: "No CHANGELOG update"
  - Action: Fix immediately
  
- **[Style/Polish]**: Code style, optional
  - Example: "Variable name not clear"
  - Action: Fix if easy, discuss if controversial

### Step 2: Fix Blockers

1. **Don't argue**, just fix (unless clearly wrong)
2. **Add tests** for fixed issues
3. **Update PR description** to reflect fixes
4. **Push new commit**
5. **Comment on PR**: "已修复 Reviewer 反馈: [list fixes]"

### Step 3: Prevent Future Blockers

**After fixing, update this skill** with new pitfalls.

---

## Phase 9: Monitor PR

1. Check CI status
2. Respond to reviewer feedback
3. Push fixes if requested
4. Celebrate when merged! 🎉

---

## Project Setup

**Local clone directory**: `~/Desktop/personal-homepage/pr-projects/`

Structure:
```
pr-projects/
├── project-1/
├── project-2/
└── ...
```

**Why this location**:
- Isolated from personal projects
- Easy to clean up

---

## Language Requirement

- **Communication with user**: Chinese (简体中文)
- **Generated docs** (plans, reviews): Chinese
- **PR description**: Match project convention (usually English for open-source)

---

## Success Criteria

### For Issue-based PR
- [ ] Issue analysis complete (including comments and PR check)
- [ ] Implementation plan approved by user
- [ ] Code changes complete + local CI passed
- [ ] **User manually tested and confirmed**
- [ ] Review materials approved by user
- [ ] PR submitted with clear description
- [ ] CI passed, maintainer reviewed (or feedback addressed)

### For Self-Discovered PR
- [ ] Problem/improvement identified
- [ ] Issue submitted (if needed) and approved by maintainer
- [ ] Implementation plan approved by user
- [ ] Code changes complete + local CI passed
- [ ] **User manually tested and confirmed**
- [ ] Review materials approved by user
- [ ] PR submitted with clear description
- [ ] CI passed, maintainer reviewed (or feedback addressed)

---

## Troubleshooting

### Push authentication failed
- Configure Git credential helper: `git config --global credential.helper store`
- Or use SSH: `git remote set-url origin git@github.com:...`
- Or use token in URL: `git remote set-url origin https://USER:TOKEN@github.com/USER/REPO.git`

### Type errors after merge
- Always run `git pull upstream main` before pushing
- Resolve conflicts by keeping both changes

### CI fails after PR submission
- Check CI logs
- Fix issues locally
- Push again (PR auto-updates)

### GitHub MCP no permission to create PR
- GitHub MCP tools may not have permission to create PR on upstream repo
- **Solution**: Use GitHub API directly with token from `.zshrc`:
  ```bash
  curl -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    "https://api.github.com/repos/OWNER/REPO/pulls" \
    -d '{"title":"...", "body":"...", "head":"FORK:BRANCH", "base":"main"}'
  ```
- Get token: `grep GITHUB_TOKEN ~/.zshrc`

---

## Common Pitfalls (from real experience)

### 1. Agent Path Out of Sync

**Project**: daily_stock_analysis Issue #1742

**Problem**:
- Only updated `src/analyzer.py` (non-agent path)
- Didn't update `src/agent/executor.py` and `src/agent/agents/decision_agent.py` (agent path)
- Result: Feature works in non-agent mode but not agent mode

**Reviewer feedback**: "[Correctness blocker] agent 生成路径仍有独立的决策仪表盘契约"

**Solution**:
```bash
# Search for all locations that define the dashboard contract
grep -r "phase_decision" src/
# Update ALL locations
```

**Prevention**: Always search for existing field names to find all paths.

### 2. No Field Validation

**Project**: daily_stock_analysis Issue #1742

**Problem**:
- Schema allows arbitrary values (int, float, string)
- LLM may return N/A, "70%", -10, or sum != 100
- Result: User sees "N/A%" or "None%" in report

**Reviewer feedback**: "[Correctness blocker] 新字段要求'四个贡献度之和必须等于 100'，但当前仅靠 prompt 约束"

**Solution**:
Add `model_validator` in Pydantic schema:
```python
@model_validator(mode="after")
def normalize_contributions(cls, values):
    # Convert string to number
    # Clamp negative to 0
    # Normalize sum to 100
    return values
```

**Prevention**: Always add validation for LLM-generated fields.

### 3. Missing Documentation

**Project**: daily_stock_analysis Issue #1742

**Problem**:
- Modified user-visible report structure
- No `docs/CHANGELOG.md` update
- Result: Reviewer flagged as "[Process blocker]"

**Reviewer feedback**: "本 PR 修改了用户可见报告结构和报告渲染，但完整改动文件里没有 docs/CHANGELOG.md 或相关 docs/* 更新"

**Solution**:
- Always update `docs/CHANGELOG.md` under `[Unreleased]`
- Follow project's changelog format

**Prevention**: Add "Update CHANGELOG" to Pre-PR checklist.

### 4. Missing Tests

**Project**: daily_stock_analysis Issue #1742

**Problem**:
- PR had no test files
- Only had real API test example in PR description
- Result: Reviewer flagged as "[验证缺口]"

**Reviewer feedback**: "完整改动没有测试文件变更... CI success 不能替代这些新契约的回归覆盖"

**Solution**:
- Add unit tests for new schema, validation, display logic
- Test edge cases: None, negative, string, sum != 100
- Add integration test with real API (if possible)

**Prevention**: Always add tests for new code.

### 5. Unclear Compatibility Statement

**Project**: daily_stock_analysis Issue #1742

**Problem**:
- PR description didn't mention model/API/config changes
- Result: Reviewer assumed breaking changes

**Reviewer feedback**: "结构化检测提示命中外部模型/API 兼容风险和运行时配置迁移风险，但 PR 描述只给了 DeepSeek 实测"

**Solution**:
- Explicitly state "无 model/provider/Base URL/默认配置变更"
- If changes exist, provide migration guide

**Prevention**: Add "兼容性说明" section to PR description template.

### 6. Duplicate PR/Issue

**Problem**:
- Waste time implementing something that already exists
- Result: PR closed as duplicate

**Solution**:
- Always search for existing PRs/Issues before starting
- Use `gh issue list --search` and `gh pr list --search`
- If Issue exists but no PR, mention "Closes #NUMBER"
- If PR already exists, coordinate or close as duplicate

**Prevention**: Add "Check for existing PRs/Issues" to Phase 2.

---

## Notes

- This skill is for AI-related open-source projects (tools, libraries, frameworks)
- Always read `CONTRIBUTING.md` before contributing
- Be respectful to maintainers (clear PR description, respond to feedback)
- If stuck, ask user for guidance
- **🚨 Key change (2026-06-25)**: Added Phase 5.5 (Pre-PR Checklist) with detailed steps and common pitfalls
- **🚨 Key change (2026-06-25)**: Simplified search strategy - only 2 sources, no keyword restrictions, free exploration
