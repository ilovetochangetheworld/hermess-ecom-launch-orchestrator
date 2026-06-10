#!/usr/bin/env python3
"""Render a workflow envelope into a shareable HTML asset pack."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def esc(value: Any) -> str:
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def text_list(items: list[Any] | None) -> str:
    items = items or []
    if not items:
        return '<span class="muted">暂无</span>'
    return "".join(f"<li>{esc(item)}</li>" for item in items)


def field(label: str, value: Any) -> str:
    return f'<div class="kv"><span>{esc(label)}</span><strong>{esc(value) or "暂无"}</strong></div>'


def section(title: str, body: str) -> str:
    return f"""
    <section class="section">
      <h2>{esc(title)}</h2>
      {body}
    </section>
    """


def render_content_versions(content_pack: dict[str, Any]) -> str:
    versions = content_pack.get("versions") or []
    if not versions:
        return '<p class="muted">暂无内容版本。</p>'
    cards = []
    for item in versions:
        hashtags = " ".join(item.get("hashtags") or [])
        cards.append(
            f"""
            <article class="copy-card">
              <div class="eyebrow">{esc(item.get("type", "内容版本"))}</div>
              <h3>{esc(item.get("title"))}</h3>
              <p>{esc(item.get("body"))}</p>
              <div class="tags">{esc(hashtags)}</div>
            </article>
            """
        )
    return "".join(cards)


def render_images(image_pack: dict[str, Any]) -> str:
    if not image_pack:
        return '<p class="muted">暂无图片信息。</p>'
    cards = []
    for key in ["cover", "feature", "lifestyle"]:
        item = image_pack.get(key) or {}
        cards.append(
            f"""
            <article class="mini-card">
              <div class="eyebrow">{esc(item.get("role", key))}</div>
              <h3>{esc(item.get("source_type", "missing"))}</h3>
              <p>{esc(item.get("why_this_image"))}</p>
              <small>{esc(item.get("required_if_missing"))}</small>
            </article>
            """
        )
    return '<div class="grid three">' + "".join(cards) + "</div>"


def render_faq(customer_service_pack: dict[str, Any]) -> str:
    faq_list = customer_service_pack.get("faq_list") or []
    if not faq_list:
        return '<p class="muted">暂无 FAQ。</p>'
    rows = []
    for item in faq_list[:12]:
        rows.append(
            f"""
            <div class="faq-row">
              <strong>{esc(item.get("Q_zh"))}</strong>
              <span>{esc(item.get("A_zh"))}</span>
              <em>{esc(item.get("category"))}</em>
            </div>
            """
        )
    return "".join(rows)


def render_asset_pack(data: dict[str, Any]) -> str:
    profile = data.get("product_profile") or {}
    decision = data.get("decision") or {}
    pricing = data.get("pricing_pack") or {}
    pricing_range = pricing.get("price_range") or {}
    costs = pricing.get("cost_breakdown") or {}
    content = data.get("content_pack") or {}
    publish = data.get("publish_result") or {}
    review = data.get("review_insight_pack") or {}
    loopback = review.get("loopback") or {}
    next_seed = data.get("next_research_seed") or {}

    title = profile.get("name") or "电商启动资产包"
    decision_body = (
        '<div class="grid four">'
        + field("结论", decision.get("verdict"))
        + field("评分", decision.get("score"))
        + field("风险", decision.get("risk_level"))
        + field("信心", data.get("confidence"))
        + "</div>"
        + f'<p class="lead-small">{esc(decision.get("one_line_reason"))}</p>'
    )
    profile_body = (
        '<div class="grid two">'
        + field("品类", profile.get("category"))
        + field("目标人群", profile.get("target_audience"))
        + field("核心卖点", profile.get("key_selling_point"))
        + field("差异化方向", profile.get("differentiation_direction"))
        + "</div>"
        + '<h3>关键特征</h3><ul class="clean">'
        + text_list(profile.get("key_features"))
        + "</ul>"
    )
    pricing_body = (
        '<div class="grid three">'
        + field("保守价", pricing_range.get("conservative"))
        + field("建议价", pricing_range.get("recommended"))
        + field("进取价", pricing_range.get("aggressive"))
        + "</div>"
        + '<h3>成本结构</h3><div class="grid four">'
        + field("采购成本", costs.get("purchase_cost"))
        + field("平台扣点", costs.get("platform_fee_rate"))
        + field("营销预留", costs.get("marketing_reserve_rate"))
        + field("含损耗成本", costs.get("loaded_cost"))
        + "</div>"
    )
    publish_body = (
        '<div class="grid two">'
        + field("发布状态", publish.get("status"))
        + field("准备度", publish.get("publishing_readiness"))
        + "</div>"
        + f'<h3>{esc(publish.get("title"))}</h3>'
        + f'<p>{esc(publish.get("body"))}</p>'
        + f'<div class="tags">{esc(" ".join(publish.get("hashtags") or []))}</div>'
        + '<h3>发布前确认清单</h3><ul class="clean">'
        + text_list(publish.get("operator_checklist"))
        + "</ul>"
    )
    review_body = (
        '<div class="grid two">'
        + field("下一步调整", loopback.get("next_selection_adjustment"))
        + field("复盘信心", loopback.get("confidence_level"))
        + "</div>"
        + '<h3>下一轮选品种子</h3><ul class="clean">'
        + text_list(
            [
                next_seed.get("recommended_keyword"),
                *(next_seed.get("must_have_features") or []),
                *(next_seed.get("supplier_requirements") or []),
            ]
        )
        + "</ul>"
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} - 电商启动资产包</title>
  <style>
    :root {{
      --ink: #17202a;
      --muted: #667085;
      --line: #d9e2ec;
      --paper: #f8fafc;
      --panel: #ffffff;
      --blue: #2563eb;
      --green: #059669;
      --amber: #d97706;
      font-family: Inter, "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; color: var(--ink); background: var(--paper); }}
    .page {{ max-width: 1180px; margin: 0 auto; padding: 44px 24px 72px; }}
    .hero {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 34px; box-shadow: 0 18px 50px rgba(15,23,42,.08); }}
    .eyebrow {{ color: var(--blue); font-size: 13px; font-weight: 800; text-transform: uppercase; letter-spacing: .04em; }}
    h1 {{ margin: 12px 0 0; font-size: 42px; line-height: 1.12; letter-spacing: 0; }}
    h2 {{ margin: 0 0 18px; font-size: 26px; letter-spacing: 0; }}
    h3 {{ margin: 18px 0 8px; font-size: 17px; }}
    p {{ line-height: 1.65; }}
    .lead-small {{ color: #344054; font-size: 17px; }}
    .section {{ margin-top: 22px; background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 28px; }}
    .grid {{ display: grid; gap: 14px; }}
    .two {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .three {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
    .four {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}
    .kv, .mini-card, .copy-card {{ border: 1px solid var(--line); border-radius: 8px; background: #fff; padding: 16px; }}
    .kv span {{ display: block; color: var(--muted); font-size: 13px; margin-bottom: 8px; }}
    .kv strong {{ display: block; font-size: 18px; line-height: 1.35; }}
    .copy-card h3 {{ font-size: 22px; margin-top: 8px; }}
    .tags {{ color: var(--green); font-weight: 700; line-height: 1.6; margin-top: 12px; }}
    .clean {{ padding-left: 20px; line-height: 1.7; }}
    .faq-row {{ display: grid; grid-template-columns: 1.1fr 1.7fr .4fr; gap: 14px; padding: 14px 0; border-top: 1px solid var(--line); align-items: start; }}
    .faq-row:first-child {{ border-top: 0; }}
    .faq-row span, .muted, small {{ color: var(--muted); }}
    .footer {{ color: var(--muted); font-size: 13px; margin-top: 26px; }}
    @media (max-width: 820px) {{
      .page {{ padding: 24px 14px 48px; }}
      h1 {{ font-size: 32px; }}
      .two, .three, .four, .faq-row {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <header class="hero">
      <div class="eyebrow">E-commerce Launch Asset Pack</div>
      <h1>{esc(title)}</h1>
      <p class="lead-small">从选品判断到发布准备、客服承接和复盘迭代的可执行资产包。</p>
    </header>
    {section("1. 选品结论", decision_body)}
    {section("2. 产品画像", profile_body)}
    {section("3. 定价和毛利", pricing_body)}
    {section("4. 内容资产", render_content_versions(content))}
    {section("5. 商品图片准备", render_images(data.get("image_pack") or {}))}
    {section("6. 发布准备包", publish_body)}
    {section("7. 客服 FAQ", render_faq(data.get("customer_service_pack") or {}))}
    {section("8. 复盘和下一轮", review_body)}
    <div class="footer">Generated from workflow envelope. Actual publishing should follow platform rules, account status, and business approval requirements.</div>
  </main>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("envelope", help="Path to workflow envelope JSON")
    parser.add_argument("--out", required=True, help="Output HTML path")
    args = parser.parse_args()

    envelope_path = Path(args.envelope)
    out_path = Path(args.out)
    data = json.loads(envelope_path.read_text(encoding="utf-8"))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_asset_pack(data), encoding="utf-8")
    print(str(out_path))


if __name__ == "__main__":
    main()
