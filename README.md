# 从 0 开张：你的 AI 电商合伙人

这是一个面向提效工坊演示的 Hermess Agent 电商 skill。它把一个小商品从选品判断推进到定价、文案、商品图片准备、发布素材包、客服 FAQ 和评论复盘，帮助用户看到 AI 如何像一个轻量电商团队一样连续工作。

## 适合谁用

- 想做电商副业，但不知道从哪里开始的人。
- 需要在客户现场演示 AI 提效闭环的团队。
- 想把一个商品快速整理成可发布、可客服、可复盘素材包的运营人员。

## 这个 skill 能做什么

1. 选品竞品分析：判断商品是否值得继续，输出目标人群、核心卖点、风险清单。
2. 定价和毛利测算：根据采购价、平台扣点、营销预留给出价格区间。
3. 种草文案生成：生成绑定商品具体参数的小红书笔记、标题和话题标签。
4. 商品图片准备：基于真实商品图、供应商图或现场实拍图，整理封面图、功能图、场景图。
5. 发布素材包：输出标题、正文、话题、图片顺序和人工发布清单。
6. 智能客服 FAQ：生成常见问题、买家意图识别和回复样例。
7. 评论复盘闭环：把评论痛点和运营数据回流成下一轮选品建议。

当前版本不演示小红书直接发布。Agent 只生成发布素材包和人工操作清单，是否发布由操作者按平台规则确认。

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

## 一键启动 Prompt

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

请先让我选择一个演示商品：
A. 便携小风扇
B. 40oz 杯子
C. 透明 MagSafe 手机壳
D. 我自己的商品

选择后，请按以下顺序推进：
1. 选品竞品分析
2. 定价和毛利测算
3. 种草文案
4. 商品图片准备
5. 发布素材包
6. 客服 FAQ 和实时问答
7. 评论复盘和下一轮选品建议

注意：
- 不要演示直接发布，只输出发布素材包和人工发布清单。
- 商品图片优先使用真实商品图、供应商图或现场实拍图。
- 所有文案必须绑定商品具体参数，不要写成任何同类商品都能套用的泛泛内容。
```

## 现场演示怎么跑

建议 10 分钟演示节奏：

| 时间 | 动作 | 观众看到的结果 |
| --- | --- | --- |
| 0:00-0:45 | 选择商品 | 商品候选 |
| 0:45-2:30 | 选品判断 | 产品画像、go/no-go、风险清单 |
| 2:30-3:30 | 定价毛利 | 价格区间、成本结构、合规提醒 |
| 3:30-5:00 | 生成文案 | 小红书标题、正文、话题标签 |
| 5:00-6:15 | 商品图片准备 | 封面图、功能图、场景图顺序和补图清单 |
| 6:15-7:15 | 发布素材包 | 标题、正文、图片顺序、人工发布清单 |
| 7:15-8:30 | 客服问答 | FAQ、回复样例、升级人工判断 |
| 8:30-10:00 | 评论复盘 | 痛点分析、下一轮选品种子 |

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

生成发布素材包：

```bash
python3 scripts/xhs_publisher.py \
  --title "桌面小风扇真香了" \
  --body "这里放正文" \
  --hashtags "#桌面好物,#夏日好物" \
  --images cover.jpg feature.jpg lifestyle.jpg
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
│   ├── demo-runbook.md           # 现场演示讲法
│   ├── quality-gates.md          # 各阶段质量检查
│   └── real-product-sources.md   # 三个商品模板来源假设
├── scripts/
│   ├── main.py                   # 统一流程样例生成器
│   ├── validate_envelope.py      # envelope 校验器
│   ├── product_image_preparer.py # 商品图片角色整理
│   └── xhs_publisher.py          # 发布素材包生成器
└── assets/
    ├── sample-envelope.json
    └── samples/                  # 三个商品样例
```

## 关键原则

- 先选品，再写文案。
- 先算毛利，再谈发布。
- 商品图优先真实来源，不把 AI 概念图当成上架图。
- 直接发布不在当前演示范围内，输出发布素材包即可。
- Agent 每一步都要主动告诉用户：现在做什么、为什么重要、需要什么、会产出什么。

