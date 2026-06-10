---
name: hermess-ecom-launch-orchestrator
description: Use this skill when Hermess Agent needs to run, demo, or troubleshoot a full e-commerce launch workflow from product research to Xiaohongshu copywriting, AI product images, publishing, customer service FAQ, review analysis, and loopback iteration. It coordinates existing e-commerce skills, validates stage outputs, chooses live/mock/manual fallback modes, and produces workshop-ready takeaways.
---

# Hermess Ecom Launch Orchestrator

Use this as the control layer for the "From zero to launch: AI e-commerce partner" workflow. It coordinates specialized skills without replacing them:

1. `ecom-product-research`
2. `xiaohongshu-copywriting`
3. `ecom-product-imaging`
4. `xiaohongshu-publish`
5. `ecom-customer-service`
6. `ecom-review-analysis`

## Core Objective

Help the user move one product through a complete launch loop:

`research -> content -> images -> publish -> customer service -> review analysis -> next research seed`

For workshops, prioritize a stable 10-minute demo with visible artifacts over exhaustive analysis.

## Operating Modes

- `live`: execute real integrations when credentials, cookies, APIs, and network are ready.
- `mock`: use prepared/sample data and local previews when a platform blocks automation.
- `manual`: generate copy-paste-ready assets when live publishing is risky or unavailable.

Default to `mock` for rehearsals, `live` only after the preflight checklist passes.

## Orchestration Workflow

### 1. Preflight

Collect or confirm:

- product name or physical product selected by the audience
- target market and platform
- demo mode: `live`, `mock`, or `manual`
- available inputs: Amazon data, 1688 data, product images, XHS cookies, comments
- time budget

If data is missing, switch to the smallest fallback that preserves the story.

### 2. Product Research

Call or guide `ecom-product-research`.

Required output:

- `product_profile`
- `pain_points`
- `profit_model`
- `decision`

Before moving on, check that `product_profile` contains concrete product details, not just a category name.

### 3. Xiaohongshu Copywriting

Call or guide `xiaohongshu-copywriting`.

Required output:

- `content_pack`
- at least 2 note versions
- hashtags
- quality check

Reject generic copy. The body must mention at least 3 concrete fields from `product_profile`.

### 4. Product Imaging

Call or guide `ecom-product-imaging`.

Required output:

- `image_pack.cover`
- `image_pack.feature`
- `image_pack.lifestyle`

Avoid fake logos, unreadable text, incorrect age labels, distorted hands, and unsafe scenes.

### 5. Publishing

Call or guide `xiaohongshu-publish`.

Select publishing path:

- use `live` if XHS cookie is fresh and xhs-cli is ready
- use `mock` if platform/session reliability is uncertain
- use `manual` if the user needs copy-paste assets

Never block the workshop on publishing. If live publishing fails, continue with a mock preview and explain the platform constraint briefly.

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
    "mode": "live|mock|manual",
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
- image prompts describe actual appearance and use scenes
- publish path is clear: live/mock/manual
- FAQ covers top pain points
- review analysis produces a usable next research seed

For detailed checks, read `references/quality-gates.md`.

## Workshop Timing

For a 10-minute live demo:

- 0:00-0:45 choose product
- 0:45-2:30 research summary
- 2:30-4:00 copywriting
- 4:00-5:30 images
- 5:30-7:00 publish or mock publish
- 7:00-8:30 customer service Q&A
- 8:30-10:00 review loopback and takeaway pack

For fallback scripts and presenter wording, read `references/demo-runbook.md`.

## Sample Data

For rehearsals or mock mode, use `assets/sample-envelope.json` as a complete example of the workflow envelope.

For v0.2 real-product-inspired mock demos, use:

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
