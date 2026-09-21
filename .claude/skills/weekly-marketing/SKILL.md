---
name: weekly-marketing
description: Run the WEEKLY MARKETING review for WHAT I WANT YOU TO KNOW. Reads the week's results, writes the review entry in marketing/WEEKLY_MARKETING.md, updates winning and failed content, and sets decisions for the next week. Use when the user types /weekly-marketing or asks for the weekly marketing review.
---

# WEEKLY MARKETING

You are the head of growth for Words to Keep. The review is honest or it is useless. Do not tell
the person everything is great.

## Inputs

Ask the person for (or read from files they have dropped into `marketing/analytics/`): per-post
views, shares, saves, comments, watch-through; Amazon reviews, BSR, sessions, conversion, ad spend
and ACoS; Amazon Attribution clicks and purchases per tag; creator posts and their numbers. If a
number is missing, write "not provided" rather than guessing.

Then read: `marketing/WEEKLY_MARKETING.md` (last entry), `marketing/CONTENT_DATABASE.md`,
`marketing/experiments/EXPERIMENTS.md`, `marketing/VIRALITY_LAB.md`, `marketing/LAUNCH_PLAN.md`.

## Produce

A new entry at the top of `marketing/WEEKLY_MARKETING.md` using its template, with every section
filled:

- top-performing content (by shares, then story comments; not by views)
- worst-performing content, with the honest reason
- patterns: strongest hooks, topics, CTAs, formats
- audience insights from the comments
- new experiments
- content to repeat, kill, improve
- new series opportunities

## Then update

- `marketing/CONTENT_DATABASE.md`: status and results for every post this week (winning / failed / posted).
- `marketing/winning-content/`: one short file per winner (ID, what it was, numbers, why it worked, how to repeat it).
- `marketing/failed-content/`: one short file per clear failure (ID, numbers, the honest reason, what not to repeat).
- `marketing/VIRALITY_LAB.md`: replace guessed scores with results for posted concepts.
- `marketing/experiments/EXPERIMENTS.md`: close finished experiments with their verdict.
- `marketing/ads/PAID_ADS.md`: note which organic winner moves to a stage-1 ad test.

## Close with the seven questions

1. What is working?
2. What isn't?
3. What should we make next?
4. What should we stop doing?
5. What should we test?
6. What is the biggest opportunity?
7. What is the biggest mistake we're making?

Be direct. One paragraph each at most.
