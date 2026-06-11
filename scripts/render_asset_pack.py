#!/usr/bin/env python3
"""Render a workflow envelope into a shareable business launch HTML page."""

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
    return f'<div class="kv"><span>{esc(label)}</span><strong>{esc(display_value(value)) or "暂无"}</strong></div>'


def display_value(value: Any) -> str:
    mapping = {
        "go": "建议继续",
        "go_with_caution": "谨慎继续",
        "pause": "暂停补充信息",
        "avoid": "不建议继续",
        "low": "低",
        "medium": "中",
        "high": "高",
        "package_ready": "素材包已准备",
        "pending_review": "待复核",
        "ready": "已就绪",
        "blocked": "受阻",
    }
    if value is None:
        return ""
    return mapping.get(str(value), str(value))


def section(title: str, body: str) -> str:
    return f"""
    <section class="section">
      <h2>{esc(title)}</h2>
      {body}
    </section>
    """


def asset_src(path: str | None) -> str:
    if not path:
        return ""
    if path.startswith(("http://", "https://", "data:", "file://", "/")):
        return path
    return path


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
        prompt = item.get("prompt") or item.get("image_prompt") or item.get("required_if_missing")
        path = item.get("source_path_or_url") or item.get("expected_output_path")
        src = asset_src(path)
        source_type = item.get("source_type") or "待补充"
        status = item.get("image_status") or ("已收到图片" if path else "等待用户根据 Prompt 生成或提交图片")
        preview = (
            f'<img class="image-preview" src="{esc(src)}" alt="{esc(item.get("role", key))}">'
            if src
            else '<div class="image-placeholder">等待图片</div>'
        )
        cards.append(
            f"""
            <article class="image-card">
              <div class="image-frame">{preview}</div>
              <div class="image-card-body">
                <div class="card-head">
                  <div>
                    <div class="eyebrow">{esc(item.get("role", key))}</div>
                    <h3>{esc(source_type)}</h3>
                  </div>
                  <span class="status-pill">{esc(status)}</span>
                </div>
                <p>{esc(item.get("why_this_image"))}</p>
                <small>{esc(path or item.get("required_if_missing"))}</small>
                <h4>中文图片 Prompt</h4>
                <pre>{esc(prompt)}</pre>
              </div>
            </article>
            """
        )
    return (
        '<p class="section-intro">用户可以先根据中文 Prompt 生成或拍摄图片，再把图片提交给 Agent。'
        '交付页会同时保留图片、来源状态和对应 Prompt，方便运营复用和二次修改。</p>'
        '<div class="image-grid">'
        + "".join(cards)
        + "</div>"
    )


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


def render_stage_progress(stage_progress: list[dict[str, Any]] | None) -> str:
    stage_progress = stage_progress or []
    if not stage_progress:
        return '<p class="muted">暂无阶段进度。</p>'
    cards = []
    for index, item in enumerate(stage_progress, start=1):
        cards.append(
            f"""
            <article class="mini-card">
              <div class="eyebrow">Stage {index}</div>
              <h3>{esc(item.get("Now doing"))}</h3>
              <p>{esc(item.get("Why it matters"))}</p>
              <small>{esc(item.get("Expected output"))}</small>
            </article>
            """
        )
    return '<div class="grid three">' + "".join(cards) + "</div>"


def build_delivery_manifest(data: dict[str, Any]) -> dict[str, Any]:
    manifest = data.get("delivery_manifest") or {}
    if manifest.get("assets"):
        return manifest

    profile = data.get("product_profile") or {}
    raw_name = profile.get("name") or "product"
    slug = "product"
    lowered = raw_name.lower()
    if "tumbler" in lowered or "cup" in lowered:
        slug = "tumbler"
    elif "fan" in lowered:
        slug = "fan"
    elif "case" in lowered:
        slug = "case"

    base_dir = "/home/agentuser"
    assets = [
        {"name": "文案素材包", "path": f"{base_dir}/{slug}_content_pack.json"},
        {"name": "客服问答包", "path": f"{base_dir}/{slug}_cs_pack.json"},
        {"name": "完整流程数据包", "path": f"{base_dir}/{slug}_workflow_envelope.json"},
        {"name": "图片Prompt包", "path": f"{base_dir}/{slug}_image_prompt_pack.json"},
    ]
    image_pack = data.get("image_pack") or {}
    for name, key in [("封面图", "cover"), ("功能图", "feature"), ("场景图", "lifestyle")]:
        path = (image_pack.get(key) or {}).get("source_path_or_url") or (image_pack.get(key) or {}).get("expected_output_path")
        if path:
            assets.append({"name": name, "path": path})
    return {
        "title": "交付文件清单",
        "assets": assets,
        "media_refs": [f"MEDIA:{item['path']}" for item in assets],
    }


def render_delivery_manifest(manifest: dict[str, Any]) -> str:
    assets = manifest.get("assets") or []
    rows = []
    for item in assets:
        rows.append(
            f"""
            <tr>
              <td>{esc(item.get("name"))}</td>
              <td><code>{esc(item.get("path"))}</code></td>
            </tr>
            """
        )
    refs = "\n".join(manifest.get("media_refs") or [])
    return f"""
    <table class="asset-table">
      <thead><tr><th>文件</th><th>路径</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
    <h3>MEDIA 引用</h3>
    <pre>{esc(refs)}</pre>
    """


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
    manifest = build_delivery_manifest(data)

    title = profile.get("name") or "商品经营启动包"
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
  <title>{esc(title)} - 商品经营启动包</title>
  <style>
    :root {{
      --ink: #17202a;
      --muted: #667085;
      --line: #d8e0ea;
      --paper: #f5f7fb;
      --panel: #ffffff;
      --blue: #1d4ed8;
      --green: #047857;
      --amber: #b45309;
      --soft-green: #ecfdf5;
      font-family: Inter, "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; color: var(--ink); background: linear-gradient(180deg, #eef4ff 0, var(--paper) 260px); }}
    .page {{ max-width: 1180px; margin: 0 auto; padding: 44px 24px 72px; }}
    .hero {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 34px; box-shadow: 0 18px 50px rgba(15,23,42,.08); position: relative; overflow: hidden; }}
    .hero:before {{ content: ""; position: absolute; inset: 0 0 auto; height: 5px; background: linear-gradient(90deg, var(--blue), var(--green)); }}
    .eyebrow {{ color: var(--blue); font-size: 13px; font-weight: 800; letter-spacing: 0; }}
    h1 {{ margin: 12px 0 0; font-size: 42px; line-height: 1.12; letter-spacing: 0; }}
    h2 {{ margin: 0 0 18px; font-size: 26px; letter-spacing: 0; }}
    h3 {{ margin: 18px 0 8px; font-size: 17px; }}
    h4 {{ margin: 16px 0 8px; font-size: 14px; color: #344054; }}
    p {{ line-height: 1.65; }}
    .lead-small {{ color: #344054; font-size: 17px; }}
    .section {{ margin-top: 22px; background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 28px; }}
    .section-intro {{ margin-top: -4px; color: #475467; }}
    .grid {{ display: grid; gap: 14px; }}
    .two {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .three {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
    .four {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}
    .kv, .mini-card, .copy-card {{ border: 1px solid var(--line); border-radius: 8px; background: #fff; padding: 16px; }}
    .kv {{ background: linear-gradient(180deg, #fff, #fbfdff); }}
    .kv span {{ display: block; color: var(--muted); font-size: 13px; margin-bottom: 8px; }}
    .kv strong {{ display: block; font-size: 18px; line-height: 1.35; }}
    .copy-card h3 {{ font-size: 22px; margin-top: 8px; }}
    .tags {{ color: var(--green); font-weight: 700; line-height: 1.6; margin-top: 12px; }}
    .clean {{ padding-left: 20px; line-height: 1.7; }}
    .faq-row {{ display: grid; grid-template-columns: 1.1fr 1.7fr .4fr; gap: 14px; padding: 14px 0; border-top: 1px solid var(--line); align-items: start; }}
    .faq-row:first-child {{ border-top: 0; }}
    .faq-row span, .muted, small {{ color: var(--muted); }}
    .image-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }}
    .image-card {{ border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: #fff; display: flex; flex-direction: column; min-width: 0; }}
    .image-frame {{ aspect-ratio: 4 / 3; background: #eef2f7; border-bottom: 1px solid var(--line); display: grid; place-items: center; overflow: hidden; }}
    .image-preview {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .image-placeholder {{ width: calc(100% - 28px); height: calc(100% - 28px); border: 1px dashed #a9b8cc; border-radius: 8px; display: grid; place-items: center; color: var(--muted); font-weight: 700; background: #f8fafc; }}
    .image-card-body {{ padding: 16px; min-width: 0; }}
    .card-head {{ display: flex; justify-content: space-between; gap: 10px; align-items: flex-start; }}
    .card-head h3 {{ margin-top: 6px; }}
    .status-pill {{ flex: 0 1 auto; max-width: 150px; background: var(--soft-green); color: var(--green); border: 1px solid #bbf7d0; border-radius: 999px; padding: 6px 9px; font-size: 12px; font-weight: 800; line-height: 1.35; text-align: center; }}
    code {{ color: #344054; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; overflow-wrap: anywhere; }}
    pre {{ white-space: pre-wrap; overflow-wrap: anywhere; background: #f8fafc; border: 1px solid var(--line); border-radius: 8px; padding: 12px; line-height: 1.55; color: #344054; }}
    .asset-table {{ width: 100%; border-collapse: collapse; }}
    .asset-table th, .asset-table td {{ text-align: left; border-top: 1px solid var(--line); padding: 12px; vertical-align: top; }}
    .asset-table th {{ color: var(--muted); font-size: 13px; }}
    .footer {{ color: var(--muted); font-size: 13px; margin-top: 26px; }}
    @media (max-width: 820px) {{
      .page {{ padding: 24px 14px 48px; }}
      h1 {{ font-size: 32px; }}
      .two, .three, .four, .faq-row, .image-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <header class="hero">
      <div class="eyebrow">商品经营启动包</div>
      <h1>{esc(title)}</h1>
      <p class="lead-small">从选品判断到发布准备、客服承接、复盘迭代和文件交付的商品经营启动包。</p>
    </header>
    {section("0. 工作流进度", render_stage_progress(data.get("stage_progress")))}
    {section("1. 选品结论", decision_body)}
    {section("2. 产品画像", profile_body)}
    {section("3. 定价和毛利", pricing_body)}
    {section("4. 内容资产", render_content_versions(content))}
    {section("5. 商品图片与 Prompt", render_images(data.get("image_pack") or {}))}
    {section("6. 发布准备包", publish_body)}
    {section("7. 客服 FAQ", render_faq(data.get("customer_service_pack") or {}))}
    {section("8. 复盘和下一轮", review_body)}
    {section("9. 交付文件清单", render_delivery_manifest(manifest))}
    <div class="footer">本页面由完整流程数据包生成。发布前请结合平台规则、账号状态和业务审批要求完成最终确认。</div>
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
