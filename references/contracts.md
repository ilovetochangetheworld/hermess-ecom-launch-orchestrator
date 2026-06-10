# Contracts

Use these contracts to keep all e-commerce skills interoperable.

## Product Profile

```json
{
  "product_profile": {
    "name": "Specific product name",
    "category": "Category",
    "key_features": ["Concrete feature with parameter"],
    "specs": {
      "suitable_ages": "Age/user fit or null",
      "materials": "Materials or null",
      "package_contents": "Package contents or null",
      "certifications": "Certifications or null",
      "colors": "Colors or null"
    },
    "supplier_price_cny": "Supplier price or range",
    "supplier_moq": "MOQ",
    "supplier_name": "Supplier name",
    "selling_price_usd": "Suggested selling price",
    "key_selling_point": "One concrete selling point",
    "differentiation_direction": "Specific differentiation direction",
    "target_audience": "Specific audience",
    "visual_style": "Image direction based on actual product appearance",
    "image_needs": ["cover image need", "feature image need", "lifestyle image need"]
  }
}
```

## Stage Progress

```json
{
  "stage_progress": [
    {
      "Now doing": "What the Agent is doing now",
      "Why it matters": "Business reason this step matters",
      "Need from you": "One essential input or confirmation",
      "Expected output": "Artifact this stage will produce"
    }
  ]
}
```

## Pricing Pack

```json
{
  "pricing_pack": {
    "platform": "xiaohongshu",
    "currency": "CNY",
    "target_margin": 0.45,
    "cost_breakdown": {
      "purchase_cost": 25,
      "return_loss_rate": 0.04,
      "platform_fee_rate": 0.1,
      "marketing_reserve_rate": 0.08,
      "loaded_cost": 26
    },
    "price_range": {
      "conservative": 64.4,
      "recommended": 70,
      "aggressive": 78.4
    },
    "compliance_warnings": [
      "Do not mark an original price unless there is real transaction evidence."
    ]
  }
}
```

## Content Pack

```json
{
  "content_pack": {
    "platform": "xiaohongshu",
    "selected_version": "A|B|null",
    "versions": [
      {
        "type": "测评型|生活型",
        "title": "Title",
        "body": "Body",
        "hashtags": ["#tag"]
      }
    ],
    "sales_claims": ["Claim grounded in product_profile"],
    "risk_words_removed": [],
    "quality_check": {
      "product_specificity_score": 0,
      "human_tone_score": 0,
      "forbidden_words_found": [],
      "generic_phrases_found": [],
      "needs_humanizer": false
    }
  }
}
```

## Image Pack

```json
{
  "image_pack": {
    "cover": {
      "role": "封面图",
      "source_type": "user_photo|supplier_image|marketplace_image|screenshot|concept_draft|missing",
      "source_path_or_url": "Local path or URL",
      "required_if_missing": "What image the operator should provide or shoot",
      "why_this_image": "Purpose"
    },
    "feature": {
      "role": "功能图",
      "source_type": "user_photo|supplier_image|marketplace_image|screenshot|concept_draft|missing",
      "source_path_or_url": "Local path or URL",
      "required_if_missing": "What image the operator should provide or shoot",
      "why_this_image": "Purpose"
    },
    "lifestyle": {
      "role": "场景图",
      "source_type": "user_photo|supplier_image|marketplace_image|screenshot|concept_draft|missing",
      "source_path_or_url": "Local path or URL",
      "required_if_missing": "What image the operator should provide or shoot",
      "why_this_image": "Purpose"
    }
  },
  "image_order": ["cover", "feature", "lifestyle"],
  "missing_image_checklist": [],
  "shot_list": [],
  "ai_visual_policy": "AI draft visuals can be used for concept exploration only; do not present them as real listing photos."
}
```

## Publish Result

```json
{
  "publish_result": {
    "publishing_readiness": "ready|pending_account|pending_review|blocked",
    "status": "package_ready|needs_operator_action|failed",
    "title": "Prepared title",
    "url": "URL or null",
    "visibility": "private|public|null",
    "failure_reason": null,
    "direct_publish_enabled": false,
    "policy_note": "Publishing readiness package prepared. Actual publishing should follow account status, platform policy, and business approval requirements.",
    "operator_checklist": [],
    "next_action": "Operator action"
  }
}
```

## Customer Service Pack

```json
{
  "customer_service_pack": {
    "faq_list": [
      {
        "id": 1,
        "Q_zh": "Chinese question",
        "A_zh": "Chinese answer",
        "Q_en": "English question",
        "A_en": "English answer",
        "category": "功能|使用|售后|对比|物流"
      }
    ],
    "sample_replies": [
      {
        "detected_lang": "zh|en",
        "matched_faq_id": 1,
        "reply": "Reply",
        "confidence": "high|medium|low",
        "buyer_intent": "price_sensitive|quality_concern|ready_to_buy|after_sales|comparison",
        "need_escalation": false,
        "escalation_reason": null
      }
    ]
  }
}
```

## Review Insight Pack

```json
{
  "review_insight_pack": {
    "sentiment": {
      "positive_pct": 0,
      "neutral_pct": 0,
      "negative_pct": 0,
      "nps_estimate": 0,
      "sample_size": 0
    },
    "pain_points": [],
    "iteration_roadmap": {},
    "loopback": {
      "original_hypothesis_valid": "true|false|null",
      "invalid_points": [],
      "new_insights": [],
      "next_selection_adjustment": "Specific adjustment",
      "confidence_level": "high|medium|low"
    }
  },
  "next_research_seed": {
    "recommended_keyword": "Keyword for next research",
    "avoid_features": [],
    "must_have_features": [],
    "new_target_audience": "Audience",
    "price_band_adjustment": "Adjustment",
    "supplier_requirements": []
  }
}
```

## Asset Pack Delivery

```json
{
  "asset_pack_html_path": "Local path to generated HTML asset pack or null",
  "delivery_note": "The workflow envelope remains the machine-readable source of truth; the HTML asset pack is the user-facing view."
}
```
