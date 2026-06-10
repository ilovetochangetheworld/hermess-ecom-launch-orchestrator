#!/usr/bin/env python3
"""Lightweight validator for the Hermess e-commerce workflow envelope."""

import json
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = [
    "workflow_meta",
    "product_profile",
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

    content = data.get("content_pack") or {}
    versions = content.get("versions") or []
    checks.append({
        "name": "content_versions_present",
        "ok": len(versions) >= 1,
    })

    images = data.get("image_pack") or {}
    checks.append({
        "name": "three_image_roles_present",
        "ok": all(role in images for role in ["cover", "feature", "lifestyle"]),
    })

    publish = data.get("publish_result") or {}
    checks.append({
        "name": "publish_mode_present",
        "ok": publish.get("publish_mode") in ["live", "mock", "manual"],
    })

    ok = all(item["ok"] for item in checks)
    print(json.dumps({"ok": ok, "checks": checks}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
