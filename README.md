# auto-contribute

GitHub 开源贡献自动化 Skill - 帮助开发者自动发现并贡献开源项目

## 📋 项目简介

`auto-contribute` 是一个为 [WorkBuddy](https://www.codebuddy.cn) 设计的自动化技能（Skill），帮助你：

- 🔍 **自动发现**可贡献的开源项目 Issue
- 🛠️ **自动实施**代码修复
- ✅ **自动验证**修改是否正确
- 📤 **自动提交** Pull Request
- 📊 **自动监控** PR 状态和反馈

**适用场景**：
- 想要定期贡献开源项目，但不知道从何开始
- 希望自动化重复性的贡献流程
- 需要遵循最佳实践的开源贡献工作流

---

## ✨ 功能特性

### 1. 智能 Issue 发现

从多种来源发现可贡献的 Issue：

- **GitHub Trending**：最近流行的项目
- **Explore 页面**：Machine Learning、AI Tools、Developer Tools 分类
- **Reddit / Hacker News**：社区推荐的项目
- **传统热门项目**：AutoGen、CrewAI、OpenHands 等（备选）

### 2. 严格的验证流程

遵循开源贡献最佳实践：

- ✅ **读取 Issue 所有评论**（评估实际状态，避免重复劳动）
- ✅ **检查 PR 关联**（避免为已有 PR 的 Issue 重复工作）
- ✅ **本地 CI 检查**（format、lint、typecheck、测试）
- ✅ **用户手动测试**（对于 GUI 应用，必须实际启动验证）
- ✅ **人工批准门控**（永远不会自动提交 PR）

### 3. 完整的贡献类型支持

不仅限于有 Issue 的 PR：

- **类型 A**：有 Issue → PR（适用于大改动）
- **类型 B**：无 Issue → PR（适用于小改动，如 bug 修复、文档改进）
- **类型 C**：自主发现贡献机会（阅读代码、使用项目时发现）

---

## 🚀 安装到 WorkBuddy

### 方法 1：从 GitHub 安装（推荐）

```bash
# 克隆仓库到 WorkBuddy skills 目录
cd ~/.workbuddy/skills/
git clone https://github.com/hsms4710-pixel/auto-contribute.git pr-contribute

# 重启 WorkBuddy 或重新加载 Skills
```

### 方法 2：手动下载

1. 下载仓库 ZIP：https://github.com/hsms4710-pixel/auto-contribute/archive/refs/heads/main.zip
2. 解压到 `~/.workbuddy/skills/pr-contribute/`
3. 重启 WorkBuddy

### 验证安装

在 WorkBuddy 中运行：
```
@skill:pr-contribute 帮我找到一个可以贡献的 issue
```

如果看到实现计划输出，说明安装成功。

---

## 📖 使用方法

### 方法 1：作为自动化任务使用（推荐）

自动化任务会在每天固定时间自动执行贡献流程。

#### 设置自动化任务

在 WorkBuddy 中：

1. 打开**自动化管理**页面
2. 创建新任务，选择 `pr-contribute` skill
3. 配置执行时间（如每天 11:00）
4. 启用任务

#### 自动化任务工作流程

```
11:00 - 任务触发
  │
  ├─ Phase 1: 发现贡献机会（30 分钟）
  │   ├─ 搜索 GitHub Trending
  │   ├─ 浏览 Explore 页面
  │   └─ 检查 Reddit/HN
  │
  ├─ Phase 2: 分析贡献机会（30 分钟）
  │   ├─ 读取 Issue 详情和评论
  │   ├─ 检查是否已有 PR 关联
  │   └─ 输出分析摘要
  │
  ├─ Phase 3: 展示实现计划（等待批准）
  │   └─ 用户批准后才继续
  │
  ├─ Phase 4: 实施并验证（60 分钟）
  │   ├─ 设置开发环境
  │   ├─ 实施代码修改
  │   ├─ 运行单元测试
  │   └─ 要求用户手动测试
  │
  ├─ Phase 5: 本地 CI 检查
  │   ├─ Format
  │   ├─ Lint
  │   ├─ Typecheck
  │   └─ 测试
  │
  ├─ Phase 6: 生成审查材料（等待批准）
  │   └─ 用户批准后才提交 PR
  │
  ├─ Phase 7: 提交 PR
  │   └─ 仅在用户明确批准后
  │
  └─ Phase 8: 监控 PR
      ├─ 检查 CI 状态
      └─ 响应审查者反馈
```

#### 自动化任务输出

任务执行后，你会收到：

1. **实现计划文档**（Phase 3 生成）
   - Issue 分析
   - 实现方案
   - 风险评估

2. **审查材料**（Phase 6 生成）
   - 修改的文件列表
   - 验证结果
   - 用户手动测试详情

3. **PR 链接**（Phase 7 创建后）
   - PR 编号和 URL
   - PR 描述

---

### 方法 2：手动使用

你可以在对话中手动调用 `pr-contribute` skill。

#### 示例 1：寻找可贡献的 Issue

```
用户：@skill:pr-contribute 帮我找一个可以贡献的 issue

Skill 输出：
我已找到 3 个可贡献的 Issue：

1. [NousResearch/hermes-agent #51754]
   标题：Enable /reasoning, /fast, /voice, /skills commands in desktop
   类型：Bug fix
   难度：中等
   
2. [microg/play-services-oss #1234]
   标题：Fix location handling in fallback mode
   类型：Bug fix
   难度：简单
   
3. [modelcontextprotocol/servers #567]
   标题：Add support for custom headers in fetch server
   类型：Feature request
   难度：中等

请选择一个 Issue，我将生成实现计划。
```

#### 示例 2：自主发现贡献机会

```
用户：@skill:pr-contribute 我正在使用 hermes-agent，发现文档有错误

Skill 输出：
我已记录你发现的问题：

- 文件：docs/installation.md
- 问题：Python 版本要求写的是 3.9+，但实际需要 3.11+
- 建议：提交文档修复 PR

是否继续？
```

---

## ⚙️ 配置说明

### GitHub Token 配置

Skill 需要 GitHub Personal Access Token 来：

- 读取 Issue 和 PR
- 创建 PR
- 推送分支到 fork

#### 设置 Token

在 `~/.zshrc` 中添加：

```bash
export GITHUB_TOKEN="ghp_xxxxxxx"  # 你的 Personal Access Token
```

**Token 权限要求**：
- `repo` (完整仓库访问权限)
- `workflow` (可选，如果需要更新 GitHub Actions)

#### 验证 Token

```bash
source ~/.zshrc
curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | jq -r '.login'
```

应该输出你的 GitHub 用户名。

---

### Git 配置

Skill 会使用 Git 来克隆仓库、创建分支、提交修改。

#### 配置 Git 用户信息

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### 配置 Git 凭证存储（推荐）

```bash
git config --global credential.helper store
```

然后在第一次推送时输入用户名和 Token（作为密码），Git 会自动保存。

---

## 📋 工作流程详解

### Phase 1: 发现贡献机会

Skill 会从以下来源寻找可贡献的 Issue：

| 来源 | 方法 | 筛选条件 |
|------|------|----------|
| GitHub Trending | 爬取 https://github.com/trending | AI 相关、最近 7 天流行 |
| Explore 页面 | 浏览 GitHub Explore | Machine Learning、AI Tools 分类 |
| Reddit | 搜索 r/MachineLearning、r/LocalLLaMA | 高赞帖子 |
| Hacker News | 搜索 "open source AI tool" | 最近讨论 |
| 传统热门项目 | 直接访问仓库 | 有 `good first issue` 标签 |

---

### Phase 2: 分析贡献机会

**🚨 重要**：此阶段会读取 Issue 的**所有评论**，以避免重复劳动。

分析内容：

1. **Issue 详情**
   - 标题、描述
   - 标签（`good first issue`、`help wanted`）
   - 创建时间、最后更新时间

2. **Issue 评论**
   - 维护者的回复（是否已有人处理？）
   - 其他贡献者的评论（是否已有 PR？）
   - 技术讨论（实现方案是否明确？）

3. **PR 关联检查**
   - 使用 `mcp__github__search_pull_requests` 搜索
   - 查询：`repo:owner/repo is:pr issue_number`
   - 如果已有 PR：
     - PR 是 open → 跳过这个 issue
     - PR 是 closed → 检查是否合并

---

### Phase 3: 展示实现计划（审批门控）

**🚨 重要**：此阶段**必须**等待用户明确批准，才会继续。

实现计划包含：

1. **贡献信息**
   - 类型（Issue-based PR / Self-discovered bug fix）
   - Issue 链接
   - 标题

2. **问题描述**
   - 当前行为
   - 期望行为
   - 根因分析

3. **实现方案**
   - 修改的文件
   - 具体的代码变更
   - 替代方案（如果有）

4. **验证计划**
   - 单元测试
   - 集成测试
   - 手动测试步骤

5. **风险评估**
   - 低/中/高
   - 回退方案

**用户响应**：
- **"批准"** 或 **"Approved"** → 继续 Phase 4
- **"修改: <指令>"** → 更新计划，重新展示
- **"拒绝"** → 终止，返回 Phase 1

---

### Phase 4: 实施并验证

**🚨 重要**：此阶段**必须**让用户手动测试，才能继续。

#### 步骤 1：设置开发环境

```bash
# 克隆仓库
git clone https://github.com/owner/repo.git
cd repo

# 安装依赖
pip install -e ".[dev]"  # Python
# 或
npm install  # Node.js
```

#### 步骤 2：实施代码修改

- 创建新分支：`git checkout -b fix/issue-description`
- 修改代码
- 添加/修改测试

#### 步骤 3：运行验证

```bash
# Python 项目
pytest tests/test_specific.py -v
pyright --project .

# Node.js 项目
npm run test
npm run typecheck
```

#### 步骤 4：要求用户手动测试

**🚨 此步骤不可跳过！**

Skill 会输出手动测试步骤，并等待用户确认：

```
我已修改代码并通过了单元测试。

在你手动测试之前，我不会提交 PR。

请按以下步骤测试：
1. 启动开发服务器：npm run dev
2. 打开应用并执行 /reasoning 命令
3. 验证命令可以正常执行
4. 验证命令不会出现在建议列表中

测试完成后，请告诉我结果。
```

**用户响应**：
- **测试通过** → 继续 Phase 5
- **测试失败** → 返回步骤 2，修复问题
- **无法测试** → 提交 Draft PR，并在描述中说明原因

---

### Phase 5: 本地 CI 检查

运行项目的完整 CI 检查：

```bash
# Python 项目
black --check .
pylint **/*.py
pyright --project .
pytest

# Node.js 项目
npm run format:check
npm run lint
npm run typecheck
npm run test
```

如果有错误，自动修复并重新检查。

---

### Phase 6: 生成审查材料

**🚨 重要**：此阶段**必须**等待用户明确批准，才会提交 PR。

审查材料包含：

1. **贡献信息**
2. **实现计划**
3. **修改的文件列表**
4. **验证结果**
   - 本地 CI 检查结果
   - 测试覆盖率
5. **🚨 用户手动测试详情**
   - 测试环境（操作系统、依赖版本）
   - 测试步骤
   - 测试结果（通过/失败）
   - 截图（如果是 GUI 应用）
6. **风险评估**
7. **PR 提交类型**
   - Normal PR（用户已充分测试）
   - Draft PR（用户无法充分测试）

**用户响应**：
- **"批准"** 或 **"Approved"** → 继续 Phase 7
- **"修改: <指令>"** → 更新材料，重新展示
- **"拒绝"** → 终止，不提交 PR

---

### Phase 7: 提交 PR

**🚨 重要**：仅在用户明确批准后执行。

#### 步骤 1：提交修改

```bash
git add .
git commit -m "fix: <description>

- <change 1>
- <change 2>

Fixes #XXXX"
```

#### 步骤 2：推送到 fork

```bash
# 添加 fork 远程仓库
git remote add fork https://github.com/your-username/repo.git

# 推送分支
git push fork fix/issue-description
```

**🚨 认证问题排查**：

如果推送失败，检查：
1. GitHub Token 是否正确配置？
2. Git 凭证存储是否配置？
3. 是否使用了正确的 Token 格式（`https://token@github.com`）？

#### 步骤 3：创建 PR

使用 `mcp__github__create_pull_request` 或手动在 GitHub 上创建。

**PR 描述模板**：

```markdown
## Summary
<简短描述修改内容>

## Related Issue
Fixes #XXXX

## Changes Made
- <change 1>
- <change 2>

## Test Plan
- [x] 单元测试通过
- [x] 本地 CI 检查通过
- [x] 用户手动测试通过（详见审查材料）

## Notes
<其他说明>
```

**🚨 重要**：
- ❌ 不要在 PR 描述中写 "无法充分测试" 或 "needs manual verification"
- ✅ 如果确实无法测试，提交 Draft PR，并在描述中说明原因

---

### Phase 8: 监控 PR

提交 PR 后，Skill 会持续监控：

1. **CI 状态**
   - 检查 GitHub Actions 是否通过
   - 如果失败，诊断原因并修复

2. **审查者反馈**
   - 读取 PR 评论
   - 响应审查者的请求变更
   - 更新代码并推送

3. **合并状态**
   - 检查 PR 是否已合并
   - 如果合并，关闭相关 Issue（如果未自动关闭）

---

## 🚨 重要注意事项

### 1. 必须先让用户手动测试

**❌ 错误做法**：
- 只运行单元测试就提交 PR
- 在 PR 描述中写 "无法充分测试（需要图形界面）"

**✅ 正确做法**：
- 对于 GUI 应用，启动应用并手动验证 UI 行为
- 对于 CLI 工具，运行命令并验证输出
- 如果用户无法测试，提交 Draft PR

---

### 2. 必须检查 Issue 是否已有 PR 关联

**❌ 错误做法**：
- 直接开始实施，结果发现已有 PR

**✅ 正确做法**：
- 在开始实施前，使用 `mcp__github__search_pull_requests` 检查
- 查询：`repo:owner/repo is:pr issue_number`
- 如果已有 PR：
  - PR 是 open → 跳过这个 issue
  - PR 是 closed → 检查是否合并

---

### 3. PR 描述不能写借口

**❌ 错误做法**：
```markdown
## Notes
Since this PR involves Electron GUI application, I cannot fully test it locally (needs graphical interface).
Please ask maintainers or community members to help verify the GUI behavior.
```

**✅ 正确做法**：
- 如果已充分测试 → 正常写 PR 描述
- 如果无法充分测试 → 提交 Draft PR，并说明：
  ```markdown
  ## Notes
  - Tested backend logic (unit tests pass)
  - Cannot test GUI behavior (no macOS environment)
  - Requesting help from maintainers to verify GUI
  ```

---

### 4. 遵循项目贡献指南

**❌ 错误做法**：
- 不读 CONTRIBUTING.md 就提交 PR
- 使用错误的代码风格

**✅ 正确做法**：
- 读取并遵循 CONTRIBUTING.md
- 运行项目推荐的 format/lint 工具
- 使用项目约定的提交信息格式

---

## 📊 今天的经验教训（2026-06-24）

### 错误 1: 提交 PR 前未充分测试

**问题**：提交了 PR #51768，但在描述中写 "无法充分测试（需要图形界面）"

**后果**：用户要求关闭 PR，因为这是借口

**教训**：
- ✅ 必须先让用户手动测试，通过后才提交 PR
- ✅ 如果遇到测试障碍（如需要 GUI），应该先解决测试问题，或提交 Draft PR
- ❌ 不要在 PR 描述中写 "cannot test locally" 这种话

---

### 错误 2: 未检查 Issue 是否已有 PR 关联

**问题**：Issue #51754 已经有 PR #51768 关联（是我自己创建的）

**后果**：浪费时间在已有的 PR 上

**教训**：
- ✅ 在开始实施前，必须检查 Issue 是否已有 PR 关联
- ✅ 使用 `mcp__github__search_pull_requests` 搜索
- ✅ 如果已有 PR，检查其状态（open/closed/merged）

---

### 错误 3: 推送分支到 fork 时认证失败

**问题**：使用 `https://username:token@github.com` 格式推送失败

**原因**：GitHub 已不支持密码认证，必须使用正确的 Token 格式或 SSH

**解决方案**：
- ✅ 配置 Git credential helper: `git config --global credential.helper store`
- ✅ 将 Token 写入 `~/.git-credentials`: `https://token@github.com`
- ✅ 或者使用 SSH 密钥

---

## 🛠️ 故障排除

### 问题 1：Skill 无法读取 Issue 详情

**症状**：`mcp__github__issue_read` 返回错误

**原因**：
- GitHub Token 未配置或已过期
- Token 权限不足

**解决方案**：
1. 检查 Token 是否配置：`echo $GITHUB_TOKEN`
2. 验证 Token 权限：访问 https://github.com/settings/tokens
3. 重新生成 Token（如果需要）

---

### 问题 2：无法推送分支到 fork

**症状**：`git push` 失败，提示认证错误

**原因**：
- Git 凭证未配置
- Token 格式错误

**解决方案**：
1. 配置 Git credential helper：
   ```bash
   git config --global credential.helper store
   echo "https://${GITHUB_TOKEN}@github.com" > ~/.git-credentials
   chmod 600 ~/.git-credentials
   ```

2. 或者使用 SSH：
   ```bash
   # 生成 SSH 密钥
   ssh-keygen -t ed25519 -C "your_email@example.com"
   
   # 添加 SSH 密钥到 GitHub
   cat ~/.ssh/id_ed25519.pub
   # 然后访问：https://github.com/settings/keys 添加
   
   # 更新 fork remote URL 为 SSH
   git remote set-url fork git@github.com:your-username/repo.git
   ```

---

### 问题 3：PR 描述中的中文显示乱码

**症状**：PR 描述中的中文变成乱码

**原因**：Git 提交信息编码问题

**解决方案**：
1. 配置 Git 使用 UTF-8：
   ```bash
   git config --global i18n.commitEncoding utf-8
   git config --global i18n.logOutputEncoding utf-8
   ```

2. 在提交信息中避免中文（如果项目要求）

---

## 📚 参考资料

### WorkBuddy 文档

- [WorkBuddy 官网](https://www.codebuddy.cn)
- [Skill 开发指南](https://www.codebuddy.cn/docs/skills)
- [自动化任务配置](https://www.codebuddy.cn/docs/automations)

### 开源贡献最佳实践

- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [Writing a Good PR Description](https://github.blog/2015-01-21-how-to-write-the-perfect-pull-request/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

### 项目链接

- **GitHub 仓库**：https://github.com/hsms4710-pixel/auto-contribute
- **Issue 追踪**：https://github.com/hsms4710-pixel/auto-contribute/issues
- **PR 列表**：https://github.com/hsms4710-pixel/auto-contribute/pulls

---

## 📄 许可证

MIT License

---

## 👥 贡献指南

欢迎贡献这个 Skill！

1. Fork 这个仓库
2. 创建你的功能分支：`git checkout -b feature/amazing-feature`
3. 提交你的修改：`git commit -m 'Add some amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 提交 Pull Request

---

## 📧 联系方式

如果你有任何问题或建议，请：

- 提交 Issue：https://github.com/hsms4710-pixel/auto-contribute/issues
- 发送邮件：your-email@example.com

---

**Happy Contributing! 🎉**
