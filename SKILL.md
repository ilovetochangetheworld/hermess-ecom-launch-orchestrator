---
name: solo-ecom-pilot
description: 用于电商商品启动工作流：从选品调研、定价毛利、内容生成、图片 Prompt 与真实素材准备、发布准备、客服 FAQ、合规检查、数据诊断到复盘回流。Agent 必须在每一步主动说明当前正在做什么。
---

# Solo Ecom Pilot

这是「从 0 开张：你的 AI 电商合伙人」的统一工作流 Skill。

它把分散的电商 Prompt、脚本和交付模板收敛成一个可交互、可确认、可导出的经营流程。Agent 使用这个 Skill 时，应像一个 AI 电商合伙人一样推进业务，而不是只被动回答问题。

## 核心定位

- 使用业务语言，不使用内部工程语言向用户解释。
- 发布相关能力只做「发布准备」：整理标题、正文、话题、图片顺序、合规提醒和发布前检查项。实际发布动作应由用户或运营人员结合账号状态、平台规则和业务审批要求完成。
- 商品图片优先来自真实来源：用户实拍、供应商图、商品截图、详情页图片或平台素材。图片阶段默认只输出图片 Prompt、拍摄要求、素材顺序和标注建议；除非用户明确要求，不调用生图 API，也不把 AI 概念图描述成真实上架图。
- Agent 必须在每个阶段主动说明：现在做什么、为什么重要、需要用户提供什么、会产出什么。

## Token 控制规则

- 默认每个阶段只输出简洁结果：一张进度说明卡、最多 5 条关键发现、阶段确认选项。
- 不要在每个阶段反复粘贴完整 JSON。完整 JSON 保留在内部，只有用户要求导出或生成「商品经营启动包」时再输出或写入文件。
- 只在当前阶段需要时读取 reference 文件，不要一开始加载所有参考资料。
- 不重复已经确认的商品事实；除非字段发生变化，否则用「已确认产品画像」指代。
- 客服 FAQ 在对话中默认展示 Top 8；导出客服包时再扩展到 20 条。
- 评论/数据复盘在对话中只总结 Top 3 痛点，完整分析写入 envelope/export。
- 图片准备阶段默认输出 3 条简洁中文 Prompt 和图片顺序；除非用户明确要求，不生成图片。

## 触发关键词

- 选品类：选品、爆款、蓝海、市场分析、竞品分析、卖什么
- 定价类：定价、利润计算、毛利率、成本核算、怎么定价
- 内容类：商品标题、详情页、卖点提炼、种草文案、短视频脚本、直播话术
- 图片类：产品图、商品图片、封面图、功能图、场景图、供应商图、实拍图
- 发布类：小红书发布、笔记发布、发布素材、上传图片
- 客服类：客服话术、售后处理、退换货、差评回复、客户投诉
- 合规类：广告法、违禁词、极限词、虚假宣传、七日无理由
- 数据类：转化率、店铺诊断、运营日报、ROI、DSR、评论复盘
- 编排类：全链路、闭环流程、从0开张、AI电商合伙人

## 沟通契约

每个阶段开始前，以及任何外部动作开始前，必须输出：

```text
Now doing: ...
Why it matters: ...
Need from you: ...
Expected output: ...
```

规则：

- 不要静默跑完整个流程。
- 每次只问一个最关键的缺失输入。
- 信息缺失时可以继续，但必须标注假设和信心等级。
- 输出要让业务用户能立即判断和行动。
- 默认按阶段交互，不默认一口气跑完整流程。
- 每个阶段结束后暂停，让用户选择：继续下一阶段、修改当前阶段、停止并导出当前资产。
- 除非用户明确说「连续跑完」或「不用确认」，否则不要自动进入下一阶段。
- 阶段确认时要包含：阶段摘要、已产出资产、未解决假设、推荐下一步。

## 统一工作流

### 1. MarketIntel：智能选品

目的：判断这个商品是否值得继续推进。

能力：

- 提供三个启动模板：便携小风扇、40oz 杯子、透明 MagSafe 手机壳。
- 接收用户自己的商品名、链接、图片、供应商页面或粗略描述。
- 采集商品事实，不编造缺失信息。
- 从以下维度评估市场机会：
  - 市场容量
  - 竞争强度
  - 利润空间
  - 季节性
  - 供应链门槛
  - 个人卖家适配度
- 接收后续评论和数据复盘产生的 loopback seed，用于下一轮选品。

运行本阶段前读取 `references/product-research-flow.md`。

必须产出：

- `decision`
- `product_profile`
- `risk_checklist`
- `confidence`

### 2. PricingEngine：定价与毛利

目的：在生成内容和发布准备前，先确认商品是否具备经营可行性。

能力：

- 支持国内平台定价假设：淘宝、天猫、拼多多、抖音、小红书、京东。
- 使用平台/类目扣点逻辑进行毛利估算。
- 合约中支持 Amazon/FBA 成本字段；如需精确 FBA 计算，应后续补充真实 `profit_calculator.py` 源文件。
- 自动检查价格合规风险：
  - 虚构原价
  - 虚假折扣
  - 价格歧视
  - 无依据的限量/库存话术

必须产出：

- 保守价 / 建议价 / 进取价
- 成本结构
- 毛利估算
- 合规提醒

### 3. ContentFactory：内容工厂

目的：把产品定位转成可发布、可复用的内容资产。

能力：

- 小红书笔记：测评型、生活型。
- 商品标题和卖点提炼。
- 基于 FAB 逻辑生成详情页大纲。
- 用户需要时生成短视频脚本或直播话术。
- 用户需要时做多平台内容适配。
- 每次内容生成后都必须做合规检查。

规则：

- 文案必须绑定 `product_profile`，不能写成泛品类模板。
- 在事实可用时，至少提到 3 个具体商品事实。
- 避免极限词、无依据功效承诺和无法证明的安全/认证宣称。

必须产出：

- 标题
- 正文
- 话题标签
- 内容质量检查
- 合规检查结果

### 4. ProductImagePrep：图片 Prompt 与真实素材准备

目的：默认不消耗生图额度，先准备可信的商品图片要求和素材结构。

能力：

- 把真实商品图片组织成：
  - 封面图
  - 功能/细节图
  - 场景/使用图
- 如果真实图片缺失，或用户需要创意 brief，生成三条中文图片 Prompt：
  - 封面图 Prompt
  - 功能/细节图 Prompt
  - 场景/使用图 Prompt
- 生成拍摄清单，供运营或设计执行。
- 建议图片标注点和图片顺序。
- 除非用户明确要求，不调用图片生成工具或外部图片 API。
- 如果用户后续要求生成图片，AI 图片只能标注为概念图或素材候选，不得表述为真实上架图。
- 如果用户根据 Prompt 生成、拍摄或上传图片，接收图片路径或文件，并更新 `image_pack.source_path_or_url`、`source_type`、`image_status`。
- 最终「商品经营启动包（HTML交付页）」中的「商品图片与 Prompt」区块必须展示每个图片角色、已提交图片预览、图片来源/状态，以及用于生成或指导该图片的中文 Prompt。

Prompt 规则：

- 图片 Prompt 默认必须使用中文；只有用户明确要求英文时才输出英文。
- 每条图片 Prompt 必须包含主体：商品名、可见外观、材质/颜色、包装或数量。
- 每条图片 Prompt 必须包含商品背景：目标用户、使用语境、核心卖点、这张图要回答的买家疑虑。
- 功能图 Prompt 必须明确商品主体和要演示的功能；不要只写「发声演示 + 软胶材质」这种没有主体的片段。
- 封面图 Prompt 必须定义构图、背景、光线、风格、标题安全区，并避免编造功能。
- 场景图 Prompt 必须定义用户、场景、动作、商品位置；涉及儿童时必须说明隐私约束和真实感要求。
- 未核验事实必须标注「需要确认」或直接避开。不要静默编造认证、材质、尺寸、续航、年龄段或安全宣称。

必须产出：

- `image_pack`
- 缺图清单
- 图片顺序
- 3 条中文图片 Prompt
- 拍摄清单 / 运营 brief

### 5. PublishingReadiness：发布准备

目的：整理平台提交前所需的全部素材和检查项。

政策：

- 除非用户明确提供已发布链接，否则不要声称 Agent 已经发布成功。
- 准备发布素材包：文案、话题、图片顺序、合规提醒、发布前检查清单。
- 最终发布动作属于用户或运营人员，应结合账号状态、平台规则和业务审批要求执行。

必须产出：

- 标题
- 正文
- 话题标签
- 图片顺序
- 发布前检查清单
- 账号/平台准备状态说明

### 6. ServiceBot：智能客服

目的：展示商品发布后，Agent 如何承接买家问题。

能力：

- 中文 FAQ。
- 有跨境语境时提供英文 FAQ。
- 买家意图识别：
  - price_sensitive
  - quality_concern
  - ready_to_buy
  - after_sales
  - comparison
- 人工升级标记。
- 从重复问题中提取详情页优化信号。
- 售后决策树：
  - 质量问题
  - 物流问题
  - 七日无理由
  - 投诉
  - 差评

必须产出：

- FAQ 列表
- 实时回复样例
- 买家意图
- 是否升级人工
- 页面/FAQ 优化建议

### 7. AnalyticsDashboard：评论复盘与数据诊断

目的：闭环复盘，把真实反馈带回下一轮选品。

能力：

- 评论情绪和痛点提取。
- 用户提供运营数据时，做经营健康诊断：
  - 转化率
  - 客单价
  - 退款率
  - 好评率
  - ROI
  - DSR
  - 复购率
  - 客服响应问题
- 回流触发条件：
  - refund_rate > 10%
  - positive_review_rate < 90%
  - ROI < 1.5
  - DSR < 4.5
  - 多个条件同时成立时，必须生成 `next_research_seed`

必须产出：

- Top concerns
- 正向信号
- 详情页优化建议
- FAQ 优化建议
- 下一轮选品种子

### 8. AssetPackRenderer：商品经营启动包

目的：把 workflow envelope 转成可分享、可打开、可交付的商品经营启动包。

能力：

- 从完整 workflow envelope 渲染 HTML 交付页。
- 商品图片包含在交付物中时，优先生成可移交的 ZIP 包。ZIP 包必须使用相对路径，保证 HTML 下载或转发后仍能正确显示图片。
- 推荐包结构：
  - `{slug}_asset_pack.html`
  - `assets/images/{slug}_cover.png`
  - `assets/images/{slug}_feature.png`
  - `assets/images/{slug}_lifestyle.png`
  - `assets/data/workflow_envelope.json`
  - `assets/data/content_pack.json`
  - `assets/data/customer_service_pack.json`
  - `assets/data/publish_readiness.json`
  - `assets/data/image_prompt_pack.json`
- HTML 页面需按业务顺序组织：选品结论、产品画像、定价、内容、图片准备、发布准备、FAQ、复盘回流。
- 交付文件清单必须使用业务用户能理解的名称、相对路径和可用的 `MEDIA:` 引用。
- 「商品图片与 Prompt」区块必须专业展示：封面图/功能图/场景图卡片、已提交图片预览、图片来源/状态、中文 Prompt、图片用途。
- 如果图片尚未提交，显示清晰占位和中文 Prompt，方便用户继续生成或拍摄。
- 最终共享 HTML 不得依赖 Hermess 运行环境绝对路径，例如 `/home/agentuser/...`。本地可用图片必须复制进 `assets/images/`，并把 HTML 和 `image_pack` 路径改写为相对路径。
- 「完整流程数据包（workflow envelope JSON）」是机器可读的事实源，HTML 是业务用户阅读视图。

必须产出：

- `workflow_envelope`：完整流程数据包
- `asset_pack_html_path`：商品经营启动包（HTML交付页）路径，生成时提供
- `asset_pack_zip_path`：商品经营启动包（可分享压缩包）路径，生成时提供
- HTML 内的交付文件清单

## 默认运行顺序

标准流程按以下顺序推进。默认每完成一个阶段就总结并等待用户确认。

1. 选择商品。
2. 选品分析与 go/no-go 判断。
3. 定价与毛利测算。
4. 小红书内容生成。
5. 图片 Prompt 与真实商品素材准备。
6. 发布准备包。
7. 客服 Q&A。
8. 评论/数据复盘与 loopback。
9. 用户需要可分享交付物时，生成「商品经营启动包（HTML交付页）」；若包含商品图片，优先生成「商品经营启动包（ZIP交付包）」。

## 阶段确认格式

每个阶段结束时输出：

```text
Stage complete: ...
Produced: ...
Open assumptions: ...
Recommended next action: ...
Please choose:
1. Continue to {next_stage}
2. Revise this stage
3. Stop and export current assets
```

如果用户选择 1，继续下一阶段。  
如果用户选择 2，只询问最小必要修改。  
如果用户选择 3，生成当前「完整流程数据包（workflow envelope JSON）」；条件允许时，同时生成「商品经营启动包（ZIP交付包，内含 HTML 交付页、图片和 JSON 数据）」。

## 共享字段契约

使用 `references/contracts.md` 约束以下字段：

- `stage_progress`
- `product_profile`
- `pricing_pack`
- `content_pack`
- `image_pack`
- `publish_result`
- `customer_service_pack`
- `review_insight_pack`
- `next_research_seed`
- `asset_pack_html_path`
- `asset_pack_zip_path`

使用 `scripts/validate_envelope.py` 校验 workflow envelope。

使用 `scripts/render_asset_pack.py` 把 workflow envelope 渲染成可分享的商品经营启动包。图片需要和 HTML 保持关联时，优先使用 `--bundle-dir` 和 `--zip`。

## 参考文件

- `references/product-research-flow.md`：选品阶段详细交互流程。
- `references/contracts.md`：共享数据结构。
- `references/quality-gates.md`：各阶段质量门。
- `references/demo-runbook.md`：培训或工作坊讲解参考。
- `references/orchestration-prompts.md`：可复用启动 Prompt。
- `references/real-product-sources.md`：三个商品模板的来源假设。

## 脚本

- `scripts/main.py`：统一确定性辅助脚本，包含选品、定价、内容、图片准备、发布准备、客服、数据诊断和编排器。
- `scripts/validate_envelope.py`：校验 workflow envelope。
- `scripts/render_asset_pack.py`：把 workflow envelope 渲染成用户可读的商品经营启动包（HTML交付页或 ZIP交付包）。
- `scripts/xhs_publisher.py`：发布准备包辅助脚本。
- `scripts/product_image_preparer.py`：商品图片角色和拍摄清单辅助脚本。

## 示例模板

以下仅作为启动示例：

- `assets/samples/portable-fan-envelope.json`
- `assets/samples/insulated-tumbler-envelope.json`
- `assets/samples/clear-magsafe-case-envelope.json`

如果用户提供真实商品信息，优先使用用户数据，不使用示例模板覆盖。

## 最终回复格式

流程结束时总结：

- 选择了什么商品
- 做出了什么经营判断
- 生成了哪些资产
- 发布准备到什么程度
- 客服 Bot 能回答哪些问题
- 下一轮选品应吸收什么反馈
- 如果生成了「商品经营启动包（HTML交付页或 ZIP交付包）」，说明保存位置
