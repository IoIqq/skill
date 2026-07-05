# FTB Quests Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Minecraft](https://img.shields.io/badge/Minecraft-1.20%2B-green.svg)](https://www.minecraft.net/)
[![FTB Quests](https://img.shields.io/badge/FTB%20Quests-Modern%20JSON5-blue.svg)](https://github.com/FTBTeam/FTB-Quests)

中文

一个为 Minecraft 整合包生成 **FTB Quests** 配置文件的 Claude Code 技能——输出当前 FTB Quests 使用的**现代 JSON5 磁盘格式**。

> 格式已于 2026-06-19 对照 FTB Quests 源码验证
> ([`FTBTeam/FTB-Quests`](https://github.com/FTBTeam/FTB-Quests) `main`，MC `26.1.x`，
> [`FTBTeam/FTB-Library`](https://github.com/FTBTeam/FTB-Library)，
> [`marhali/json5-java`](https://github.com/marhali/json5-java))。

## 功能特性

- **C3 混合架构**：Python 负责确定性 ID / 坐标 / 依赖项 / 清单；LLM 负责标题、描述、任务与奖励内容。可分层编辑，不会丢失玩家进度。
- **智能格式检测**：自动识别现有整合包中的现代 JSON5 与旧版 SNBT 格式。
- **模组元数据提取**：`extract_mods.py` 解析 `mods/*.jar`（NeoForge / Forge / Fabric / 旧版 mcmod），面试时可根据实际模组集推荐章节。
- **物品名→ID 批量查询**：`extract_items.py` 顺带写出 `item_names.json5`（en+zh 显示名→ID 轻量索引，只读一次 jar），`lookup_item.py` 一次性解析 N 个名字（收集任务/大量物品任务），同名多 ID（如 "Copper Ingot" 跨 mod）会列出全部候选而非瞎猜（禁止脑补）。
- **增量更新**：重新运行生成器会保留游戏内编辑。清单通过内容哈希跟踪每个技能所有对象；重命名通过 `aliases` 保留 hex ID。
- **安全部署**：`generate_quests.py --deploy <整合包>` 把生成的 `quests/` 子文件夹安全合并进现有整合包——可叠加文件（`data.json5`/`chapter_groups.json5`/lang）做**合并**（新内容与原版同处一文件），同名章节先**备份原版**再替换；覆盖前用 ⚠️ 报告醒目标注会改动整合包原版的文件，原版备份到 `.ftbq-backup/<时间戳>/`（点前缀目录，FTB 扫描器跳过），文件名全程不变方便排查。
- **重型验证器**：18 种诊断代码，带 `file:line:col` 定位；缺失依赖项有模糊"你是不是想说"提示；`--fix` 自动修复；`--json` CI 输出；`--strict` 警告即错误。
- **面试驱动**：逐分支烤问用户——每次一个问题并附带推荐答案，代码库优先（先探索索引的任务/模组再提问）——涵盖主题、模组、结构和奖励。
- **国际化**：Lang 文件使用 `@chapter/quest.subkey` 占位符；生成器会重写为 hex key。首次生成后 lang 文件完全归用户所有。
- **跟随用户语言**：中文对话全程用中文（面试、推荐、平衡评审、总结、报错说明），英文对话用英文，随用户切换。生成任务文本的语言由面试中确定的 `locales` 决定，与对话语言相互独立。
- **上下文与记忆（可选）**：安装 CodeGraph/Memory 工具链后，Step 1 索引时加载该整合包的先前会话决策，生成后于 Step 5b 捕获；否则依赖自身索引 + 验证器，默认便携。

## 解决的关键问题

手动操作容易出错的地方，技能会自动处理：

- **JSON5 而非 SNBT**：字段间有逗号、纯数字（`0.0` 而非 `0.0d`）、`true`/`false`（而非 `1b`）
- **物品作为对象**：`item: { id: "...", count: N }`，绝不使用裸字符串
- **物品任务数量陷阱**：所需数量是*同级* `count` 字段，不是物品的 count
- **文本在 lang 文件中**：现代 FTB Quests 忽略内联标题
- **确定性 ID**：使用 `md5("<pack>/<chapter>/<obj>/<name>")` 确保稳定再生成

## 安装

### 方式一：直接克隆（推荐）

```bash
# Linux/macOS
git clone https://github.com/IoIqq/ftb-quests-skills.git ~/.claude/skills/ftb-quests

# Windows (PowerShell)
git clone https://github.com/IoIqq/ftb-quests-skills.git C:\Users\<你>\.claude\skills\ftb-quests
```

### 方式二：手动下载

1. 下载 [最新版本](https://github.com/IoIqq/ftb-quests-skills/releases)
2. 解压到 `~/.claude/skills/ftb-quests/`（Windows 为 `C:\Users\<你>\.claude\skills\ftb-quests\`）

## 使用方法

在任何 Claude Code 会话中，提出 FTB Quests 相关需求：

- `帮我生成 FTB 任务线`
- `Create FTB quests for my modpack`
- `Generate quest config`

技能会：
1. 检测你的整合包格式与索引（若有现有任务；若已装 CodeGraph/Memory 工具链，同时加载先前会话记忆）
2. 逐分支烤问你——每次一个问题并附带推荐答案，依次覆盖主题 → 模组 → 结构 → 奖励
3. 生成完整的任务配置文件（干净 `quests/` 子文件夹，可直接复制）
4. 交付前运行验证；已有整合包可用 `--deploy` 安全合并（合并可叠加文件、备份原版）；若已装工具链，于部署后记住本次决策供下次使用

### 示例工作流

```
你: 帮我用 FTB Quests 生成一个科技整合包的任务线

Claude: [如果已安装 CodeGraph 工具链，加载整合包的先前记忆]
[逐分支烤问：主题、模组、章节数、奖励理念——每次一个问题，附带推荐答案...]
[生成 data.json5, chapters/*.json5, lang/zh_cn/quests.json5]
[运行验证脚本]
✅ 生成 3 个章节、12 个任务、18 个任务项、15 个奖励
```

## 环境要求

- **Claude Code** 或兼容的技能系统
- **Python 3.6+**（用于验证脚本）
- **整合包文件夹**，含 `mods/` 目录或 `manifest.json`（可选——新建包也可使用）
- **游戏内**：`/ftbquests editing_mode` 加载生成的任务

## 项目结构

```
ftb-quests/
├── SKILL.md                                    # 操作手册: 工作流 + 格式规则 + grill/核实指令
├── ftbq/                                       # 共享核心
│   ├── json5.py                                # 字符串感知词法/语法分析器 w/ line:col
│   ├── snbt.py                                 # 1.20.1 SNBT 解析器 + 生成器
│   ├── ids.py                                  # md5 16-hex ID + top-bit mask + content_hash
│   ├── canonical.py                            # 字节稳定的 JSON5 生成器
│   ├── audit.py                                # DLC-vs-installed 审计索引/diff
│   └── deploy.py                               # 安全部署: 覆盖检测 + 合并 + .ftbq-backup 备份
├── scripts/
│   ├── extract_mods.py                         # mods/*.jar → .ftbq-cache/mods.json5
│   ├── extract_items.py                        # jar lang → items.json5（已验证 ID）+ item_names.json5（name→id 索引，en+zh）
│   ├── index_quests.py                         # 现有任务 → existing_quests.json5 + known_item_ids
│   ├── pack_briefing.py                        # 一条命令出 pack 摘要（token-saving）
│   ├── quest_detail.py                         # 单 quest 详情（Step 4 循环）
│   ├── lookup_item.py                          # 批量 name→id 查询（收集任务/大量物品，token-saving）
│   ├── generate_quests.py                      # spec → quests/ + manifest（--deploy 安全落地）
│   ├── validate_quests.py                      # 诊断代码 + 自动修复
│   ├── audit_index.py                          # DLC 审计索引
│   └── audit_diff.py                           # DLC vs installed diff（resume-first）
├── reference/                                  # 按需加载的参考材料
│   ├── ftb-quests-reference.md                 # §1-§20 字段/类型/规范/诊断/部署
│   ├── design/                                 # 设计指南（Step 2/3/4 按需加载）
│   │   ├── design-guide.md                     # 原则/脊梁/协同/实证/布局/写作风格
│   │   ├── difficulty-curve.md                 # 难度曲线
│   │   ├── reward-economy.md                   # 奖励经济
│   │   └── tech-progression.md                 # tech mod 进阶（orientation only，须 JEI/EMI 核实）
│   ├── audit-workflow.md                       # DLC-vs-installed 审计工作流
│   └── *.json                                  # enchantments / potion_effects
├── tests/                                      # 295 个单元测试（改动相关模块即可，无需每次全量）
├── README.md                                    # 中文说明（本文件）
├── CONTRIBUTING.md                             # 贡献指南
├── CHANGELOG.md                                # 版本历史
└── LICENSE                                     # MIT 许可证
```

## 验证

```bash
python scripts/validate_quests.py /path/to/your/quests/
python scripts/validate_quests.py /path/to/your/quests/ --strict --json
python scripts/validate_quests.py /path/to/your/quests/ --fix
```

检查项（完整目录见 reference §15）：
- `E_PARSE`（JSON5 语法，含 file:line:col）
- `E_ID_FORMAT`、`E_ID_DUP`、`E_ID_MISSING`
- `E_DEP_MISSING` 带模糊"你是不是想说"提示
- `E_DEP_CYCLE`
- `E_ITEM_BARE_STRING`（可自动修复）
- `E_TYPE_SUFFIX`（可自动修复）
- `E_FILENAME_MISMATCH`（可自动修复）
- `E_INLINE_TEXT_MODERN`（警告）
- `E_LANG_MISSING_TITLE` / `E_LANG_ORPHAN`（警告）
- `E_COORD_DUP`（警告）
- `E_MANIFEST_HASH_MISMATCH` / `_DANGLING` / `_DUP_ID`

## 贡献

请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解问题报告、功能建议或 Pull Request 提交指南。

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。

## 致谢

- [FTB Team](https://github.com/FTBTeam) — FTB Quests 模组
- [marhali](https://github.com/marhali) — json5-java 库
- [Anthropic](https://www.anthropic.com/) — Claude Code
