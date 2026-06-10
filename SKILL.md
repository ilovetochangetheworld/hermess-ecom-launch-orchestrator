---
name: hermess-ecom-launch-orchestrator
description: Use this skill when Hermess Agent needs to run or demo the customer-facing workshop case "From zero to launch: your AI e-commerce partner". It guides a product from selection research to Xiaohongshu copywriting, real product image preparation, publishing assets, customer service FAQ, review analysis, and loopback iteration. It coordinates existing e-commerce skills, proactively tells the user what it is doing at every stage, validates stage outputs, and produces workshop-ready takeaways.
---

# Hermess Ecom Launch Orchestrator

Use this as the control layer for the "From zero to launch: AI e-commerce partner" workflow. It coordinates specialized skills without replacing them:

1. `ecom-product-research`
2. `xiaohongshu-copywriting`
3. `ecom-product-imaging` or product image preparation tools
4. `xiaohongshu-publish`
5. `ecom-customer-service`
6. `ecom-review-analysis`

## Core Objective

Help the user move one product through a complete launch loop:

`research -> content -> product images -> publish -> customer service -> review analysis -> next research seed`

For workshops, prioritize a real, customer-facing 10-minute demo with visible artifacts over exhaustive analysis.

## Agent Communication Contract

The Agent must not silently work through the flow. At the beginning of every stage and before every external action, proactively tell the user:

- **Now doing:** the current action in one sentence.
- **Why it matters:** the business purpose of this action.
- **Need from you:** the minimum user input needed now, or "nothing yet".
- **Expected output:** what artifact will be produced next.

Use short, customer-facing language. Do not expose internal implementation detail unless the user asks.

Example:

```text
Now doing: I am checking whether this product has enough demand and margin to be worth launching.
Why it matters: We should not write copy or prepare images before confirming the product has a sellable angle.
Need from you: Please choose one product: portable fan, 40oz tumbler, clear phone case, or your own product.
Expected output: A go/no-go decision, target audience, selling angle, and risk checklist.
```

## Orchestration Workflow

### 1. Preflight

Collect or confirm:

- product name or physical product selected by the audience
- target market and platform
- available inputs: marketplace data, supplier data, real product images, XHS publishing readiness, comments
- time budget

If data is missing, continue with clearly marked assumptions and tell the user what confidence is affected.

### 2. Product Research

Call or guide `ecom-product-research`.

Required output:

- `product_profile`
- `pain_points`
- `profit_model`
- `decision`

Before moving on, check that `product_profile` contains concrete product details, not just a category name.

For the detailed product research interaction flow, read `references/product-research-flow.md`.

### 3. Xiaohongshu Copywriting

Call or guide `xiaohongshu-copywriting`.

Required output:

- `content_pack`
- at least 2 note versions
- hashtags
- quality check

Reject generic copy. The body must mention at least 3 concrete fields from `product_profile`.

### 4. Product Image Preparation

Use real product images whenever possible:现场实拍、供应商图、选品截图、商品详情图. AI may help organize, annotate, rank, and describe images, but do not position draft visuals as the real product listing source.

Required output:

- `image_pack.cover`
- `image_pack.feature`
- `image_pack.lifestyle`
- image usage reason and missing-image checklist

If real images are missing, ask the user for product photos or supplier links. If the user explicitly asks for generated scene drafts, label them as draft visual concepts, not real product photos.

### 5. Publishing

Call or guide `xiaohongshu-publish`.

Prepare the publishable title, body, hashtags, and image order. If platform/account status changes, still produce a complete publishing package and explain the operator action needed to publish.

### 6. Customer Service

Call or guide `ecom-customer-service`.

Required output:

- bilingual FAQ
- realtime reply result
- buyer intent
- escalation flag and reason

Demonstrate with 2-3 audience questions, preferably price, quality, comparison, or after-sales.

### 7. Review Analysis and Loopback

Call or guide `ecom-review-analysis`.

Required output:

- sentiment summary
- pain point ranking
- iteration roadmap
- `next_research_seed`

Close the loop by explaining how review insights become the next product research inputs.

## Stage Output Envelope

Whenever possible, consolidate outputs into this envelope:

```json
{
  "workflow_meta": {
    "workflow_name": "from_zero_to_launch",
    "mode": "customer_demo|real_launch",
    "current_stage": "preflight|research|copywriting|imaging|publishing|customer_service|review_analysis|complete",
    "demo_status": "ready|partial_ready|blocked"
  },
  "product_profile": {},
  "content_pack": {},
  "image_pack": {},
  "publish_result": {},
  "customer_service_pack": {},
  "review_insight_pack": {},
  "next_research_seed": {},
  "audience_takeaway": []
}
```

For detailed schemas, read `references/contracts.md`.

## Prompt Templates

When the user wants to run the workflow or rehearse a demo, use `references/orchestration-prompts.md`.

## Quality Gates

Before presenting a result, check:

- product details are specific enough for the next stage
- copy mentions concrete product parameters
- product images come from real product sources or are clearly marked as concept drafts
- publishing package is complete
- FAQ covers top pain points
- review analysis produces a usable next research seed

For detailed checks, read `references/quality-gates.md`.

## Workshop Timing

For a 10-minute live demo:

- 0:00-0:45 choose product
- 0:45-2:30 research summary
- 2:30-4:00 copywriting
- 4:00-5:30 product image preparation
- 5:30-7:00 publishing package or publishing execution
- 7:00-8:30 customer service Q&A
- 8:30-10:00 review loopback and takeaway pack

For presenter wording, read `references/demo-runbook.md`.

## Sample Data

For rehearsals or customer demos, use `assets/sample-envelope.json` as a complete example of the workflow envelope.

For real-product-inspired demo templates, use:

- `assets/samples/portable-fan-envelope.json`
- `assets/samples/insulated-tumbler-envelope.json`
- `assets/samples/clear-magsafe-case-envelope.json`

For source assumptions behind these samples, read `references/real-product-sources.md`.

## Final Response Pattern

At the end of a run, summarize:

- what was completed
- what assets were generated
- which mode was used
- what is safe to show in the workshop
- what the next operator action is

Keep the user-facing answer short and demo-oriented.
