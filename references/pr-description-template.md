# PR Description Template (for daily_stock_analysis)

Use this template when creating PRs for daily_stock_analysis project.

## When to use

- Creating PR for daily_stock_analysis
- Need to follow project PR standards
- Want to avoid reviewer blockers

## Template

```markdown
## 概述

本 PR 实现了 Issue #NUMBER 的需求，为...添加...功能。

## 解决的问题

- 当前系统...
- 用户无法...
- 缺少...

## 主要改动

### 1. 数据模型 (`src/schemas/report_schema.py`)

- 新增 `ModelName` 模型，包含：
  - `field1`: 描述 (类型)
  - `field2`: 描述 (类型)
- 在 `ParentModel` 中新增 `field_name` 字段
- **添加 `model_validator` 验证器**：自动转换字符串为数字、归零负数、归一化...

### 2. Prompt 优化 (`src/analyzer.py`)

- 在 SYSTEM_PROMPT 和 LEGACY_DEFAULT_SYSTEM_PROMPT 中添加 `field_name` 字段说明
- **详细说明字段含义**（定义、示例、计算方法）
- **强制约束**：...
- 添加"必须输出"指令，确保 LLM 生成该字段

### 3. Agent 路径同步 (`src/agent/executor.py`, `src/agent/agents/decision_agent.py`)

- 更新 `LEGACY_DEFAULT_AGENT_SYSTEM_PROMPT` 和 `AGENT_SYSTEM_PROMPT` 的 JSON 示例，添加 `field_name`
- 添加"必须输出 `dashboard.field_name`"约束
- 更新 `decision_agent.py` 的 prompt，要求包含 `field_name` 字段
- **确保 agent/multi-agent 分析时也生成 field_name 字段**

### 4. 报告展示 - 默认模式 (`src/notification.py`)

- 在 `generate_dashboard_report()` 中添加字段展示代码
- 展示...
- **添加辅助函数**：正确处理 None 值

### 5. 报告展示 - 渲染模式 (`templates/report_markdown.j2`)

- 添加 `field_name` 的 Jinja2 模板代码
- 支持条件渲染（仅在字段有内容时显示）
- **正确处理 None 值**：不显示 "None%"

### 6. 国际化支持 (`src/report_language.py`)

- 新增 N 个国际化标签（中英文）
- 包括：...

## 测试

### 真实 API 测试

- 使用 XXX API 进行测试
- LLM 成功生成 `field_name` 字段
- **约束条件满足** ✅
- 示例输出：
  ```json
  "field_name": {
    "field1": value1,
    "field2": value2
  }
  ```

### 回归测试（新增 `tests/test_feature.py`）

- ✅ Schema 验证测试（N 个测试用例）
- ✅ 字符串转换测试
- ✅ 边界值处理测试
- ✅ None 值处理测试
- ✅ 字段归一化测试
- ✅ 中英文国际化标签测试

### CI 检查

- ✅ 已执行 `./scripts/ci_gate.sh`
- ✅ M 个测试通过
- ✅ 所有检查通过
- ✅ Python 语法检查通过
- ✅ flake8 检查通过

## 模型/API/配置兼容性说明

**本 PR 无以下变更**:
- ❌ 无 provider 变更
- ❌ 无 model 变更
- ❌ 无 Base URL 变更
- ❌ 无默认模型变更
- ❌ 无保存前清理逻辑变更
- ❌ 无配置迁移变更

本 PR 仅添加新的可选字段，不影响现有功能。

## Checklist

- [x] 代码自测通过
- [x] 真实 API 测试通过
- [x] 与其他字段实现一致（schema、prompt、notification、template）
- [x] Agent 路径同步完成
- [x] 添加字段验证/防护逻辑
- [x] 添加国际化支持
- [x] 更新 docs/CHANGELOG.md
- [x] 添加回归测试
- [x] CI 检查通过 (`./scripts/ci_gate.sh`)

## 后续优化建议

1. **字段名 字段展示**：当前 `字段名` 字段在 `notification.py` 中缺少展示代码，建议后续补充（已创建 Issue #XXX 追踪）
2. **字段计算优化**：可以进一步优化 prompt，让 LLM 更准确地计算字段值
3. **前端展示优化**：可以添加可视化图表展示...

## 相关 Issue

Closes #NUMBER

---

**注意**：这是针对上游仓库 `OWNER/REPO` 的 PR，来自 fork 仓库 `FORK_USER/REPO` 的 `BRANCH_NAME` 分支。
```

## Usage

1. Copy template to project root as `PR_DESCRIPTION_DRAFT.md`
2. Replace placeholders (NUMBER, field_name, etc.) with actual values
3. Adjust sections based on actual changes
4. Use this as the PR description when creating PR
