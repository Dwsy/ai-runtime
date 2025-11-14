# Issue: 升级记忆系统为时间分层 + SQL 风格 CLI 检索

**日期**: 2025-11-14

## 背景

当前记忆系统：
- `short-term/consciousness.md` 表示当前意识状态（单文件）。
- `long-term/project-context.md` 表示项目架构长期记忆（单文件）。
- `episodic/timeline.md` 将所有历史事件集中在一个时间线文件中，不利于按时间/标签做精细检索和增量写入。

目标：
- 为 `episodic` 记忆引入 **大时间段目录 + 事件文件** 的结构（`YYYY/MM/DD/` + `YYYYMMDD-HHMM-slug.md`）。
- 基于 `episodic/index.yml` 维护事件索引（时间/级别/标签等元信息）。
- 提供一个参考 `.ai-runtime/toolkit/discover` 风格的 **CLI 工具**，但参数语义尽量对齐 SQL（`SELECT/WHERE/ORDER BY/LIMIT`）。

## 范围

本 Issue 仅实现：
- 记忆发现与查询库：`.ai-runtime/memory/memory_discovery.py`
- CLI 入口：`.ai-runtime/memory/memory_cli.py`
- 基于 `index.yml` 的只读查询（不负责构建 index）
- 规划好迁移脚本接口，但迁移本身可以在后续 Issue 中完成

## 目录与规范（摘要）

- 事件文件：
  - 根目录：`.ai-runtime/memory/episodic/`
  - 目录分层：`YYYY/MM/DD/`
  - 文件命名：`YYYYMMDD-HHMM-<slug>.md`
- 索引文件：
  - `.ai-runtime/memory/episodic/index.yml`
  - 记录字段：`id, type, level, timestamp, date_bucket, path, title, tags, related`

## SQL 风格查询参数

CLI 设计对齐以下 SQL 语义：

```sql
SELECT <columns>
FROM episodic_events
WHERE <conditions>
ORDER BY <fields>
LIMIT <n> OFFSET <m>;
``

对应 CLI 参数：
- `--select "id,timestamp,title"`
- `--where "level='day' AND date>='2025-11-14' AND tags CONTAINS 'architecture'"`
- `--order-by "timestamp desc"`
- `--limit 20 --offset 0`

## 任务拆解

### Task 1: 记忆查询库 (memory_discovery)

- 定义 `MemoryEvent` 数据模型：
  - 字段：`id, type, level, timestamp, date_bucket, path, title, tags, related`
  - 提供 `date` 只读属性（`YYYY-MM-DD`）。
- 从 `episodic/index.yml` 加载事件列表：
  - 不存在 index.yml 时，返回空列表，保持容错。
- 提供 SQL 风格的查询接口：
  - `query(where: str | None, order_by: str | None, limit: int | None, offset: int) -> List[MemoryEvent]`
  - 支持 Where 条件子集：
    - `field = 'value'` / `!=` / `>=` / `<=`
    - `tags CONTAINS 'tag'`
    - `AND` 连接（不支持 OR/括号，故意保持简单）。
  - `field` 支持：`id, type, level, date, timestamp, title`，以及 `tags` 的 `CONTAINS`。
- 输出格式：
  - `format_events(events, select_fields, format_type='table|json') -> str`
  - `table` 模式下对齐列宽，适合终端阅读。
  - `json` 模式下返回结构化 JSON，便于其他工具再利用。

### Task 2: CLI 入口 (memory_cli)

- 使用 `argparse` 提供 `query` 子命令：
  - `python3 .ai-runtime/memory/memory_cli.py query [OPTIONS]`
- 参数映射：
  - `--select`：逗号分隔字段列表，映射到 `SELECT`。
  - `--where`：SQL 风格过滤表达式，传给 discovery 的 `where`。
  - `--order-by`：如 `"timestamp desc"`，解析为排序字段+方向。
  - `--limit, --offset`：分页控制。
  - `--format table|json`：输出格式选择。
- CLI 结构参考 `ToolkitCLI`：
  - 有独立的 `MemoryCLI` 类，封装 parser 和命令分发。
  - 主入口 `main()` 将 `.ai-runtime/memory` 作为 `memory_root` 传入 `MemoryDiscovery`。

### Task 3: 迁移脚本（后续 Issue 可拆出）

- 脚本位置建议：`.ai-runtime/scripts/migrate_episodic_timeline.py`
- 功能：
  - 解析 `episodic/timeline.md`，按事件拆分为日级事件文件。
  - 构建/更新 `episodic/index.yml`。
- 本 Issue 中只需要为脚本预留接口约定，不强制实现。

## 验收标准

- 在没有 `index.yml` 的情况下运行：
  - `python3 .ai-runtime/memory/memory_cli.py query` 不报错，优雅提示“当前无索引/无事件”。
- 有简单示例 `index.yml` 时：
  - 能通过 `--where/--order-by/--limit` 正确筛选和排序。
- `docs/issues` 下本文件作为后续 PR 描述和回顾的依据。
