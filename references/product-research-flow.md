# Product Research Flow

This file defines how Hermess Agent should run the first stage of "From zero to launch: your AI e-commerce partner".

The goal of product research is not to produce a long report. The goal is to decide whether a product is worth continuing into copywriting, image preparation, publishing, customer service, and review loopback.

## Principle

The Agent must make the process visible. Before every sub-step, say what it is doing, why it matters, what it needs from the user, and what it will output.

Use this format:

```text
Now doing: ...
Why it matters: ...
Need from you: ...
Expected output: ...
```

Keep each message concise enough for the user to act on immediately.

## Research Stage Map

### Step 0: Product Choice

What the Agent can do:

- Offer 3 starter product templates: portable fan, 40oz tumbler, clear MagSafe phone case.
- Accept the user's own product name, link, photo, supplier page, or rough description.
- Clarify the target platform and buyer group.

Agent message:

```text
Now doing: I am helping you choose the product for this launch workflow.
Why it matters: The rest of the workflow needs a concrete product, not a broad category.
Need from you: Choose one template product, or give me your own product name/link/photo.
Expected output: A single product candidate and initial buyer scenario.
```

Minimum user input:

- Product name or selected template.

Optional user input:

- Target buyer.
- Target price.
- Supplier link or product photo.
- Platform, default Xiaohongshu.

### Step 1: Product Fact Capture

What the Agent can do:

- Extract or ask for product facts: material, size, color, functions, package contents, supplier price, MOQ, logistics constraints.
- Turn loose descriptions into a structured `product_facts` object.
- Flag missing facts instead of inventing them.

Agent message:

```text
Now doing: I am turning the product into structured facts.
Why it matters: Later copy, images, FAQ, and publishing must be grounded in real product details.
Need from you: If you have supplier price, product photo, or key specs, send them now. If not, I will mark assumptions.
Expected output: Product facts, missing fields, and confidence level.
```

Output:

```json
{
  "product_facts": {
    "name": "",
    "category": "",
    "functions": [],
    "materials": "",
    "colors": "",
    "package_contents": "",
    "supplier_price_cny": "",
    "supplier_moq": "",
    "source": "user|supplier_link|starter_template",
    "missing_fields": []
  },
  "confidence": "high|medium|low"
}
```

### Step 2: Demand Hypothesis

What the Agent can do:

- Identify likely buyer groups and purchase scenarios.
- Create 3 possible selling angles.
- Use available marketplace/social signals when tools are available.
- If browsing or platform data is unavailable, label the result as a hypothesis.

Agent message:

```text
Now doing: I am checking who might buy this and why.
Why it matters: A product only becomes sellable when the buyer, scene, and pain point are clear.
Need from you: Tell me if you want to target students, office workers, parents, gift buyers, or another group.
Expected output: Target audience, usage scenarios, and top selling angles.
```

Output:

```json
{
  "target_audiences": [
    {
      "audience": "",
      "scene": "",
      "pain": "",
      "buying_motivation": ""
    }
  ],
  "selling_angles": [
    {
      "angle": "",
      "why_it_works": "",
      "proof_needed": ""
    }
  ]
}
```

### Step 3: Competition and Differentiation

What the Agent can do:

- Compare the candidate with typical alternatives.
- Identify common competitor claims.
- Find a differentiation direction that is specific and defensible.
- Avoid claiming "best", "first", or unverifiable superiority.

Agent message:

```text
Now doing: I am comparing this product against likely alternatives.
Why it matters: We need a reason for buyers to choose this, not just another generic listing.
Need from you: If you know a competing product or brand, send it. Otherwise I will compare against common market alternatives.
Expected output: Competitor patterns and one clear differentiation direction.
```

Output:

```json
{
  "competitor_patterns": [],
  "differentiation_direction": "",
  "claims_to_avoid": [],
  "claims_to_prove": []
}
```

### Step 4: Margin and Feasibility

What the Agent can do:

- Estimate gross margin from supplier price, expected selling price, platform fees, shipping, ad cost, and return loss.
- Call deterministic calculator tools if available.
- If data is missing, produce a range and explain assumptions.

Agent message:

```text
Now doing: I am estimating whether the product has enough margin to continue.
Why it matters: A product with weak margin should not move into content and publishing without caution.
Need from you: Send supplier price and intended selling price if you have them. Otherwise I will estimate a cautious range.
Expected output: Margin range, break-even warning, and go/no-go recommendation.
```

Output:

```json
{
  "profit_assumption": {
    "supplier_price_cny": "",
    "selling_price": "",
    "fees": "",
    "shipping": "",
    "ad_cost": "",
    "return_loss": ""
  },
  "margin_assessment": "excellent|good|thin|risky|unknown",
  "break_even_warning": "",
  "confidence": "high|medium|low"
}
```

### Step 5: Risk Checklist

What the Agent can do:

- Flag product, compliance, logistics, claim, quality, and after-sales risks.
- Convert risks into checks the operator can perform.
- Decide whether risk blocks the launch workflow or just needs disclosure.

Agent message:

```text
Now doing: I am checking the launch risks before we write copy.
Why it matters: Good AI output should reduce avoidable mistakes, not make risky claims faster.
Need from you: Tell me if this is a regulated product, has batteries, touches food/skin, or has safety claims.
Expected output: Risk checklist and required confirmations.
```

Output:

```json
{
  "risk_checklist": [
    {
      "risk": "",
      "level": "high|medium|low",
      "operator_check": "",
      "copywriting_rule": ""
    }
  ],
  "blocked_claims": [],
  "safe_claims": []
}
```

### Step 6: Go / No-Go Decision

What the Agent can do:

- Give a clear recommendation.
- Explain the decision in customer-facing language.
- Produce the `product_profile` that downstream stages will use.
- Ask for user confirmation before moving to copywriting.

Agent message:

```text
Now doing: I am turning the research into a launch decision.
Why it matters: The next stages should only use a clear product profile and selling direction.
Need from you: Confirm whether to continue with this positioning or adjust the target audience/price.
Expected output: Go/no-go decision, product profile, and next-step handoff to copywriting.
```

Output:

```json
{
  "decision": {
    "verdict": "go|go_with_caution|pause|avoid",
    "score": 0,
    "one_line_reason": ""
  },
  "product_profile": {
    "name": "",
    "category": "",
    "key_features": [],
    "target_audience": "",
    "key_selling_point": "",
    "differentiation_direction": "",
    "safe_claims": [],
    "claims_to_avoid": [],
    "image_needs": [],
    "faq_seeds": []
  },
  "handoff": {
    "next_stage": "copywriting",
    "user_confirmation_needed": true,
    "recommended_next_prompt": ""
  }
}
```

## Interaction Rules

- Ask for only one essential missing input at a time.
- If the user needs a fast run, keep moving with marked assumptions instead of over-asking.
- Do not invent supplier facts, certifications, exact margins, battery duration, safety claims, or platform fees.
- Always label confidence as `high`, `medium`, or `low`.
- Every stage must produce a visible artifact.
- Before moving from research to copywriting, ask: "Do you want to continue with this product positioning?"

## Starter Product Templates

Use these only as starting points. If the user provides real product information, prefer the user's information.

### Portable Fan

- Buyer: commuters, students, office workers.
- Core scene: hot commute, dorm, desk, outdoor queue.
- Facts to confirm: battery capacity, charging port, speed levels, noise level, safety certification.
- Common risks: overclaiming battery life, noise expectations, battery shipping.

### 40oz Tumbler

- Buyer: commuters, office workers, gym users.
- Core scene: hydration at work, driving, gym.
- Facts to confirm: material, food contact compliance, lid sealing, cupholder base size, dishwasher safety.
- Common risks: claiming full leakproof performance for straw lids, weight when full, metallic taste.

### Clear MagSafe Phone Case

- Buyer: iPhone users who want protection without hiding phone color.
- Core scene: daily commute, wireless charging, phone protection.
- Facts to confirm: exact phone model, magnet strength, raised bezel, anti-yellowing material, compliance.
- Common risks: model mismatch, overclaiming anti-yellowing, weak magnets.
