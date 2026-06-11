#!/usr/bin/env python3
"""Deterministic helpers for the Solo Ecom Pilot skill.

These helpers do not replace the language model. They provide stable scoring,
schemas, compliance checks, and packaging logic for the e-commerce workflow.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from typing import Any


def clamp(value: float, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, round(value)))


class Progress:
    @staticmethod
    def message(now: str, why: str, need: str, output: str) -> dict[str, str]:
        return {
            "Now doing": now,
            "Why it matters": why,
            "Need from you": need,
            "Expected output": output,
        }


@dataclass
class ProductFacts:
    name: str
    category: str = ""
    target_audience: str = ""
    supplier_price_cny: float | None = None
    selling_price: float | None = None
    key_features: list[str] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)


class MarketIntel:
    """Product research and go/no-go scoring."""

    DEMO_PRODUCTS = {
        "portable_fan": {
            "name": "USB-C 充电便携小风扇",
            "category": "便携降温小家电",
            "target_audience": "通勤人群、学生和办公室用户",
            "key_features": ["USB-C 充电", "小巧便携机身", "桌面支架", "电量显示"],
        },
        "insulated_tumbler": {
            "name": "40oz 大容量保温随行杯",
            "category": "饮水杯具",
            "target_audience": "通勤人群、健身用户和办公室用户",
            "key_features": ["40oz 大容量", "便携手柄", "吸管杯盖", "适配车载杯架的杯底"],
        },
        "clear_magsafe_case": {
            "name": "透明 MagSafe 兼容手机壳",
            "category": "手机配件",
            "target_audience": "想保护手机但不想遮住机身颜色的 iPhone 用户",
            "key_features": ["透明背板", "MagSafe 磁吸环", "高于屏幕和镜头的保护边", "防摔缓冲四角"],
        },
    }

    def from_template(self, key: str) -> ProductFacts:
        item = self.DEMO_PRODUCTS[key]
        return ProductFacts(**item)

    def score(self, facts: ProductFacts, signals: dict[str, Any] | None = None) -> dict[str, Any]:
        signals = signals or {}
        demand = clamp(signals.get("demand", 65))
        competition = clamp(100 - signals.get("competition", 45))
        profit = clamp(signals.get("profit", 60))
        seasonality = clamp(100 - signals.get("seasonality_risk", 30))
        supply = clamp(signals.get("supply_chain", 65))
        solo_fit = clamp(signals.get("solo_fit", 70))
        total = clamp(demand * 0.22 + competition * 0.18 + profit * 0.22 + seasonality * 0.12 + supply * 0.14 + solo_fit * 0.12)
        verdict = "go" if total >= 75 else "go_with_caution" if total >= 60 else "pause" if total >= 45 else "avoid"
        return {
            "decision": {
                "verdict": verdict,
                "score": total,
                "risk_level": "low" if total >= 75 else "medium" if total >= 60 else "high",
                "one_line_reason": self._reason(verdict, facts),
            },
            "six_dimension_scores": {
                "market_capacity": demand,
                "competition_opportunity": competition,
                "profit_space": profit,
                "seasonality_stability": seasonality,
                "supply_chain_threshold": supply,
                "solo_seller_fit": solo_fit,
            },
            "product_profile": {
                "name": facts.name,
                "category": facts.category,
                "key_features": facts.key_features,
                "target_audience": facts.target_audience,
                "key_selling_point": self._selling_point(facts),
                "differentiation_direction": "用具体商品事实建立差异化，并保持适合个人卖家执行的运营动作。",
                "safe_claims": facts.key_features,
                "claims_to_avoid": ["最强", "第一", "永久", "100%有效", "保证结果"],
                "image_needs": ["清晰商品主图", "功能/细节图", "真实使用场景图"],
                "faq_seeds": ["价格", "质量", "物流", "售后", "对比"],
            },
            "risk_checklist": [
                {
                    "risk": "关键商品事实尚未完全核验。",
                    "level": "中",
                    "operator_check": "发布前确认供应价、材质、包装内容和适用平台限制。",
                    "copywriting_rule": "不要宣称未核验的认证、续航、材质或功效。",
                }
            ],
            "confidence": "medium" if facts.missing_fields else "high",
        }

    def _reason(self, verdict: str, facts: ProductFacts) -> str:
        return {
            "go": f"{facts.name} 的购买场景清楚，已有足够商品事实继续推进。",
            "go_with_caution": f"{facts.name} 可以继续，但毛利或供应假设还需要确认。",
            "pause": f"{facts.name} 需要补充更多商品事实后再生成内容和发布准备。",
            "avoid": f"{facts.name} 暂不适合进入本次启动流程。",
        }[verdict]

    def _selling_point(self, facts: ProductFacts) -> str:
        if facts.key_features:
            return f"{facts.name} 面向{facts.target_audience}，核心特征包括{'、'.join(facts.key_features[:3])}。"
        return f"{facts.name} 面向{facts.target_audience}。"


class PricingEngine:
    PLATFORM_FEES = {
        "taobao": 0.008,
        "tmall": 0.04,
        "pinduoduo": 0.015,
        "douyin": 0.05,
        "xiaohongshu": 0.10,
        "jd": 0.05,
        "amazon": 0.15,
    }

    def price(self, cost: float, platform: str = "xiaohongshu", target_margin: float = 0.45) -> dict[str, Any]:
        fee = self.PLATFORM_FEES.get(platform.lower(), 0.10)
        return_loss = 0.04
        marketing = 0.08
        loaded_cost = cost * (1 + return_loss)
        recommended = loaded_cost / max(0.1, 1 - fee - marketing - target_margin)
        return {
            "pricing_pack": {
                "platform": platform,
                "currency": "CNY",
                "target_margin": target_margin,
                "cost_breakdown": {
                    "purchase_cost": cost,
                    "return_loss_rate": return_loss,
                    "platform_fee_rate": fee,
                    "marketing_reserve_rate": marketing,
                    "loaded_cost": round(loaded_cost, 2),
                },
                "price_range": {
                    "conservative": round(recommended * 0.92, 2),
                    "recommended": round(recommended, 2),
                    "aggressive": round(recommended * 1.12, 2),
                },
                "compliance_warnings": [
                    "Do not mark an original price unless there is real transaction evidence.",
                    "Do not claim a fake limited-time discount.",
                ],
            },
        }


class AdComplianceChecker:
    FORBIDDEN = {
        "最": "热销/优选/更适合",
        "第一": "人气之选/高关注",
        "唯一": "少见/特色",
        "顶级": "高品质",
        "100%": "尽量/有效帮助",
        "永久": "持久",
        "绝对": "更稳定/更安心",
        "包治": "不适用，删除医疗承诺",
    }

    def check(self, text: str) -> dict[str, Any]:
        hits = []
        for word, suggestion in self.FORBIDDEN.items():
            if word in text:
                hits.append({"word": word, "suggestion": suggestion})
        return {"passed": not hits, "hits": hits}


class ContentFactory:
    def __init__(self) -> None:
        self.compliance = AdComplianceChecker()

    def xiaohongshu_note(self, profile: dict[str, Any]) -> dict[str, Any]:
        name = profile.get("name", "这款商品")
        audience = profile.get("target_audience", "目标用户")
        features = profile.get("key_features", [])[:3]
        feature_text = "、".join(features) if features else "核心卖点明确"
        title = f"{name[:12]}怎么选"
        body = f"如果你是{audience}，这款{name}可以重点看。它的具体特点是{feature_text}。选它不是因为概念新，而是因为使用场景清楚、卖点能被图片和客服解释清楚。发布前建议把价格、规格、售后和真实商品图都补齐。"
        return {
            "content_pack": {
                "platform": "xiaohongshu",
                "selected_version": "A",
                "versions": [{"type": "工作流样例版", "title": title, "body": body, "hashtags": ["#电商选品", "#小红书开店", "#好物分享"]}],
                "sales_claims": features,
                "risk_words_removed": [],
                "quality_check": {
                    "product_specificity_score": 80 if features else 50,
                    "human_tone_score": 70,
                    "forbidden_words_found": [],
                    "generic_phrases_found": [],
                    "needs_humanizer": False,
                    "compliance": self.compliance.check(title + body),
                },
            }
        }


class ProductImagePrep:
    ROLES = ["cover", "feature", "lifestyle"]

    def prepare(self, image_sources: list[str] | None = None, product_profile: dict[str, Any] | None = None) -> dict[str, Any]:
        image_sources = image_sources or []
        product_profile = product_profile or {}
        pack = {}
        missing = []
        for index, role in enumerate(self.ROLES):
            source = image_sources[index] if index < len(image_sources) else None
            if not source:
                missing.append(role)
            pack[role] = {
                "role": {"cover": "封面图", "feature": "功能图", "lifestyle": "场景图"}[role],
                "source_type": "用户提交图片" if source else "待补充",
                "source_path_or_url": source,
                "prompt": self._prompt(role, product_profile),
                "required_if_missing": self._requirement(role),
                "why_this_image": self._reason(role),
                "image_status": "已收到图片，可放入商品经营启动包" if source else "未收到图片，先使用中文 Prompt 指导拍摄或生成",
            }
        return {
            "image_pack": pack,
            "missing_image_checklist": [self._requirement(role) for role in missing],
            "image_order": ["cover", "feature", "lifestyle"],
            "shot_list": [
                "封面图：收集或拍摄一张干净清晰的商品正面/45 度图。",
                "功能图：收集或拍摄一张能证明最强卖点的细节图或拼图。",
                "场景图：收集或拍摄一张包含目标用户使用语境的真实场景图。",
            ],
            "generation_policy": "默认只输出中文图片 Prompt、拍摄清单和图片顺序；除非用户明确要求，不调用生图接口。",
            "ai_visual_policy": "用户根据 Prompt 生成并提交的图片可以作为概念图或发布素材候选，必须在交付页中标明来源；不要把未核验概念图表述为真实商品实拍。",
        }

    def _prompt(self, role: str, profile: dict[str, Any]) -> str:
        name = profile.get("name") or "已确认商品"
        audience = profile.get("target_audience") or "目标买家"
        selling_point = profile.get("key_selling_point") or "已确认的核心卖点"
        features = "、".join((profile.get("key_features") or [])[:4]) or "已确认的可见特征"
        category = profile.get("category") or "商品品类"
        return {
            "cover": (
                f"封面图 Prompt：主体必须是 {name}（{category}），画面要清楚展示商品真实外观、颜色、材质和包装/数量；"
                f"背景使用干净明亮的电商首图场景，突出 {selling_point}；构图为居中或三分法，顶部预留标题安全区，"
                f"柔和自然光，真实产品摄影风格；面向 {audience}，解决买家第一眼不知道这是什么、是否适合自己的疑虑；"
                "不要添加未确认功能、认证标志或夸张效果。"
            ),
            "feature": (
                f"功能图 Prompt：主体必须是 {name}，用白底或浅色背景的拼图/信息图展示已确认卖点：{features}；"
                f"每个分镜都要出现商品本体，例如手部演示核心功能、材质/细节特写、结构设计说明，并留出简短标注区域；"
                f"画面目标是证明 {selling_point}，帮助 {audience} 判断功能是否真实、材质是否可靠；"
                "真实产品摄影 + 清晰标注风格，不要只写功能词，不要出现未验证认证或绝对化功效。"
            ),
            "lifestyle": (
                f"场景图 Prompt：主体必须是 {name}，展示 {audience} 在真实生活场景中使用该商品；"
                f"商品要清楚可见并与使用动作发生关系，场景应解释为什么需要 {selling_point}；"
                "构图为中景或近景，温暖自然光，真实生活方式摄影风格；如果涉及儿童，只拍背影、手部或非识别角度，"
                "画面解决买家对使用场景、尺寸感和安全感的疑虑；不要把概念图当作真实上架图。"
            ),
        }[role]

    def _requirement(self, role: str) -> str:
        return {
            "cover": "提供一张用于首屏识别的清晰真实商品主图。",
            "feature": "提供一张能证明核心卖点的功能或细节图。",
            "lifestyle": "提供一张真实使用场景图或供应商生活方式图。",
        }[role]

    def _reason(self, role: str) -> str:
        return {
            "cover": "帮助买家第一眼看清商品是什么、适不适合自己。",
            "feature": "把核心卖点变成可被看见和验证的证据。",
            "lifestyle": "帮助买家代入真实使用场景，降低决策成本。",
        }[role]


class PublishingPackage:
    def build(self, content_pack: dict[str, Any], image_pack: dict[str, Any]) -> dict[str, Any]:
        version = (content_pack.get("versions") or [{}])[0]
        return {
            "publish_result": {
                "publishing_readiness": "pending_review",
                "status": "package_ready",
                "title": version.get("title"),
                "body": version.get("body"),
                "hashtags": version.get("hashtags", []),
                "image_order": list(image_pack.keys()),
                "visibility": None,
                "failure_reason": None,
                "direct_publish_enabled": False,
                "policy_note": "已生成发布准备包。实际发布前请结合账号状态、平台规则和业务审批要求确认。",
                "operator_checklist": [
                    "确认账号状态和平台规则是否满足发布要求。",
                    "确认图片 Prompt、图片顺序，以及真实商品图、供应商图或用户回传图片是否齐备。",
                    "复核标题、正文、话题标签、价格表述和售后话术。",
                    "通过合适的平台流程提交或排期已确认的发布素材。",
                ],
                "next_action": "复核发布准备包，处理待确认事项后，再通过对应平台流程提交。",
            }
        }


class ServiceBot:
    def faq(self, profile: dict[str, Any]) -> dict[str, Any]:
        name = profile.get("name", "商品")
        return {
            "customer_service_pack": {
                "faq_list": [
                    {
                        "id": 1,
                        "Q_zh": f"{name}适合谁？",
                        "A_zh": f"适合{profile.get('target_audience', '目标用户')}，具体以规格和使用场景为准。",
                        "Q_en": f"Who is {name} for?",
                        "A_en": f"It is for {profile.get('target_audience', 'the target audience')}. Please check specs and use cases before purchase.",
                        "category": "使用",
                    },
                    {
                        "id": 2,
                        "Q_zh": "可以退换吗？",
                        "A_zh": "按平台规则和商品状态处理，未使用且不影响二次销售通常更容易处理。",
                        "Q_en": "Can I return or exchange it?",
                        "A_en": "Returns depend on platform rules and product condition. Unused items are usually easier to process.",
                        "category": "售后",
                    },
                    {
                        "id": 3,
                        "Q_zh": "质量怎么样？",
                        "A_zh": "建议查看材质、规格、实拍图和用户评价；不确定的信息我帮您确认后回复。",
                        "Q_en": "How is the quality?",
                        "A_en": "Please check materials, specs, real photos, and reviews. If unsure, I will confirm before replying.",
                        "category": "功能",
                    },
                ],
                "sample_replies": [
                    {
                        "detected_lang": "zh",
                        "matched_faq_id": 1,
                        "reply": f"这款更适合{profile.get('target_audience', '目标用户')}。如果您关心尺寸、材质或售后，我可以继续帮您确认。",
                        "confidence": "medium",
                        "buyer_intent": "quality_concern",
                        "need_escalation": False,
                        "escalation_reason": None,
                    }
                ],
            }
        }


class AnalyticsDashboard:
    def diagnose(self, metrics: dict[str, float] | None = None) -> dict[str, Any]:
        metrics = metrics or {}
        triggers = {
            "refund_rate_high": metrics.get("refund_rate", 0) > 0.10,
            "positive_review_low": metrics.get("positive_review_rate", 1) < 0.90,
            "roi_low": metrics.get("roi", 99) < 1.5,
            "dsr_low": metrics.get("dsr", 5) < 4.5,
        }
        force_loopback = sum(triggers.values()) >= 2
        return {
            "review_insight_pack": {
                "sentiment": {
                    "positive_pct": 0,
                    "neutral_pct": 0,
                    "negative_pct": 0,
                    "nps_estimate": 0,
                    "sample_size": 0,
                },
                "pain_points": [],
                "iteration_roadmap": {},
                "health_triggers": triggers,
                "force_loopback": force_loopback,
                "loopback": {
                    "next_selection_adjustment": "收紧供应商要求，避免继续使用导致咨询或退款的未核验卖点。",
                    "confidence_level": "medium" if metrics else "low",
                },
            },
            "next_research_seed": {
                "recommended_keyword": "",
                "avoid_features": [],
                "must_have_features": [],
                "new_target_audience": "",
                "price_band_adjustment": "",
                "supplier_requirements": [],
            },
        }


class Orchestrator:
    def __init__(self) -> None:
        self.market = MarketIntel()
        self.pricing = PricingEngine()
        self.content = ContentFactory()
        self.images = ProductImagePrep()
        self.publisher = PublishingPackage()
        self.service = ServiceBot()
        self.analytics = AnalyticsDashboard()

    def run_template(self, template: str) -> dict[str, Any]:
        facts = self.market.from_template(template)
        progress = [
            Progress.message("选择商品并建立产品事实", "选品先判断商品是否值得继续，避免后续内容空转。", "选择商品或提供链接、图片、供应价。", "产品画像和 go/no-go 结论。"),
            Progress.message("计算价格和毛利空间", "使用者需要看到这个商品不只是能写文案，也有经营可行性。", "采购价、目标平台和预期毛利。", "保守/建议/进取三个价格。"),
            Progress.message("生成绑定产品事实的内容", "好内容必须引用真实参数和目标人群。", "确认目标用户和不可夸大的卖点。", "标题、正文、标签和合规提示。"),
            Progress.message("整理图片 Prompt 与素材要求", "商品图要支撑信任，默认先输出 Prompt 和拍摄清单，不消耗生图。", "提供实拍、供应商图、商品截图，或确认先用商品画像生成 Prompt。", "封面/功能/场景三类图片 Prompt、图片顺序和补拍清单。"),
            Progress.message("生成发布准备包", "发布前需要把素材、合规和账号状态整理清楚。", "确认账号状态、平台规则和审批要求。", "标题、正文、标签、图片顺序和发布前确认清单。"),
            Progress.message("准备客服和复盘闭环", "发布后真正的效率来自问答承接和反馈回流。", "提供常见问题、评论或运营数据。", "FAQ、回复样例和下一轮选品种子。"),
        ]
        research = self.market.score(facts)
        price = self.pricing.price(cost=facts.supplier_price_cny or 25)
        content = self.content.xiaohongshu_note(research["product_profile"])
        images = self.images.prepare(product_profile=research["product_profile"])
        publish = self.publisher.build(content["content_pack"], images["image_pack"])
        service = self.service.faq(research["product_profile"])
        analytics = self.analytics.diagnose()
        return {
            "workflow_meta": {
                "workflow_name": "from_zero_to_launch",
                "mode": "standard_workflow",
                "current_stage": "complete",
                "workflow_status": "ready",
                "direct_publish_enabled": False,
            },
            "stage_progress": progress,
            **research,
            **price,
            **content,
            **images,
            **publish,
            **service,
            **analytics,
            "handoff_summary": [
                "选品判断",
                "定价建议",
                "小红书内容",
                "图片 Prompt 和拍摄清单",
                "发布准备包",
                "客服 FAQ",
                "复盘回流种子",
            ],
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("template", choices=sorted(MarketIntel.DEMO_PRODUCTS))
    args = parser.parse_args()
    print(json.dumps(Orchestrator().run_template(args.template), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
