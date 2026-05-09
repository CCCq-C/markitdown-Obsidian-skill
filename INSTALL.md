---
audience: AI agent (Claude Code / Cursor / 任何能执行 Bash / PowerShell 的 AI)
purpose: 让 AI 自动为用户安装本仓库提供的 markitdown-converter Skill
---

# markitdown-converter · AI 安装指引

> **使用方式：** 把本文档（或仓库链接）发给你的 AI 助手，并对它说：
>
> > "请按照这份文档帮我安装 markitdown-converter skill。"
>
> AI 会自动按下面的步骤完成所有安装，你只需在它问 vault 路径时回答即可。

---

## 📋 给 AI 的指令（请严格按顺序执行）

你的任务是为用户安装 `markitdown-converter` Claude Code Skill。

**这个 skill 做什么：** 把任意文件（PDF / Word / Excel / PPT / 图片 / 音频 / URL / YouTube 等）转成 Markdown 笔记，直接保存到用户的 Obsidian vault。**纯本地转换，不消耗 AI token。**

**安装的本质就是 4 件事：**

1. 确认用户的 Obsidian vault 路径
2. 安装 `uv`（Python 包管理器，自动管理依赖，无需用户预装 Python）
3. 把本仓库 `git clone` 到 `<vault>/.claude/skills/markitdown-converter/`
4. 创建 `config.json`，验证安装

---

## Step 1 · 确认 Obsidian Vault 路径

**先问用户：** "你的 Obsidian vault 在哪个路径？（完整绝对路径，例如 `/Users/yourname/Documents/Obsidian` 或 `C:\Users\yourname\Documents\Obsidian`）"

> 💡 自动检测建议：在询问前可以先探测常见位置，发现就直接展示给用户确认。
>
> **Mac：**
> ```bash
> for p in "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian" \
>          "$HOME/Documents/Obsidian" \
>          "$HOME/Desktop/Obsidian"; do
>   [ -d "$p" ] && echo "找到: $p"
> done
> ```
>
> **Windows (PowerShell)：**
> ```powershell
> @("$env:USERPROFILE\Documents\Obsidian", "$env:OneDrive\Documents\Obsidian") |
>   Where-Object { Test-Path $_ } | ForEach-Object { "找到: $_" }
> ```

**确认得到的路径后，把它存成变量备用**（下文用 `$VAULT` / `<VAULT>` 占位）：

- Mac/Linux：`VAULT="/Users/yourname/Documents/Obsidian"`
- Windows：`$VAULT = "C:\Users\yourname\Documents\Obsidian"`

---

## Step 2 · 安装 uv（如未安装）

uv 是用 Rust 写的 Python 包管理器，**单文件二进制，不依赖系统 Python**。

### Mac / Linux

```bash
if ! command -v uv &>/dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi
uv --version    # 应该输出版本号
```

### Windows (PowerShell)

```powershell
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    $env:PATH = "$env:USERPROFILE\.local\bin;$env:USERPROFILE\.cargo\bin;$env:PATH"
}
uv --version
```

### 预热依赖（可选但推荐）

```bash
uv run --with "markitdown[all]" python -c "from markitdown import MarkItDown; print('OK')"
```

第一次执行需 1-3 分钟下载 ~50MB，之后就有缓存了。

---

## Step 3 · Clone 本仓库到 Vault 内

> 仓库地址：https://github.com/CCCq-C/markitdown-Obsidian-skill
>
> 注意：远程仓库名是 `markitdown-Obsidian-skill`，但本地 clone 时**必须用 `markitdown-converter` 作为目录名**——这是 SKILL.md 里 `name:` 字段定义的 skill 名，Claude Code 用这个识别 skill。

### Mac / Linux

```bash
# 确保 .claude/skills 目录存在
mkdir -p "$VAULT/.claude/skills"

# Clone 到 vault 内的 skills 目录
git clone https://github.com/CCCq-C/markitdown-Obsidian-skill \
  "$VAULT/.claude/skills/markitdown-converter"
```

### Windows (PowerShell)

```powershell
New-Item -ItemType Directory -Force -Path "$VAULT\.claude\skills" | Out-Null

git clone https://github.com/CCCq-C/markitdown-Obsidian-skill `
  "$VAULT\.claude\skills\markitdown-converter"
```

> 如果用户机器上没有 git，可以改用 `curl -L .../archive/refs/heads/main.zip` 下载并解压。

---

## Step 4 · 创建 config.json

把 `config.json.example` 复制为 `config.json`，并把 `vault_path` 改成用户的真实 vault 路径。

### Mac / Linux 一行命令

```bash
cat > "$VAULT/.claude/skills/markitdown-converter/config.json" << EOF
{
  "vault_path": "$VAULT"
}
EOF
```

### Windows (PowerShell)

```powershell
@{ vault_path = $VAULT } | ConvertTo-Json |
  Set-Content "$VAULT\.claude\skills\markitdown-converter\config.json" -Encoding UTF8
```

---

## Step 5 · 验证安装

执行以下命令，输出非空即代表 skill 完全可用：

### Mac / Linux

```bash
echo "测试文档" > /tmp/test.txt
python3 "$VAULT/.claude/skills/markitdown-converter/scripts/convert.py" /tmp/test.txt \
  && echo "✅ 验证通过"
```

### Windows (PowerShell)

```powershell
"测试文档" | Out-File -Encoding UTF8 "$env:TEMP\test.txt"
python "$VAULT\.claude\skills\markitdown-converter\scripts\convert.py" "$env:TEMP\test.txt"
if ($LASTEXITCODE -eq 0) { Write-Host "✅ 验证通过" }
```

---

## Step 6 · 通知用户

向用户报告：

> ✅ markitdown-converter skill 已装好，位置：`<VAULT>/.claude/skills/markitdown-converter/`
>
> **使用方式：** 重启 Claude Code，然后对我说：
> - "帮我把 ~/Desktop/report.pdf 转成笔记"
> - "把这个 Word 文档导入 Obsidian"
> - "把 https://youtu.be/xxx 转成 Markdown"
>
> 我会自动调用 skill，转好的笔记会按文件类型路由到对应文件夹（书籍 → `书籍拆解/`、图片 → `FuJian/` 等）。
>
> **修改 vault 路径：** 编辑 `<VAULT>/.claude/skills/markitdown-converter/config.json`。
> **更新 skill：** `cd "<VAULT>/.claude/skills/markitdown-converter" && git pull`

---

## 📌 Troubleshooting（给 AI 排错用）

| 症状 | 原因 | 修复 |
|---|---|---|
| `command not found: uv` | uv 装好但 PATH 没刷新 | `export PATH="$HOME/.local/bin:$PATH"` 后重试 |
| Windows `python` 跳转到 Microsoft Store | 系统装了 Store 存根 | 用 `uv run` 直接跑，或装真正的 Python |
| 转换 PDF 输出为空 | 扫描版 PDF（纯图片） | 提示用户用 OCR 工具（如 ocrmypdf） |
| `markitdown 在托管环境中仍无法加载` | uv 缓存损坏 | `uv cache clean` 后重试 |
| Claude Code 重启后仍未识别 skill | skill 不在该 vault 内 | 检查 `<vault>/.claude/skills/` 是否真的存在该目录 |
| `git: command not found` | 用户没装 git | 改用 zip 下载：`curl -L https://github.com/CCCq-C/markitdown-Obsidian-skill/archive/refs/heads/main.zip -o /tmp/m.zip && unzip /tmp/m.zip -d "$VAULT/.claude/skills/" && mv "$VAULT/.claude/skills/markitdown-Obsidian-skill-main" "$VAULT/.claude/skills/markitdown-converter"` |

---

## 🔧 卸载方法

```bash
# Mac / Linux
rm -rf "$VAULT/.claude/skills/markitdown-converter"

# Windows
Remove-Item -Recurse -Force "$VAULT\.claude\skills\markitdown-converter"
```

uv 本身可以保留（其他工具也用得到）；如要彻底卸载：`rm -rf ~/.local/share/uv ~/.local/bin/uv`。
