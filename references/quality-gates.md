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
- Otherwise continue in `mock` mode with sample assumptions clearly marked.

## Copywriting

Pass conditions:

- Each note body includes at least 3 concrete fields from `product_profile`.
- Title is short enough for Xiaohongshu.
- Forbidden words are absent.
- No generic phrases such as "quality life", "must-have artifact", or "high-end texture" unless supported by product facts.

Fail action:

- Rewrite once with stricter grounding.
- If still weak, produce a `needs_humanizer: true` flag and explain what needs manual polishing.

## Imaging

Pass conditions:

- Each prompt states actual product appearance.
- There are three roles: cover, feature, lifestyle.
- Negative prompt discourages fake logos, wrong labels, deformed people, and unreadable text.

Fail action:

- Regenerate prompt before calling the image API.
- If image generation fails, continue with prompt cards or prebuilt sample images.

## Publishing

Pass conditions:

- `publish_mode` is known.
- For `live`, cookie freshness and xhs-cli availability have been checked.
- For `mock`, preview output is available.
- For `manual`, copy-paste package is complete.

Fail action:

- Switch from `live` to `mock`, then from `mock` to `manual`.
- Do not let publishing failure stop the workshop.

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
