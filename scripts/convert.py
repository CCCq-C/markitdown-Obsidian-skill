#!/usr/bin/env python3
"""
MarkItDown 转换脚本（跨平台版）
用法: python convert.py "<文件路径或URL>"
输出: Markdown 内容到 stdout，错误到 stderr

依赖查找顺序：
  1. 当前 Python 环境已有 markitdown → 直接使用
  2. 系统有 uv → uv run --with markitdown[all]（自动管理依赖，推荐）
  3. ~/.markitdown-venv 存在 → 用 venv 里的 Python 重新运行（向后兼容）
  4. 都没有 → 报错并给出安装建议
"""

import sys
import os
import subprocess
import shutil


VENV_PYTHON_PATHS = [
    os.path.expanduser("~/.markitdown-venv/bin/python"),
    os.path.expanduser("~/.markitdown-venv/Scripts/python.exe"),
    os.path.expanduser("~/.markitdown-venv/Scripts/python"),
]


def find_uv():
    """查找 uv 可执行文件"""
    candidates = [
        os.path.expanduser("~/.local/bin/uv"),      # astral 默认安装位置 (Mac/Linux)
        os.path.expanduser("~/.cargo/bin/uv"),       # cargo 安装
        "/opt/homebrew/bin/uv",                      # Homebrew (Mac)
        "/usr/local/bin/uv",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return shutil.which("uv")  # 从 PATH 查找


def find_venv_python():
    """查找虚拟环境中的 Python（旧方式，向后兼容）"""
    for path in VENV_PYTHON_PATHS:
        if os.path.exists(path):
            return path
    return None


def main():
    if len(sys.argv) < 2:
        print("用法: python convert.py <文件路径或URL>", file=sys.stderr)
        sys.exit(1)

    source = sys.argv[1]

    # ── 尝试直接导入 markitdown ──────────────────────────────
    try:
        from markitdown import MarkItDown

    except ImportError:
        # 防止递归循环（已在托管环境中时不再重试）
        if os.environ.get("_MARKITDOWN_SPAWNED"):
            print(
                "错误: markitdown 在托管环境中仍无法加载，请重新运行安装脚本。",
                file=sys.stderr
            )
            sys.exit(3)

        env = {**os.environ, "_MARKITDOWN_SPAWNED": "1"}

        # 优先用 uv（自动管理依赖，无需手动安装 Python 包）
        uv = find_uv()
        if uv:
            result = subprocess.run(
                [uv, "run", "--with", "markitdown[all]", __file__] + sys.argv[1:],
                env=env,
                capture_output=False
            )
            sys.exit(result.returncode)

        # 回退：用旧版 venv
        venv_python = find_venv_python()
        if venv_python and venv_python != sys.executable:
            result = subprocess.run(
                [venv_python, __file__] + sys.argv[1:],
                env=env,
                capture_output=False
            )
            sys.exit(result.returncode)

        # 都找不到，给出明确指引
        print(
            "错误: 未找到 markitdown，也未找到 uv 或虚拟环境。\n"
            "请安装 uv：\n"
            "  Mac/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh\n"
            "  Windows:   powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"",
            file=sys.stderr
        )
        sys.exit(3)

    # ── 执行转换 ─────────────────────────────────────────────
    try:
        md = MarkItDown()
        result = md.convert(source)

        if not result or not result.text_content or not result.text_content.strip():
            print(
                "[警告] 转换结果为空。\n"
                "可能原因：PDF 是扫描版（图片型），没有文字层\n"
                "建议：使用 OCR 工具处理扫描版 PDF",
                file=sys.stderr
            )
            sys.exit(2)

        print(result.text_content)

    except FileNotFoundError:
        print(f"错误: 文件不存在 - {source}\n请确认路径是否正确", file=sys.stderr)
        sys.exit(4)
    except Exception as e:
        print(f"错误: 转换失败 - {e}", file=sys.stderr)
        sys.exit(4)


if __name__ == "__main__":
    main()
