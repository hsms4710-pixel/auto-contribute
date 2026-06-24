---
name: pr-contribute
description: Open-source PR contribution workflow for AI-related projects. Use when the user wants to contribute to open-source projects (AI tools, libraries, frameworks, etc.), submit pull requests, or automate the contribution process. This skill enforces actual code verification, local CI checks, and human approval before PR submission. Supports both issue-based and self-discovered contributions.
agent_created: true
---

# PR Contribute Skill

Automate open-source contributions with verification, validation, and human approval.

## When to Use This Skill

This skill should be used when:
- User wants to contribute to open-source AI-related projects (tools, libraries, frameworks, etc.)
- User asks to "提交 PR", "贡献开源项目", "find contributable issues"
- User wants to automate the PR contribution process
- User mentions specific GitHub issues or repositories
- User discovers a bug or improvement opportunity in an open-source project

## Open-Source Contribution Conventions

### Do You Need Approval Before Submitting a PR?

**Short answer**: ❌ **No general rule requires approval before submitting a PR**.

**Detailed explanation**:

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

### Do You Need a Corresponding Issue to Submit a PR?

**Short answer**: ❌ **You don't need a corresponding issue to submit a PR**.

**Detailed explanation**:

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

## Core Principles

1. **Actually verify code changes** - Never guess or assume; always run the project and test changes
2. **Local CI checks first** - Run format, lint, typecheck, and tests locally before submitting
3. **Human approval required** - Never auto-submit PR; always generate review materials and wait for approval
4. **🚨 User must manually test before PR submission** - For any code changes, the user MUST manually verify the fix works in a real environment. Unit tests passing is NOT sufficient for GUI applications. If the user cannot test (e.g., no GUI environment), explicitly state this in the PR and consider submitting as Draft PR.
5. **Monitor PR status** - Track CI checks and maintainer feedback after submission
6. **Plan approval gate** - Present implementation plan before starting work; wait for explicit approval
7. **Not limited to issues** - Can submit PRs for self-discovered bugs or improvements
8. **Follow project conventions** - Read and follow CONTRIBUTING.md
9. **Language requirement** - All outputs must be in 简体中文 (Simplified Chinese)

## Language Requirement (语言要求)

**🚨 IMPORTANT**: All outputs of this skill must be in **简体中文 (Simplified Chinese)**.

This includes:
- All communication with the user
- All generated documentation (implementation plans, review materials, PR descriptions)
- All phase outputs (analysis, verification results, risk assessments)
- All error messages and troubleshooting guidance

**Exception**: Code comments can remain in English if the project uses English comments, but all explanatory text must be in Chinese.

## Workflow

### Phase 1: Discover Contribution Opportunities

**Method 1: Search for Issues**
1. Use GitHub MCP connector or `gh` CLI to search issues
2. Filter criteria:
   - Issue is open and not assigned
   - Issue is actionable (clear description, reproducible bug, or well-defined feature request)
   - Issue is recent (within last 30 days)
   - Issue description is clear and actionable
3. Prioritize issues that match user's expertise (Python, TypeScript, etc.)

**Method 2: Explore New Projects (Diverse Sources)**
1. **GitHub Trending** (https://github.com/trending)
   - Filter: AI-related, last 7 days, actively maintained
2. **GitHub Explore** (https://github.com/explore)
   - Categories: Machine Learning, AI Tools, Developer Tools
3. **Reddit / Hacker News**
   - Reddit: r/MachineLearning, r/LocalLLaMA, r/Python
   - HN: Search "open source AI tool"
   - Find recently discussed open-source projects
4. **Traditional Popular Projects (Backup)**
   - AutoGen, CrewAI, OpenHands, LangChain, Dify
   - Only use as backup when no new projects found

**Method 3: Self-Discover Contribution Opportunities**
1. Read project's README, documentation, code
2. Look for improvement opportunities:
   - Unclear documentation → Improve docs
   - Missing examples → Add examples
   - Insufficient test coverage → Add tests
   - Potential bugs in code → Fix and submit PR
3. Use the project, discover bugs or improvements

### Phase 2: Analyze Contribution Opportunity

**🚨 语言要求**: 本阶段的所有输出（Issue 分析、评论分析）必须使用**简体中文**。

**If it's an Issue-based contribution**:
1. Read the issue description thoroughly using `mcp__github__issue_read`
2. Understand the problem:
   - What is the expected behavior?
   - What is the actual behavior?
   - Are there reproduction steps?
   - Are there error messages?
3. **🚨 CRITICAL: Read and analyze ALL issue comments** (使用 `mcp__github__list_issue_comments` 或 `mcp__github__get_issue_comments`)
   - **目的**: 评估 issue 的实际状态，避免重复劳动或提交无效的 PR
   - **必须检查的内容**:
     a. **Issue 是否已被修复？**
        - 搜索评论中的关键词："fixed", "resolved", "closed", "PR #XXXX"
        - 检查是否有相关的 PR 已经合并
     b. **是否有人正在处理？**
        - 搜索评论中的关键词："I'm working on it", "I'll take it", "assign me"
        - 检查 issue 是否已被分配给某人（assignee）
     c. **维护者的回复是什么？**
        - 维护者是否确认这是 bug？
        - 维护者是否提出了特定的修复方案？
        - 维护者是否表示这个 issue 不重要或不会修复？
     d. **是否有相关的 PR？**
        - 搜索评论中的 PR 链接
        - 检查是否有 abandoned PR（放弃的 PR）
     e. **Issue 的讨论是否已有定论？**
        - 是否有 consensus（共识）？
        - 是否有明确的实施方案？
   - **输出**: Issue 评论分析摘要（见下方的"Issue 评论分析模板"）
4. Check if the issue is still relevant:
   - Based on comment analysis, determine if the issue is still valid
   - If issue is already fixed → Skip this issue, select another
   - If someone is already working on it → Skip this issue, select another
   - If maintainer said they won't fix → Skip this issue
5. Output: 
   - Issue analysis summary (problem, impact, reproduction steps)
   - **Issue 评论分析摘要** (status, assignee, related PRs, maintainer response)

**If it's a self-discovered contribution**:
1. Confirm the problem/improvement opportunity
2. Check if there's already a related Issue or PR
3. Confirm the project welcomes this type of contribution (read CONTRIBUTING.md)
4. Output: Contribution opportunity description (problem, proposed solution, impact)

**Important**: At this stage, only analyze. Do NOT start implementing.

#### Issue 评论分析模板（必须包含在 Phase 3 的审批材料中）

```markdown
## Issue 评论分析（Phase 2 输出）

### 评论总数
- **评论数量**: X 条
- **最后评论时间**: YYYY-MM-DD

### Issue 状态评估
- **是否已被修复？**: 是/否 - <详细说明>
- **是否有人正在处理？**: 是/否 - <assignee 信息或评论引用>
- **维护者是否确认？**: 是/否 - <维护者回复摘要>
- **是否有相关 PR？**: 是/否 - <PR 链接和状态>
- **Issue 是否仍有效？**: 是/否 - <决定是否继续>

### 关键评论摘要
1. **Comment #1** (by @user, YYYY-MM-DD):
   - <评论内容摘要>
   - <对实施的影响>
2. **Comment #2** (by @maintainer, YYYY-MM-DD):
   - <维护者回复摘要>
   - <建议的修复方案>

### 实施建议
- **是否建议继续？**: 是/否
- **如果继续，需要注意**: <从评论中获得的经验教训>
- **如果不继续，原因**: <为什么这个 issue 不适合>
```

**If it's a self-discovered contribution**:
1. Confirm the problem/improvement opportunity
2. Check if there's already a related Issue or PR
3. Confirm the project welcomes this type of contribution (read CONTRIBUTING.md)
4. Output: Contribution opportunity description (problem, proposed solution, impact)

**Important**: At this stage, only analyze. Do NOT start implementing.

### Phase 3: Present Plan for Approval (MANDATORY)

**🛑 MANDATORY APPROVAL GATE**: Before starting implementation, you MUST present the plan to the user and wait for explicit approval.

**🚨 语言要求**: 本阶段生成的实现计划文档必须使用**简体中文**。

#### What to Present

Create a detailed plan document with the following sections:

```markdown
# Implementation Plan for <Issue #number or "Self-Discovered: <description>">

## 1. PR Information
- **Suggested PR Title**: <concise, descriptive title following project conventions>
- **Corresponding Issue**: <Issue link (if applicable), or "None (self-discovered)">
- **Contribution Type**: <Issue-based PR / Bug fix / Documentation improvement / Code cleanup / New feature>
- **Issue Author**: @<author> (if applicable)
- **Issue Created**: <date> (if applicable)

## 2. Problem / Improvement Description

### Problem Description (for bug fixes)
<verbatim or paraphrased problem description from the issue, or self-discovered problem>

### Improvement Description (for enhancements)
<what improvement is proposed and why it's needed>

### Reproduction Steps (for bugs)
<exact steps to reproduce the issue, copied from the issue or derived from analysis>

### Expected Behavior
<what should happen according to the issue or intended behavior>

### Actual Behavior
<what actually happens, including error messages>

### Impact
<who is affected and how severe is the issue / why the improvement is valuable>

### Issue 评论分析（仅适用于基于 Issue 的贡献）
**🚨 必须包含**: 从 Phase 2 的 issue 评论分析输出
（使用上方"#### Issue 评论分析模板"的内容）

## 3. Implementation Plan

### Root Cause Analysis
<technical analysis of why the bug occurs or why the feature is missing>

### Proposed Solution
<detailed description of the fix or implementation approach>

### Files to Modify
1. `<file-path-1>`:
   - <what changes will be made>
   - <why this file needs to be modified>
2. `<file-path-2>`:
   - <what changes will be made>

### Code Changes (Detailed)

#### Change 1: <description>
```python
# Add this function/class
<code snippet showing the new/modified code>
```

#### Change 2: <description>
```python
# Modify this function
<before/after code snippet>
```

### Tests to Add/Modify
1. <test-case-1>: <what it tests>
2. <test-case-2>: <what it tests>

### Edge Cases to Consider
- <edge-case-1>
- <edge-case-2>

## 4. Verification Plan

How to verify the fix works:
1. <step-1: e.g., "Run the reproduction script from the issue">
2. <step-2: e.g., "Add a unit test that covers the fix">
3. <step-3: e.g., "Run existing tests to ensure no regressions">

## 5. Risk Assessment

- **Risk Level**: <Low/Medium/High>
- **Breaking Changes**: <Yes/No - explain>
- **Backward Compatibility**: <explanation of how backward compatibility is maintained>
- **Potential Issues**: <what could go wrong>

## 6. Alternative Approaches Considered

<optional: if there were other ways to solve this, list them and explain why they were not chosen>

---

**Please review this plan and respond with:**
- **"Approved"** or **"批准"** → I will proceed with implementation
- **"Modify: <instructions>"** → I will update the plan according to your instructions
- **"Reject"** or **"拒绝"** → I will stop and select a different issue
```

#### Steps to Follow

1. **Generate the plan document** (like the template above)
2. **Present it to the user** in a clear, organized message
3. **Wait for explicit approval** - do NOT proceed without it
4. If user approves → Proceed to Phase 4 (Implement)
5. If user rejects → Return to Phase 1 (Search) or terminate
6. If user requests modifications → Update the plan and re-present

#### Example Presentation (示例展示 - 必须使用中文)

```
我已分析了 Issue #7833 并创建了实现计划。
请查看下方的详细信息，并告知是否继续。

<在此插入计划文档（必须使用中文）>

**你是否批准这个计划？** 请回复 "批准" 以继续。
```

**🚨 语言要求**: 所有与用户的沟通、生成的文档、阶段输出都必须使用**简体中文**。

### Phase 4: Implement with Verification

**Prerequisite**: Phase 3 approved by user.

**CRITICAL**: Always actually run the project and verify changes. **User must manually test before PR submission.**

Steps:
1. Set up the development environment:
   ```bash
   # Clone the repository (if not already cloned)
   git clone https://github.com/owner/repo.git
   cd repo
   
   # Install dependencies
   pip install -e ".[dev]"  # Python projects
   # or
   npm install  # Node.js projects
   ```

2. Make the code changes:
   - Follow the project's coding standards
   - Add necessary imports
   - Update `__all__` if exporting new symbols
   - Add/modify tests

3. **Actually verify the changes**:
   ```bash
   # Run the specific module/function to verify it works
   python -c "from module import ClassName; print(ClassName())"
   
   # Run relevant tests
   pytest tests/test_specific.py -v
   
   # Test the example from the issue (if provided)
   ```

4. **🚨 MANDATORY: Ask user to manually test the changes**
   
   **For GUI applications (Electron, React, Vue, etc.):**
   - User must launch the application
   - User must manually verify the UI behavior
   - Example for Electron apps:
     ```bash
     # Start the app in development mode
     npm run dev  # or whatever command the project uses
     ```
   - User must test: Click buttons, enter commands, verify UI updates correctly
   
   **For CLI tools:**
   - User must run the CLI command
   - User must verify the output is correct
   
   **For libraries:**
   - User must write a small test script
   - User must verify the library function works as expected

5. **Document verification results**
   - Record what the user tested
   - Record the test results (screenshots if GUI)
   - If user cannot test (e.g., no GUI environment), explicitly note this

**Common Mistakes to Avoid**:
- ❌ Don't just edit files without running the project
- ❌ Don't assume the code works without testing
- ❌ Don't skip edge cases
- ❌ **Don't submit PR if user hasn't manually tested** (unless explicitly marked as Draft PR)
- ❌ **Don't say "cannot test locally" in PR description** - this means you shouldn't submit the PR yet

### Phase 5: Local Validation (CI Checks)

Run local CI checks before submitting PR. This prevents embarrassing failures and speeds up review.

For Python projects using `poe` (like AutoGen):

```bash
# Format check
uv run poe fmt --directory ./packages/<package-name>

# Lint check
uv run poe lint --directory ./packages/<package-name>

# Type check (pyright)
uv run poe pyright --directory ./packages/<package-name>

# Run tests
uv run poe test --directory ./packages/<package-name>
```

For other projects, check their CI configuration (`.github/workflows/`) and run equivalent commands locally.

Use the `LocalValidator` class in `ai_contribute_bot.py` to automate this:

```bash
python ai_contribute_bot.py validate --repo-path /path/to/repo --package <package-name>
```

Fix any issues found before proceeding.

### Phase 6: Generate Review Materials

**🚨 语言要求**: 本阶段生成的所有审查材料必须使用**简体中文**。

**CRITICAL**: Never submit PR without human approval.

To generate review materials:

1. Create a review document with:
   - Contribution summary (issue-based or self-discovered)
   - Implementation approach
   - Files modified (with diff)
   - Verification results
   - Local validation results (CI checks)
   - Test coverage
   - Potential risks

2. Save review materials to a file (e.g., `.PR_REVIEW.md`)

3. Present to user and ask for approval

Example review material format:
```markdown
# PR Review: <issue-title or "Self-Discovered: <description>">

## Contribution Info
- Type: <Issue-based PR / Self-discovered bug fix / Documentation improvement>
- Issue Link: https://github.com/owner/repo/issues/XXXX (if applicable)
- Title: <title>

## Implementation Plan
<description>

## Files Modified
- `path/to/file.py`: <changes>

## Verification
- [ ] Ran project locally
- [ ] Tested the specific change
- [ ] All existing tests pass
- [ ] **🚨 User has manually tested the changes in real environment**
- [ ] **For GUI changes: User has launched the app and verified UI behavior**

**User Testing Details:**
- What did the user test? <details>
- How did the user test? <steps>
- What were the results? <screenshots or descriptions>

## Local CI Checks
- [x] Format (black/isort)
- [x] Lint (pylint)
- [x] Type check (pyright)
- [x] Tests pass

## Risk Assessment
<low/medium/high> - <explanation>

## PR Submission Type
- [ ] **Normal PR** - User has fully tested, confident it works
- [ ] **Draft PR** - User cannot fully test (explain why), requesting help from maintainers

## Approval Required
**🚨 Before submitting PR, confirm:**
1. User has manually tested the changes
2. User approves PR submission
3. If user cannot test, PR will be submitted as Draft

Please review and approve before PR submission.
```

### Phase 7: Submit PR (After Approval)

Only after explicit human approval:

1. Commit changes:
   ```bash
   git add .
   git commit -m "fix: <description> (closes #XXXX)"  # If fixing an issue
   # or
   git commit -m "fix: <description>"  # If self-discovered
   git push origin <branch-name>
   ```

2. Create PR using `gh` CLI or GitHub web interface:
   ```bash
   gh pr create --title "fix: <title>" --body "$(cat PR_BODY.md)" --base main
   ```

3. Monitor PR status:
   - Check CI checks
   - Respond to reviewer feedback
   - Address comments

### Phase 8: Monitor PR

After PR submission:

1. Check CI status regularly:
   ```bash
   gh pr checks <PR-number>
   ```

2. Respond to reviewer comments:
   - Be polite and professional
   - Address all feedback
   - Push fixes promptly

3. Track PR until merge or closure

## Using the Automation Script

The skill includes `ai_contribute_bot.py` (located in the user's project directory) that automates most of this workflow.

### Commands

- `search`: Search for contributable issues
- `prepare`: Analyze issue and prepare implementation (includes validation)
- `validate`: Run local CI checks
- `submit`: Submit PR (requires approval file)
- `monitor`: Monitor PR status

### Example Usage

```bash
# Search for issues
python ai_contribute_bot.py search --keywords "exception handling" --labels good-first-issue

# Prepare implementation (includes validation)
python ai_contribute_bot.py prepare --issue-url https://github.com/owner/repo/issues/XXXX

# Validate locally
python ai_contribute_bot.py validate --repo-path ~/repos/autogen --package autogen-core

# Submit PR (after approval)
python ai_contribute_bot.py submit --pr-file ~/.pr/XXXX.md
```


---

## Local Test Project Directory Configuration

### Purpose

When contributing to open-source projects, you need a local directory to clone repositories, set up development environments, and test modifications. This section defines the default local test project directory and its usage.

---

### Default Directory

**Default path**: `~/Desktop/personal-homepage/pr-projects/`

This directory is used to store all open-source project repositories that you are contributing to.

**Why this location**:
- ✅ Easy to find (on Desktop)
- ✅ Isolated from your personal projects
- ✅ Can be easily cleaned up when no longer needed

---

### Directory Structure

After cloning and setting up projects, the directory structure should look like this:

```
~/Desktop/personal-homepage/pr-projects/
├── hermes-agent/              # Example project 1
│   ├── .git/
│   ├── apps/
│   ├── package.json
│   └── ... (project files)
├── autogen/                   # Example project 2
│   ├── .git/
│   ├── autogen/
│   ├── setup.py
│   └── ... (project files)
└── ... (more projects)
```

---

### Configuration

#### Method 1: Use default directory (recommended)

No configuration needed. The skill will automatically use `~/Desktop/personal-homepage/pr-projects/` as the local test directory.

#### Method 2: Custom directory

If you want to use a different directory, set the environment variable in `~/.zshrc`:

```bash
# Add to ~/.zshrc
export PR_PROJECTS_DIR="$HOME/Desktop/personal-homepage/pr-projects"
```

Then reload the configuration:

```bash
```

---

### Usage in Automation Tasks

When the automation task runs, it will:

1. **Check if the directory exists**
   ```bash
   if [ ! -d "$PR_PROJECTS_DIR" ]; then
     mkdir -p "$PR_PROJECTS_DIR"
   fi
   ```

2. **Clone the repository**
   ```bash
   cd "$PR_PROJECTS_DIR"
   git clone https://github.com/owner/repo.git
   ```

3. **Set up development environment**
   ```bash
   cd "$PR_PROJECTS_DIR/repo"
   npm install  # or pip install -e ".[dev]"
   ```

4. **Create a branch and implement changes**
   ```bash
   git checkout -b fix/issue-description
   # ... make changes ...
   ```

5. **Test the changes**
   ```bash
   npm run test  # or pytest
   ```

6. **Ask user to manually test**
   - For GUI apps: Launch the app and verify
   - For CLI tools: Run the command and verify output

---

### Best Practices

#### 1. Clean up old projects regularly

After a PR is merged or closed, you can delete the local clone to save disk space:

```bash
# Delete a specific project
rm -rf "$PR_PROJECTS_DIR/repo-name"

# List all projects and their disk usage
du -sh "$PR_PROJECTS_DIR"/*
```

**Recommendation**: Clean up projects that haven't been modified in 30+ days.

#### 2. Use meaningful branch names

When creating a branch for a PR, use a descriptive name:

```bash
# Good branch names
fix/desktop-slash-commands-hidden
feat/add-model-picker
docs/fix-python-version-requirement

# Avoid vague names
fix-issue
my-branch
test
```

#### 3. Keep fork in sync with upstream

If you have a fork, regularly sync it with the upstream repository:

```bash
cd "$PR_PROJECTS_DIR/repo"

# Add upstream remote (if not already added)
git remote add upstream https://github.com/original-owner/repo.git

# Fetch upstream
git fetch upstream

# Merge upstream changes
git checkout main
git merge upstream/main

# Push to fork
git push fork main
```

---

### Troubleshooting

#### Problem 1: Directory does not exist

**Symptom**: Automation task fails with "directory not found" error.

**Solution**:

```bash
mkdir -p ~/Desktop/personal-homepage/pr-projects/
```

#### Problem 2: Disk space full

**Symptom**: Cannot clone new repositories.

**Solution**:

```bash
# Check disk usage
df -h ~/Desktop/personal-homepage/pr-projects/

# Clean up old projects
rm -rf ~/Desktop/personal-homepage/pr-projects/old-project/
```

#### Problem 3: Permission denied

**Symptom**: Cannot write to the directory.

**Solution**:

```bash
# Check permissions
ls -la ~/Desktop/personal-homepage/ | grep pr-projects

# Fix permissions
chmod 755 ~/Desktop/personal-homepage/pr-projects/
```

---

### Example: Full Workflow

Here's a complete example of how the local test project directory is used:

```bash
# 1. Automation task starts
# 2. Check if directory exists
mkdir -p ~/Desktop/personal-homepage/pr-projects/

# 3. Clone the repository
cd ~/Desktop/personal-homepage/pr-projects/
git clone https://github.com/NousResearch/hermes-agent.git

# 4. Set up development environment
cd hermes-agent
npm install

# 5. Create a branch
git checkout -b fix/desktop-slash-commands-hidden

# 6. Make changes
vim apps/desktop/src/lib/desktop-slash-commands.ts

# 7. Run tests
cd apps/desktop
npm run test

# 8. Ask user to manually test
echo "Please test the changes:"
echo "  1. Run: cd ~/Desktop/personal-homepage/pr-projects/hermes-agent/apps/desktop"
echo "  2. Run: npm run dev"
echo "  3. Test /reasoning command"

# 9. After user confirms, commit and push
git add .
git commit -m "fix: ..."
git push fork fix/desktop-slash-commands-hidden

# 10. Create PR
gh pr create --repo NousResearch/hermes-agent --head hsms4710-pixel:fix/desktop-slash-commands-hidden

# 11. Clean up (optional, after PR is merged)
# rm -rf ~/Desktop/personal-homepage/pr-projects/hermes-agent
```

---

### Notes

- ✅ The directory is created automatically if it doesn't exist
- ✅ Each project has its own subdirectory
- ✅ You can have multiple projects in the directory at the same time
- ✅ The directory is not tracked by Git (you can add it to `~/.gitignore` if needed)
- ⚠️ Make sure you have enough disk space (some projects can be large)
- ⚠️ Regularly clean up old projects to save disk space

---

## Important Reminders

1. **🚨 Testing Requirements (MANDATORY)**

   **What constitutes "verification":**
   - ✅ **Unit tests pass** - Necessary but NOT sufficient
   - ✅ **User manually tests the changes** - MANDATORY before PR submission
   - ✅ **User verifies in real environment** - Not just in test suite

   **For different types of applications:**

   | Application Type | How User Must Test |
   |------------------|-------------------|
   | **GUI Application (Electron, React, Vue, etc.)** | Launch the app, manually click buttons, enter commands, verify UI updates correctly |
   | **CLI Tool** | Run the CLI command in terminal, verify output is correct |
   | **Library/Framework** | Write a small test script, import the function, verify it works |
   | **API Server** | Start the server, send HTTP requests, verify responses |

   **If user cannot test:**
   - ❌ **Don't submit normal PR** - This will likely be rejected
   - ✅ **Submit as Draft PR** - Clearly explain in description: "Cannot fully test locally (reason: <reason>), requesting help from maintainers to verify"
   - ✅ **Or ask for help** - Ask user to provide testing environment or request community help

   **What NOT to do:**
   - ❌ Don't say "cannot test locally" in a normal PR description
   - ❌ Don't assume unit tests passing means the code works
   - ❌ Don't submit PR without user's manual testing (unless Draft PR)

2. **🚨 Check Issue for Existing PRs (MUST DO)**

   **Before starting implementation, ALWAYS check if the issue already has a linked PR:**
   - Use `mcp__github__search_pull_requests` with query `repo:owner/repo is:pr issue_number`
   - Or check the issue timeline/discussion for linked PRs
   - If a PR already exists:
     - ✅ If the PR is open and recent → **Skip this issue, select another**
     - ✅ If the PR is closed without merging → Check why, then decide
     - ✅ If the PR is merged → **Issue is already fixed, skip**

   **Today's lesson (2026-06-24):**
   - Issue #51754 had PR #51768 already linked
   - Always check to avoid duplicate work

3. **Token Management**:
   - Use correct GitHub token (personal access token with `repo` scope)
   - Token should be `ghp_` prefix (full access), not `ghu_` (limited)
   - Sync token from `~/.zshrc` to WorkBuddy connector if needed

2. **🚨 Testing Requirements (MANDATORY)**
   
   **What constitutes "verification":**
   - ✅ **Unit tests pass** - Necessary but NOT sufficient
   - ✅ **User manually tests the changes** - MANDATORY before PR submission
   - ✅ **User verifies in real environment** - Not just in test suite
   
   **For different types of applications:**
   
   | Application Type | How User Must Test |
   |------------------|-------------------|
   | **GUI Application (Electron, React, Vue, etc.)** | Launch the app, manually click buttons, enter commands, verify UI updates correctly |
   | **CLI Tool** | Run the CLI command in terminal, verify output is correct |
   | **Library/Framework** | Write a small test script, import the function, verify it works |
   | **API Server** | Start the server, send HTTP requests, verify responses |
   
   **If user cannot test:**
   - ❌ **Don't submit normal PR** - This will likely be rejected
   - ✅ **Submit as Draft PR** - Clearly explain in description: "Cannot fully test locally (reason: <reason>), requesting help from maintainers to verify"
   - ✅ **Or ask for help** - Ask user to provide testing environment or request community help
   
   **What NOT to do:**
   - ❌ Don't say "cannot test locally" in a normal PR description
   - ❌ Don't assume unit tests passing means the code works
   - ❌ Don't submit PR without user's manual testing (unless Draft PR)

3. **Fork vs Direct Push**:
   - First-time contributors typically need to fork
   - Check if you have write access to the repository
   - Use fork-based workflow if needed

4. **CI Approval for First-Time Contributors**:
   - Some projects require maintainer approval for CI runs (security measure)
   - Be patient and responsive to maintainer requests

5. **Code Style**:
   - Follow the project's style guide
   - Run formatters (black, isort) before committing
   - Use type hints (Python) or TypeScript types

6. **Not Limited to Issues**:
   - Can submit PRs for self-discovered bugs or improvements
   - Small changes (docs, bug fixes) don't need corresponding issues
   - Large changes (new features) should discuss in issues first

7. **Follow Project Conventions**:
   - Read and follow CONTRIBUTING.md
   - Some projects require signing CLA
   - Some projects have specific PR naming conventions

## Troubleshooting

### Issue: CI checks fail after PR submission
**Solution**: Run the same checks locally before submitting. Use `poe` tasks or equivalent.

### Issue: "Recipient not found" when pushing
**Solution**: Ensure you're pushing to the correct branch and have proper authentication.

### Issue: PR submitted without approval
**Solution**: The skill enforces approval check via `.PR_APPROVAL` file. Ensure this file exists with "APPROVED" content before allowing submission.

### Issue: Wrong GitHub token
**Solution**: Check token in `~/.zshrc` and sync to WorkBuddy connector. Use `ghp_` prefix token.

### Issue: User rejects the implementation plan
**Solution**: Return to Phase 1 (Search) and select a different issue, or terminate the workflow.

### Issue: Unsure if PR needs a corresponding issue
**Solution**: For small changes (bug fixes, docs), submit PR directly. For large changes (new features), open an issue first to discuss.

## Reference Files

- `scripts/ai_contribute_bot.py`: Main automation script (located in user's project directory)
- `references/best-practices.md`: Lessons learned and best practices
- `references/workflow_diagram.md`: Visual workflow (if needed)

## Future Improvements

- [ ] Auto-detect project's CI system and commands
- [ ] Integrate with more projects (not just AutoGen)
- [ ] Auto-generate tests for simple issues
- [ ] Smart issue recommendation based on user's expertise
- [ ] Auto-generate implementation plan in Phase 3
- [ ] Discover projects from GitHub Trending, Reddit, Hacker News
