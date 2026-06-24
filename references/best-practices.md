# PR Contribute - Best Practices & Lessons Learned

## Open-Source Contribution Conventions

### Convention 1: Do You Need Approval Before Submitting a PR?

**Answer**: ❌ **No general rule requires approval before submitting a PR**.

**Detailed Explanation**:

| Scenario | Need Prior Approval? | Explanation |
|----------|----------------------|-------------|
| **Bug fix** | ❌ No | If you discover and fix a bug, you can submit a PR directly |
| **Small changes (docs, formatting)** | ❌ No | Submit PR directly |
| **New feature/large change** | ⚠️ Recommended to discuss first | Better to open an issue first to avoid wasted effort |
| **Project has explicit contributing guidelines** | ✅ Need to follow | Some projects require opening an issue before PR |
| **Does your PR align with project direction** | ⚠️ Recommended to confirm | Avoid submitting PRs for changes the project doesn't want |

**Best Practices**:
1. **Read the project's `CONTRIBUTING.md`** - Understand the project's specific requirements
2. **For large changes, open an issue first** - Ensure maintainers want the change
3. **For small changes, submit PR directly** - Explain the motivation in the PR description

---

### Convention 2: Do You Need a Corresponding Issue to Submit a PR?

**Answer**: ❌ **You don't need a corresponding issue to submit a PR**.

**Detailed Explanation**:

| PR Type | Need Corresponding Issue? | Example |
|---------|----------------------|---------|
| **Bug fix** | ❌ No | You discover a bug, fix it, submit PR directly |
| **Documentation improvement** | ❌ No | Fix typos, improve docs |
| **Code cleanup** | ❌ No | Refactoring, remove deprecated code |
| **New feature** | ⚠️ Recommended to have one | Better to open issue first to discuss if the feature is wanted |
| **Performance optimization** | ❌ Not necessarily | If the optimization is obvious, submit PR directly |
| **Fix existing issue** | ✅ Has corresponding issue | Reference in PR: "Closes #XXXX" |

**Key Principles**:
- **Issues are problem tracking tools** - Used to discuss and track problems
- **PRs are code contribution tools** - Used to submit specific code changes
- **They can exist independently**, or be linked (PR closes issue)

---

### Common Open-Source Contribution Flows

#### Flow A: Issue → PR (Recommended for large changes)
```
1. Discover Issue #1234 (bug report or feature request)
2. Discuss solution in Issue
3. Implement fix/feature
4. Submit PR, reference Issue: "Closes #1234"
```

#### Flow B: No Issue → PR (Suitable for small changes)
```
1. Discover bug or improvement opportunity
2. Fix/improve directly
3. Submit PR, explain in description:
   - What problem
   - How to fix
   - How to verify
```

#### Flow C: Open Issue First → Then PR (Suitable for new features)
```
1. Have new feature idea
2. Open Issue describing feature, ask if maintainers want it
3. Maintainer replies "Yes, we want this"
4. Implement feature
5. Submit PR, reference Issue
```

---

## Key Lessons from Real Contributions

### Lesson 1: Always Use Correct GitHub Token

**Mistake**: Used `ghu_` token (limited permissions) instead of `ghp_` token (full access).

**Solution**:
- Check `~/.zshrc` for correct token (usually has `ghp_` prefix)
- Sync token to WorkBuddy connector: Settings → Connectors → GitHub → Update token
- Verify token has `repo` scope

**How to check**:
```bash
# Check current token
cat ~/.zshrc | grep GITHUB_TOKEN

# Test token
gh auth status
```

### Lesson 2: Actually Run and Verify Code Changes

**Mistake**: Made code changes without actually running the project, leading to incorrect assumptions.

**Solution**:
1. Set up development environment properly
2. Install package in editable mode: `pip install -e .`
3. Actually import and test the modified code
4. Run existing tests to ensure nothing breaks

**Verification Checklist**:
- [ ] Can import the modified module without errors?
- [ ] Does the specific change work as expected?
- [ ] Do all existing tests still pass?
- [ ] Are there any regressions?

**Example**:
```bash
# Wrong way (just edit files)
vim exceptions.py
git add .
git commit -m "add exception"

# Right way (verify first)
pip install -e .
python -c "from autogen_core.exceptions import RecipientNotFoundError; print(RecipientNotFoundError('test'))"
pytest tests/ -v
# If all pass, then commit
```

### Lesson 3: Enforce Human Approval Before PR Submission

**Mistake**: Submitted PR without user approval (happened twice!).

**Solution**:
1. Generate comprehensive review materials
2. Save to file (e.g., `.PR_REVIEW.md`)
3. Present to user and explicitly ask for approval
4. Create `.PR_APPROVAL` file only after receiving explicit "approved" confirmation
5. Check for `.PR_APPROVAL` file before allowing PR submission

**Review Material Template**:
```markdown
# PR Review: <issue-title>

## Issue
- URL: https://github.com/owner/repo/issues/XXXX
- Title: <title>

## Implementation
- Files modified: <list>
- Approach: <description>

## Verification
- [x] Ran project locally
- [x] Tested the specific change
- [x] All tests pass

## Local CI Checks
- [x] Format
- [x] Lint
- [x] Type check
- [x] Tests

## Risk
<low/medium/high>: <explanation>

**APPROVAL REQUIRED**: Please review and confirm before I submit this PR.
```

**Approval Check Logic**:
```python
approval_file = Path(".PR_APPROVAL")
if not approval_file.exists() or approval_file.read_text().strip() != "APPROVED":
    print("ERROR: PR submission requires approval. Generate review materials first.")
    return
```

### Lesson 4: Run Local CI Checks Before Submission

**Mistake**: Submitted PR without running CI checks locally, leading to immediate failures.

**Solution**:
1. Understand the project's CI system (GitHub Actions, etc.)
2. Identify equivalent local commands
3. Run all CI checks locally before submitting

**Common CI Checks for Python Projects**:

| Check | Command (AutoGen) | Command (Generic) |
|-------|---------------------|-------------------|
| Format | `uv run poe fmt --directory ./packages/<pkg>` | `black . && isort .` |
| Lint | `uv run poe lint --directory ./packages/<pkg>` | `pylint <module>` |
| Type Check | `uv run poe pyright --directory ./packages/<pkg>` | `mypy <module>` |
| Test | `uv run poe test --directory ./packages/<pkg>` | `pytest tests/` |

**Using LocalValidator Class**:
```python
from ai_contribute_bot import LocalValidator

validator = LocalValidator(repo_path="/path/to/repo")
result = validator.validate_package("autogen-core")

if not result["passed"]:
    print("CI checks failed. Fix issues before submitting.")
    print(result["details"])
```

### Lesson 5: Understand Fork-based Workflow for First-Time Contributors

**Context**: First-time contributors to a repository may need to:
1. Fork the repository
2. Push changes to their fork
3. Create PR from fork to upstream

**Solution**:
1. Check if user has write access: `gh repo view owner/repo --json permissions`
2. If no write access, use fork workflow:
   ```bash
   gh repo fork owner/repo --clone
   cd repo
   git remote -v  # Verify upstream and origin
   # Make changes
   git push origin <branch>
   gh pr create --repo owner/repo
   ```

### Lesson 6: Present Implementation Plan Before Starting Work

**Mistake**: Started implementing an issue without presenting the plan to the user, leading to wasted effort if the user disagrees with the approach or the issue is not suitable.

**Solution**:
1. After analyzing the issue (Phase 2), generate a detailed implementation plan
2. Present the plan to the user with all necessary information
3. Wait for explicit approval before starting implementation (Phase 4)
4. If user rejects, return to Phase 1 (Search) or terminate

**What to Include in the Plan**:

```markdown
# Implementation Plan for Issue #<number>

## 1. PR Information
- **Suggested PR Title**: <concise, descriptive title>
- **Issue Link**: https://github.com/owner/repo/issues/<number>
- **Issue Author**: @<author>
- **Issue Created**: <date>

## 2. Issue Details

### Problem Description
<verbatim or paraphrased problem description>

### Reproduction Steps
<exact steps to reproduce the issue>

### Expected Behavior
<what should happen>

### Actual Behavior
<what actually happens, including error messages>

### Impact
<who is affected and how severe is the issue>

## 3. Implementation Plan

### Root Cause Analysis
<technical analysis of why the bug occurs>

### Proposed Solution
<detailed description of the fix>

### Files to Modify
1. `<file-path-1>`:
   - <what changes will be made>
2. `<file-path-2>`:
   - <what changes will be made>

### Code Changes (Detailed)

#### Change 1: <description>
```python
# Add this function/class
<code snippet>
```

### Tests to Add/Modify
1. <test-case-1>: <what it tests>
2. <test-case-2>: <what it tests>

### Edge Cases to Consider
- <edge-case-1>
- <edge-case-2>

## 4. Verification Plan

How to verify the fix works:
1. <step-1>
2. <step-2>
3. <step-3>

## 5. Risk Assessment

- **Risk Level**: <Low/Medium/High>
- **Breaking Changes**: <Yes/No - explain>
- **Backward Compatibility**: <explanation>
- **Potential Issues**: <what could go wrong>
```

**Approval Process**:

1. **Generate the plan** using the template above
2. **Present to user** in a clear message
3. **Wait for explicit approval** - do NOT proceed without it
4. If user approves → Proceed to Phase 4 (Implement)
5. If user rejects → Return to Phase 1 (Search) or terminate
6. If user requests modifications → Update the plan and re-present

**Example Presentation**:

```
I've analyzed Issue #7833 and created an implementation plan. 
Please review the details below and let me know if you'd like to proceed.

<insert the plan document here>

**Do you approve this plan?** Please respond with "Approved" to proceed.
```

**User Response Options**:

- **"Approved"** or **"批准"** → Proceed with implementation
- **"Modify: <instructions>"** → Update the plan according to instructions
- **"Reject"** or **"拒绝"** → Stop and select a different issue

---

### Lesson 7: Monitor PR Status After Submission

**Context**: After submitting PR, need to:
1. Monitor CI checks (some may require maintainer approval)
2. Respond to reviewer comments
3. Push fixes promptly

**Solution**:
```bash
# Monitor CI checks
gh pr checks <PR-number>

# View PR details
gh pr view <PR-number> --comments

# Push fixes
git add .
git commit -m "address review comments"
git push origin <branch>
```

---

### Lesson 8: Check Issue Comments Before Proceeding 🚨

**Context**: In the initial workflow, I didn't check issue comments before deciding to work on an issue. This led to:
- Wasting time on already-fixed issues
- Duplicating work someone else was doing
- Missing maintainer's feedback that the issue won't be fixed

**Requirement**: 
**MUST read and analyze all issue comments** in Phase 2 (Analyze Contribution Opportunity).

**What to Check in Comments**:
1. **Is the issue already fixed?**
   - Search for "fixed", "resolved", "closed", "PR #XXXX" in comments
   - Check if a related PR was merged
2. **Is someone already working on it?**
   - Search for "I'm working on it", "I'll take it", "assign me"
   - Check if the issue has an assignee
3. **What did maintainers say?**
   - Did they confirm it's a bug?
   - Did they suggest a specific fix?
   - Did they say they won't fix it?
4. **Are there related PRs?**
   - Search for PR links in comments
   - Check if there are abandoned PRs
5. **Is there a consensus on the solution?**
   - Read through the discussion
   - Note any agreed-upon approach

**Output**: Include an "Issue 评论分析" section in the Phase 3 approval document.

**Example** (Chinese output required):
```
## Issue 评论分析

### 评论总数
- **评论数量**: 12 条
- **最后评论时间**: 2026-06-20

### Issue 状态评估
- **是否已被修复？**: 否 - 无相关 PR 或修复评论
- **是否有人正在处理？**: 是 - @user123 在 2026-06-15 评论 "I'll take this"
- **维护者是否确认？**: 是 - @maintainer 在 2026-06-14 确认这是 bug
- **是否有相关 PR？**: 否
- **Issue 是否仍有效？**: 是 - 无人提交 PR，建议继续

### 关键评论摘要
1. **Comment #3** (by @user123, 2026-06-15):
   - "I'll take this issue"
   - 对实施的影响: 已有用户声明处理，但至今无 PR，可能已放弃
2. **Comment #7** (by @maintainer, 2026-06-14):
   - "Yes, this is a bug. We should fix it by adding X"
   - 建议的修复方案: 添加 X 功能

### 实施建议
- **是否建议继续？**: 是 - 虽然 @user123 声明处理，但至今无 PR
- **如果继续，需要注意**: 参考维护者建议的方案（添加 X）
```

---

### Lesson 9: Use Chinese Output 🚨

**Context**: The user requested that all skill outputs be in Chinese (简体中文).

**Requirement**:
All outputs of this skill MUST be in **简体中文 (Simplified Chinese)**, including:
1. All communication with the user
2. All generated documentation (implementation plans, review materials, PR descriptions)
3. All phase outputs (analysis, verification results, risk assessments)
4. All error messages and troubleshooting guidance

**Exception**: 
- Code comments can remain in English if the project uses English comments
- But all explanatory text MUST be in Chinese

**How to Implement**:
1. Add "Language Requirement" section in `SKILL.md`
2. Add "🚨 语言要求" notes to each Phase section
3. Update all examples to show Chinese output
4. When generating documents, explicitly state "必须使用简体中文"

**Example** (Phase 3 Example Presentation - MUST be in Chinese):
```
我已分析了 Issue #7833 并创建了实现计划。
请查看下方的详细信息，并告知是否继续。

<在此插入计划文档（必须使用中文）>

**你是否批准这个计划？** 请回复 "批准" 以继续。
```

---

## Project-Specific Configurations

### AutoGen

**Repository**: https://github.com/microsoft/autogen

**CI System**: GitHub Actions with `poe` task runner

**Local Commands**:
```bash
# Format
uv run poe fmt --directory ./packages/<package-name>

# Lint
uv run poe lint --directory ./packages/<package-name>

# Type check
uv run poe pyright --directory ./packages/<package-name>

# Test
uv run poe test --directory ./packages/<package-name>
```

**Package Structure**:
- `python/packages/autogen-core/`: Core package
- `python/packages/autogen-agentchat/`: Agent chat package
- `python/packages/autogen-studio/`: Studio package

**Development Setup**:
```bash
git clone https://github.com/microsoft/autogen.git
cd autogen
uv sync  # Install dependencies
```

### CrewAI

**Repository**: https://github.com/crewAIInc/crewAI

**CI System**: GitHub Actions with `pytest` and `flake8`

**Local Commands**:
```bash
pip install -e ".[dev]"
pytest tests/
flake8 crewai/
```

### OpenHands

**Repository**: https://github.com/All-Hands-AI/OpenHands

**CI System**: GitHub Actions with `pre-commit` hooks

**Local Commands**:
```bash
pre-commit run --all-files
pytest tests/
```

## Common Issue Patterns

### Pattern 1: Add Fine-Grained Exception Classes

**Example**: Issue #4964 in AutoGen - "Add specific exception classes"

**Approach**:
1. Add new exception class in `exceptions.py`
2. Update `__all__` to export the new exception
3. Use the new exception in relevant code
4. Add tests for the new exception

**Files to Modify**:
- `exceptions.py`: Add exception class
- Relevant module: Use the exception
- `tests/`: Add tests

### Pattern 2: Fix Bug with Clear Error Message

**Example**: "Improve error message when X fails"

**Approach**:
1. Locate where the error is raised
2. Improve the error message with actionable information
3. Add test to verify the new error message

### Pattern 3: Add Missing Functionality

**Example**: "Support X in Y"

**Approach**:
1. Understand existing API
2. Implement the new functionality
3. Add tests
4. Update documentation

## Automation Script Usage

### Search Issues

```bash
python ai_contribute_bot.py search \
  --max-results 10
```

### Prepare Implementation

```bash
python ai_contribute_bot.py prepare \
  --issue-url https://github.com/owner/repo/issues/XXXX
```

This command will:
1. Analyze the issue
2. Create implementation plan
3. Make code changes
4. Run local validation
5. Generate review materials

### Validate Locally

```bash
python ai_contribute_bot.py validate \
  --repo-path /path/to/repo \
  --package <package-name>
```

### Submit PR (After Approval)

```bash
python ai_contribute_bot.py submit \
  --pr-file ~/.pr/XXXX.md
```

### Monitor PR

```bash
python ai_contribute_bot.py monitor \
  --pr-url https://github.com/owner/repo/pull/XXXX
```

## Checklist for Each Contribution

Before starting:
- [ ] Selected issue is clear and actionable
- [ ] Issue is not assigned to anyone
- [ ] Have necessary permissions (or prepared to fork)

During implementation:
- [ ] Set up development environment
- [ ] Actually ran the project
- [ ] Made code changes
- [ ] Verified changes work as expected
- [ ] All existing tests pass

Before submission:
- [ ] Ran local CI checks (format, lint, typecheck, test)
- [ ] Generated review materials
- [ ] Received explicit human approval
- [ ] Commit message is clear and follows conventions

After submission:
- [ ] Monitoring CI checks
- [ ] Responding to reviewer comments
- [ ] Address feedback promptly

## Resources

- [AutoGen Contributing Guide](https://github.com/microsoft/autogen/blob/main/CONTRIBUTING.md)
- [CrewAI Contributing Guide](https://github.com/crewAIInc/crewAI/blob/main/CONTRIBUTING.md)
- [OpenHands Contributing Guide](https://github.com/All-Hands-AI/OpenHands/blob/main/CONTRIBUTING.md)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [Conventional Commits](https://www.conventionalcommits.org/)
