# STAGE 8 — Cover Concepts and Decision

**Status:** Decided. Direction B ("Ink") is built as the paperback wrap in `build/paperback-wrap.pdf`.
**Rebuild:** `python3 06-cover/build_cover.py` (renders all three concepts as PNG and the wrap as PDF).

## Visual direction (from the brief)

Modern heirloom. Minimal. Timeless. Premium. Quietly emotional. Beautiful stationery plus literary
nonfiction plus family archive. Nothing on the list of things to avoid appears on any concept: no
photography, no illustration, no florals, hearts, script, foil effects, prompt counts, or badges.

## The three directions

| | A. Bone | B. Ink (chosen) | C. Rules |
|---|---|---|---|
| Ground | Warm off-white (#f3efe6) | Deep ink blue (#1e2838) | Warm off-white |
| Type | Charcoal Cormorant Garamond caps, letterspaced | Cream Cormorant Garamond caps | Charcoal caps |
| Device | A single short rule | A short rule, plus seven faint cream writing lines in the lower third | Eight faint gray writing lines in the lower third |
| Reads as | A literary hardcover jacket | A stationer's notebook, a boxed keepsake | A writing book |
| Thumbnail behaviour | Quiet. Risks disappearing against white Amazon backgrounds | Strong. The only dark, typographic cover in a wall of watercolor and florals | Quiet, like A |
| Matte-laminate wear | Light ground hides scuffs | Dark ground shows edge wear over years | Light ground hides scuffs |
| Gift-table test | Elegant, could be mistaken for a novel | Reads as a keepsake at arm's length | Reads as a journal |

## Why B

1. **The thumbnail is the sale.** On a search page this category is pastel, floral, and busy. A deep ink rectangle with cream capitals is the one result that does not look like the others. That contrast is the entire visual strategy from Stage 1.
2. **It says "premium" without foil.** Dark ground, cream type, restrained rule. It borrows from stationery brands the buyer already trusts.
3. **The lines say what the book is.** Seven faint writing rules in the lower third tell a buyer this is a book to be written in, without a single word of explanation and without a "250 questions" badge.
4. **It carries the series.** A Mom or Dad edition later changes one line of type and nothing else.

The one cost, edge wear on matte dark laminate, is real. The mitigation is in the artwork: no
hairline elements near the trim, and the ink color is deep enough that a scuff reads as patina.

## Front cover, as built

- Title: Cormorant Garamond SemiBold, 44 pt, caps, 0.14 em tracking, two lines, cream.
- Short rule, 1.1 in, cream at 80%.
- Tagline: EB Garamond Italic, 16 pt, *My stories. My memories. My words.*
- Seven writing rules, 0.75 pt, cream at 28%, 0.36 in pitch, lower third.
- Author in small caps, 13 pt. Imprint in Inter caps, 7.5 pt, 0.26 em tracking.
- Nothing within 0.25 in of any trim edge except the ground color.

## Spine (0.625 in for 250 pages on cream)

Title in cream caps reading top to bottom, author in small caps after it, imprint mark at the foot.
KDP requires text spines only at 100+ pages; this book qualifies. Text is kept 0.0625 in clear of the
spine edges as required.

## Back cover

Ink ground. Back copy in cream (Stage 9). Barcode reserve: a white 2 x 1.2 in box at the lower right,
0.35 in from the trim, which KDP fills with the ISBN barcode. Imprint at lower left.

## Hardcover

Same artwork. KDP case-laminate hardcover uses a different wrap size (wider spine, wraparound flaps of
0.75 in on all sides). Regenerate the wrap using KDP's hardcover template dimensions at upload; the
build script takes the spine width and bleed as variables.

## File spec

| File | Size | Use |
|---|---|---|
| `build/paperback-wrap.pdf` | 14.875 x 10.25 in, single page, fonts embedded | Upload as the paperback cover |
| `build/concept-B-ink.png` | 7 x 10 in at 192 dpi | Reference and listing mock-ups |
| `build/concept-A-bone.png`, `build/concept-C-rules.png` | same | Alternatives, kept for the record |

Before upload: run the wrap through KDP's Cover Calculator template to confirm the spine width
KDP computes for the final page count matches 0.625 in. If the interior page count changes, rebuild
with the new spine value.
