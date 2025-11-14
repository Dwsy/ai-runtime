#!/bin/bash
# 记忆系统快速查询脚本

MEMORY_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLI_SCRIPT="$MEMORY_ROOT/memory_cli.py"

# 帮助信息
show_help() {
    cat << EOF
记忆系统快速查询工具

用法: $0 [命令] [选项]

命令:
    today           查看今天的事件
    week            查看本周的事件
    recent <天数>   查看最近N天的事件
    search <关键词> 搜索标题包含关键词的事件
    types           统计事件类型分布
    tags            统计标签使用情况
    stats           显示系统统计信息
    help            显示此帮助信息

示例:
    $0 today
    $0 week
    $0 recent 3
    $0 search "认证"
    $0 types
    $0 tags
    $0 stats

EOF
}

# 检查CLI脚本是否存在
check_cli() {
    if [ ! -f "$CLI_SCRIPT" ]; then
        echo "错误: 找不到 memory_cli.py 脚本 ($CLI_SCRIPT)"
        exit 1
    fi
}

# 执行查询
run_query() {
    python3 "$CLI_SCRIPT" query "$@"
}

# 主逻辑
main() {
    check_cli

    case "${1:-help}" in
        "today")
            echo "=== 今天的事件 ==="
            run_query --where "date='$(date +%Y-%m-%d)'" --order-by "timestamp desc"
            ;;
        "week")
            echo "=== 本周的事件 ==="
            run_query --where "date>='$(date -d 'last monday' +%Y-%m-%d)'" --order-by "timestamp desc"
            ;;
        "recent")
            days="${2:-7}"
            echo "=== 最近 $days 天的事件 ==="
            run_query --where "timestamp >= '$(date -d "$days days ago" +%Y-%m-%dT%H:%M:%S)'" --order-by "timestamp desc"
            ;;
        "search")
            keyword="${2:-}"
            if [ -z "$keyword" ]; then
                echo "错误: 请提供搜索关键词"
                exit 1
            fi
            echo "=== 搜索包含 '$keyword' 的事件 ==="
            # 注意: 当前CLI不支持LIKE操作，这里用简单的方式
            run_query --where "title LIKE '%$keyword%'" 2>/dev/null || run_query | grep -i "$keyword"
            ;;
        "types")
            echo "=== 事件类型统计 ==="
            run_query --select "type" --format json 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
types = {}
for item in data:
    t = item.get('type', 'unknown')
    types[t] = types.get(t, 0) + 1
for t, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
    print(f'{t}: {count}')
" || echo "需要安装python3和支持JSON格式的CLI"
            ;;
        "tags")
            echo "=== 标签使用统计 ==="
            run_query --select "tags" --format json 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
tags = {}
for item in data:
    for tag in item.get('tags', []):
        tags[tag] = tags.get(tag, 0) + 1
for tag, count in sorted(tags.items(), key=lambda x: x[1], reverse=True)[:20]:
    print(f'{tag}: {count}')
" || echo "需要安装python3和支持JSON格式的CLI"
            ;;
        "stats")
            echo "=== 记忆系统统计 ==="
            echo "Episodic事件数量: $(find "$MEMORY_ROOT/episodic" -name "*.md" 2>/dev/null | wc -l)"
            echo "Long-term文档数量: $(find "$MEMORY_ROOT/long-term" -name "*.md" 2>/dev/null | wc -l)"
            echo "Short-term文件数量: $(find "$MEMORY_ROOT/short-term" -name "*.md" 2>/dev/null | wc -l)"
            echo "总计: $(find "$MEMORY_ROOT" -name "*.md" 2>/dev/null | wc -l)"
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

main "$@"
