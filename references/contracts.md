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
      "source_type": "用户提交图片|供应商图|平台截图|商品截图|概念图|待补充",
      "source_path_or_url": "Local path or URL",
      "prompt": "中文图片生成或拍摄提示词",
      "expected_output_path": "Only present if a real/generated file already exists",
      "required_if_missing": "缺图时用户应提供、拍摄或生成什么图片",
      "why_this_image": "图片用途",
      "image_status": "已收到图片，可放入商品经营启动包|未收到图片，先使用中文 Prompt 指导拍摄或生成"
    },
    "feature": {
      "role": "功能图",
      "source_type": "用户提交图片|供应商图|平台截图|商品截图|概念图|待补充",
      "source_path_or_url": "Local path or URL",
      "prompt": "中文图片生成或拍摄提示词",
      "expected_output_path": "Only present if a real/generated file already exists",
      "required_if_missing": "缺图时用户应提供、拍摄或生成什么图片",
      "why_this_image": "图片用途",
      "image_status": "已收到图片，可放入商品经营启动包|未收到图片，先使用中文 Prompt 指导拍摄或生成"
    },
    "lifestyle": {
      "role": "场景图",
      "source_type": "用户提交图片|供应商图|平台截图|商品截图|概念图|待补充",
      "source_path_or_url": "Local path or URL",
      "prompt": "中文图片生成或拍摄提示词",
      "expected_output_path": "Only present if a real/generated file already exists",
      "required_if_missing": "缺图时用户应提供、拍摄或生成什么图片",
      "why_this_image": "图片用途",
      "image_status": "已收到图片，可放入商品经营启动包|未收到图片，先使用中文 Prompt 指导拍摄或生成"
    }
  },
  "image_order": ["cover", "feature", "lifestyle"],
  "missing_image_checklist": [],
  "shot_list": [],
  "generation_policy": "默认只输出中文图片 Prompt、拍摄清单和图片顺序；除非用户明确要求，不调用生图接口。",
  "ai_visual_policy": "用户根据 Prompt 生成并提交的图片可以作为概念图或发布素材候选，必须在交付页中标明来源；不要把未核验概念图表述为真实商品实拍。"
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
  "asset_pack_html_path": "Local path to generated 商品经营启动包（HTML交付页） or null",
  "delivery_manifest": {
    "title": "交付文件清单",
    "assets": [
      { "name": "文案素材包", "path": "/home/agentuser/product_content_pack.json" },
      { "name": "客服问答包", "path": "/home/agentuser/product_cs_pack.json" },
      { "name": "完整流程数据包", "path": "/home/agentuser/product_workflow_envelope.json" },
      { "name": "封面图", "path": "/home/agentuser/xhs_product_demo/封面图.png" },
      { "name": "功能图", "path": "/home/agentuser/xhs_product_demo/功能图.png" },
      { "name": "场景图", "path": "/home/agentuser/xhs_product_demo/场景图.png" }
    ],
    "media_refs": [
      "MEDIA:/home/agentuser/product_content_pack.json"
    ]
  },
  "delivery_note": "The complete workflow data package remains the machine-readable source of truth; the 商品经营启动包（HTML交付页） is the user-facing view and should include the delivery file list when files are available."
}
```
