#!/usr/bin/env python3
"""Lightweight validator for the Hermess e-commerce workflow envelope."""

import json
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = [
    "workflow_meta",
    "stage_progress",
    "decision",
    "product_profile",
    "risk_checklist",
    "pricing_pack",
    "content_pack",
    "image_pack",
    "publish_result",
    "customer_service_pack",
    "review_insight_pack",
    "next_research_seed",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_envelope.py /path/to/envelope.json", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))

    missing = [key for key in REQUIRED_TOP_LEVEL if key not in data]
    if missing:
        print(json.dumps({"ok": False, "missing": missing}, ensure_ascii=False, indent=2))
        return 1

    checks = []
    product = data.get("product_profile") or {}
    checks.append({
        "name": "product_profile_specific",
        "ok": bool(product.get("name")) and len(product.get("key_features") or []) >= 3,
    })

    decision = data.get("decision") or {}
    checks.append({
        "name": "decision_present",
        "ok": decision.get("verdict") in ["go", "go_with_caution", "pause", "avoid"] and isinstance(decision.get("score"), int),
    })

    risk_checklist = data.get("risk_checklist") or []
    checks.append({
        "name": "risk_checklist_present",
        "ok": bool(risk_checklist),
    })

    progress = data.get("stage_progress") or []
    checks.append({
        "name": "agent_progress_contract_present",
        "ok": bool(progress) and all(
            all(key in item for key in ["Now doing", "Why it matters", "Need from you", "Expected output"])
            for item in progress
        ),
    })

    pricing = data.get("pricing_pack") or {}
    checks.append({
        "name": "pricing_pack_present",
        "ok": bool(pricing.get("price_range")) and bool(pricing.get("cost_breakdown")),
    })

    content = data.get("content_pack") or {}
    versions = content.get("versions") or []
    checks.append({
        "name": "content_versions_present",
        "ok": len(versions) >= 1 and bool(content.get("quality_check")) and "selected_version" in content,
    })

    images = data.get("image_pack") or {}
    checks.append({
        "name": "three_image_roles_present",
        "ok": all(role in images for role in ["cover", "feature", "lifestyle"]),
    })

    publish = data.get("publish_result") or {}
    checks.append({
        "name": "publishing_readiness_present",
        "ok": publish.get("publishing_readiness") in [
            "ready",
            "pending_account",
            "pending_review",
            "blocked",
        ],
    })

    checks.append({
        "name": "direct_publish_disabled",
        "ok": publish.get("direct_publish_enabled") is False,
    })

    review = data.get("review_insight_pack") or {}
    checks.append({
        "name": "review_loopback_present",
        "ok": bool(review.get("loopback")) and "sentiment" in review,
    })

    ok = all(item["ok"] for item in checks)
    print(json.dumps({"ok": ok, "checks": checks}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
