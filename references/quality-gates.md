# Quality Gates

Use these checks before moving from one stage to the next.

## Product Research

Pass conditions:

- `product_profile.name` is a specific product, not only a category.
- At least 3 `key_features` contain concrete details such as material, size, age band, color, bundle, or function.
- `target_audience` is specific.
- `decision.verdict` and `risk_level` are present.
- Missing data and assumptions are explicit when Amazon or 1688 data is incomplete.

Fail action:

- Ask for one missing input if it is essential.
- Otherwise continue with clearly marked assumptions and lower the confidence level.

## Copywriting

Pass conditions:

- Each note body includes at least 3 concrete fields from `product_profile`.
- Title is short enough for Xiaohongshu.
- Forbidden words are absent.
- No generic phrases such as "quality life", "must-have artifact", or "high-end texture" unless supported by product facts.

Fail action:

- Rewrite once with stricter grounding.
- If still weak, produce a `needs_humanizer: true` flag and explain what needs manual polishing.

## Product Image Preparation

Pass conditions:

- Real product image sources are identified: user photo, supplier image, marketplace image, or product screenshot.
- There are three roles: cover, feature, lifestyle.
- Each image role has a clear usage reason.
- If AI-generated visual concepts are used, they are clearly labeled as concept drafts, not real product photos.

Fail action:

- Ask for product photos, supplier links, or screenshots.
- If images are still unavailable, produce an image shot list and do not claim product photos are ready.

## Publishing

Pass conditions:

- Title, body, hashtags, image order, and operator publishing action are clear.
- Platform/account readiness is known or clearly marked as pending.
- If direct publishing is unavailable, a complete publishing package is still produced.

Fail action:

- Explain what is blocking direct publishing.
- Continue by delivering the complete publishing package and required operator action.

## Customer Service

Pass conditions:

- FAQ covers function, usage, after-sales, comparison, and logistics.
- Top research pain points are covered.
- Realtime replies include confidence and escalation.
- Unknown details are not invented.

Fail action:

- Add FAQ entries for uncovered pain points.
- Mark low-confidence responses for manual follow-up.

## Review Analysis

Pass conditions:

- Sentiment and pain points are summarized.
- Roadmap actions are staged by timeline.
- `next_research_seed` is concrete enough for another product research run.

Fail action:

- If comments are unavailable, use a prepared sample comment set.
- Mark confidence as low if sample data is used.
