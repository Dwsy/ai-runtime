# AI Runtime 版本化文档索引

## 概述

为了更好地管理文档的历史版本，我们建立了versioned-docs目录结构。按照语义化版本控制，每个主要版本都有对应的目录。

## 版本结构

```
.ai-runtime/versioned-docs/
├── v1.0/           # 初始版本（单一大型文档）
├── v2.0/           # 当前版本（渐进式披露架构）
└── README.md       # 版本索引和导航
```

## 版本说明

### v1.0 (2025-11-14)
**状态**: 历史版本，已归档
**架构**: 单一大型Markdown文档
**特点**: 所有信息集中在一个文件中
**文件**:
- `memory-system-complete.md` - 完整记忆系统文档（266行）
- `toolkit-registry-complete.md` - 完整工具装备文档（291行）
- `external-tools-complete.md` - 完整外部工具文档（83行）

### v2.0 (2025-11-14) - 当前版本
**状态**: 活跃版本
**架构**: 渐进式披露多层结构
**特点**: SKILL.md + references/ + scripts/
**优势**:
- 按需加载，避免上下文过载
- 模块化组织，便于维护
- 渐进式信息披露，用户友好

## 版本导航

### 从v1.0迁移到v2.0

| v1.0 文档 | v2.0 对应位置 |
|-----------|----------------|
| memory-system-complete.md | memory/SKILL.md + memory/references/ |
| toolkit-registry-complete.md | toolkit/SKILL.md + toolkit/references/ |
| external-tools-complete.md | toolkit/EXTERNAL-TOOLS-SKILL.md + toolkit/references/ |

### 快速访问当前版本

```bash
# 记忆系统
cat .ai-runtime/memory/SKILL.md                    # 核心概念
ls .ai-runtime/memory/references/                 # 详细文档

# 命令系统
cat .ai-runtime/commands/SKILL.md                 # 核心功能
ls .ai-runtime/commands/references/               # 详细文档

# 工具装备系统
cat .ai-runtime/toolkit/SKILL.md                  # 核心功能
ls .ai-runtime/toolkit/references/                # 详细文档
```

## 版本管理策略

### 何时创建新版本
- 架构发生重大变化（如文档结构重构）
- 功能增加导致文档数量显著变化
- API或接口发生不兼容变更

### 版本命名规则
- **MAJOR**: 架构或设计理念的重大变化（如从v1到v2）
- **MINOR**: 功能增强或文档优化
- **PATCH**: 小的修复或澄清

### 历史版本保留策略
- 保留最近3个主要版本的历史文档
- 超过3个月未访问的版本可考虑归档
- 重要里程碑版本永久保留

## 贡献指南

### 添加新版本
1. 创建新的版本目录: `mkdir v{version}/`
2. 复制当前完整文档: `cp *-complete.md v{version}/`
3. 更新版本索引: 编辑此README.md
4. 提交版本: `git tag v{version}`

### 更新版本说明
在对应版本目录中添加CHANGELOG.md说明变更内容。

---

*版本管理遵循语义化版本控制原则，确保文档演进的可追溯性*
