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
    "image_prompts": ["cover prompt", "feature prompt", "lifestyle prompt"]
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
      "prompt": "Prompt",
      "negative_prompt": "wrong product, extra objects, unreadable text, distorted hands, deformed face, low quality, blurry, watermark, logo, fake brand name, incorrect age label, unsafe use scene",
      "file_path": "Local path or URL",
      "why_this_image": "Purpose"
    },
    "feature": {
      "role": "功能图",
      "prompt": "Prompt",
      "negative_prompt": "Same negative prompt",
      "file_path": "Local path or URL",
      "why_this_image": "Purpose"
    },
    "lifestyle": {
      "role": "场景图",
      "prompt": "Prompt",
      "negative_prompt": "Same negative prompt",
      "file_path": "Local path or URL",
      "why_this_image": "Purpose"
    }
  }
}
```

## Publish Result

```json
{
  "publish_result": {
    "publish_mode": "live|mock|manual",
    "status": "published|preview_ready|copy_pack_ready|failed",
    "title": "Published title",
    "url": "URL or null",
    "visibility": "private|public|mock|null",
    "failure_reason": null,
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
