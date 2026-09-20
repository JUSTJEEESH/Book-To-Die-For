# Cover Prompts and Dimensions — The Four New Books

For generating cover art with an image model, then finishing in Illustrator. The rule that makes
these covers work: **the model makes the ground and the single device; Illustrator sets every word.**
Image models render type unreliably and KDP rejects soft or misspelled text. Generate art with no
text in it, then set the title, tagline, author, and imprint in vector over it, in the house type
(Cormorant Garamond SemiBold caps for titles, EB Garamond Italic for taglines, Inter for the
imprint). The four books then sit on a shelf as one family next to the flagship.

---

## 1. Dimensions

### Final files (what KDP receives)

KDP wants one PDF per format containing the full wrap: back cover, spine, front cover, plus 0.125 in
bleed on every outer edge. Spine width for cream paper is page count × 0.0025 in. Confirm every
number in KDP's Cover Calculator before export; page counts below are the planned counts and the
spine changes if the count changes.

| Book | Trim | Pages (planned) | Spine | Paperback full wrap (in) | At 300 dpi (px) |
|---|---|---|---|---|---|
| The Stories I Made Up | 7 x 10 | 120 | 0.300 | 14.550 x 10.250 | 4365 x 3075 |
| Still Me | 8.5 x 11 | 120 | 0.300 | 17.550 x 11.250 | 5265 x 3375 |
| Lo Que Quiero Que Sepas | 7 x 10 | 254 | 0.635 | 14.885 x 10.250 | 4466 x 3075 |
| The Words We Brought With Us | 7 x 10 | 130 | 0.325 | 14.575 x 10.250 | 4373 x 3075 |

Hardcover wraps are larger (wrap 0.591 in, hinge 0.394 in, a thicker spine) and change with page
count; get them from the calculator for each book when its page count is final. For reference, the
flagship's 254-page 7 x 10 hardcover is 16.399 x 11.417 in. Our build script can produce the
hardcover wrap from the calculator numbers, so for the hardcover you only need the front art.

### Front-cover art (what to generate)

Generate the front panel only, at the trim ratio, with room to extend into bleed and spine:

| Book | Front panel with bleed (in) | Aspect ratio | Generate at (px) | Final at 300 dpi (px) |
|---|---|---|---|---|
| The Stories I Made Up | 7.125 x 10.125 | 0.704 (about 7:10) | 1434 x 2048 or the model's largest 7:10 | 2138 x 3038 |
| Still Me | 8.625 x 11.125 | 0.775 (about 7:9) | 1587 x 2048 | 2588 x 3338 |
| Lo Que Quiero Que Sepas | 7.125 x 10.125 | 0.704 | 1434 x 2048 | 2138 x 3038 |
| The Words We Brought With Us | 7.125 x 10.125 | 0.704 | 1434 x 2048 | 2138 x 3038 |

Practical notes for the generation step:

- If the model only offers 2:3 or 3:4, use 2:3 (portrait) and crop. Ask for "a wide margin of plain background on every side" so cropping and extending are safe.
- Upscale the result to the final pixel size with a real upscaler (Photoshop's Super Resolution, Topaz, or the model's own 2x). Flat grounds and paper textures upscale cleanly; that is one reason these designs use them.
- Generate the back cover ground the same way at the same size, or simply extend the front's ground color across the whole wrap in Illustrator, which is what the flagship does.
- Keep the art in sRGB. KDP accepts RGB and converts. Do a soft-proof in Illustrator (View > Proof Colors, U.S. Web Coated) to check that the deep colors do not go muddy; if they do, lighten the ground by 5–8% and re-export.

### Safe zones (where type may sit)

- Front and back panels: nothing important within 0.25 in of the trim, and nothing within 0.375 in of the spine.
- Spine: text only if the spine is 0.25 in or wider (all four qualify); keep text 0.0625 in from the spine edges and set it no larger than spine width minus 0.125 in.
- Barcode: leave a 2 x 1.2 in white box at the lower right of the back cover, 0.25 in from the trim. KDP prints the barcode there.

---

## 2. The house system, so the four read as a family

- **Type:** title in Cormorant Garamond SemiBold, all caps, 0.12–0.14 em tracking, cream or charcoal. Tagline in EB Garamond Italic. Author in EB Garamond small caps. Imprint (WORDS TO KEEP) in Inter, letterspaced, small.
- **One ground color per book.** The flagship is deep ink. The four below take their own color so the shelf reads as a set with distinct spines.
- **One device per cover, never two.** The flagship's device is a set of faint writing rules. Each book below has its own single device.
- **No photographs, no faces, no florals, no hearts, no foil effects, no badges, no prompt counts.**

---

## 3. The Stories I Made Up

**Ground:** deep indigo, a shade bluer and warmer than the flagship's ink (#1e2748). Reads as
bedtime without a single cliché.
**Device:** one small paper-cut dragon, cream, the kind a five-year-old would recognize, sitting
low on the front cover as if on the bottom shelf of a bookcase. Alternative device: a cream crescent
moon the size of a thumbnail, upper right.
**Type color:** cream (#efe7d6).
**Tagline:** *Every story I ever told you, written down.*

**Prompt A (recommended):**
> A flat, matte, deep indigo blue background (hex 1e2748), completely plain and even, with a very subtle uncoated paper texture. Near the bottom center, a single small silhouette of a friendly dragon made of cut cream-colored paper, simple rounded shapes, slightly imperfect edges as if cut with scissors, no outline, no shading, no other objects. Large empty space above for text. No text anywhere. Book cover art, portrait 7:10, minimal, modern heirloom stationery style, high resolution.

**Prompt B (moon variant):**
> A flat, matte, deep indigo blue background (hex 1e2748) with a very subtle uncoated paper texture. In the upper right, a single small crescent moon cut from cream paper, slightly imperfect scissor-cut edges, no glow, no stars, no clouds. Everything else empty. No text anywhere. Book cover art, portrait 7:10, minimal, modern stationery style.

**Prompt C (bolder, for A+ imagery rather than the cover):**
> A child's crayon drawing of a dragon, a truck, and a moon on cream paper, drawn by a five-year-old, naive and joyful, no text, flat scan, high resolution.

**Negative prompt (all variants):** text, letters, watermark, stars, clouds, castle, cartoon face, eyes, gradient, glossy, 3D render, photo, gold foil, sparkles.

**Illustrator:** title in three lines (THE STORIES / I MADE / UP) centered in the upper half, cream; tagline beneath; dragon or moon untouched; author and imprint at the foot. Spine: title and author in cream on the same indigo.

---

## 4. Still Me

**Ground:** warm oatmeal linen (#e9e2d3), light, so the book is calm in a hand and does not look
like a medical product or a memorial. Type in deep green-charcoal (#2b3a34).
**Device:** a single small circle of ochre (#c8973f), like a low sun, off-center upper left, the
only color on the cover. It says "still here" without saying it.
**Tagline:** *A life-story book, filled in together.*

**Prompt A (recommended):**
> A plain warm oatmeal-colored linen fabric texture, very fine weave, evenly lit, flat, soft, no folds or wrinkles, filling the whole frame (hex e9e2d3). In the upper left third, one small perfect circle in muted ochre gold (hex c8973f), matte, painted flat with slightly soft edges as if printed on the linen. Nothing else. No text anywhere. Book cover art, portrait about 7:9, minimal, calm, modern heirloom stationery.

**Prompt B (no device, texture only):**
> A plain warm oatmeal-colored linen fabric texture, very fine weave, evenly lit, flat, filling the whole frame (hex e9e2d3). Nothing else at all. No text. High resolution, seamless, for use as a book cover background.

**Negative prompt:** text, forget-me-nots, flowers, brain, puzzle pieces, ribbon, hands, faces, photo, gradient, glossy, wrinkles, shadows, gold foil.

**Illustrator:** title STILL ME large, two words on one line, deep green-charcoal, set just below the vertical center; tagline beneath; the ochre circle above and to the left of the title, never behind it. This is the one cover of the five with a light ground, which is deliberate: on the memory-care shelf everything else is dark or clinical.

---

## 5. Lo Que Quiero Que Sepas

**No new art needed.** This is the flagship's cover in Spanish, so a buyer sees that it is the same
book. Same deep ink, same cream type, same faint writing rules. The build script produces it from
the same template; only the words change:

- Title: LO QUE QUIERO QUE SEPAS (four lines fit the panel well: LO QUE / QUIERO / QUE / SEPAS, or two lines at a smaller size)
- Tagline: *Mis historias. Mis recuerdos. Mis palabras.*
- Author and imprint unchanged.

If you want the Spanish edition to be distinguishable at a glance while staying in the family, shift
the ground one step warmer (deep oxblood, #4a1f24, with the same cream type). Recommendation: keep
the ink. Sameness is the message.

---

## 6. The Words We Brought With Us

**Ground:** deep forest green (#1f3a2f). Cream type.
**Device:** a field of faint handwriting in several scripts, illegible, cream at about 18% opacity,
running across the lower third like the flagship's writing rules. It says "many languages, one hand"
without a flag or a map.
**Tagline:** *The words, the sayings, and the songs we still say.*

**Prompt A (recommended):**
> A flat, matte, deep forest green background (hex 1f3a2f) with a very subtle uncoated paper texture. Across the lower third, faint cream-colored handwriting in several different scripts (Latin cursive, Cyrillic, Greek, Arabic, Devanagari, Chinese, Korean hangul, Tagalog Latin script) written in different hands, overlapping slightly, deliberately illegible, at low opacity like a watermark, forming a soft horizontal band. Upper two thirds completely empty. No legible words. No text meant to be read. Book cover art, portrait 7:10, minimal, modern heirloom stationery.

**Prompt B (single line variant):**
> A flat, matte, deep forest green background (hex 1f3a2f) with subtle paper texture. One single line of faint cream cursive handwriting in an old hand, deliberately illegible, at low opacity, running horizontally just below the center. Nothing else. No readable text. Book cover art, portrait 7:10, minimal.

**Negative prompt:** flags, map, globe, passport, suitcase, legible words, real words, logos, faces, photo, gradient, glossy, gold foil.

**Illustrator:** the handwriting band must stay illegible; if the model produces a real word in any language, paint it out. Title in four lines (THE WORDS / WE BROUGHT / WITH / US) in cream, upper half; tagline; author and imprint. Check the band at 18–22% opacity against the cream title for contrast.

---

## 7. Finishing checklist in Illustrator (every book)

1. New document at the full wrap size in inches (table above), 300 ppi, RGB. Add guides at bleed (0.125 in), at the spine edges, and at the 0.25 in safe margin on all panels.
2. Place the generated art on the front panel, scaled to cover the front plus bleed and to extend 0.375 in past the spine edge so the fold has no seam. Fill the rest of the wrap with the exact ground hex.
3. Set all type in vector. Title tracking 0.12–0.14 em. Optical kerning on.
4. Back cover: the back copy in cream (or charcoal on Still Me), 12–13 pt, and the barcode reserve box (white, 2 x 1.2 in) at lower right, 0.25 in from trim.
5. Spine: title and author reading top to bottom, centered on the spine width, inside the 0.0625 in spine margin.
6. Export: File > Save As > Adobe PDF, preset PDF/X-1a or "High Quality Print," fonts embedded, no printer's marks, bleed 0.125 in, single page. Under 40 MB.
7. Upload to KDP and read the Previewer's spine and margin warnings; they are exact.

For the hardcover: give me the front art at the final pixel size and KDP's calculator numbers for
the book's page count, and the build script produces the wrap.
