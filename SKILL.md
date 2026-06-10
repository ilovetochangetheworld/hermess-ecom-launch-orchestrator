---
name: solo-ecom-pilot
description: Use this skill for the customer-facing workshop case "From zero to launch: your AI e-commerce partner". It is a unified e-commerce operating skill for solo sellers: product research, pricing, content, real product image preparation, publishing package creation, customer service FAQ, compliance review, data diagnosis, and loopback iteration. The agent must proactively explain what it is doing at every step.
---

# Solo Ecom Pilot

This is the unified skill for the workshop case:

**从 0 开张：你的 AI 电商合伙人**

It replaces scattered e-commerce prompts with one customer-facing flow. The skill must behave like an AI e-commerce co-pilot, not a passive prompt library.

## Critical Positioning

- The demo is for customers, so use business language, not internal engineering language.
- Xiaohongshu direct publishing is temporarily paused for policy reasons. Generate a complete publishing package instead of demonstrating live publishing.
- Product images should come from real sources:现场实拍、供应商图、选品截图、商品详情图. AI may help rank, annotate, and describe images, but draft visuals must not be positioned as real product listing photos.
- The Agent must proactively say what it is doing at every stage.

## Trigger Keywords

- 选品类：选品、爆款、蓝海、市场分析、竞品分析、卖什么
- 定价类：定价、利润计算、毛利率、成本核算、怎么定价
- 内容类：商品标题、详情页、卖点提炼、种草文案、短视频脚本、直播话术
- 图片类：产品图、商品图片、封面图、功能图、场景图、供应商图、实拍图
- 发布类：小红书发布、笔记发布、发布素材、上传图片
- 客服类：客服话术、售后处理、退换货、差评回复、客户投诉
- 合规类：广告法、违禁词、极限词、虚假宣传、七日无理由
- 数据类：转化率、店铺诊断、运营日报、ROI、DSR、评论复盘
- 编排类：全链路演示、闭环演示、从0开张、AI电商合伙人

## Communication Contract

Before every stage and before any external action, output:

```text
Now doing: ...
Why it matters: ...
Need from you: ...
Expected output: ...
```

Rules:

- Do not silently work through the flow.
- Ask for only one essential missing input at a time.
- If information is missing, continue with marked assumptions and a confidence level.
- Keep updates short enough to be read aloud in a workshop.
- Before moving to the next stage, summarize the artifact produced and ask for confirmation only when business judgment is required.

## Unified Flow

### 1. MarketIntel: Product Research

Purpose: decide whether the product is worth continuing.

Capabilities:

- Offer three demo templates: portable fan, 40oz tumbler, clear MagSafe phone case.
- Accept the user's own product name, link, photo, supplier page, or rough description.
- Capture product facts without inventing missing details.
- Score market opportunity using:
  - market capacity
  - competition intensity
  - profit space
  - seasonality
  - supply-chain threshold
  - solo-seller fit
- Include loopback seed from later comments/data.

Read `references/product-research-flow.md` before running this stage.

Required output:

- `decision`
- `product_profile`
- `risk_checklist`
- `confidence`

### 2. PricingEngine: Pricing and Margin

Purpose: make pricing credible before content and publishing.

Capabilities:

- Domestic platform pricing assumptions: Taobao, Tmall, Pinduoduo, Douyin, Xiaohongshu, JD.
- Platform/category fee logic inspired by solo-ecom-pilot.
- Amazon/FBA cost fields are supported in the contract, but exact FBA calculation requires a real `profit_calculator.py` source file to be added later.
- Price compliance checks:
  - fake original price
  - false discount
  - price discrimination
  - unsupported limited-stock claims

Required output:

- conservative / recommended / aggressive price
- cost breakdown
- margin estimate
- compliance warnings

### 3. ContentFactory: Content Generation

Purpose: turn product positioning into publishable content.

Capabilities:

- Xiaohongshu note: review style and lifestyle style.
- Product title and selling points.
- Detail page outline using FAB logic.
- Short video / live script if needed.
- Multi-platform adaptation if the user asks.
- Every content result must call compliance review.

Rules:

- Bind copy to `product_profile`; do not write generic category copy.
- Mention at least three concrete product facts when available.
- Avoid extreme claims and unsupported effectiveness claims.

Required output:

- titles
- note body
- hashtags
- content quality check
- compliance check result

### 4. ProductImagePrep: Real Product Image Preparation

Purpose: prepare trustworthy listing images.

Capabilities:

- Organize real product images into:
  - cover image
  - feature/detail image
  - lifestyle/use-scene image
- Generate an image shot list if real images are missing.
- Suggest annotation points and image order.
- Label AI draft visuals only as concept drafts, not listing photos.

Required output:

- `image_pack`
- missing image checklist
- image order
- shot list

### 5. PublishingPackage: Publishing Assets

Purpose: prepare everything needed for publishing while direct Xiaohongshu publishing is paused.

Policy:

- Do not demo direct Xiaohongshu publishing for now.
- Do not claim the Agent has published unless a user explicitly provides a confirmed post URL.
- Produce a publishing package instead.

Required output:

- title
- body
- hashtags
- image order
- operator publishing checklist
- account/platform readiness notes

### 6. ServiceBot: Customer Service

Purpose: show the Agent can receive buyer questions after publishing.

Capabilities:

- Chinese FAQ.
- English FAQ when cross-border context exists.
- Buyer intent detection:
  - price_sensitive
  - quality_concern
  - ready_to_buy
  - after_sales
  - comparison
- Escalation flag.
- Detail page improvement signal from repeated questions.
- After-sales decision tree:
  - quality issue
  - logistics issue
  - no-reason return
  - complaint
  - negative review

Required output:

- FAQ list
- realtime reply
- buyer intent
- escalation decision
- page/FAQ improvement suggestion

### 7. AnalyticsDashboard: Review and Data Diagnosis

Purpose: close the loop and feed the next research run.

Capabilities:

- Comment sentiment and pain point extraction.
- Data health diagnosis when metrics are provided:
  - conversion rate
  - average order value
  - refund rate
  - positive review rate
  - ROI
  - DSR
  - repeat purchase rate
  - customer service response issue
- Loopback trigger:
  - refund_rate > 10%
  - positive_review_rate < 90%
  - ROI < 1.5
  - DSR < 4.5
  - If multiple conditions are true, force a `next_research_seed`.

Required output:

- top concerns
- positive signals
- detail page improvements
- FAQ improvements
- next research seed

## Workshop Run Order

Use this 10-minute customer demo sequence:

1. Choose product.
2. Product research and go/no-go.
3. Pricing and margin.
4. Xiaohongshu content.
5. Real product image preparation.
6. Publishing package.
7. Customer service Q&A.
8. Comment/data review and loopback.

## Shared Contracts

Use `references/contracts.md` for:

- `stage_progress`
- `product_profile`
- `pricing_pack`
- `content_pack`
- `image_pack`
- `publish_result`
- `customer_service_pack`
- `review_insight_pack`
- `next_research_seed`

Use `scripts/validate_envelope.py` to check the workflow envelope.

## References

- `references/product-research-flow.md`: detailed product research interaction.
- `references/contracts.md`: shared data structures.
- `references/quality-gates.md`: stage checks.
- `references/demo-runbook.md`: presenter wording.
- `references/orchestration-prompts.md`: reusable launch prompts.
- `references/real-product-sources.md`: assumptions behind demo templates.

## Scripts

- `scripts/main.py`: unified deterministic helper with research, pricing, content, image prep, publishing package, service, analytics, and an orchestrator.
- `scripts/validate_envelope.py`: validates the workflow envelope.
- `scripts/xhs_publisher.py`: publishing package helper; direct publishing is disabled by policy.
- `scripts/product_image_preparer.py`: image role and shot-list helper.

## Demo Templates

Use these as starting points only:

- `assets/samples/portable-fan-envelope.json`
- `assets/samples/insulated-tumbler-envelope.json`
- `assets/samples/clear-magsafe-case-envelope.json`

If the user provides real product information, prefer the user's data over demo templates.

## Final Response Pattern

At the end of a run, summarize:

- what product was selected
- what decision was made
- what assets were generated
- what is ready for publishing
- what questions the customer service bot can answer
- what should feed the next round of product research
