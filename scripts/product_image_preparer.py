#!/usr/bin/env python3
"""Prepare product image roles from real image sources."""

from __future__ import annotations

import argparse
import json


ROLES = {
    "cover": ("封面图", "A clear real product photo for first-screen recognition."),
    "feature": ("功能图", "A detail image that proves the key selling point."),
    "lifestyle": ("场景图", "A real use-scene or supplier lifestyle image."),
}


def prepare(images: list[str]) -> dict:
    result = {}
    missing = []
    for index, (key, (role, requirement)) in enumerate(ROLES.items()):
        source = images[index] if index < len(images) else None
        if not source:
            missing.append(requirement)
        result[key] = {
            "role": role,
            "source_type": "user_photo" if source else "missing",
            "source_path_or_url": source,
            "prompt": prompt_for(key),
            "required_if_missing": requirement,
            "why_this_image": requirement,
        }
    return {
        "image_pack": result,
        "image_order": list(ROLES.keys()),
        "missing_image_checklist": missing,
        "shot_list": [
            "Use a real front or three-quarter product photo as the cover.",
            "Use a real detail photo to prove the strongest selling point.",
            "Use a real use-scene or supplier lifestyle image for context.",
        ],
        "generation_policy": "Default output is prompts only. Do not call image generation APIs unless the user explicitly asks.",
        "ai_visual_policy": "AI draft visuals can be used for concept exploration only; do not present them as real listing photos.",
    }


def prompt_for(role: str) -> str:
    prompts = {
        "cover": "Clean front-facing product photo prompt: exact product shape, color, material, and package contents on a simple bright background, realistic ecommerce photography, no invented features.",
        "feature": "Feature/detail image prompt: close-up of the strongest verified selling point, clear annotation space, realistic product detail photography, no exaggerated claims.",
        "lifestyle": "Lifestyle scene prompt: target user using the real product in a natural daily setting, warm practical lighting, realistic proportions, no fake brand marks.",
    }
    return prompts[role]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="*")
    args = parser.parse_args()
    print(json.dumps(prepare(args.images), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
