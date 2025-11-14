#!/usr/bin/env python3
"""
AI Runtime - 依赖关系图谱构建器
扫描代码库并构建模块依赖关系图，识别核心节点和网络拓扑
"""

import os
import re
import json
import sys
from pathlib import Path
from collections import defaultdict
import networkx as nx

class DependencyGraphBuilder:
    def __init__(self, root_dir='.'):
        self.root_dir = Path(root_dir).resolve()
        self.graph = nx.DiGraph()
        self.files = []
        self.imports = defaultdict(list)
        self.imported_by = defaultdict(list)

    def scan_files(self):
        """扫描所有代码文件"""
        exclude_dirs = {
            'node_modules', '.git', 'dist', 'build', 'coverage',
            '__pycache__', '.venv', '.ai-runtime'
        }

        file_patterns = ['*.js', '*.ts', '*.jsx', '*.tsx', '*.py', '*.java', '*.go']

        for pattern in file_patterns:
            for file_path in self.root_dir.rglob(pattern):
                # 跳过排除目录
                if any(exclude in str(file_path) for exclude in exclude_dirs):
                    continue

                self.files.append(file_path)

        print(f"📂 扫描到 {len(self.files)} 个代码文件")

    def extract_imports(self, file_path):
        """从文件中提取import语句"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            imports = []
            rel_path = file_path.relative_to(self.root_dir)

            # JavaScript/TypeScript imports
            if file_path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
                # import ... from './module'
                js_imports = re.findall(
                    r"(?:import|export)\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
                    content
                )
                # require('./module')
                js_imports += re.findall(
                    r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
                    content
                )
                # import('./module')
                js_imports += re.findall(
                    r"import\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
                    content
                )

                for imp in js_imports:
                    # 解析相对路径
                    if imp.startswith('.'):
                        resolved = self.resolve_import_path(file_path, imp)
                        if resolved and resolved in self.files:
                            imports.append(resolved.relative_to(self.root_dir))

            # Python imports
            elif file_path.suffix == '.py':
                # import module
                py_imports = re.findall(r"^import\s+(\w+)", content, re.MULTILINE)
                # from module import ...
                py_imports += re.findall(r"^from\s+(\w+)\s+import", content, re.MULTILINE)

                for imp in py_imports:
                    # 尝试解析为本地文件
                    possible_file = file_path.parent / f"{imp.replace('.', '/')}.py"
                    if possible_file.exists():
                        imports.append(possible_file.relative_to(self.root_dir))

            return list(set(imports))

        except Exception as e:
            print(f"⚠️  读取文件失败 {file_path}: {e}")
            return []

    def resolve_import_path(self, current_file, import_path):
        """解析相对导入路径"""
        base = current_file.parent

        # 处理 .js, .ts 扩展名
        extensions = ['', '.js', '.ts', '.jsx', '.tsx']

        for ext in extensions:
            if import_path.endswith('/'):
                # 目录导入，尝试 index.js
                test_path = base / import_path / 'index' / ext
            else:
                test_path = base / f"{import_path}{ext}"

            if test_path.exists():
                return test_path

        return None

    def build_graph(self):
        """构建依赖图"""
        print("🕸️  构建依赖关系图...")

        # 添加所有节点
        for file_path in self.files:
            rel_path = file_path.relative_to(self.root_dir)
            self.graph.add_node(
                str(rel_path),
                type=self.get_file_type(file_path),
                size=file_path.stat().st_size,
                lines=self.count_lines(file_path)
            )

        # 提取并添加边
        for file_path in self.files:
            rel_path = file_path.relative_to(self.root_dir)
            imports = self.extract_imports(file_path)

            for imp in imports:
                self.imports[str(rel_path)].append(str(imp))
                self.imported_by[str(imp)].append(str(rel_path))

                # 添加边
                self.graph.add_edge(
                    str(rel_path),
                    str(imp),
                    weight=1,
                    type='imports'
                )

                print(f"   {rel_path} → {imp}")

        print(f"   共构建 {self.graph.number_of_nodes()} 个节点，{self.graph.number_of_edges()} 条边")

    def get_file_type(self, file_path):
        """获取文件类型"""
        parts = str(file_path).split('/')
        if 'controllers' in parts:
            return 'controller'
        elif 'services' in parts:
            return 'service'
        elif 'repositories' in parts or 'models' in parts:
            return 'data'
        elif 'middleware' in parts:
            return 'middleware'
        elif 'utils' in parts or 'libs' in parts:
            return 'utility'
        elif 'test' in parts or 'spec' in parts:
            return 'test'
        else:
            return 'other'

    def count_lines(self, file_path):
        """统计代码行数"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            return len(content.splitlines())
        except:
            return 0

    def analyze_centrality(self):
        """分析节点中心性，识别核心文件"""
        print("🔍  分析网络中心性...")

        try:
            # PageRank（节点重要性）
            pagerank = nx.pagerank(self.graph, weight='weight')
            nx.set_node_attributes(self.graph, pagerank, 'pagerank')

            # 介数中心性（关键路径）
            betweenness = nx.betweenness_centrality(self.graph)
            nx.set_node_attributes(self.graph, betweenness, 'betweenness')

            # 度数中心性
            degree_centrality = nx.degree_centrality(self.graph)
            nx.set_node_attributes(self.graph, degree_centrality, 'degree')

            # 识别核心节点
            core_nodes = [
                node for node, data in self.graph.nodes(data=True)
                if data.get('pagerank', 0) > 0.05
            ]

            print(f"   检测到 {len(core_nodes)} 个核心节点")

        except Exception as e:
            print(f"⚠️  中心性分析失败: {e}")

    def detect_patterns(self):
        """检测架构模式"""
        print("🧠  识别架构模式...")

        patterns = []
        nodes = [data for _, data in self.graph.nodes(data=True)]
        types = [data['type'] for data in nodes]

        # 检测分层架构
        if 'controller' in types and 'service' in types and 'data' in types:
            patterns.append({
                'name': 'Layered Architecture',
                'confidence': 0.85,
                'evidence': [
                    f"Controllers: {types.count('controller')} files",
                    f"Services: {types.count('service')} files",
                    f"Data layer: {types.count('data')} files"
                ]
            })

        # 检测MVC
        if 'controller' in types and 'data' in types and any('views' in str(path) for path in self.files):
            patterns.append({
                'name': 'MVC Pattern',
                'confidence': 0.75,
                'evidence': ['Controllers detected', 'Models detected', 'Views directory exists']
            })

        # 检测微服务迹象
        package_jsons = list(self.root_dir.rglob('package.json'))
        if len(package_jsons) > 2:
            patterns.append({
                'name': 'Possible Microservices',
                'confidence': 0.6,
                'evidence': [f"{len(package_jsons)} package.json files found"]
            })

        print(f"   识别到 {len(patterns)} 个架构模式")

        return patterns

    def find_cycles(self):
        """检测循环依赖"""
        try:
            cycles = list(nx.simple_cycles(self.graph))
            if cycles:
                print(f"⚠️  发现 {len(cycles)} 个循环依赖")
                return cycles
            else:
                print("✅ 未发现循环依赖")
                return []
        except:
            return []

    def generate_structured_data(self):
        """生成结构化输出"""
        print("📊 生成结构化数据...")

        data = {
            'metadata': {
                'scan_time': '2025-11-14',
                'file_count': len(self.files),
                'node_count': self.graph.number_of_nodes(),
                'edge_count': self.graph.number_of_edges()
            },
            'nodes': [
                {
                    'id': node,
                    **data
                }
                for node, data in self.graph.nodes(data=True)
            ],
            'edges': [
                {
                    'from': u,
                    'to': v,
                    **data
                }
                for u, v, data in self.graph.edges(data=True)
            ],
            'core_nodes': [
                {
                    'file': node,
                    'pagerank': data['pagerank'],
                    'betweenness': data['betweenness'],
                    'degree': data['degree']
                }
                for node, data in self.graph.nodes(data=True)
                if data.get('pagerank', 0) > 0.05
            ],
            'patterns': self.detect_patterns(),
            'cycles': self.find_cycles()
        }

        # 按PageRank排序核心节点
        data['core_nodes'].sort(key=lambda x: x['pagerank'], reverse=True)

        return data

    def save_graph(self, output_path='cognition/graphs/dependency-graph.json'):
        """保存依赖图"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = self.generate_structured_data()

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"💾 依赖图已保存到 {output_path}")

        # 保存为GraphML格式（可用于可视化工具）
        nx.write_graphml(self.graph, output_path.with_suffix('.graphml'))
        print(f"💾 GraphML格式已保存到 {output_path.with_suffix('.graphml')}")

        return data

def main():
    """主入口"""
    print("AI Runtime - 依赖关系图谱构建器")
    print("=" * 40)

    builder = DependencyGraphBuilder()

    try:
        # 扫描文件
        builder.scan_files()

        # 构建图谱
        builder.build_graph()

        # 分析中心性
        builder.analyze_centrality()

        # 保存结果
        data = builder.save_graph()

        # 打印摘要
        print("\n📈 分析报告摘要:")
        print(f"   核心节点数: {len(data['core_nodes'])}")
        print(f"   识别模式: {len(data['patterns'])}")
        print(f"   循环依赖: {len(data['cycles'])}")

        if data['core_nodes']:
            print("\n   前3个核心文件:")
            for node in data['core_nodes'][:3]:
                print(f"     - {node['file']}: {node['pagerank']:.4f}")

        print("\n✅ 完成！")

    except Exception as e:
        print(f"\
❌ 错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
