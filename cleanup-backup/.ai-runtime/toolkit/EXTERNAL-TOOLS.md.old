# 外部工具推荐清单

**最后更新**: 2025-11-14
**版本**: 1.0.0

---

## 概述

本文档列出了强烈推荐安装的外部CLI工具。这些工具**不应重新实现**，而应作为系统的一部分直接使用。

**核心理念**: **整合 > 创造**

---

## 基础必备（所有用户都应安装）

### 1. fzf (Fuzzy Finder) ⭐⭐⭐⭐⭐

**用途**: 命令行模糊查找

**安装**: macOS
```bash
brew install fzf
$(brew --prefix)/opt/fzf/install  # 安装键盘快捷键
```

**安装**: Ubuntu/Debian
```bash
sudo apt-get install fzf
```

**基础使用**:
```bash
# 文件名查找
find . -type f | fzf

# 历史命令
history | fzf

# Git分支
git branch | fzf
```

**进阶配置** (添加到 ~/.bashrc):
```bash
# 使用Ctrl-R搜索历史
export FZF_CTRL_R_OPTS="--preview 'echo {}' --preview-window down:3:wrap"

# 使用Ctrl-T搜索文件
export FZF_CTRL_T_COMMAND="fd --type f --hidden --follow --exclude .git"
export FZF_CTRL_T_OPTS="--preview 'bat -n --color=always {}'"
```

---

### 2. eza (ls替代) ⭐⭐⭐⭐⭐

**用途**: 现代化文件列表

**安装**: macOS
```bash
brew install eza
```

**安装**: Ubuntu/Debian
```bash
sudo apt-get install -y gpg wget
wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/gierens.gpg
echo "deb http://deb.gierens.de stable main" | sudo tee /etc/apt/sources.list.d/gierens.list
sudo apt-get update
sudo apt-get install -y eza
```

**配置** (添加到 ~/.bashrc):
```bash
alias ll='eza -lah'
alias ls='eza'
alias tree='eza --tree --level=2'
```

**使用**:
```bash
# 详细列表
ll

# Git状态
ll --git

# 树形结构
tree
```

---

### 3. zoxide (cd替代) ⭐⭐⭐⭐⭐

**用途**: 智能目录跳转

**安装**: 所有平台
```bash
curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh
```

**配置** (添加到 ~/.bashrc):
```bash
eval "$(zoxide init bash)"
alias cd='z'
alias cdi='zi'
```

**使用**:
```bash
# 第一次需要完整路径
cd ~/projects/ai-runtime

# 之后只需
z ai-runtime

# 查看访问频率
z --list | head

# 交互式选择
zi
```

---

### 4. fd (find替代) ⭐⭐⭐⭐⭐

**用途**: 简单友好的文件查找

**安装**: macOS
```bash
brew install fd
```

**安装**: Ubuntu/Debian
```bash
sudo apt-get install fd-find  # 注意：命令是fdfind
ln -s $(which fdfind) ~/.local/bin/fd
```

**配置** (添加到 ~/.bashrc):
```bash
alias find='fd'
```

**使用**:
```bash
# 查找Python文件
fd .py

# 在当前目录
cd ~/projects
fd .py

# 忽略.gitignore，搜索所有文件
fd --hidden .py

# 执行操作
fd .py -x rm {}

# 与fzf集成
fd .py | fzf --multi | xargs code
```

**技巧**:
```bash
# 查找并打开文件
fd .py --exec vim {}

# 删除所有pycache
fd __pycache__ --type d -x rm -rf
```

---

### 5. bat (cat替代) ⭐⭐⭐⭐⭐

**用途**: 语法高亮的文件查看

**安装**: macOS
```bash
brew install bat
```

**安装**: Ubuntu/Debian
```bash
sudo apt-get install bat
```

**配置** (添加到 ~/.bashrc):
```bash
alias cat='bat -p'
alias catn='bat'
```

**使用**:
```bash
# 查看文件（有语法高亮）
bat app.py

# 分页查看（保留高亮）
bat -p app.py | less -R

# 查看Git修改
bat -d app.py

# 查看行号
bat -n app.py
```

---

### 6. ripgrep (rg) ⭐⭐⭐⭐⭐

**用途**: 极速代码搜索

**安装**: macOS
```bash
brew install ripgrep
```

**安装**: Ubuntu/Debian
```bash
sudo apt-get install ripgrep
```

**配置** (添加到 ~/.bashrc):
```bash
alias grep='rg'
```

**使用**:
```bash
# 搜索Python文件中的TODO
rg "TODO" -g "*.py"

# 显示上下文
rg -A 3 -B 3 "def function_name" app.py

# 统计匹配数
rg --count "import"

# 搜索并打开文件
rg "TODO" --files-with-matches | fzf | xargs bat
```

**技巧**:
```bash
# 搜索并替换（预览）
rg "old_function" -S | fzf

# 忽略大小写
rg -i "error" logs/

# 指定编码
rg --encoding utf8 "pattern"
```

---

### 7. starship (Shell提示符) ⭐⭐⭐⭐⭐

**用途**: 智能Shell提示符

**安装**: 所有平台
```bash
curl -sS https://starship.rs/install.sh | sh
```

**配置** (添加到 ~/.bashrc):
```bash
eval "$(starship init bash)"
```

**配置** (创建 ~/.config/starship.toml):
```toml
# 显示git信息
[git_branch]
symbol = "🌿 "

# 显示Python版本
[python]
symbol = "🐍 "

# 显示目录
directory]
truncate_to_repo = true
truncation_symbol = "…/"
```

**效果**:
```bash
# 从
~/projects/ai-runtime $

# 到
~/p/a on main 🌿 +2 ~1 🐍 v3.11.5 $
```

---

## 进阶推荐

### 8. jq (JSON处理) ⭐⭐⭐⭐⭐

**用途**: JSON查询和转换

**安装**: macOS
```bash
brew install jq
```

**安装**: Ubuntu/Debian
```bash
sudo apt-get install jq
```

**基础使用**:
```bash
# 美化打印
cat data.json | jq '.'

# 提取字段
cat api.json | jq '.users[0].name'

# 数组长度
cat data.json | jq '.items | length'

# 过滤
cat logs.json | jq '.[] | select(.level == "ERROR")'

# 转换
cat data.json | jq '{new_name: .old_name, count: .items | length}'
```

**在ai-runtime中的使用**:
```bash
# 分析JSON格式的认知记录
jq '.entries[] | select(.type == "ERROR")' .ai-runtime/memory/episodic/timeline.json

# 发现工具统计显示
python3 discover-toolkit.py list --json | jq '.[] | {tool: .tool_name, lang: .language}'
```

**技巧**:
```bash
# 函数式编程风格
cat data.json | jq 'map(.value * 2) | add'

# 条件判断
cat config.json | jq '.env.WIN_VERBOSE = if .debug then "true" else "false" end'
```

---

### 9. zellij (tmux替代) ⭐⭐⭐⭐

**用途**: 终端复用器

**vs tmux**:
- Rust编写，更现代
- 配置文件更简单（YAML）
- 内置布局

**安装**: 所有平台
```bash
cargo install zellij
```

**配置**:
```bash
# 创建默认配置
zellij setup --dump-config > ~/.config/zellij/config.kdl
```

**基本使用**:
```bash
# 启动
zellij

# 快捷键 (与tmux类似)
Ctrl-o n  # 新窗格
Ctrl-o h  # 水平分割
Ctrl-o d  # 向下分割
Ctrl-o x  # 关闭窗格
Ctrl-o q  # 退出

# 附带状态栏
Ctrl-o b  # 显示状态栏
```

---

### 10. procs (ps替代) ⭐⭐⭐⭐

**用途**: 进程查看器

**vs ps**:
- 彩色输出
- 树形显示
- 搜索过滤

**安装**:
```bash
cargo install procs
```

**使用**:
```bash
# 查看所有进程
procs

# 搜索进程
procs python

# 树形显示
procs --tree
```

---

## 专家级

### 11. just (make替代) ⭐⭐⭐⭐

**用途**: 任务运行器

**vs make**:
- 语法更现代
- 错误信息更清晰
- 跨平台

**安装**:
```bash
cargo install just
```

**创建 justfile**:
```makefile
# 在项目中创建 justfile
lint:
  @echo "Running pylint..."
  pylint src/

test:
  @echo "Running pytest..."
  pytest tests/

check:
  just lint
  just test
```

**使用**:
```bash
just lint
just test
just check
```

---

### 12. hyperfine (benchmark) ⭐⭐⭐⭐

**用途**: 命令行性能测试

**使用**:
```bash
# 测试两个命令性能
hyperfine 'find . -name "*.py"' 'fd .py'

# 预热
hyperfine --warmup 3 'python app.py'

# 导出结果
hyperfine --export-markdown results.md 'cmd1' 'cmd2'
```

---

## 整合到ai-runtime

### 1. 在discover-toolkit.py中添加"external"分类

可以扩展discover-toolkit.py，使其能够检索系统已安装的外部工具。

### 2. 在脚本中使用

示例：在runtime-explore.sh中
```bash
# 使用fzf选择文件
FILE=$(fd .py | fzf --preview 'bat -n --color=always {}')
read_file_content "$FILE"
```

### 3. 配置检查

在系统初始化时检查关键工具是否安装：
```bash
# check-tools.sh
for tool in fzf eza zoxide fd bat rg jq; do
    if ! command -v $tool &> /dev/null; then
        echo "❌ $tool 未安装"
    else
        echo "✅ $tool 已安装"
    fi
done
```

---

## 总结：个人工具箱

推荐每个人建立自己的"工具箱":

### 最小工具箱（4个）
- fzf + eza + zoxide + fd

### 完整工具箱（10个）
- fzf + eza + zoxide + fd + bat + rg + starship + jq + xh + delta

### 终极工具箱（20+个）
- 所有上面工具 + glances + hyperfine + just + age + ...

---

## 维护

**定期检查**: 每月检查是否有新工具发布

**更新策略**:
- 基础工具（fzf, eza, zoxide, fd）: 建议始终使用最新版
- 进阶工具: 根据需求更新
- 专家工具: 有新功能时再更新

**废弃管理**:
- 记录工具替代关系（如ripgrep > grep）
- 在meta.yml中标记"replaced_by"
- 维护向后兼容策略

---

**最后更新**: 2025-11-14
**下次审查**: 2025-12-14
