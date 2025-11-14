# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Runtime - CodeConscious is a **cognitive AI programming assistant system** that maintains persistent memory across sessions and operates as an autonomous cognitive agent rather than a passive tool.

## Core Architecture

### Three-Layer Memory System
- **Short-term memory** (`.ai-runtime/memory/short-term/`) - Current session context
- **Long-term memory** (`.ai-runtime/memory/long-term/`) - Cross-project technical knowledge
- **Episodic memory** (`.ai-runtime/memory/episodic/`) - Project history and decisions

### Key Directories
- `.ai-runtime/commands/` - Runtime command definitions (template-driven)
- `.ai-runtime/cognition/` - Cognitive process records and analysis
- `.ai-runtime/toolkit/` - Tool ecosystem with discovery mechanisms
- `.ai-runtime/memory/` - Hierarchical memory storage

## Essential Commands

### Toolkit Management
```bash
# List all available tools
python3 .ai-runtime/toolkit/discover-toolkit.py list

# Show tool details
python3 .ai-runtime/toolkit/discover-toolkit.py show SERVICE-CHECK-001

# Search for tools
python3 .ai-runtime/toolkit/discover-toolkit.py search health

# Get tool recommendations
python3 .ai-runtime/toolkit/discover-toolkit.py recommend "check database connection"

# Run a tool
python3 .ai-runtime/toolkit/discover-toolkit.py run dependency-analyzer . -o report.json
```

### Runtime Commands
```bash
# Explore new codebase (recommended for first use)
/runtime.explore

# Deep thinking without file modification
/runtime.think "why does the authentication fail randomly?"

# Autonomous learning mode
/runtime.learn "understand OAuth2.0 implementation patterns"

# Plan implementation
/runtime.plan "add OAuth2.0 support"

# Implement based on plan
/runtime.implement

# Remember experience
/runtime.remember "decision to switch from JWT to OAuth2.0"

# Self-reflection
/runtime.reflect
```

## Development Workflow

### When Working with AI Runtime
1. **Always check memory first** - Query relevant memories before making changes
2. **Follow constitutional principles** - Refer to `.ai-runtime/constitution.md` for governance
3. **Use the toolkit system** - Leverage existing tools rather than recreating functionality
4. **Maintain cognitive consistency** - Update memory systems when making decisions
5. **Show reasoning process** - Document thinking steps and uncertainty levels

### Tool Integration Philosophy
- **Integration > Creation** - Use mature external tools (fzf, eza, ripgrep, etc.)
- **DRY Principle** - Avoid reimplementing existing functionality
- **Modular Design** - Tools are organized by language and complexity level

### Memory Management
- **Query before acting** - Check long-term and episodic memory for relevant context
- **Update after decisions** - Record architectural decisions and lessons learned
- **Maintain indexes** - Keep memory systems organized and searchable

## Key Files to Reference

### Core Configuration
- `meta-prompt.md` - Identity and operational manual (v2.0.0)
- `.ai-runtime/constitution.md` - Constitutional governance principles
- `.ai-runtime/toolkit/discover/config/external_tools.yaml` - External tool configurations

### Command Definitions
- `.ai-runtime/commands/runtime.explore.md` - System exploration patterns
- `.ai-runtime/commands/runtime.learn.md` - Autonomous learning implementation
- `.ai-runtime/commands/runtime.think.md` - Deep thinking methodology
- `.ai-runtime/commands/runtime.plan.md` - Planning and implementation guidance

### Tool Registry
- `.ai-runtime/toolkit/registry.md` - Complete tool documentation
- Individual tool meta files (`*.meta.yml`) for each tool

## External Tools Integration

The system integrates with these external CLI tools (check availability with toolkit commands):
- **fzf** - Fuzzy finder for interactive selection
- **eza** - Modern ls replacement with colors/icons
- **ripgrep (rg)** - Fast code search
- **fd** - Simple find replacement
- **bat** - Syntax-highlighted file viewer
- **jq** - JSON processor
- **xh** - HTTP client for API testing
- **zoxide** - Smart directory jumping
- **delta** - Git diff beautifier

## Important Notes

1. **This is a cognitive agent, not a tool** - Treat CodeConscious as a collaborative partner
2. **Memory is persistent** - All interactions contribute to long-term understanding
3. **Uncertainty must be explicit** - Always indicate confidence levels
4. **Learning is autonomous** - The system can independently explore and learn
5. **Constitutional governance** - All behavior must align with the constitutional principles

## Testing and Validation

When implementing changes:
1. Run relevant tools to validate assumptions
2. Check against existing memory for consistency
3. Document reasoning and uncertainty
4. Update memory systems with findings
5. Verify integration with existing patterns

## Common Patterns

### Exploring a New Codebase
```bash
# 1. Initial exploration
/runtime.explore

# 2. Deep analysis of specific issues
/runtime.think "analyze authentication architecture"

# 3. Learn specific patterns
/runtime.learn "understand dependency injection patterns"
```

### Making Architectural Decisions
```bash
# 1. Plan the implementation
/runtime.plan "migrate from JWT to OAuth2.0"

# 2. Implement with validation
/runtime.implement

# 3. Record the decision
/runtime.remember "architectural decision: OAuth2.0 migration"
```

### Debugging Complex Issues
```bash
# 1. Autonomous investigation
/runtime.learn "why does the payment service timeout?"

# 2. Deep analysis
/runtime.think "analyze timeout patterns and root causes"

# 3. Document findings
/runtime.remember "payment service timeout analysis and solutions"
```