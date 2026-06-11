#!/usr/bin/env python3
"""Prepare product image roles from real image sources."""

from __future__ import annotations

import argparse
import json


ROLES = {
    "cover": ("封面图", "用于首屏识别的清晰商品主图。"),
    "feature": ("功能图", "用于证明核心卖点的功能或细节图。"),
    "lifestyle": ("场景图", "用于建立使用代入感的真实场景图。"),
}


def prepare(images: list[str], product: str = "已确认商品", features: str = "已确认的可见特征", audience: str = "目标买家", selling_point: str = "已确认的核心卖点") -> dict:
    result = {}
    missing = []
    for index, (key, (role, requirement)) in enumerate(ROLES.items()):
        source = images[index] if index < len(images) else None
        if not source:
            missing.append(requirement)
        result[key] = {
            "role": role,
            "source_type": "用户提交图片" if source else "待补充",
            "source_path_or_url": source,
            "prompt": prompt_for(key, product, features, audience, selling_point),
            "required_if_missing": requirement,
            "why_this_image": requirement,
            "image_status": "已收到图片，可放入商品经营启动包" if source else "未收到图片，先使用中文 Prompt 指导拍摄或生成",
        }
    return {
        "image_pack": result,
        "image_order": list(ROLES.keys()),
        "missing_image_checklist": missing,
        "shot_list": [
            "封面图：使用真实正面或 45 度角商品图，第一眼看清商品主体。",
            "功能图：使用细节图或拼图证明最强卖点，避免只有文字没有商品。",
            "场景图：使用真实使用场景或供应商生活方式图，帮助用户理解适用场景。",
        ],
        "generation_policy": "默认只输出中文图片 Prompt、拍摄清单和图片顺序；除非用户明确要求，不调用生图接口。",
        "ai_visual_policy": "用户根据 Prompt 生成并提交的图片可以作为概念图或发布素材候选，必须在交付页中标明来源；不要把未核验概念图表述为真实商品实拍。",
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
    parser.add_argument("--product", default="已确认商品")
    parser.add_argument("--features", default="已确认的可见特征")
    parser.add_argument("--audience", default="目标买家")
    parser.add_argument("--selling-point", default="已确认的核心卖点")
    args = parser.parse_args()
    print(json.dumps(prepare(args.images, args.product, args.features, args.audience, args.selling_point), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
