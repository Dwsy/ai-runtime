# AI Runtime 记忆系统

## 概述

AI Runtime的记忆系统采用分层架构，模拟人类大脑的记忆机制，实现持续存在和认知主体性。系统分为三个层次，通过专门的工具支持SQL风格查询和智能管理。

## 架构层次

```
短期记忆（工作记忆） ← 当前会话上下文
    ↓ 固化
长期记忆（语义记忆） ← 跨项目技术知识
    ↓ 时间戳
情景记忆（体验记忆） ← 项目历史事件
```

### 设计原则

- **短期记忆**: 7±2组块限制，实时衰减，支撑当前任务
- **长期记忆**: 结构化知识图谱，跨项目复用
- **情景记忆**: 时间线序列，可追溯性，支持复杂查询

## 文件夹结构

### episodic/ - 情景记忆
存储项目历史事件、关键决策、错误教训和会议纪要。

**文件格式**:
- 使用YAML front matter + Markdown正文
- 支持时间推断（文件名/YAML/front matter）
- 自动生成时间线索引

**示例文件结构**:
```
---
id: event-001
type: decision
level: day
timestamp: "2025-11-14T10:30:00"
tags: [architecture, decision]
---

# 事件标题

## 时间
2025-11-14 10:30:00

## 标签
architecture, decision

## 内容
详细的事件描述...
```

### long-term/ - 长期记忆
存储跨项目的技术知识、设计模式、代码质量经验。

**内容类型**:
- 项目架构记忆
- 技术栈知识
- 设计模式经验
- 用户偏好记录

### short-term/ - 短期记忆
存储当前会话上下文、工作状态和临时假设。

**管理方式**:
- 自动清理过期内容
- 实时更新工作状态
- 支持快速检索

## 工具使用指南

### memory_cli.py - 情景记忆查询工具

提供SQL风格的命令行接口查询episodic记忆。

#### 基本用法

```bash
# 进入记忆系统目录
cd .ai-runtime/memory

# 查询所有事件
python3 memory_cli.py query

# 按日期过滤
python3 memory_cli.py query --where "date>='2025-11-14'"

# 按标签过滤
python3 memory_cli.py query --where "tags CONTAINS 'architecture'"

# 组合条件查询
python3 memory_cli.py query \
    --where "date>='2025-11-14' AND tags CONTAINS 'decision'" \
    --order-by "timestamp desc" \
    --limit 10

# JSON格式输出
python3 memory_cli.py query --format json --limit 5
```

#### 查询语法

**支持的WHERE条件**:
- `field = 'value'` - 精确匹配
- `field != 'value'` - 不等于
- `field >= 'value'` - 大于等于
- `field <= 'value'` - 小于等于
- `tags CONTAINS 'tag'` - 标签包含

**支持的字段**:
- `id` - 事件ID
- `type` - 事件类型
- `level` - 时间级别 (year/month/day/event)
- `title` - 事件标题
- `date` - 日期 (YYYY-MM-DD)
- `timestamp` - 完整时间戳

**排序语法**:
- `field asc` - 升序
- `field desc` - 降序

### memory_discovery.py - 记忆发现引擎

核心记忆解析和查询引擎，提供编程接口。

#### 主要功能

```python
from memory_discovery import MemoryDiscovery

# 初始化发现器
discovery = MemoryDiscovery("path/to/memory/root")

# 刷新索引
discovery.refresh()

# SQL风格查询
events = discovery.query(
    where="date>='2025-11-14' AND tags CONTAINS 'architecture'",
    order_by="timestamp desc",
    limit=20
)

# 格式化输出
output = discovery.format_events(events, select=["id", "title", "date"])
print(output)
```

#### 事件解析协议

**时间推断顺序**:
1. YAML front matter `timestamp`/`time`
2. 正文 `## 时间` 段落第一行
3. 文件名模式 `YYYYMMDD-HHMM.md`
4. 文件名模式 `YYYYMMDD.md`
5. 文件修改时间 (mtime)

**标签解析顺序**:
1. YAML front matter `tags`
2. 正文 `## 标签` 段落（逗号分隔）

**标题解析顺序**:
1. YAML front matter `title`
2. 正文第一个 `# ` 标题
3. 文件名（去除扩展名）

## 维护指南

### 添加新事件

1. 创建Markdown文件到对应目录结构：
   ```
   episodic/2025/11/14/event-description.md
   ```

2. 添加YAML front matter：
   ```yaml
   ---
   id: unique-event-id
   type: event|decision|error|meeting
   level: day
   timestamp: "2025-11-14T10:30:00"
   tags: [tag1, tag2]
   ---
   ```

3. 编写事件内容，包含时间、标签、详细描述

### 记忆固化流程

**短期 → 长期**:
1. 识别有价值的模式或知识
2. 整理成结构化文档
3. 移动到 `long-term/` 目录
4. 更新索引

**工作记忆 → 情景记忆**:
1. 关键事件自动记录
2. 手动调用 `/runtime.remember` 命令
3. 添加时间戳和上下文

### 清理和归档

**自动清理**:
- 短期记忆定期清理（7天）
- 过期工作状态删除

**手动归档**:
- 重要事件移动到归档目录
- 合并相似记忆条目
- 更新索引文件

## 查询示例

### 查找架构决策
```bash
python3 memory_cli.py query \
    --where "type='decision' AND tags CONTAINS 'architecture'" \
    --order-by "timestamp desc"
```

### 查看今天的事件
```bash
python3 memory_cli.py query \
    --where "date='2025-11-14'" \
    --select "timestamp,title,tags"
```

### 搜索特定关键词
```bash
python3 memory_cli.py query \
    --where "title LIKE '%OAuth%'" \
    --format table
```

## 故障排除

### 常见问题

**事件不显示**: 检查时间戳格式和文件路径结构
**查询无结果**: 验证WHERE条件语法和字段名称
**性能问题**: 使用LIMIT限制结果数量，优化WHERE条件

### 调试工具

```bash
# 查看解析后的所有事件
python3 -c "
from memory_discovery import MemoryDiscovery
d = MemoryDiscovery('.')
for e in d.events:
    print(f'{e.id}: {e.title} ({e.date})')
"
```

---

## 相关链接

- [宪法文档](../constitution.md)
- [命令系统](../commands/)
- [工具装备系统](../toolkit/)
- [认知记录](../cognition/)
