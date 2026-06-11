#!/usr/bin/env python3
"""Publishing readiness package helper.

This script packages publish-ready assets and pre-publish checks. Actual
publishing should follow account status, platform policy, and business
approval requirements.
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
        "policy_note": "Publishing readiness package prepared. Actual publishing should follow account status, platform policy, and business approval requirements.",
        "operator_checklist": [
            "Confirm account readiness",
            "Confirm image order and whether each image is a real file or a prompt-only placeholder",
            "Review compliance warnings",
            "Submit or schedule the approved package through the appropriate platform workflow",
        ],
    }


def publish_disabled() -> dict:
    return {
        "ok": False,
        "reason": "This helper only prepares publishing readiness packages.",
        "next_action": "Use build_package(), resolve checklist items, and submit through the appropriate platform workflow.",
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
