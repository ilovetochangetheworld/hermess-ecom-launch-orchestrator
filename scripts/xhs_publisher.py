#!/usr/bin/env python3
"""Publishing package helper.

Direct Xiaohongshu publishing is intentionally disabled for the current
customer demo. This script only packages publish-ready assets and operator
actions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DIRECT_PUBLISHING_ENABLED = False


def build_package(title: str, body: str, hashtags: list[str], images: list[str]) -> dict:
    return {
        "publishing_readiness": "pending_review",
        "status": "package_ready",
        "title": title,
        "body": body,
        "hashtags": hashtags,
        "image_order": images,
        "direct_publish_enabled": DIRECT_PUBLISHING_ENABLED,
        "policy_note": "Direct Xiaohongshu publishing demo is paused. This helper only prepares assets for approved operator workflow.",
        "operator_checklist": [
            "Confirm account readiness",
            "Confirm all images are real product/supplier/user-provided images",
            "Review compliance warnings",
            "Paste title, body, hashtags, and images into the platform",
        ],
    }


def publish_disabled() -> dict:
    return {
        "ok": False,
        "reason": "Direct platform publishing is disabled for this workshop skill.",
        "next_action": "Use build_package() and publish through the approved operator workflow.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--hashtags", default="")
    parser.add_argument("--images", nargs="*", default=[])
    parser.add_argument("--out")
    args = parser.parse_args()
    data = build_package(args.title, args.body, [x for x in args.hashtags.split(",") if x], args.images)
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
