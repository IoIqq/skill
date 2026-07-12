# Phase 4 审查员 B — 完备性审查

> **审查范围：** Cycle 8 Phase 2/3 新增规则 R42、R43、R44、R45、MP39、dependency_requirement 选项、Game Stages 闭环、教学快速推入
> **审查视角：** 完备性——边界情况是否遗漏？多包场景是否覆盖？规则交叉是否澄清？

---

## 需要补充边界说明

### R42 — Stage-Internal Item Reachability（阶段内物品可达性）

- **遗漏的边界情况 1：NBT 变体物品**
  - R42 的伪代码按 `leaf_node.id` 匹配阶段资源表，但未考虑 NBT 变体。例如：同一物品 ID 但带有不同附魔、耐久度或自定义数据的物品，其合成链可能完全不同。一个普通的 `minecraft:iron_sword` 在阶段内可达，但一个需要 `minecraft:iron_sword{Enchantments:[...]}` 的合成配方可能需要当前阶段未解锁的附魔台或铁砧操作。
  - **建议补充：** 在伪代码的叶子节点检查中增加注释："NBT-sensitive matching: 如果包使用了 NBT-dependent recipes（如附魔、自定义合成），叶子节点的比较应包含关键 NBT 字段而非仅 item ID。L1 降级时可忽略 NBT（标记为 `[unverified:nbt]`），L2 完整检查时应纳入。"

- **遗漏的边界情况 2：OreDict/Tag 匹配**
  - R42 按精确 item ID 构建合成树叶子节点，但现代 Minecraft（1.14+）使用 tag 系统（`#forge:ingots/copper`），多个物品可满足同一配方输入。如果任务要求提交 `thermal:copper_ingot`，但合成链中某一步的配方接受 `#forge:ingots/copper`（任何铜锭），则实际的叶子节点可达性范围比 R42 检查的更宽。
  - **建议补充：** 在 R42 描述中增加一段："Tag-aware reachability: 构建合成树时，如果配方的输入使用 tag（如 `#forge:ingots/iron`），则 tag 下的任意物品均视为可达。检查逻辑：`leaf_node ∈ tag_members(tag_id)` 而非 `leaf_node == exact_id`。L1 降级时不做 tag 展开（标记为 `[unverified:tag]`）。"

- **遗漏的边界情况 3：`consume_items: true` vs `consume_items: false`**
  - 当 `consume_items: false` 时，玩家只需获得物品一次即可反复提交，这意味着物品的可达性要求更低（不需要持续供应）。当 `consume_items: true`（默认行为）时，每次提交都消耗物品，需要确保物品的获取途径可重复。R42 当前未区分这两种模式。
  - **建议补充：** 在伪代码中增加条件分支："`consume_items: false` 的任务物品，其叶子节点可达性检查只需验证'至少存在一次性获取途径'；`consume_items: true` 的任务物品，需验证'存在可重复获取途径'（如可刷怪、可种植、可合成循环）。L1 层面无法区分，标记为 INFO 级人类审查项。"

- **遗漏的边界情况 4：怪物掉落物作为叶子节点**
  - R42 的描述中提到"如果叶子节点需要击杀怪物获得，该怪物是否在当前可达区域生成"，但伪代码中没有对应的检测逻辑。这是一个被识别但未被编码的边界情况。
  - **建议补充：** 在伪代码中增加第三个检查分支："`elif leaf_node.source == 'mob_drop': mob_spawn_dim = mob_dimension_map.get(leaf_node.mob_id); if mob_spawn_dim and mob_spawn_dim not in reachable_dims(Q): ERROR`。L1 降级时标记为 `[unverified:mob_drop]`。"

### R43 — Stage-Quest Causal Chain Acyclic（因果链无环）

- **遗漏的边界情况 1：Optional quest 形成的"伪环"**
  - R43 在扩展图中不区分 mandatory 和 optional quest。如果一个 optional quest Q_opt 的 command reward 激活了 Stage A，而 Stage A 解锁的物品 X 是 Q_opt 自身的依赖链中的需求——这形成了一个"伪环"。但因为 Q_opt 是可选的，跳过它不会导致死锁。R43 会将此标记为 ERROR，但实际影响可能只是"这个可选任务设计有问题，跳过的玩家不受影响"。
  - **建议补充：** 在 R43 的循环检测后增加严重度分级："如果循环路径上的所有 quest 均为 optional，降级为 WARNING（可选任务自环，不影响主线进度）；如果循环路径上存在 mandatory quest，保持 ERROR（主线死锁）。"

- **遗漏的边界情况 2：Stage 的隐式层级关系**
  - R43 的伪代码假设 Stage 之间的依赖完全由 quest command reward 显式激活。但 Game Stages 文档明确指出"阶段无默认层级关系，所有依赖手动配置"（Phase 3 draft D5/Game Stages 技术架构）。这意味着 Stage A 和 Stage B 之间可能存在 CraftTweaker 脚本中配置的隐式依赖（如 `GameStages.requireStage("bronze_age", "stone_age")`），这种依赖在 FTB Quests 配置中不可见。
  - **建议补充：** 在 R43 的数据依赖中增加："L2 数据应包含 Stage 间的显式依赖关系（来自 CraftTweaker/KubeJS 脚本）。如果未提供 Stage 依赖图，标记为 `[unverified:stage_deps]`。"

- **遗漏的边界情况 3：多 Stage 同时激活**
  - 一个 command reward 可以激活多个 Stage（如 `/gamestage add {p} stage_a` 后面跟 `/gamestage add {p} stage_b`），或者一个 quest 有多个 command reward。R43 的伪代码用 `cmd_reward.activates_stage(stage_name)` 处理单个 stage，但未显式处理一个 quest 激活多个 stage 的情况。
  - **建议补充：** 伪代码中的 `activates_stage` 应返回一个列表而非单个值。"for stage_name in cmd_reward.activated_stages(): add_edge(Q.id, stage_name)"——实际上伪代码的循环结构已隐含支持多个 command reward，但应明确标注"一个 quest 可激活多个 Stage"。

### R44 — Reward-Stage Matching（奖励-阶段匹配）

- **遗漏的边界情况 1：`reward_table`（随机奖励）的阶段匹配**
  - R44 的伪代码仅检查 `Q.item_rewards()`——即 `type: "item"` 的确定性物品奖励。但 Craftoria 的 Create 章节中 92.6% 的奖励是 `type: "random"`（引用 reward_table），E10 使用 `type: "loot"`（28 个 reward_tables），AoF3 的 reward_table 内甚至混合了 item + xp + xp_levels 条目。R44 对随机奖励完全失效——reward_table 中可能包含跨阶段物品。
  - **建议补充：** 在 R44 中增加 reward_table 阶段检查逻辑：
    ```
    for reward in Q.rewards:
        if reward.type in ("random", "loot", "choice"):
            table = load_reward_table(reward.table_id)
            for entry in table.rewards:
                if entry.type == "item":
                    entry_stage = stage_map.get(entry.item.id)
                    if entry_stage and entry_stage > quest_stage + 1:
                        WARNING: "reward_table {table.id} contains {entry.item.id}
                                  (stage {entry_stage}) exceeding quest stage {quest_stage} + 1"
    ```
    对于 `random` 和 `loot` 类型，由于玩家实际获得的物品是随机的，严重度应降一级（expert 包从 ERROR 降为 WARNING，kitchen-sink 包保持 INFO）。对于 `choice` 类型，玩家可以选择，保持原严重度。

- **遗漏的边界情况 2：XP / xp_levels / command 等非物品奖励的阶段匹配**
  - R44 只检查 `item_rewards()`，XP 奖励、command 奖励（如 `/gamestage add`）被完全忽略。虽然 XP 本身不存在"跨阶段"问题，但 command 奖励中的 gamestage 激活可能构成"奖励阶段的隐性跨级"——例如一个 stage 2 的 quest 通过 command reward 激活了 stage 5 的 stage，等同于奖励了 3 个阶段的进度跳跃。
  - **建议补充：** 增加 command reward 的阶段检查："for cmd in Q.command_rewards: if cmd.activates_stage(s): stage_gap = s - quest_stage; if stage_gap > 1: WARNING: 'command reward skips {stage_gap} stages'。" 此检查与 R43 的因果链检查互补——R43 检查环，R44 检查跳跃。

- **遗漏的边界情况 3：同一物品在不同阶段的重复出现**
  - 某些物品（如 `minecraft:iron_ingot`）可能在多个阶段都有任务要求。stage_map 应该映射到哪个阶段？如果映射到最低阶段，R44 可能对后期奖励误报；如果映射到最高阶段，可能对早期奖励误报。
  - **建议补充：** 在 R44 的 `stage_map` 定义中明确："物品的阶段取其**首次出现的最低阶段**（即该物品首次在游戏中可达的阶段）。如果一个物品在多个阶段都被使用，其 `stage_map` 值应为最低阶段。"

### R45 — Reward Guidance Bridging（奖励引导衔接）

- **遗漏的边界情况 1：非物品奖励的引导**
  - R45 的伪代码仅检查 `capstone.item_rewards()` 和 `entry_quests.item_tasks()` 的物品交集。如果 capstone 的奖励是纯 XP、xp_levels、command（如 gamestage 解锁）或 reward_table（随机奖励），`completion_rewards` 将为空集，R45 会跳过检查（因为 `bridge` 为空但 `entry_items` 非空时才 WARNING）。这意味着一个章节以"XP + gamestage 解锁"结尾、下一章以物品需求开始的情况会被标记为 WARNING，但实际上 gamestage 解锁可能正是下一章所需的"钥匙"。
  - **建议补充：** 扩展 `completion_rewards` 的定义，包含非物品奖励的引导价值：
    ```
    completion_rewards = set(r.item.id for r in capstone.item_rewards())
    # Add stage unlocks as virtual "bridge items"
    for cmd in capstone.command_rewards:
        if cmd.activates_stage(s):
            completion_rewards.add(f"stage:{s}")
    # Match against next chapter's stage requirements
    entry_stage_requirements = set(q.required_stage for q in entry_quests if q.required_stage)
    stage_bridge = completion_rewards.intersection(entry_stage_requirements)
    if stage_bridge:
        # Stage-based bridging is valid even without item bridging
        pass
    elif not bridge and entry_items:
        WARNING
    ```

- **遗漏的边界情况 2：跨章节依赖链（chapter N 的 capstone 不直接连接 chapter N+1 的 entry quest）**
  - R45 假设章节衔接是"capstone → next chapter entry quests"的直接桥接。但在很多包中，章节之间的过渡是通过跨章节依赖实现的——chapter N+1 的 entry quest 直接 `depends_on` chapter N 的某个非 capstone quest。此时 R45 的 `find_capstone_quest(C)` 可能找到了错误的桥接源。
  - **建议补充：** 增加跨章节依赖的识别："entry_quests 的判定应优先使用实际的跨章节依赖边：`entry_quests = [q for q in next_chapter.quests if any(d in C.quests for d in q.dependencies)]`。仅当无跨章节依赖时，退回到 order_index 顺序推断。"——实际上现有伪代码已包含此逻辑（`all(d in C.quests for d in q.dependencies)`），但应进一步区分"有显式跨章节依赖"和"无显式依赖，仅靠 order_index 推断"两种情况，对后者的 WARNING 降低可信度。

- **遗漏的边界情况 3：最后一个章节没有 next_chapter**
  - 伪代码中 `if not next_chapter: continue` 跳过了最后一个章节。但最后一个章节的 capstone 奖励如果完全无用（因为后面没有内容），这本身就是 AP6（Dead-End Reward）的章节级放大。
  - **建议补充：** 对最后一个章节增加终局奖励检查："if not next_chapter: check R13 (Capstone Reward Magnitude) — terminal chapter's capstone should have the richest reward in the pack."

### MP39 — Alternative-Reward Progression（替代奖励进度）

- **遗漏的边界情况：替代奖励系统与 FTB Quests 内置奖励的共存**
  - MP39 描述了"任务书承担教学引导职责，替代系统承担正反馈职责"的模式。但未讨论两种奖励系统共存时的冲突：如果 FTB Quests 同时有内置物品奖励，且替代系统（如货币商店）也在运行，玩家可能获得双重奖励，导致通胀。
  - **建议补充：** 增加一条设计约束："MP39 模式下，FTB Quests 内置奖励应**仅**包含引导性内容（教学工具、下一阶段起始材料、信息类奖励），不应包含可在替代奖励系统中购买的同类物品。否则会破坏替代系统的经济平衡。"

### dependency_requirement 完整选项

- **遗漏的边界情况：`min_required_dependencies` 与 `dependency_requirement` 的交互**
  - 文档正确描述了 `min_required_dependencies` 会覆盖 `dependency_requirement` 的语义。但未说明一个容易出错的边界：当 `min_required_dependencies` 设为大于 `dependencies` 列表长度的值时，该 quest 永远无法完成（AP3 变体）。
  - **建议补充：** 在 R20（Chapter Completion Testability）中增加检查："if Q.min_required_dependencies > len(Q.dependencies): ERROR: 'min_required_dependencies exceeds dependency count — quest unfinishable'。"

### 教学快速推入策略

- **遗漏的边界情况：教学推入与 `progression_mode: "linear"` 的交互**
  - 教学快速推入建议"前 3-5 个任务应包含明确的教学文本"。但如果 `progression_mode: "linear"`，这些教学任务本身就会成为门控——玩家必须完成教学才能继续。R41（Early-Game Flexible Mode）建议早期使用 `flexible` 模式来避免此问题，但两个规则之间没有显式的优先级声明。
  - **建议补充：** 在教学快速推入策略中增加与 R41 的交互说明："教学快速推入策略应优先与 R41（Early-Game Flexible Mode）配合使用——教学任务设为 `flexible` 或 `checkmark` 类型，确保教学信息可被阅读但不强制门控。"

---

## 需要新增规则

### R46 — Reward Table Cross-Stage Leakage（奖励表跨阶段泄漏检测）

- **为什么需要：** R44 检查确定性物品奖励的阶段匹配，但 reward_table 是一个独立的实体，可以被多个 quest 引用。一个 reward_table 可能在早期章节被引用，但其中包含后期阶段的物品——这是 R44 无法捕获的，因为 R44 以 quest 为粒度检查，而 reward_table 是独立于 quest 的共享资源。Craftoria 的 19 个 reward tables、E10 的 28 个 reward tables 都存在这种风险。
- **建议规则内容：**
  ```
  for each reward_table T:
      table_stage = determine_table_stage(T)  # 基于引用该表的 quest 所在阶段的众数
      for entry in T.rewards:
          if entry.type == "item":
              entry_stage = stage_map.get(entry.item.id)
              if entry_stage and entry_stage > table_stage + 1:
                  WARNING: "reward_table {T.id} (stage ~{table_stage}) contains
                            {entry.item.id} (stage {entry_stage})"
  ```
  严重度：expert 包 WARNING，kitchen-sink 包 INFO。
  此规则在 Step 5 执行（需要全量 reward_table 数据）。

### R47 — Empty/Skeleton Chapter Detection（空章节/骨架章节检测）

- **为什么需要：** Cycle 8 的新规则（R42-R45）都以"章节有 quest"为前提。但在实际包开发中，可能出现：(a) 空章节（chapter 中无任何 quest，可能为占位符）；(b) 骨架章节（只有 1 个 quest 的章节，可能是未完成的草稿）。这两种情况会导致 R45 的 `find_capstone_quest` 返回 None 并跳过检查，R42 的阶段资源表构建缺少数据。
- **建议规则内容：**
  ```
  for each chapter C:
      quest_count = len(C.quests)
      if quest_count == 0:
          WARNING: "Chapter {C.name} has zero quests — possible placeholder or abandoned draft"
      elif quest_count == 1:
          INFO: "Chapter {C.name} has only 1 quest — verify this is intentional"
  ```
  Step 5 执行，P3 (INFO/WARNING)。

### R48 — Stage Definition Consistency（阶段定义一致性检测）

- **为什么需要：** Cycle 8 的多条规则（R42、R43、R44）都依赖"阶段"概念，但阶段可能来自两个独立来源：(a) FTB Quests 的 chapter group / order_index 定义；(b) Game Stages 模组的 stage 注册。如果两者不一致（如 FTB Quests 认为章节 3 是 "Electric Age" 但 Game Stages 中没有注册 `electric_age` stage），R43 的扩展图会缺少边，R44 的阶段映射会失败。
- **建议规则内容：**
  ```
  ftb_stages = set(extract_stages_from_chapter_groups(quest_book))
  game_stages = set(load_registered_stages(gamestages_config))

  missing_in_gs = ftb_stages - game_stages
  missing_in_ftb = game_stages - ftb_stages

  for s in missing_in_gs:
      WARNING: "Stage '{s}' defined in quest book but not registered in Game Stages"
  for s in missing_in_ftb:
      INFO: "Stage '{s}' registered in Game Stages but no corresponding chapter group"
  ```
  Step 5 执行，P2 (WARNING)。需要 L2 数据（Game Stages 配置文件）。

---

## 规则交叉需要澄清

### R42 vs R1/R4

- **冲突/重叠点：** R1 检查"物品本身是否来自可达维度"，R4 检查"物品是否属于正确的阶段"，R42 检查"物品的合成链中每个原材料是否在当前阶段可达"。三者存在层级包含关系：R1 ⊂ R4 ⊂ R42（R42 是最细粒度的检查）。但三条规则可能在同一物品上同时触发，产生重复报告。
- **建议澄清：** 在 R42 的描述中增加执行优先级说明："R1、R4、R42 按递进粒度执行。如果 R1 已标记某物品维度不可达，R42 跳过该物品的合成链检查（避免无意义的级联报告）。R4 和 R42 可能同时触发但关注点不同：R4 报告'物品不属于此阶段'，R42 报告'合成链中的原材料不可达'——前者是分类错误，后者是供应链断裂。"

### R44 vs R10-R12

- **冲突/重叠点：** R10（Reward-to-Dependent Bridge）检查 quest 级别的奖励-依赖桥接，R12（Reward Value Progression）检查奖励价值随深度递增，R44 检查奖励物品的阶段匹配。三者的检查对象都是"奖励物品"，但视角不同。潜在的冲突场景：R10 认为"奖励物品 X 桥接到了依赖任务"（合格），但 R44 认为"物品 X 超出了当前阶段 +1"（不合格）——同一奖励在桥接维度合格但在阶段维度不合格。
- **建议澄清：** 增加分工说明："R10 检查奖励的**连接性**（是否桥接到下游），R12 检查奖励的**价值曲线**（是否随深度递增），R44 检查奖励的**阶段合规性**（是否越级）。三条规则独立运行，同一奖励可能通过 R10 但违反 R44——这意味着奖励桥接方向正确但物品等级过高。R44 的 expert 包 ERROR 应优先于 R10 的 INFO 报告。"

### R43 vs R5-R8

- **冲突/重叠点：** R5 检测 quest 依赖图中的循环，R43 检测 Stage-Quest 交叉图中的循环。两者检测的是不同图结构中的环，但可能在同一个包中同时触发。关键问题是：如果 R5 检测到了 quest 级别的环，是否还需要运行 R43？反之亦然？
- **建议澄清：** 增加执行顺序说明："R5 先于 R43 执行。R5 检测的 quest 级别循环是直接的配置错误（`dependencies` 字段形成环），应优先修复。R43 检测的 Stage-Quest 交叉循环需要 R5 无环作为前提——如果 quest 图本身有环，R43 的扩展图也会有环，导致 R43 的报告是 R5 的级联结果而非独立问题。因此：R5 有 ERROR 时，R43 跳过执行或将其环报告标记为 `[cascaded from R5]`。" 此外，R7（Optional-Gate-Mandatory）与 R43 的 optional quest 伪环问题相关——R7 已检查 mandatory quest 是否依赖 optional quest，R43 的 optional 伪环降级（见上文建议）与 R7 的精神一致。

### R45 vs R10

- **冲突/重叠点：** R10 在 quest 级别检查奖励-依赖桥接，R45 在 chapter 级别检查奖励引导衔接。如果 R10 已经确认 chapter N 的每个 quest 奖励都桥接到了下游 quest（包括 chapter N+1 的 quest），那么 R45 的检查是冗余的。但如果 chapter 之间没有显式依赖边（仅靠 order_index 推断顺序），R10 无法执行跨章节检查，此时 R45 是必要的补充。
- **建议澄清：** 在 R45 中增加条件逻辑："如果 chapter N 和 chapter N+1 之间存在显式跨章节依赖（R22 已验证），R45 的检查与 R10 存在重叠，降低 R45 WARNING 为 INFO（`[covered by R10]`）。如果两个章节之间无显式依赖，R45 保持 WARNING。"

---

## 完备性良好（无需补充）

### Game Stages 闭环集成（mod-item-reachability / mod-reward-design）

- **理由：** Phase 2/3 的补充内容充分覆盖了 Game Stages 的核心集成模式：(a) Item Stages / Recipe Stages / Dimension Stages 三层锁定已被描述；(b) "任务完成 → Stage 激活 → 解锁"闭环已被 R43 保护；(c) "弱锁"策略已被识别并标记为低可编码性的人类审查项；(d) 1.12.2 与现代版本的工具链差异已被记录。多维联动（时间/空间/资源/社会四维模型）的描述也足够全面。唯一不足是 Game Stages 配置层面的验证需要 L2 数据，这已在 R43 的数据依赖中标注。

### dependency_requirement 完整选项参考（mod-dependency-graph）

- **理由：** 四个标准选项（`all_completed`、`all_started`、`one_completed`、`one_started`）加上 `min_required_dependencies` 数值控制已完整覆盖 FTB Quests 的依赖配置功能。配套配置项（`optional`、`hide`、`hide_details_until_startable`、`tasks_ignore_dependencies`、`progression_mode`、`require_sequential_tasks`）也已列举。Real case 覆盖了 Monifactory、Create: Delight、ATM-10 三个代表性包的不同使用模式。上文建议的 `min_required_dependencies > len(dependencies)` 边界检查是唯一遗漏，已通过新增 R47 相关检查补充。

### MP39 — Alternative-Reward Progression 核心定义

- **理由：** MP39 的核心概念（替代奖励系统承担正反馈、任务书承担引导）基于 4 个实际包（TerraFirma Rescue、GTNH、RAD2、E2E）的交叉验证，加上 ATM-10 的反面案例。Phase 2 的 V1 验证已确认"纯零奖励几乎不存在，成功的硬核包都使用替代系统"。上文建议的"替代系统与内置奖励共存"冲突是一个实践层面的补充需求，MP39 的核心模式定义本身是完备的。

### 教学快速推入策略（mod-teaching-pacing）

- **理由：** 该策略的三层框架（R41 结构层 + 教学推入内容层 + R14 顺序层）已形成完整的教学保障体系。Monifactory #2359 的失败案例提供了反面验证。上文建议的与 R41 交互说明是一个优化项，策略本身的原则描述是完备的。FTB Quests 多种任务类型的教学应用（复选框、文本面板、维度任务）已被覆盖。

### 阶段划分的四维模型（mod-dependency-graph）

- **理由：** 四维模型（时间、空间、资源、社会）从多个独立来源交叉验证，覆盖了从简单时间维度到复杂多维联动的全部场景。三段式生命周期（早期钩住、中期延长、后期复用）与 R41（早期灵活模式）和 R19（瓶颈间距）形成呼应。阶段数建议（3-7 个）基于多个成功包的统计。"上阶段顶级 = 下阶段入门"的过渡原则已被识别为中等可编码性的人类审查项，这是合理的分类。

---

## 审查总结

| 类别 | 数量 | 说明 |
|------|------|------|
| 需要补充边界说明 | 14 条 | R42(4) + R43(3) + R44(3) + R45(3) + MP39(1) |
| 需要新增规则 | 3 条 | R46(奖励表跨阶段) + R47(空章节检测) + R48(阶段定义一致性) |
| 规则交叉需要澄清 | 4 对 | R42-R1/R4 + R44-R10/R12 + R43-R5/R8 + R45-R10 |
| 完备性良好 | 5 项 | Game Stages 闭环 + dependency_requirement + MP39 核心 + 教学推入 + 四维模型 |

**最高优先级修补项：**
1. **R44 的 reward_table 检查**——Craftoria 92.6% 的 Create 章节奖励是 random 类型，R44 对最大比例的奖励类型完全失效
2. **R45 的非物品奖励引导**——纯 XP/gamestage 结尾被误报为"衔接断裂"，忽略了 stage 解锁本身就是有效引导
3. **R43 的 optional quest 伪环降级**——避免对不影响主线的可选循环误报 ERROR
