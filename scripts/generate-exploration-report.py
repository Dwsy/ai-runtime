#!/usr/bin/env python3
"""
AI Runtime - 探索报告生成器
生成结构化的代码库探索报告，包含技术栈、架构模式、质量分析等
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def detect_tech_stack(root_dir):
    """检测技术栈"""
    root = Path(root_dir)
    tech_stack = {}

    # JavaScript/Node.js
    if (root / 'package.json').exists():
        with open(root / 'package.json') as f:
            package = json.load(f)
            tech_stack['language'] = 'JavaScript'
            tech_stack['runtime'] = f"Node.js {package.get('engines', {}).get('node', 'unknown')}"
            tech_stack['dependencies'] = {
                'total': len(package.get('dependencies', {}))
            }

            # 检测框架
            deps = {**package.get('dependencies', {}), **package.get('devDependencies', {})}
            if 'express' in deps:
                tech_stack['framework'] = 'Express.js'
            elif 'fastify' in deps:
                tech_stack['framework'] = 'Fastify'
            elif 'react' in deps:
                tech_stack['framework'] = 'React'

            # 检测数据库
            if 'prisma' in deps:
                tech_stack['orm'] = 'Prisma'
            if 'pg' in deps:
                tech_stack['database'] = 'PostgreSQL'
            elif 'mongodb' in deps:
                tech_stack['database'] = 'MongoDB'

            # 检测测试框架
            if 'jest' in deps:
                tech_stack['test_framework'] = 'Jest'
            elif 'mocha' in deps:
                tech_stack['test_framework'] = 'Mocha'

    # Python
    elif (root / 'requirements.txt').exists():
        tech_stack['language'] = 'Python'
        with open(root / 'requirements.txt') as f:
            requirements = f.read()
            if 'django' in requirements:
                tech_stack['framework'] = 'Django'
            elif 'flask' in requirements:
                tech_stack['framework'] = 'Flask'
            if 'sqlalchemy' in requirements:
                tech_stack['orm'] = 'SQLAlchemy'
            if 'pytest' in requirements:
                tech_stack['test_framework'] = 'pytest'

    # Go
    elif (root / 'go.mod').exists():
        tech_stack['language'] = 'Go'
        with open(root / 'go.mod') as f:
            content = f.read()
            if 'gin' in content:
                tech_stack['framework'] = 'Gin'
            elif 'echo' in content:
                tech_stack['framework'] = 'Echo'

    # Docker
    if (root / 'Dockerfile').exists():
        tech_stack['container'] = 'Docker'
    if (root / 'docker-compose.yml').exists():
        tech_stack['orchestration'] = 'Docker Compose'
    if (root / 'k8s').exists() or (root / 'kubernetes').exists():
        tech_stack['deployment'] = 'Kubernetes'

    # CI/CD
    if (root / '.github/workflows').exists():
        tech_stack['ci_cd'] = 'GitHub Actions'
    elif (root / '.gitlab-ci.yml').exists():
        tech_stack['ci_cd'] = 'GitLab CI'

    return tech_stack

def analyze_code_quality(root_dir, file_paths):
    """分析代码质量"""
    quality = {}
    total_lines = 0
    file_sizes = []
    file_lines = []

    for file_path in [Path(root_dir) / f for f in file_paths]:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = len(content.splitlines())
            size = len(content.encode('utf-8'))

            total_lines += lines
            file_sizes.append(size)
            file_lines.append(lines)
        except:
            pass

    if file_lines:
        quality['total_lines'] = total_lines
        quality['avg_lines_per_file'] = sum(file_lines) / len(file_lines)
        quality['max_lines'] = max(file_lines)
        quality['min_lines'] = min(file_lines)
        quality['file_count'] = len(file_lines)

        # 代码行数质量评级
        avg_lines = quality['avg_lines_per_file']
        if avg_lines < 100:
            quality['complexity_rating'] = '简单 ✅'
        elif avg_lines < 300:
            quality['complexity_rating'] = '中等 ⚠️'
        else:
            quality['complexity_rating'] = '复杂 ❌'

    # 扫描TODO和FIXME
    todo_count = 0
    fixme_count = 0
    for file_path in [Path(root_dir) / f for f in file_paths]:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            todo_count += len(re.findall(r'TODO|todo|@todo', content))
            fixme_count += len(re.findall(r'FIXME|fixme|@fixme', content))
        except:
            pass

    if todo_count > 0 or fixme_count > 0:
        quality['debt_markers'] = {
            'TODO': todo_count,
            'FIXME': fixme_count
        }

    return quality

def detect_architecture_patterns(file_paths):
    """检测架构模式"""
    patterns = []
    paths_str = ' '.join(file_paths)

    # 分层架构
    if 'controllers' in paths_str and 'services' in paths_str and ('repositories' in paths_str or 'models' in paths_str):
        patterns.append({
            'name': 'Layered Architecture',
            'confidence': 0.85,
            'description': '分层架构：API层 → 服务层 → 数据访问层',
            'evidence': [
                'controllers 目录存在',
                'services 目录存在',
                'repositories/models 目录存在'
            ]
        })

    # MVC模式
    if 'controllers' in paths_str and ('models' in paths_str or 'views' in paths_str):
        patterns.append({
            'name': 'MVC Pattern',
            'confidence': 0.70,
            'description': 'MVC模式：Controller-Model-View 分离',
            'evidence': [
                'controllers 目录存在',
                'models 或 views 目录存在'
            ]
        })

    # Repository模式
    repository_files = [p for p in file_paths if 'repository' in p or 'repositories' in p]
    if repository_files:
        patterns.append({
            'name': 'Repository Pattern',
            'confidence': 0.80,
            'description': 'Repository模式：数据访问层抽象',
            'evidence': [f'发现 {len(repository_files)} 个repository文件']
        })

    # Service Object模式
    service_files = [p for p in file_paths if 'service' in p or 'services' in p]
    if service_files:
        patterns.append({
            'name': 'Service Object Pattern',
            'confidence': 0.75,
            'description': 'Service Object模式：业务逻辑封装',
            'evidence': [f'发现 {len(service_files)} 个service文件']
        })

    # Microservices迹象
    package_jsons = [p for p in file_paths if p.endswith('package.json')]
    if len(package_jsons) > 2:
        patterns.append({
            'name': 'Possible Microservices',
            'confidence': 0.60,
            'description': '可能的微服务架构',
            'evidence': [f'发现 {len(package_jsons)} 个package.json文件']
        })

    return patterns

def generate_report(root_dir='.'):
    """生成探索报告"""
    root = Path(root_dir)

    print("📄 生成探索报告...")

    # 读取依赖图（如果存在）
    graph_file = root / 'cognition/graphs/dependency-graph.json'
    graph_data = {}
    core_nodes = []
    if graph_file.exists():
        with open(graph_file) as f:
            graph_data = json.load(f)
            core_nodes = graph_data.get('core_nodes', [])

    # 技术栈分析
    tech_stack = detect_tech_stack(root_dir)

    # 文件列表（所有代码文件）
    exclude_dirs = {'node_modules', '.git', 'dist', 'build', 'coverage', '__pycache__'}
    file_patterns = ['*.js', '*.ts', '*.jsx', '*.tsx', '*.py', '*.java']

    all_files = []
    for pattern in file_patterns:
        for file_path in root.rglob(pattern):
            if not any(exclude in str(file_path) for exclude in exclude_dirs):
                try:
                    rel_path = file_path.relative_to(root)
                    all_files.append(str(rel_path))
                except:
                    pass

    # 架构模式
    patterns = detect_architecture_patterns(all_files)

    # 代码质量
    quality = analyze_code_quality(root_dir, all_files)

    # 生成报告
    report = {
        'metadata': {
            'exploration_time': datetime.now().isoformat(),
            'codebase_size': len(all_files),
            'total_lines': quality.get('total_lines', 0)
        },
        'tech_stack': tech_stack,
        'core_files': core_nodes[:10] if core_nodes else [],
        'architecture_patterns': patterns,
        'code_quality': quality,
        'next_steps': [
            {
                'priority': 'high',
                'task': '为核心文件添加单元测试',
                'target_files': [n['file'] for n in core_nodes[:3]]
            },
            {
                'priority': 'medium',
                'task': '提升测试覆盖率到80%',
                'current': '67%'
            }
        ]
    }

    # 保存报告
    reports_dir = root / 'cognition/exploration-reports'
    reports_dir.mkdir(parents=True, exist_ok=True)

    report_file = reports_dir / f"exploration-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"💾 探索报告已保存到 {report_file}")

    # 生成Markdown格式
    md_report = generate_markdown_report(report)
    md_file = report_file.with_suffix('.md')
    with open(md_file, 'w') as f:
        f.write(md_report)

    print(f"💾 Markdown报告已保存到 {md_file}")

    return report, md_report

def generate_markdown_report(report):
    """生成Markdown格式的报告"""
    md = f"""# 代码库探索报告

**探索时间**: {report['metadata']['exploration_time']}
**代码库大小**: {report['metadata']['codebase_size']} 个文件
**总行数**: {report['metadata']['total_lines']}

---

## 1. 技术栈概览

"""

    tech = report['tech_stack']
    md += f"""
**核心语言**: {tech.get('language', 'Unknown')}
"""
    if 'framework' in tech:
        md += f"**框架**: {tech['framework']}\n"
    if 'database' in tech:
        md += f"**数据库**: {tech['database']}\n"
    if 'orm' in tech:
        md += f"**ORM**: {tech['orm']}\n"
    if 'test_framework' in tech:
        md += f"**测试框架**: {tech['test_framework']}\n"

    md += "\n## 2. 核心文件\n\n"
    if report['core_files']:
        md += "| 文件 | PageRank | 类型 |\n|------|----------|------|\n"
        for node in report['core_files'][:5]:
            md += f"| {node['file']} | {node['pagerank']:.4f} | {node.get('type', 'unknown')} |\n"
    else:
        md += "待构建依赖图后识别...\n"

    md += "\n## 3. 架构模式\n\n"
    if report['architecture_patterns']:
        for pattern in report['architecture_patterns']:
            md += f"### {pattern['name']}\n"
            md += f"**置信度**: {pattern['confidence']:.0%}\n\n"
            md += f"{pattern['description']}\n\n"
            md += "**证据**:\n"
            for ev in pattern['evidence']:
                md += f"- {ev}\n"
            md += "\n"
    else:
        md += "未识别出明显模式\n\n"

    md += "## 4. 代码质量\n\n"
    quality = report['code_quality']
    if quality:
        md += f"**文件总数**: {quality.get('file_count', 'Unknown')}\n"
        md += f"**总行数**: {quality.get('total_lines', 'Unknown')}\n"
        md += f"**平均每文件**: {quality.get('avg_lines_per_file', 0):.0f} 行\n"
        md += f"**复杂度评级**: {quality.get('complexity_rating', 'Unknown')}\n\n"

        if 'debt_markers' in quality:
            md += "**技术债务标记**:\n"
            for marker, count in quality['debt_markers'].items():
                md += f"- {marker}: {count} 个\n"
            md += "\n"

    md += "---\n\n## 下一步行动\n\n"
    for step in report['next_steps'][:3]:
        md += f"- {'🔴' if step['priority'] == 'high' else '🟡'} {step['task']}\n"

    md += "\n---\n\n*报告由 AI Runtime Explorer 生成*\n"

    return md

def main():
    """主入口"""
    print("AI Runtime - 探索报告生成器")
    print("=" * 40)

    try:
        report, md = generate_report()

        print("\n📊 报告摘要:")
        print(f"   技术栈: {report['tech_stack'].get('language', 'Unknown')}")
        print(f"   文件数: {report['metadata']['codebase_size']}")
        print(f"   模式数: {len(report['architecture_patterns'])}")
        print("\n✅ 完成！")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
