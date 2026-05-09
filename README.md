# markitdown-converter

> 一个 Claude Code Skill — 把 **PDF / Word / PPT / Excel / 图片 / 音频 / 网页 / YouTube** 一键转成 Markdown 笔记，直接存入你的 Obsidian vault。
>
> ✨ **纯本地转换，不消耗任何 AI token。**

## 支持格式

PDF · Word (.docx) · PowerPoint (.pptx) · Excel (.xlsx/.xls) · 图片 (JPG/PNG/GIF/WEBP) · 音频 (MP3/WAV) · HTML · CSV · JSON · XML · EPUB · YouTube · 普通网页 URL

---

## 🚀 推荐安装方式：让 AI 帮你装

把下面这段话发给你的 AI 助手（Claude Code / Cursor / Codex 等任何能执行命令的 AI）：

> 请按照这份文档帮我安装 markitdown-converter skill：
> https://github.com/CCCq-C/markitdown-Obsidian-skill/blob/main/INSTALL.md

AI 会自动：
1. 问你的 Obsidian vault 路径
2. 安装 `uv`（Python 包管理器，零依赖）
3. 把 skill 装到你的 vault 内
4. 验证可用性

整个过程 2-5 分钟，**你只需要回答一次"你的 vault 在哪儿"。**

---

## 🔧 手动安装（懂命令行的用户）

### 1️⃣ 安装 uv

```bash
# Mac / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2️⃣ Clone 到 vault 内

```bash
# 把 <VAULT> 换成你的 Obsidian vault 绝对路径
VAULT="/Users/yourname/Documents/Obsidian"

git clone https://github.com/CCCq-C/markitdown-Obsidian-skill \
  "$VAULT/.claude/skills/markitdown-converter"
```

### 3️⃣ 创建 config.json

```bash
cp "$VAULT/.claude/skills/markitdown-converter/config.json.example" \
   "$VAULT/.claude/skills/markitdown-converter/config.json"

# 编辑该文件，把 vault_path 改成你自己的 vault 绝对路径
```

### 4️⃣ 重启 Claude Code

完成。重启后对 Claude 说"帮我把 xxx.pdf 转成笔记"即可。

---

## 📖 使用示例

安装后，对你的 Claude Code 说：

- "帮我把 `~/Desktop/report.pdf` 转成笔记"
- "把这个 Word 文档导入 Obsidian"
- "把 https://youtu.be/xxx 转成 Markdown"
- "把 `销售分析.xlsx` 转成笔记，放到书籍拆解文件夹"

Claude 会自动：
- 调用 `convert.py` 完成本地转换（用 uv 自动管理 Python 依赖）
- 按文件类型路由到对应文件夹（书籍 → `书籍拆解/`、图片 → `FuJian/`、其他 → vault 根目录）
- 生成带 frontmatter 的 Markdown 笔记

---

## 🏗️ 工作原理

- 转换核心：微软开源的 [MarkItDown](https://github.com/microsoft/markitdown) 库
- 依赖管理：[uv](https://github.com/astral-sh/uv)（无需手动配置 Python 环境）
- 触发机制：Claude Code Skills，自动识别"转换文件"类指令

```
用户:        "把这个 PDF 转成笔记"
   ↓
Claude:      读取 SKILL.md → 触发 markitdown-converter
   ↓
convert.py:  调用 uv run --with markitdown[all] 完成转换
   ↓
Claude:      把 Markdown 写入对应的 vault 文件夹
```

唯一例外：**扫描版 PDF（纯图片）** 无法自动提取文字，需先用 OCR 工具处理。

---

## 📁 仓库结构

```
markitdown-converter/
├── README.md              ← 本文件
├── INSTALL.md             ← 给 AI 读的详细安装指引（推荐入口）
├── SKILL.md               ← Skill 元文件 + 工作流定义
├── scripts/
│   └── convert.py         ← 转换脚本（跨平台）
├── config.json.example    ← 配置模板（vault_path）
├── LICENSE                ← MIT
└── .gitignore             ← 忽略本地 config.json
```

---

## ❓ 常见问题

**Q: 装完后 Claude 不识别 skill？**
A: 确认 skill 装在 `<vault>/.claude/skills/markitdown-converter/` 目录下，且重启了 Claude Code。

**Q: 我有多个 vault，怎么办？**
A: 每个 vault 单独 clone 一份即可，互不干扰。每个 vault 的 `config.json` 各自指向自己。

**Q: PDF 转出来是空的？**
A: 大概率是扫描版 PDF（纯图片），用 [ocrmypdf](https://github.com/ocrmypdf/OCRmyPDF) 先 OCR 一遍。

**Q: 修改了 vault 位置怎么办？**
A: 编辑 `<vault>/.claude/skills/markitdown-converter/config.json` 的 `vault_path` 字段。

**Q: 怎么更新 skill？**
A: `cd "<vault>/.claude/skills/markitdown-converter" && git pull`

---

## 📜 License

[MIT](./LICENSE) · 任意使用与修改。
