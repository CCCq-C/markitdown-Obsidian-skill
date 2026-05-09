---
name: markitdown-converter
description: 使用 MarkItDown 将各种文件（PDF、Word、Excel、PPT、图片、音频、URL、YouTube 等）转成 Markdown 并存入 Obsidian 笔记。当用户说"帮我把文件转成笔记"、"把这个PDF导入Obsidian"、"把文件转成md"、"导入文档"、"转换文件"、"把PPT/Excel/Word转成笔记"，或者拖拽文件、提到任何需要把文档内容变成可阅读笔记的场景时，必须触发此 skill。
---

# MarkItDown Converter

把任意文件或 URL 转换为 Markdown，然后在 Obsidian vault 中创建笔记。

## 工具路径

- **转换脚本**：skill 目录下的 `scripts/convert.py`
- **依赖管理**：脚本自动处理，优先用 uv，回退到 venv，无需手动干预
- **配置文件**：与本 SKILL.md 同目录的 `config.json`（位于 `<vault>/.claude/skills/markitdown-converter/config.json`）

## 工作流程

### 第一步：读取 Obsidian Vault 路径

skill 已装在 vault 内部，**vault 路径就是 SKILL.md 文件向上 3 级的祖父目录**（`<vault>/.claude/skills/markitdown-converter/SKILL.md`）。

读取同目录下的 config.json 获取规范路径：

```bash
# 相对 SKILL.md 所在目录
cat ./config.json    # vault_path 字段即为 vault 根目录
```

- 如果 config.json 存在，取 `vault_path` 字段的值
- 如果不存在，使用 SKILL.md 所在目录向上 3 级的路径作为 vault 根目录

### 第二步：识别输入

用户可能提供：
- **本地文件路径**：如 `/Users/ziyan/Desktop/report.pdf`（Mac）或 `C:\Users\user\Desktop\report.pdf`（Windows）
- **URL**：如 `https://example.com`、YouTube 链接 `https://youtu.be/xxx`
- **文件名（无完整路径）**：如 `report.pdf`，先在 Desktop、Downloads 查找

### 第三步：执行转换

```bash
# Mac / Linux（<vault> 即第一步获取的 vault 根目录）
python3 "<vault>/.claude/skills/markitdown-converter/scripts/convert.py" "<文件路径或URL>"

# Windows (PowerShell)
python "<vault>\.claude\skills\markitdown-converter\scripts\convert.py" "<文件路径或URL>"
```

脚本自动查找可用的 Python 环境（uv → venv → 报错），输出 Markdown 到 stdout。

### 第四步：确定 Obsidian 保存路径

根据输入类型路由到合适的文件夹（基于第一步获取的 vault 路径）：

| 输入类型 | 保存位置 |
|---------|---------|
| 书籍、PDF 书籍、EPUB | `<vault>/书籍拆解/` |
| 论文、学术文章 | `<vault>/论文工作流/` |
| 图片（JPG、PNG 等） | `<vault>/FuJian/` |
| 通用文档（Word、PPT、Excel）| `<vault>/`（根目录） |
| 网页 / YouTube / URL | `<vault>/`（根目录） |
| 不确定 | 询问用户 |

### 第五步：生成笔记文件名

格式：`YYYY年M月D日-原文件名关键词.md`

示例：
- `report.pdf` → `2026年5月7日-report.md`
- `销售分析.xlsx` → `2026年5月7日-销售分析.md`
- YouTube 链接 → `2026年5月7日-youtube-视频标题.md`

### 第六步：添加 YAML frontmatter

在 Markdown 内容前加上：

```yaml
---
source: "<原始文件路径或URL>"
converted_at: "YYYY-MM-DD"
type: "<pdf|docx|pptx|xlsx|image|url|youtube|...>"
tags:
  - markitdown
  - imported
---
```

### 第七步：写入 Obsidian 并更新 ProjectMap

1. 将完整内容（frontmatter + Markdown）写入目标路径
2. 如果目标文件夹有 `ProjectMap.md`，在表格末尾追加新记录

## 错误处理

- **config.json 不存在**：询问用户 vault 路径，写入后继续
- **文件不存在**：报告错误，询问用户确认路径
- **转换结果为空**：告知用户该文件可能是扫描版图片，建议 OCR 工具处理
- **找不到 uv 或 venv**：提示用户安装 uv（curl -LsSf https://astral.sh/uv/install.sh | sh）

## 支持的格式

PDF、DOCX、PPTX、XLSX、XLS、图片（JPG/PNG/GIF/WEBP）、音频（MP3/WAV）、HTML、CSV、JSON、XML、EPUB、ZIP、YouTube URL、普通 URL
