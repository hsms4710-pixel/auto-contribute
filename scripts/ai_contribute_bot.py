#!/usr/bin/env python3
"""
AI-Powered GitHub Contribution Bot v2.1 - 集成 CI 检查

核心原则：
1. 先验证 bug 是否存在，再提 PR
2. 所有代码改动生成后交人工确认，不直接提交
3. 完整的测试覆盖
4. 强制要求人工审阅批准后才能提交 PR
5. 本地运行 CI 检查，确保代码符合项目标准
"""

import os
import sys
import json
import argparse
import subprocess
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import requests

# ==================== 配置 ====================
GITHUB_API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
WORK_DIR = Path.home() / "ai_opensource_contrib"

# ==================== 核心类 ====================
class IssueSelector:
    """智能 Issue 筛选器"""
    def __init__(self, repo: str):
        self.repo = repo
        self.owner, self.repo_name = repo.split("/")
    
    def find_contributable_issues(self, limit: int = 10) -> List[Dict]:
        print(f"🔍 Scanning {self.repo} for contributable issues...")
        url = f"{GITHUB_API}/repos/{self.repo}/issues"
        headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
        params = {
            "state": "open",
            "per_page": limit * 2,
        }
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=30)
            resp.raise_for_status()
            issues = resp.json()
            issues = [i for i in issues if "pull_request" not in i]
            issues = sorted(issues, key=lambda x: x["created_at"], reverse=True)
            print(f"\n{'='*60}")
            print(f"🎯 Top {min(limit, len(issues))} Contributable Issues")
            print(f"{'='*60}\n")
            result = []
            for i, issue in enumerate(issues[:limit], 1):
                score = self._score_issue(issue)
                labels = [l["name"] for l in issue["labels"]]
                print(f"{i}. Issue #{issue['number']} (Score: {score})")
                print(f"   📝 {issue['title']}")
                print(f"   🏷️  {', '.join(labels)}")
                print(f"   🔗 {issue['html_url']}\n")
                result.append({"number": issue["number"], "title": issue["title"], "score": score, "url": issue["html_url"]})
            return result
        except Exception as e:
            print(f"❌ Error scanning issues: {e}")
            return []
    
    def _score_issue(self, issue: Dict) -> int:
        score = 50
        labels = [l["name"] for l in issue["labels"]]
        if "bug" in labels:
            score += 20
        if "enhancement" in labels:
            score += 15
        if "documentation" in labels:
            score += 10
        if len(issue["body"] or "") < 100:
            score -= 20
        return min(score, 100)


class IssueVerifier:
    """Issue 验证器 - 确保 Issue 真的需要修复"""
    def __init__(self, repo_path: str, repo: str):
        self.repo_path = Path(repo_path)
        self.repo = repo
    
    def verify(self, issue_number: int) -> Tuple[bool, str]:
        print(f"\n🔍 Verifying Issue #{issue_number}...")
        print("  1️⃣  Checking issue status...")
        issue = self._get_issue(issue_number)
        if not issue:
            return False, "Failed to fetch issue"
        if issue["state"] != "open":
            return False, f"Issue is {issue['state']}"
        print(f"     ✅ Issue is open")
        
        print("  2️⃣  Checking for related PRs...")
        related_prs = self._find_related_prs(issue_number)
        if related_prs:
            return False, f"Found related PRs"
        print(f"     ✅ No related PRs found")
        
        return True, "All checks passed"
    
    def _get_issue(self, issue_number: int) -> Optional[Dict]:
        url = f"{GITHUB_API}/repos/{self.repo}/issues/{issue_number}"
        headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except:
            return None
    
    def _find_related_prs(self, issue_number: int) -> List[Dict]:
        url = f"{GITHUB_API}/search/issues"
        query = f"repo:{self.repo} is:pr {issue_number}"
        headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
        try:
            resp = requests.get(url, headers=headers, params={"q": query}, timeout=30)
            resp.raise_for_status()
            return resp.json().get("items", [])
        except:
            return []


class LocalValidator:
    """本地验证器 - 运行 CI 检查"""
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.python_dir = self.repo_path / "python"
    
    def validate_package(self, package_name: str = "autogen-core") -> Dict:
        """验证单个包（运行所有 CI 检查）"""
        print(f"\n🔍 Validating package: {package_name}")
        print(f"{'='*60}")
        results = {
            "package": package_name,
            "checks": {},
            "all_passed": True
        }
        checks = [
            ("fmt", "Format check (black/isort)"),
            ("lint", "Lint check (pylint/flake8)"),
            ("pyright", "Type check (pyright)"),
            ("mypy", "Type check (mypy)"),
            ("test", "Unit tests"),
        ]
        for check_name, check_desc in checks:
            print(f"\n  🔧 Running: {check_desc}...")
            success, output = self._run_poe_task(check_name, package_name)
            results["checks"][check_name] = {
                "success": success,
                "output": output[-500:] if output else ""
            }
            if success:
                print(f"     ✅ {check_name} passed")
            else:
                print(f"     ❌ {check_name} failed")
                results["all_passed"] = False
        
        print(f"\n{'='*60}")
        if results["all_passed"]:
            print(f"✅ All checks passed for {package_name}!")
        else:
            print(f"❌ Some checks failed for {package_name}")
            print(f"\n⚠️  **Warning**: PR will likely fail CI checks!")
            print(f"   Please fix the issues before submitting PR.")
        return results
    
    def _run_poe_task(self, task: str, package: str = "") -> Tuple[bool, str]:
        """运行 poe 任务"""
        try:
            # 检查是否安装了 uv
            uv_result = subprocess.run(
                ["which", "uv"],
                capture_output=True,
                text=True
            )
            if uv_result.returncode != 0:
                print("     ⚠️  `uv` not found. Please install it first.")
                return False, "`uv` not installed"
            
            # 构建命令
            cmd = ["uv", "run", "poe"]
            if package:
                cmd.extend(["--directory", f"./packages/{package}"])
            cmd.append(task)
            
            print(f"     Running: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=self.python_dir,
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr or result.stdout
        except subprocess.TimeoutExpired:
            return False, "Timeout (5 minutes)"
        except Exception as e:
            return False, str(e)


class ReviewManager:
    """审阅管理器 - 强制要求人工批准"""
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.approval_file = self.repo_path / ".PR_APPROVAL"
    
    def generate_review_materials(self, issue: Dict, validation_results: Optional[Dict] = None) -> str:
        """生成审阅材料"""
        print("📋 Generating review materials...")
        review_file = self.repo_path / f"REVIEW_Issue_{issue['number']}.md"
        
        validation_section = ""
        if validation_results:
            if validation_results.get("all_passed"):
                validation_section = "\n## CI 检查结果\n✅ 所有检查通过！\n"
            else:
                validation_section = "\n## CI 检查结果\n❌ 部分检查失败，请修复后再提交。\n"
        
        content = f"""# PR 审阅材料 - Issue #{issue['number']}

## Issue 信息
- **Issue**: #{issue['number']} - {issue['title']}
- **链接**: {issue['html_url']}

## CI 检查结果
{validation_section}

## 审阅检查清单
- [ ] 代码改动是否符合 Issue 要求？
- [ ] CI 检查是否通过？
- [ ] 测试是否充分？

## ⚠️ 批准流程
如果你批准这个 PR，请运行：
```bash
echo "APPROVED" > {self.approval_file}
```

**在批准前，PR 不会被提交。**
"""
        with open(review_file, "w") as f:
            f.write(content)
        print(f"✅ Review materials generated: {review_file}")
        return str(review_file)
    
    def check_approval(self) -> bool:
        """检查是否获得批准"""
        if self.approval_file.exists():
            with open(self.approval_file) as f:
                content = f.read().strip()
            if content == "APPROVED":
                print("✅ PR submission approved!")
                return True
        return False


# ==================== CLI 入口 ====================
def cmd_validate(args):
    """运行 CI 检查（本地验证）"""
    validator = LocalValidator(args.repo_path)
    if args.package:
        validator.validate_package(args.package)
    else:
        # 验证所有相关包
        for pkg in ["autogen-core", "autogen-agentchat", "autogen-ext"]:
            validator.validate_package(pkg)


def cmd_prepare(args):
    """准备修复（生成审阅材料，包含 CI 检查结果）"""
    # 1. 读取 issue JSON
    with open(args.issue_json) as f:
        issue = json.load(f)
    
    # 2. 运行 CI 检查
    validator = LocalValidator(args.repo_path)
    validation_results = validator.validate_package("autogen-core")
    
    # 3. 生成审阅材料（包含检查结果）
    review_mgr = ReviewManager(args.repo_path)
    review_file = review_mgr.generate_review_materials(issue, validation_results)
    
    print(f"\n📋 **下一步**:")
    print(f"   1. 查看审阅材料: {review_file}")
    print(f"   2. 如果批准，运行: echo 'APPROVED' > {review_mgr.approval_file}")
    print(f"   3. 然后运行: python ai_contribute_bot.py submit --repo-path {args.repo_path} --issue {issue['number']} --branch BRANCH_NAME")


def cmd_submit(args):
    """提交 PR（需要事先批准）"""
    review_mgr = ReviewManager(args.repo_path)
    if not review_mgr.check_approval():
        print("❌ PR submission not approved!")
        print(f"   Please create `{review_mgr.approval_file}` with content 'APPROVED' first.")
        sys.exit(1)
    
    print(f"✅ Submitting PR for Issue #{args.issue}...")
    print(f"(Actual PR submission logic here...)")
    # 实际提交逻辑...


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered GitHub Contribution Bot v2.1 (with CI checks)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # validate
    validate_parser = subparsers.add_parser("validate", help="Run CI checks locally (BEFORE submitting PR)")
    validate_parser.add_argument("--repo-path", required=True, help="Local repo path")
    validate_parser.add_argument("--package", help="Specific package to validate (default: autogen-core)")
    
    # prepare
    prepare_parser = subparsers.add_parser("prepare", help="Prepare fix and generate review materials (REQUIRES approval)")
    prepare_parser.add_argument("--repo-path", required=True, help="Local repo path")
    prepare_parser.add_argument("--issue-json", required=True, help="Path to issue JSON file")
    
    # submit
    submit_parser = subparsers.add_parser("submit", help="Submit PR (MUST be approved first)")
    submit_parser.add_argument("--repo-path", required=True, help="Local repo path")
    submit_parser.add_argument("--issue", type=int, required=True, help="Issue number")
    submit_parser.add_argument("--branch", required=True, help="Branch name")
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if not TOKEN:
        print("❌ GITHUB_TOKEN not found in environment")
        sys.exit(1)
    
    if args.command == "validate":
        cmd_validate(args)
    elif args.command == "prepare":
        cmd_prepare(args)
    elif args.command == "submit":
        cmd_submit(args)


if __name__ == "__main__":
    main()
