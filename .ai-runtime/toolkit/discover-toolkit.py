#!/usr/bin/env python3
"""
Toolkit Discovery Tool
用于发现和查询工具装备的工具
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse

class ToolkitDiscovery:
    def __init__(self, toolkit_root: Path):
        self.root = toolkit_root
        self.registry = {}
        self.tools = []
        self.external_tools = []
        self.load_registry()
        self.detect_external_tools()

    def load_registry(self):
        """加载工具注册表"""
        registry_file = self.root / "registry.md"
        if registry_file.exists():
            self.extract_tools_from_registry(registry_file)

        # 扫描所有语言目录
        for lang_dir in self.root.iterdir():
            if lang_dir.is_dir() and not lang_dir.name.startswith('.'):
                self.scan_language_tools(lang_dir)

    def extract_tools_from_registry(self, registry_file: Path):
        """从registry.md中提取工具列表"""
        content = registry_file.read_text()
        # 简单的提取逻辑，实际可以解析markdown表格
        # 这里我们先跳过，主要通过.meta.yml文件
        pass

    def scan_language_tools(self, lang_dir: Path):
        """扫描语言目录下的所有工具"""
        for meta_file in lang_dir.rglob("*.meta.yml"):
            try:
                tool_info = self.parse_meta_file(meta_file)
                if tool_info:
                    self.tools.append(tool_info)
            except Exception as e:
                print(f"⚠️  解析失败 {meta_file}: {e}", file=sys.stderr)

    def parse_meta_file(self, meta_file: Path) -> Optional[Dict[str, Any]]:
        """解析元数据文件"""
        try:
            content = yaml.safe_load(meta_file.read_text())
            if not content:
                return None

            # 获取工具所在的实际文件
            tool_file = None
            possible_extensions = ['.sh', '.py', '.js', '.ts']
            for ext in possible_extensions:
                possible_file = meta_file.with_suffix(ext)
                if possible_file.exists():
                    tool_file = possible_file
                    break

            return {
                "meta_file": str(meta_file.relative_to(self.root)),
                "tool_file": str(tool_file.relative_to(self.root)) if tool_file else None,
                "tool_id": content.get("tool_id", "unknown"),
                "tool_name": content.get("tool_name", "未命名工具"),
                "language": content.get("基本信息", {}).get("语言", "unknown"),
                "file": content.get("基本信息", {}).get("文件", "unknown"),
                "complexity": content.get("基本信息", {}).get("复杂度", "unknown"),
                "purpose": content.get("用途分类", []),
                "description": content.get("功能描述", {}).get("简介", ""),
                "usage": content.get("使用方法", {}),
                "last_use": content.get("上次使用", {}),
                "satisfaction": content.get("上次使用", {}).get("满意度", 0),
                "full_meta": content
            }
        except Exception as e:
            return None

    def detect_external_tools(self):
        """检测系统已安装的外部CLI工具"""
        external_tool_configs = [
            {
                "tool_id": "EXT-FZF-001",
                "tool_name": "fzf (Fuzzy Finder)",
                "command": "fzf",
                "description": "命令行模糊查找器，用于交互式选择",
                "category": "搜索/交互",
                "use_cases": ["文件名查找", "历史命令搜索", "Git分支切换"],
                "install_guide": "brew install fzf (macOS) / apt-get install fzf (Ubuntu)"
            },
            {
                "tool_id": "EXT-EZA-001",
                "tool_name": "eza (Modern ls)",
                "command": "eza",
                "description": "现代化的ls替代品，带彩色输出和图标",
                "category": "文件列表",
                "use_cases": ["查看文件列表", "树形结构显示", "Git状态查看"],
                "install_guide": "brew install eza"
            },
            {
                "tool_id": "EXT-ZOXIDE-001",
                "tool_name": "zoxide (Smart cd)",
                "command": "zoxide",
                "description": "智能目录跳转工具，学习访问习惯",
                "category": "目录导航",
                "use_cases": ["快速跳转目录", "访问频率学习"],
                "install_guide": "curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh"
            },
            {
                "tool_id": "EXT-FD-001",
                "tool_name": "fd (Simple find)",
                "command": "fd",
                "description": "简单友好的find替代品",
                "category": "文件搜索",
                "use_cases": ["查找文件", "忽略.gitignore搜索", "执行操作"],
                "install_guide": "brew install fd"
            },
            {
                "tool_id": "EXT-RG-001",
                "tool_name": "ripgrep (rg)",
                "command": "rg",
                "description": "极速代码搜索工具",
                "category": "代码搜索",
                "use_cases": ["搜索代码", "显示上下文", "统计匹配数"],
                "install_guide": "brew install ripgrep"
            },
            {
                "tool_id": "EXT-BAT-001",
                "tool_name": "bat (cat with syntax)",
                "command": "bat",
                "description": "带语法高亮的cat替代品",
                "category": "文件查看",
                "use_cases": ["查看代码文件", "分页查看", "Git修改查看"],
                "install_guide": "brew install bat"
            },
            {
                "tool_id": "EXT-JQ-001",
                "tool_name": "jq (JSON processor)",
                "command": "jq",
                "description": "JSON数据的命令行处理器",
                "category": "数据处理",
                "use_cases": ["JSON美化", "字段提取", "数据过滤", "格式转换"],
                "install_guide": "brew install jq"
            },
            {
                "tool_id": "EXT-XH-001",
                "tool_name": "xh (HTTP client)",
                "command": "xh",
                "description": "友好的HTTP客户端，替代curl",
                "category": "API测试",
                "use_cases": ["发送HTTP请求", "API测试", "文件下载"],
                "install_guide": "brew install xh"
            },
            {
                "tool_id": "EXT-DELTA-001",
                "tool_name": "delta (Git diff美化)",
                "command": "delta",
                "description": "Git diff的美化工具",
                "category": "Git工具",
                "use_cases": ["查看Git diff", "语法高亮", "行号显示"],
                "install_guide": "brew install git-delta"
            }
        ]

        import shutil
        for config in external_tool_configs:
            if shutil.which(config["command"].split()[0]):
                config["installed"] = True
                config["path"] = shutil.which(config["command"].split()[0])
            else:
                config["installed"] = False
                config["path"] = None

            self.external_tools.append(config)

    def list_tools(self, lang: Optional[str] = None, purpose: Optional[str] = None, query: Optional[str] = None, include_external: bool = False, external_only: bool = False):
        """列出工具，支持过滤"""
        if external_only:
            return self.external_tools

        filtered = self.tools

        if lang:
            filtered = [t for t in filtered if t["language"] == lang]

        if purpose:
            filtered = [t for t in filtered if purpose in t["purpose"]]

        if query:
            filtered = [t for t in filtered if query.lower() in t["tool_name"].lower() or query.lower() in t["description"].lower()]

        if include_external:
            filtered = filtered + self.external_tools

        return filtered

    def show_tool_detail(self, tool_name_or_id: str):
        """显示工具详细信息"""
        tool = self.find_tool(tool_name_or_id)
        if not tool:
            print(f"❌ 未找到工具: {tool_name_or_id}")
            return False

        self.print_tool_detail(tool)
        return True

    def find_tool(self, name_or_id: str) -> Optional[Dict[str, Any]]:
        """查找工具"""
        # 先尝试精确匹配
        for tool in self.tools:
            if tool["tool_id"] == name_or_id or tool["tool_name"] == name_or_id:
                return tool

        # 尝试模糊匹配
        matches = [t for t in self.tools if name_or_id.lower() in t["tool_name"].lower()]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            print(f"⚠️  找到多个匹配工具:")
            for i, tool in enumerate(matches[:5], 1):
                print(f"  {i}. {tool['tool_name']} ({tool['tool_id']})")
            return None

        return None

    def print_tool_detail(self, tool: Dict[str, Any]):
        """打印工具详情"""
        print(f"\n{'='*70}")
        print(f"📦 {tool['tool_name']}")
        print(f"{'='*70}")
        print(f"ID: {tool['tool_id']}")
        print(f"语言: {tool['language']}")
        print(f"文件: {tool['file']}")
        print(f"复杂度: {tool['complexity']}")
        print(f"用途: {', '.join(tool['purpose'])}")
        print(f"\n📋 描述:")
        print(f"  {tool['description']}")

        if tool['usage']:
            print(f"\n🚀 使用方法:")
            if '命令' in tool['usage']:
                print(f"  命令: {tool['usage']['命令']}")
            if '参数' in tool['usage']:
                print(f"  参数:")
                for param, desc in tool['usage']['参数'].items():
                    print(f"    - {param}: {desc}")
            if '示例' in tool['usage']:
                print(f"  示例:")
                for example in tool['usage'].get('示例', [])[:3]:
                    print(f"    • {example}")

        if tool['last_use']:
            print(f"\n📊 使用统计:")
            print(f"  上次使用: {tool['last_use'].get('时间', '未知')}")
            print(f"  用途: {tool['last_use'].get('用途', '未知')}")
            print(f"  满意度: {tool['satisfaction']}/1.0")

        print(f"\n📂 文件位置:")
        print(f"  元数据: {tool['meta_file']}")
        if tool['tool_file']:
            print(f"  工具文件: {tool['tool_file']}")

        print(f"{'='*70}\n")

    def run_tool(self, tool_name_or_id: str, args: List[str]):
        """运行工具"""
        tool = self.find_tool(tool_name_or_id)
        if not tool:
            return False

        tool_path = self.root / tool['tool_file']
        if not tool_path.exists():
            print(f"❌ 工具文件不存在: {tool_path}")
            return False

        print(f"🚀 运行工具: {tool['tool_name']}")
        print(f"📁 文件: {tool['tool_file']}")
        print(f"⏳ 正在执行...")
        print(f"{'='*70}")

        try:
            import subprocess
            cmd = [str(tool_path)] + args
            result = subprocess.run(cmd, capture_output=False)
            print(f"{'='*70}")
            print(f"✅ 执行完成 (退出码: {result.returncode})")
            return result.returncode == 0
        except Exception as e:
            print(f"❌ 执行失败: {e}")
            return False

    def recommend_tool(self, task_description: str):
        """根据任务描述推荐工具"""
        keywords = task_description.lower().split()

        # 简单的推荐算法：匹配关键词
        scores = {}
        for tool in self.tools:
            score = 0
            tool_text = (tool['tool_name'] + ' ' + tool['description'] + ' ' + ' '.join(tool['purpose'])).lower()

            for keyword in keywords:
                if keyword in tool_text:
                    score += 1

            if score > 0:
                scores[tool['tool_id']] = (score, tool)

        # 按分数排序
        sorted_tools = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)

        if not sorted_tools:
            print(f"💡 未找到匹配的工具，尝试使用更通用的关键词搜索")
            return

        print(f"\n🔍 为任务 '{task_description}' 推荐工具:")
        print(f"{'='*70}")

        for i, (tool_id, (score, tool)) in enumerate(sorted_tools[:5], 1):
            print(f"\n{i}. {tool['tool_name']} (匹配度: {score})")
            print(f"   ID: {tool_id}")
            print(f"   语言: {tool['language']}")
            print(f"   描述: {tool['description'][:60]}...")

        print(f"\n{'='*70}")
        print(f"💡 使用: python3 discover-toolkit.py show <tool-id> 查看详情")
        print(f"💡 使用: python3 discover-toolkit.py run <tool-id> [args] 运行工具\n")

def main():
    toolkit_root = Path(__file__).parent
    discovery = ToolkitDiscovery(toolkit_root)

    parser = argparse.ArgumentParser(description="工具包发现和管理工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有工具")
    list_parser.add_argument("--lang", help="按语言过滤 (bash/python/node)")
    list_parser.add_argument("--purpose", help="按用途过滤 (DATA/CODE/TEST/BUILD/MONITOR/DOC)")
    list_parser.add_argument("--query", help="按名称或描述搜索")
    list_parser.add_argument("--json", action="store_true", help="JSON格式输出")
    list_parser.add_argument("--external", action="store_true", help="仅显示外部工具")
    list_parser.add_argument("--include-external", action="store_true", help="包含外部工具")

    # show 命令
    show_parser = subparsers.add_parser("show", help="显示工具详情")
    show_parser.add_argument("tool", help="工具ID或名称")

    # run 命令
    run_parser = subparsers.add_parser("run", help="运行工具")
    run_parser.add_argument("tool", help="工具ID或名称")
    run_parser.add_argument("args", nargs=argparse.REMAINDER, help="工具参数")

    # recommend 命令
    recommend_parser = subparsers.add_parser("recommend", help="推荐工具")
    recommend_parser.add_argument("task", help="任务描述")

    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索工具")
    search_parser.add_argument("keyword", help="搜索关键词")

    args = parser.parse_args()

    if args.command == "list":
        # 处理外部工具选项
        include_external = args.include_external or False
        external_only = args.external or False

        tools = discovery.list_tools(args.lang, args.purpose, args.query, include_external, external_only)

        if args.json:
            print(json.dumps(tools, indent=2, ensure_ascii=False))
        else:
            if not tools:
                print("⚠️  未找到匹配的工具")
                return

            # 分离内部工具和外部工具
            internal_tools = [t for t in tools if 'language' in t]
            external_tools = [t for t in tools if 'category' in t]

            # 显示内部工具
            if internal_tools and not external_only:
                print(f"\n📦 找到 {len(internal_tools)} 个内部工具:")
                print(f"{'='*110}")
                print(f"{'名称':<25} {'ID':<25} {'语言':<8} {'用途':<15} {'描述':<30}")
                print(f"{'-'*110}")

                for tool in internal_tools:
                    purposes = ','.join(tool['purpose'])[:13]
                    desc = tool['description'][:28]
                    print(f"{tool['tool_name']:<25} {tool['tool_id']:<25} {tool['language']:<8} {purposes:<15} {desc:<30}")

                print(f"{'='*110}")

            # 显示外部工具
            if external_tools and (include_external or external_only):
                if internal_tools:
                    print()
                print(f"\n🌟 找到 {len(external_tools)} 个外部工具:")
                print(f"{'='*100}")
                print(f"{'名称':<25} {'ID':<20} {'分类':<12} {'安装状态':<10} {'描述':<30}")
                print(f"{'-'*100}")

                for tool in external_tools:
                    status = "✅ 已安装" if tool.get('installed') else "❌ 未安装"
                    desc = tool['description'][:30]
                    print(f"{tool['tool_name']:<25} {tool['tool_id']:<20} {tool['category']:<12} {status:<10} {desc:<30}")

                print(f"{'='*100}")
                if not external_only:
                    print("\n💡 提示: 使用 --external 仅显示外部工具")
                    print("💡 提示: 外部工具是系统级的CLI工具，需单独安装")

            print()

    elif args.command == "show":
        discovery.show_tool_detail(args.tool)

    elif args.command == "run":
        discovery.run_tool(args.tool, args.args)

    elif args.command == "recommend":
        discovery.recommend_tool(args.task)

    elif args.command == "search":
        tools = discovery.list_tools(query=args.keyword)
        if not tools:
            print(f"⚠️  未找到包含 '{args.keyword}' 的工具")
            return

        print(f"\n🔍 搜索 '{args.keyword}' 找到 {len(tools)} 个结果:")
        for tool in tools:
            print(f"  • {tool['tool_name']} ({tool['tool_id']}) - {tool['description'][:50]}...")
        print()

    else:
        parser.print_help()
        print("\n💡 示例:")
        print("  python3 discover-toolkit.py list                    # 列出所有工具")
        print("  python3 discover-toolkit.py list --lang python     # 列出Python工具")
        print("  python3 discover-toolkit.py list --external        # 仅显示外部工具")
        print("  python3 discover-toolkit.py list --include-external # 包含外部工具")
        print("  python3 discover-toolkit.py show SERVICE-CHECK-001 # 查看工具详情")
        print("  python3 discover-toolkit.py run dependency-analyzer . # 运行工具")
        print("  python3 discover-toolkit.py recommend '分析日志'    # 推荐工具")
        print("  python3 discover-toolkit.py search json             # 搜索工具")
        print()

if __name__ == "__main__":
    main()
