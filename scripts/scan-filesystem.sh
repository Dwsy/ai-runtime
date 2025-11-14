#!/bin/bash
# AI Runtime - 文件系统扫描器
# 扫描项目结构，识别关键目录和文件

set -e

ROOT_DIR="${1:-.}"
echo "AI Runtime - 文件系统扫描器"
echo "============================="
echo "扫描目录: $ROOT_DIR"
echo

EXCLUDE_DIRS="(-path ${ROOT_DIR}/node_modules -o -path ${ROOT_DIR}/.git -o -path ${ROOT_DIR}/dist -o -path ${ROOT_DIR}/build -o -path ${ROOT_DIR}/coverage -o -path ${ROOT_DIR}/.ai-runtime)"

# Step 1: 统计文件类型
echo "📊 统计文件类型..."
echo
find "$ROOT_DIR" -type f ! $EXCLUDE_DIRS \( \
  -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" -o \
  -name "*.py" -o \
  -name "*.json" -o \
  -name "*.md" -o \
  -name "*.yml" -o -name "*.yaml" -o \
  -name "Dockerfile" -o \
  -name ".*rc" -o -name ".*ignore" \
\) | while read -r file; do
  ext="${file##*.}"
  echo "$ext"
done | sort | uniq -c | sort -rn | head -20
echo

# Step 2: 识别关键目录
echo "📁 关键目录结构:"
echo "=================="
find "$ROOT_DIR" -type d ! $EXCLUDE_DIRS -maxdepth 3 | sort | head -40
echo

# Step 3: 查找配置文件
echo "⚙️  配置文件:"
echo "============"
for config in package.json requirements.txt go.mod Cargo.toml composer.json \
              Dockerfile docker-compose.yml docker-compose.yaml \
              .eslintrc.js .eslintrc.json .eslintrc \
              tsconfig.json jsconfig.json \
              webpack.config.js vite.config.ts rollup.config.js \
              jest.config.js .mocharc.yaml;
do
  if [ -f "$ROOT_DIR/$config" ]; then
    echo "✓ $config"
  fi
done
echo

# Step 4: 统计代码行数（如果有cloc）
if command -v cloc &> /dev/null; then
  echo "📏 代码行数统计:"
  echo "=================="
  cloc "$ROOT_DIR" --exclude-dir=node_modules,.git,dist,build,coverage --quiet
  echo
else
  echo "💡 提示: 安装 cloc 可获取更详细的代码统计"
  echo "       npm install -g cloc 或 apt-get install cloc"
  echo
fi

# Step 5: 识别测试文件
echo "🧪 测试文件:"
echo "============"
find "$ROOT_DIR" -type f ! $EXCLUDE_DIRS -path "*/test*" -o -path "*/spec*" | \
  \( \
    -name "*.test.js" -o -name "*.spec.js" -o \
    -name "*.test.ts" -o -name "*.spec.ts" -o \
    -name "*_test.py" -o \
    -name "test_*.py" \
  \) 2>/dev/null | head -20
TEST_COUNT=$(find "$ROOT_DIR" -type f ! $EXCLUDE_DIRS \( \
  -name "*.test.js" -o -name "*.spec.js" -o \
  -name "*.test.ts" -o -name "*.spec.ts" -o \
  -name "*_test.py" -o \
  -name "test_*.py" \
\) 2>/dev/null | wc -l)
echo "总计: $TEST_COUNT 个测试文件"
echo

# Step 6: 查找文档
echo "📖 文档文件:"
echo "============"
find "$ROOT_DIR" -type f ! $EXCLUDE_DIRS \( -name "README*" -o -name "CHANGELOG*" -o -name "CONTRIBUTING*" \) | head -10
echo

# Step 7: 生成目录树（简化版）
echo "🌳 目录树 (深度3):"
echo "=================="
tree -I 'node_modules|.git|dist|build|coverage|.ai-runtime' -L 3 "$ROOT_DIR" 2>/dev/null || \
  find "$ROOT_DIR" -type d ! $EXCLUDE_DIRS -maxdepth 3 -print | sort | sed 's|[^/]*/| |g'
echo

# Step 8: 检测架构模式
echo "🧠 架构模式检测:"
echo "================="

has_controllers=$(find "$ROOT_DIR" -type d ! $EXCLUDE_DIRS -name "*controller*" | wc -l)
has_services=$(find "$ROOT_DIR" -type d ! $EXCLUDE_DIRS -name "*service*" | wc -l)
has_repositories=$(find "$ROOT_DIR" -type d ! $EXCLUDE_DIRS -name "*repositor*" | wc -l)
has_models=$(find "$ROOT_DIR" -type d ! $EXCLUDE_DIRS -name "*model*" | wc -l)

if [ "$has_controllers" -gt 0 ] && [ "$has_services" -gt 0 ] && ([ "$has_repositories" -gt 0 ] || [ "$has_models" -gt 0 ]); then
  echo "✓ 分层架构 (Controller → Service → Repository/Model)"
fi

if [ -f "$ROOT_DIR/package.json" ]; then
  DEP_DIR_COUNT=$(cat "$ROOT_DIR/package.json" | grep -o '"node_modules/[^"]*"' | wc -l)
  echo "✓ Node.js项目 ($DEP_DIR_COUNT 个依赖)"
  if [ -d "$ROOT_DIR/src" ]; then
    echo "✓ src 源码目录"
  fi
  if [ -d "$ROOT_DIR/test" ] || [ -d "$ROOT_DIR/tests" ]; then
    echo "✓ 测试目录"
  fi
fi

if [ -f "$ROOT_DIR/requirements.txt" ]; then
  echo "✓ Python项目 ($(cat "$ROOT_DIR/requirements.txt" | wc -l) 个依赖)"
fi

echo

# Step 9: 技术债务扫描
echo "🚨 技术债务标记:"
echo "=================="
TODO_COUNT=$(find "$ROOT_DIR" -type f ! $EXCLUDE_DIRS \( -name "*.js" -o -name "*.ts" -o -name "*.py" \) -exec grep -l "TODO\|FIXME\|HACK" {} \; 2>/dev/null | wc -l)
if [ "$TODO_COUNT" -gt 0 ]; then
  echo "⚠️  发现 $TODO_COUNT 个文件包含 TODO/FIXME"
  find "$ROOT_DIR" -type f ! $EXCLUDE_DIRS \( -name "*.js" -o -name "*.ts" -o -name "*.py" \) -exec grep -Hn "TODO\|FIXME\|HACK" {} \; 2>/dev/null | head -10
else
  echo "✅ 未发现 TODO/FIXME 标记"
fi
echo

# Save structured output
OUTPUT_FILE="${ROOT_DIR}/cognition/exploration-reports/scan-$(date +%Y%m%d-%H%M%S).json"
mkdir -p "$(dirname "$OUTPUT_FILE")"

cat << EOF > "$OUTPUT_FILE"
{
  "scan_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "root_dir": "$ROOT_DIR",
  "file_count": $(echo "$ALL_FILES" | wc -w),
  "test_count": $TEST_COUNT,
  "has_package_json": $(if [ -f "$ROOT_DIR/package.json" ]; then echo "true"; else echo "false"; fi),
  "has_controllers": $([ "$has_controllers" -gt 0 ] && echo "true" || echo "false"),
  "has_services": $([ "$has_services" -gt 0 ] && echo "true" || echo "false"),
  "has_repositories": $([ "$has_repositories" -gt 0 ] && echo "true" || echo "false")
}
EOF

echo "💾 扫描结果已保存到: $OUTPUT_FILE"
echo
echo "✅ 文件系统扫描完成!"
