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


def prepare(images: list[str], product: str = "the exact product", features: str = "verified visible features", audience: str = "the target buyer", selling_point: str = "the verified core selling point") -> dict:
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
            "prompt": prompt_for(key, product, features, audience, selling_point),
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


def prompt_for(role: str, product: str, features: str, audience: str, selling_point: str) -> str:
    prompts = {
        "cover": (
            f"封面图 Prompt：主体必须是 {product}，清楚展示商品真实外观、颜色、材质、包装/数量；"
            f"干净明亮电商首图背景，突出 {selling_point}；居中或三分法构图，顶部预留标题安全区，柔和自然光，真实产品摄影；"
            f"面向 {audience}，解决买家第一眼不知道这是什么、是否适合自己的疑虑；不要添加未确认功能、认证标志或夸张效果。"
        ),
        "feature": (
            f"功能图 Prompt：主体必须是 {product}，用白底或浅色背景拼图展示已确认卖点：{features}；"
            f"每个分镜都要出现商品本体，例如手部演示核心功能、材质/细节特写、结构设计说明，并留出简短标注区域；"
            f"画面目标是证明 {selling_point}，帮助 {audience} 判断功能是否真实、材质是否可靠；不要只写功能词，不要出现未验证认证。"
        ),
        "lifestyle": (
            f"场景图 Prompt：主体必须是 {product}，展示 {audience} 在真实生活场景中使用该商品；"
            f"商品清楚可见并与使用动作发生关系，场景解释为什么需要 {selling_point}；"
            "中景或近景，温暖自然光，真实生活方式摄影；涉及儿童时只拍背影、手部或非识别角度；不要把概念图当作真实上架图。"
        ),
    }
    return prompts[role]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="*")
    parser.add_argument("--product", default="the exact product")
    parser.add_argument("--features", default="verified visible features")
    parser.add_argument("--audience", default="the target buyer")
    parser.add_argument("--selling-point", default="the verified core selling point")
    args = parser.parse_args()
    print(json.dumps(prepare(args.images, args.product, args.features, args.audience, args.selling_point), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
