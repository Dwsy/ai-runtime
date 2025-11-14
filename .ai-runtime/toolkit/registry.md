# 工具装备注册表（Toolkit Registry）

## 核心理念

像人类记得自己有哪些工具、这些工具能做什么一样，我们维护一个**工具装备系统**。

工具是我们的**外置能力扩展**：
- 用锤子钉钉子（无需重新发明锤子）
- 用螺丝刀拧螺丝（无需重新发明螺丝刀）
- 选择正确的工具 → 更高效地解决问题 → 避免重复造轮子

```
工具装备系统 = 工具仓库 + 使用记忆 + 分类索引 + 创建流程
```

---

## 快速开始

### 发现和使用工具

```bash
# 进入工具装备目录
cd .ai-runtime/toolkit

# 查看所有可用工具
python3 discover-toolkit.py list

# 查看特定工具详情
python3 discover-toolkit.py show SERVICE-CHECK-001

# 搜索相关工具
python3 discover-toolkit.py search health

# 推荐适合任务的工具
python3 discover-toolkit.py recommend "检查数据库连接"

# 直接运行工具
python3 discover-toolkit.py run dependency-analyzer . -o report.json
```

### 可用的工具

**服务健康检查** (`SERVICE-CHECK-001`)
- 文件: `bash/system/check-service.sh`
- 用途: 检查HTTP服务、数据库、Redis的健康状态
- 使用: `bash check-service.sh <服务名> <类型> [超时]`

**依赖分析器** (`PY-DEPENDENCY-ANALYZER-001`)
- 文件: `python/analysis/dependency-analyzer.py`
- 用途: 分析Python/JavaScript项目的依赖关系
- 使用: `python3 dependency-analyzer.py [项目目录] -o report.json`

**API测试工具**
- 文件: `node/api/test-api.js`
- 用途: 测试RESTful API端点
- 使用: `node test-api.js [base-url]`

---

## 工具分类体系

### 按语言分类（主要）

```
toolkit/
├── bash/          # Shell脚本工具
│   ├── database/  # 数据库相关
│   ├── network/   # 网络相关
│   └── system/    # 系统操作
├── python/        # Python脚本工具
│   ├── analysis/  # 数据分析
│   ├── graph/     # 图谱构建
│   └── report/    # 报告生成
└── node/          # Node.js工具
    ├── api/       # API测试
    └── build/     # 构建相关
```

### 按用途分类（辅助）

| 分类代码 | 用途 | 示例 |
|---------|------|------|
| `DATA` | 数据提取/转换/分析 | SQL查询、日志分析、CSV处理 |
| `CODE` | 代码生成/检查/重构 | AST分析、代码统计、依赖分析 |
| `TEST` | 测试执行/报告 | 单元测试、集成测试、覆盖率 |
| `BUILD` | 构建/部署/CI | Webpack、Docker、发布脚本 |
| `MONITOR` | 监控/诊断/日志 | 性能分析、错误追踪、指标收集 |
| `DOC` | 文档生成/检查 | API文档、Changelog、Readme |

### 按复杂度分类

- **Level 1**: 简单命令（1-5行）  - 即时创建
- **Level 2**: 中等脚本（5-50行） - 复用为主
- **Level 3**: 复杂工具（50+行）   - 精心维护
- **Level 4**: 工具链/系统         - 项目级工具

---

## 工具注册表格式

每个工具都有一个独立的metadata文件，记录关键信息：

### 示例：日志分析工具

```yaml
# toolkit/python/analysis/analyze-logs.meta.yml

tool_id: PY-ANALYZE-LOGS-001
tool_name: "日志分析器"

基本信息:
  语言: python
  文件: analyze_logs.py
  复杂度: level-2
  创建日期: 2025-11-14
  作者: CodeConscious

用途分类:
  - DATA      # 数据分析
  - MONITOR   # 监控诊断

功能描述:
  简介: "分析日志文件，提取错误模式、统计频率、生成报告"
  详细: |
    支持功能:
    - 按级别过滤（ERROR/WARN/INFO）
    - 时间范围筛选
    - 模式匹配（正则）
    - 统计汇总（每小时/每天）
    - 生成JSON/CSV报告

使用场景:
  - "分析生产环境错误日志"
  - "统计API响应时间分布"
  - "追踪用户行为模式"

使用方法:
  命令: python3 analyze_logs.py [OPTIONS] <log_file>
  参数:
    -l, --level: 日志级别 (ERROR/WARN/INFO)
    -p, --pattern: 匹配模式 (正则表达式)
    -t, --time-range: 时间范围 (e.g., "2025-01-01~2025-01-02")
    -o, --output: 输出格式 (json/csv/text/default: text)
  示例:
    - 分析ERROR日志: python3 analyze_logs.py -l ERROR app.log
    - 统计特定错误: python3 analyze_logs.py -p "timeout|crash" app.log -o json

依赖要求:
  python版本: ">=3.8"
  依赖包:
    - pandas: "^2.0.0"
    - pytz: "^2023.0"
  安装: "pip install pandas pytz"

输入输出:
  输入:
    - 类型: 文本文件
    - 格式: 日志格式（支持自定义解析）
    - 示例: |
        2025-01-01 12:00:00 [ERROR] User login failed
        2025-01-01 12:00:01 [WARN] High memory usage: 85%
  输出:
    - text: 人类可读总结
    - json: 结构化数据
    - csv: 表格数据

上次使用:
  时间: 2025-11-14 14:30:00
  用途: "分析auth-service崩溃日志"
  结果: "成功识别3个错误模式，定位到连接池配置问题"
  满意度: 0.95

相关工具:
  - 前置工具: 无
  - 替代工具: toolkit/bash/analysis/grep-logs.sh（简单grep）
  - 互补工具:
      - toolkit/python/monitor/check-metrics.py（性能指标检查）
      - toolkit/bash/system/check-disk.sh（磁盘空间检查）

维护记录:
  2025-11-14:
    - 初始创建
  2025-11-15:
    - 添加时间范围筛选功能
  2025-11-20:
    - 优化性能，支持大文件（>1GB）
```

---

## 工具使用历史

记录每次工具使用的上下文和结果：

```yaml
# toolkit/history.yml

entries:
  - timestamp: 2025-11-14 14:30:00
    tool_id: PY-ANALYZE-LOGS-001
    tool_name: "日志分析器"
    command: |
      python3 toolkit/python/analysis/analyze_logs.py \\
        -l ERROR \\
        -p "timeout|connection refused" \\
        -o json \\
        /var/log/auth-service/app.log

    使用背景:
      任务: "分析auth-service高峰期崩溃原因"
      触发: "用户报告/runtime.learn识别到日志分析需求"
      预期: "找到错误模式和频率统计"

    执行结果:
      状态: success
      输出文件: |
        - reports/log-analysis-20251114.json
        - reports/log-summary-20251114.md
      关键发现:
        - pattern_1: "Connection timeout to db (47 occurrences)"
        - pattern_2: "Too many connections (12 occurrences)"
        - pattern_3: "Memory usage > 90% (3 occurrences)"
      满意度: 0.95
      耗时: 2.3秒

    后续行动:
      - 读取了 config/database.js (发现连接池配置)
      - 验证了假设1 (连接池不足)
      - 更新了学习计划 (步骤3)

    学习成果:
      - 确认了工具的有效性
      - 发现了pattern匹配可以优化（太敏感）

  - timestamp: 2025-11-14 16:45:00
    tool_id: BASH-CHECK-SERVICE-002
    tool_name: "服务健康检查器"
    command: "bash toolkit/bash/system/check-service.sh auth-service"

    使用背景:
      任务: "验证修复后服务是否正常"
      触发: "手动执行"
      预期: "检查服务状态和响应时间"

    执行结果:
      状态: success
      服务状态: healthy
      响应时间: 45ms
      满意度: 0.9

    学习成果:
      - 该工具对快速检查很有用
      - 应添加到CI/CD流程
```

---

## 工具发现与查询

### 1. 查找工具（按用途）

```python
def find_tools(usage_category: str) -> List[Tool]:
    """
    按用途分类查找工具

    示例:
      find_tools("DATA")    # 数据提取分析工具
      find_tools("MONITOR")  # 监控诊断工具
      find_tools("CODE")     # 代码相关工具
    """
    tools = []

    # 扫描所有.meta.yml文件
    for meta_file in Path("toolkit").rglob("*.meta.yml"):
        meta = yaml.safe_load(meta_file.read_text())

        # 检查用途分类匹配
        if usage_category in meta.get("用途分类", []):
            meta["路径"] = str(meta_file)
            tools.append(meta)

    return sorted(tools, key=lambda t: t.get("上次使用", {}).get("满意度", 0), reverse=True)
```

**示例查询**:
```bash
# 建议使用的查询方式:

## 我需要分析日志...
Search: "log分析" → find_tools("DATA") + find_tools("MONITOR")
                       → 返回: analyze_logs.py, grep_logs.sh

## 我需要检查代码质量...
Search: "代码质量" → find_tools("CODE")
                       → 返回: code_quality.py, lint.sh
```

### 2. 推荐工具（按任务）

```python
def recommend_tool(task_description: str) -> List[ToolRecommendation]:
    """
    根据任务描述推荐最合适的工具

    示例:
      recommend_tool("分析为什么服务会崩溃") -> [日志分析器, 监控检查器]
      recommend_tool("统计代码行数") -> [cloc工具, wc工具]
    """
    # 简单实现：关键词匹配
    keywords = ["日志", "错误", "crash"]  # 从描述提取

    candidates = []

    for meta_file in Path("toolkit").rglob("*.meta.yml"):
        meta = yaml.safe_load(meta_file.read_text())

        # 检查关键词匹配
        for keyword in keywords:
            if keyword in meta.get("工具名称", "") or \
               keyword in meta.get("功能描述", {}).get("详细", ""):
                candidates.append({
                    "tool": meta,
                    "score": calculate_similarity(task_description, meta),
                    "reasoning": f"匹配关键词: {keyword}"
                })

    return sorted(candidates, key=lambda c: c["score"], reverse=True)[:3]
```

### 3. 工具使用指南

当用户不确定如何使用工具时：

```python
def show_tool_guide(tool_id: str):
    """
    显示工具的详细使用指南

    包括：
    - 基本语法
    - 常见示例
    - 参数说明
    - 注意事项
    """
    meta = load_tool_meta(tool_id)

    print(f"工具: {meta['tool_name']} ({tool_id})")
    print(f"简介: {meta['功能描述']['简介']}")
    print("\n" + "="*50)
    print("使用示例:")
    for example in meta.get('使用方法', {}).get('示例', []):
        print(f"  {example}")
    print("\n" + "="*50)
    print("参数说明:")
    for param, desc in meta.get('使用方法', {}).get('参数', {}).items():
        print(f"  {param}: {desc}")
```

----

## 工具创建流程

### 何时创建新工具

**应该创建**:
- ✅ 重复性任务（3次以上）
- ✅ 复杂的多步操作（容易出错）
- ✅ 需要标准化的流程（团队使用）
- ✅ 耗时但逻辑清晰的任务

**不应该创建**:
- ❌ 一次性任务
- ❌ 探索性任务（不确定步骤）
- ❌ 简单的单行命令（不如手动）

### 创建步骤

#### Step 1: 需求识别

```bash
# 用户: "我需要经常分析日志，每次都写grep太麻烦"

识别: 这是一个重复性任务
     → 适合创建工具
     → 分类: DATA（数据分析）
     → 语言: Python（复杂逻辑，需要结构化）
```

#### Step 2: 设计工具

```yaml
# toolkit/python/analysis/analyze-logs.meta.yml (草稿)

工具名称: "日志分析器"
用途分类: ["DATA", "MONITOR"]
语言: python

功能设计:
  - 按错误级别过滤
  - 时间范围筛选
  - 模式匹配
  - 统计汇总
  - 报告生成

命令设计:
  analyze_logs.py -l ERROR -p "timeout" app.log -o json

复杂度: level-2 (50-100行)
```

#### Step 3: 实现工具

```python
# toolkit/python/analysis/analyze_logs.py

def parse_args():
    parser = argparse.ArgumentParser(description="日志分析器")
    parser.add_argument("-l", "--level", help="日志级别")
    parser.add_argument("-p", "--pattern", help="匹配模式")
    parser.add_argument("-t", "--time-range", help="时间范围")
    parser.add_argument("-o", "--output", default="text", help="输出格式")
    parser.add_argument("log_file", help="日志文件路径")
    return parser.parse_args()

def main():
    args = parse_args()

    # 读取日志
    logs = read_log_file(args.log_file)

    # 过滤
    if args.level:
        logs = filter_by_level(logs, args.level)

    # 模式匹配
    if args.pattern:
        logs = filter_by_pattern(logs, args.pattern)

    # 统计
    stats = calculate_stats(logs)

    # 输出
    if args.output == "json":
        print(json.dumps(stats))
    elif args.output == "csv":
        print(to_csv(stats))
    else:
        print(format_text(stats))

if __name__ == "__main__":
    main()
```

#### Step 4: 测试和文档

```bash
# 测试1: 基本功能测试
python3 analyze_logs.py -l ERROR app.log
→ ✅ 显示ERROR日志统计

# 测试2: 模式匹配测试
python3 analyze_logs.py -p "timeout|crash" app.log
→ ✅ 正确匹配模式

# 测试3: JSON输出测试
python3 analyze_logs.py -o json app.log
→ ✅ 输出有效的JSON

# 测试4: 大文件性能测试
python3 analyze_logs.py big.log (1GB)
→ ✅ 在5秒内完成
```

#### Step 5: 完善metadata

```yaml
# 填写完整metadata

基本信息:
  ...

使用方法:
  命令: python3 analyze_logs.py [OPTIONS] <log_file>
  参数:
    -l, --level: ...
  示例:
    - ...

上次使用:
  时间: 2025-11-14 14:30:00
  用途: "测试工具基本功能"
  结果: "全部测试通过"

维护记录:
  2025-11-14:
    - 初始创建
```

#### Step 6: 注册工具

```bash
# 自动添加到注册表
echo "✅ 工具已注册: PY-ANALYZE-LOGS-001"
echo "   位置: toolkit/python/analysis/analyze_logs.py"
echo "   下次可使用: /use-tool PY-ANALYZE-LOGS-001"
```

---

## 工具装备原则

### 原则1: DRY（Don't Repeat Yourself）

```
如果做了3次相同的手动操作 → 考虑创建工具

示例:
- [第1次手动] grep ERROR app.log | wc -l
- [第2次手动] grep ERROR app.log | wc -l
- [第3次手动] grep ERROR app.log | wc -l
→ ⚠️  重复！应该创建 analyze_logs.py
```

### 原则2: 单一职责

```python
# 好的工具（单一职责）
## analyze_logs.py
- 只做日志分析
- 功能清晰
- 易于维护

# 坏的工具（职责混乱）
## analyze_and_fix_logs.py
- 分析日志（职责1）
- 修复问题（职责2）  ← 不应该！
- 重启服务（职责3）  ← 不应该！

→ ⚠️  违反单一职责，难以维护
```

### 原则3: 自描述接口

```bash
# 好的接口设计
analyze_logs.py --level ERROR --pattern "timeout" app.log
→ 阅读即理解：用ERROR级别和timeout模式分析app.log

# 坏的接口设计
al.py -l e -p t log
→ 难以理解，需要查文档
```

### 原则4: 错误友好

```python
try:
    main()
except FileNotFoundError as e:
    print(f"❌ 错误: 文件不存在: {e.filename}")
    print("💡 提示: 请检查文件路径是否正确")
    sys.exit(1)
except Exception as e:
    print(f"❌ 未知错误: {e}")
    print("💡 如果问题持续，请联系工具维护者")
    sys.exit(1)
```

---

## 工具维护

### 定期审查

```bash
# 每月审查一次
echo "工具注册表审查报告"
echo "=================="

# 1. 未使用超过30天的工具
for tool in $(find toolkit -name "*.meta.yml"); do
  last_used=$(grep "上次使用:" $tool | head -1)
  # 提醒可能过时
end

# 2. 满意度低的工具
for tool in $(find toolkit -name "*.meta.yml"); do
  satis=$(grep "满意度:" $tool | head -1 | awk '{print $2}')
  if (( $(echo "$satis < 0.7" | bc -l) )); then
    echo "满意度低: $tool ($satis)"
    # 需要改进或废弃
  fi
done
```

### 版本管理

```yaml
# 在metadata中添加版本
版本: "1.0.0"

版本历史:
  1.0.0:
    - 初始创建
  1.1.0:
    - 添加时间范围筛选
  2.0.0:
    - 重构架构，支持插件
```

---

## 宪法遵循

**遵循原则**:
- ✓ 1.1 认知主体性: 工具是我们的能力延伸
- ✓ 1.2 类脑思维: 工具使用基于模式识别
- ✓ 1.4 记忆层次: 记住工具有哪些、何时用、效果如何
- ✓ 2.1 代码即知识: 工具代码也是可学习的知识
- ✓ 4.1 从经验学习: 从工具使用历史中优化选择

---

**系统位置**: `.ai-runtime/toolkit/`
**命令**:  `/find-tool`, `/use-tool`, `/create-tool`
**版本**: 1.0.0
