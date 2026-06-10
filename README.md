# 从 0 开张：你的 AI 电商合伙人

这是一个面向独立卖家、运营团队和电商提效场景的 Hermess Agent skill。它把一个商品从选品判断推进到定价、内容、商品图片准备、发布准备、客服 FAQ 和评论复盘，帮助用户把零散任务组织成一条可重复执行的电商工作流。

## 适合谁用

- 想从 0 开始验证一个商品是否值得卖的个人或团队。
- 需要快速产出商品上架前经营素材的电商运营。
- 希望把选品、内容、客服和复盘流程标准化的业务团队。
- 负责培训、售前、客户成功或业务方案展示的团队。

## 核心能力

1. 选品竞品分析：判断商品是否值得继续，输出目标人群、核心卖点、风险清单。
2. 定价和毛利测算：根据采购价、平台扣点、营销预留给出价格区间。
3. 种草文案生成：生成绑定商品具体参数的小红书笔记、标题和话题标签。
4. 商品图片准备：基于真实商品图、供应商图或商品截图，整理封面图、功能图、场景图。
5. 发布准备包：整理标题、正文、话题、图片顺序和发布前确认清单。
6. 智能客服 FAQ：生成常见问题、买家意图识别和回复样例。
7. 评论复盘闭环：把评论痛点和运营数据回流成下一轮选品建议。
8. HTML 资产包：把完整 workflow envelope 渲染成可打开、可分享、可复制的单页 HTML。

发布相关能力聚焦于“发布前准备”：Agent 负责整理发布所需素材和检查项；实际发布动作应由使用者结合账号状态、平台规则和业务审批流程完成。

## 推荐安装方式

让 Hermess Agent 读取这个公开仓库：

```text
https://github.com/ilovetochangetheworld/hermess-ecom-launch-orchestrator
```

如果你的 Agent 支持从 GitHub 同步 skill，可以直接把上面的仓库地址作为 skill 来源。

如果需要手动安装，把仓库内容放到你的 Hermess skill 目录，例如：

```text
~/.hermes/skills/ecommerce/solo-ecom-pilot/
```

目录中必须保留：

```text
SKILL.md
agents/openai.yaml
references/
scripts/
assets/
```

## 快速开始 Prompt

把下面这段发给 Hermess Agent：

```text
请读取并使用这个 skill：
https://github.com/ilovetochangetheworld/hermess-ecom-launch-orchestrator

请运行“从 0 开张：你的 AI 电商合伙人”流程。

你必须在每个阶段开始前主动输出：
Now doing:
Why it matters:
Need from you:
Expected output:

请先让我选择一个商品：
A. 便携小风扇
B. 40oz 杯子
C. 透明 MagSafe 手机壳
D. 我自己的商品

选择后，请按以下顺序推进：
1. 选品竞品分析
2. 定价和毛利测算
3. 种草文案
4. 商品图片准备
5. 发布准备包
6. 客服 FAQ 和实时问答
7. 评论复盘和下一轮选品建议

注意：
- 发布环节输出发布准备包，包括标题、正文、话题、图片顺序和发布前确认清单。
- 商品图片优先使用真实商品图、供应商图、商品截图或用户提供的实拍图。
- 所有文案必须绑定商品具体参数，不要写成任何同类商品都能套用的泛泛内容。
```

## 标准工作流

| 阶段 | 输入 | 输出 |
| --- | --- | --- |
| 选品判断 | 商品名、链接、图片、供应价或用户描述 | 产品画像、go/no-go、风险清单 |
| 定价毛利 | 采购价、平台、预期毛利、营销预留 | 价格区间、成本结构、合规提醒 |
| 内容生成 | 产品画像、目标人群、卖点 | 标题、正文、话题标签、内容质检 |
| 图片准备 | 真实商品图、供应商图、商品截图 | 封面/功能/场景图片顺序和补图清单 |
| 发布准备 | 内容包、图片包、平台要求 | 发布准备包和发布前确认清单 |
| 客服问答 | 产品信息、售后政策、高频问题 | FAQ、回复样例、升级人工判断 |
| 复盘回流 | 评论、咨询记录、运营指标 | 痛点分析、迭代建议、下一轮选品种子 |

## 输出结构

完整流程会尽量收敛成一个 workflow envelope，核心字段包括：

```text
workflow_meta
stage_progress
product_profile
pricing_pack
content_pack
image_pack
publish_result
customer_service_pack
review_insight_pack
next_research_seed
asset_pack_html_path
```

字段定义见 `references/contracts.md`。

## 试运行脚本

仓库里带了几个辅助脚本，方便验证 skill 产物结构。

生成一个样例 workflow envelope：

```bash
python3 scripts/main.py portable_fan
```

可选模板：

```text
portable_fan
insulated_tumbler
clear_magsafe_case
```

校验样例 envelope：

```bash
python3 scripts/validate_envelope.py assets/sample-envelope.json
```

准备商品图片角色：

```bash
python3 scripts/product_image_preparer.py cover.jpg feature.jpg lifestyle.jpg
```

生成发布准备包：

```bash
python3 scripts/xhs_publisher.py \
  --title "桌面小风扇真香了" \
  --body "这里放正文" \
  --hashtags "#桌面好物,#夏日好物" \
  --images cover.jpg feature.jpg lifestyle.jpg
```

生成 HTML 资产包：

```bash
python3 scripts/render_asset_pack.py \
  assets/sample-envelope.json \
  --out outputs/sample-asset-pack.html
```

## 目录说明

```text
.
├── SKILL.md                      # Agent 使用的核心说明
├── agents/openai.yaml            # skill 展示元信息
├── references/
│   ├── contracts.md              # workflow envelope 字段结构
│   ├── product-research-flow.md  # 选品阶段交互流程
│   ├── orchestration-prompts.md  # 可复用启动 Prompt
│   ├── demo-runbook.md           # 培训或工作坊使用的讲解参考
│   ├── quality-gates.md          # 各阶段质量检查
│   └── real-product-sources.md   # 三个商品模板来源假设
├── scripts/
│   ├── main.py                   # 统一流程样例生成器
│   ├── validate_envelope.py      # envelope 校验器
│   ├── render_asset_pack.py      # HTML 资产包渲染器
│   ├── product_image_preparer.py # 商品图片角色整理
│   └── xhs_publisher.py          # 发布准备包生成器
└── assets/
    ├── sample-envelope.json
    └── samples/                  # 三个商品样例
```

## 使用原则

- 先选品，再写文案。
- 先算毛利，再谈发布。
- 商品图优先使用真实来源，不把 AI 概念图当成上架图。
- 发布准备包用于辅助上架前检查，实际发布应符合平台规则和业务审批要求。
- Agent 每一步都要主动告诉用户：现在做什么、为什么重要、需要什么、会产出什么。
