# 国际象棋书籍中文翻译项目

本项目保存英文扫描原书、OCR、中文译稿、校对记录、棋图、生成脚本与历次 PDF。Git 同步后的接续工作从本页开始；历史文件保留原路径，避免破坏原页溯源和排版引用。

## 当前工作

截至 2026-10-18，Vukovic《Art of Attack in Chess》（国际象棋进攻的艺术）全书初译、扫描校订及语言复核已完成，已应用此前确认的订正，当前为v3对照校样，进入人工校对阶段。统一交付入口是[全书各章中英对照校样](output/pdf/art_of_attack_bilingual_complete/README.md)，包括开篇、导言、十二章与两份索引。具体页数、检查范围和原书疑点见当前书说明与校勘记录。

| 书籍 | 当前状态 | 入口 |
| --- | --- | --- |
| Chess Middlegame Planning | 中文第一版已保存，后续修订须按记录接续 | [译稿说明](translations/chess_middlegame_planning/README.md) · [第一版 PDF](output/pdf/chess_middlegame_planning_zh_first_edition.pdf) |
| Art of Attack in Chess | 全书语言复核及v3对照校样已完成，待用户校对 | [项目说明](translations/art_of_attack/README.md) · [统一校样](output/pdf/art_of_attack_bilingual_complete/README.md) · [订正记录](translations/art_of_attack/translation/USER_CORRECTIONS.md) |
| Logical Chess Move By Move | 暂缓，已归档原书 | [原书清单](books/README.md) |
| How to Think in Chess | 暂缓，已归档原书 | [原书清单](books/README.md) |

## 文件分工

| 目录 | 用途 |
| --- | --- |
| `books/originals/` | 原始PDF，不直接修改；校验值见 `books/README.md` |
| `translations/` | 按书分开的译稿、OCR、扫描页、棋图、段号与校对记录 |
| `tools/art_of_attack/` | 当前书的准备、校样生成、棋谱与版面检查程序 |
| `output/pdf/` | 已生成成品与历史校样；具体版本以文件名及对应说明为准 |
| `tmp/pdfs/` | 历史脚本、排版块、渲染图与检查记录；含复现第一版所需资料，不能整体删除 |
| `tmp/skill_backups/` | 历史翻译技能快照，不能当作最新规则覆盖后续用户订正 |
| `docs/` | 接续说明、迁移问题与文件清单 |

## 接续入口

- [下一步工作与迁移说明](docs/HANDOFF.md)
- [已确认术语与执行约定](docs/TRANSLATION_RULES.md)
- [全文件清单](docs/inventory/files.csv) · [本机检查结果](docs/inventory/audit.json)
- [早期排版方案](books/TRANSLATION_LAYOUT_GUIDE.md)：其中出版版式建议与当前双语校样用途不同；后续用户确认的规则优先。

在项目根目录运行以下只读检查，不需要第三方 Python 库：

```powershell
.\.venv\Scripts\python.exe tools/audit_workspace.py
```

本机依赖已安装到项目虚拟环境。运行 `.\.venv\Scripts\python.exe tools/check_environment.py` 检查依赖、字体、Poppler、OCR引擎与校样路径；需要复现安装时见[迁移说明](docs/HANDOFF.md)。

显式加 `--write` 时只更新 `docs/inventory/` 下的清单与报告。扫描范围为 Git 已跟踪文件及未被忽略的新文件，不含 `.git` 内部文件和本机依赖缓存。二进制文件校验字节及来源完整性；清单不代表重新逐页目检所有 PDF 和图片。

日常校对默认记录意见或修改指定译稿；只有明确要求更新校样 PDF 时才重新生成、视觉检查并交付。原书、原始 OCR 和历史归档与人工校订稿分开维护。
