# Cover v2 — image prompt and exact text placement

**Book:** *What I Want You to Know: A Guided Legacy Journal for Parents and Grandparents to Leave Their Stories, Memories, and Words to the People They Love* — Joshua Caleb Green. 7 x 10 in, 254 pages, cream paper. Paperback (spine 0.635 in) and case-laminate hardcover (KDP calculator numbers below).

**What this replaces:** the all-type ink cover (`06-cover/build/`). It is elegant at full size and nearly invisible at 160 px, which is where every Amazon decision is made. The new direction keeps the brand (deep navy, cream serif, "modern heirloom") and adds the two things the current cover lacks: a picture that says *write your life down* in one glance, and a title heavy enough to read on a phone.

**Reference files (all in `06-cover/v2/build/`):**
- `paperback-wrap-v2-GUIDE.png` / `hardcover-wrap-v2-GUIDE.png` — every piece of type in its final place, with trim, spine, safe-zone and barcode boxes drawn on. Placeholder art; yours replaces it.
- `paperback-wrap-v2.png`, `hardcover-wrap-v2.png` — the same without guides.
- `front-thumb-160.png` — the front at Amazon search size. Check your version against it.

---

## 1. The concept

A kitchen table at night, lit by one lamp. An open journal, a pen, a few old photographs, a cup of tea, a dark window behind. Nobody in the picture: the chair is the reader's. The top half of the image is quiet navy so the title sits in it; the bottom half glows.

Why this and not a house, a tree, or a pair of hands: hands and faces force a gender, an age and a skin tone, and this book is for every parent and grandparent. A tree with roots is the category cliché. The table scene is warm, not sad, and it shows the product (a book you write in by lamplight) without a single word.

Style is **painterly, not photographic**. Painterly hides the 2x upscale from the image model, looks like a literary hardcover rather than a stock photo, and matches the heirloom feel of the interior.

## 2. The prompt (paste into ChatGPT Image 2 HD)

Generate **portrait, 2:3** (the tallest option the tool offers). Make 4 to 6 variations and pick with the checklist in section 3.

```
A painterly book cover illustration, portrait orientation, no text anywhere.

Scene: an old wooden kitchen table at night, seen from a slightly raised angle, lit by a single warm brass table lamp just outside the frame on the right. On the table, an open hardbound journal with cream pages lies in the centre, a fountain pen resting diagonally across the right-hand page. Beside it, a small stack of old faded photographs with white borders, a pair of folded reading glasses, and a cup of tea with a thin curl of steam. The journal pages carry a few loose lines of handwriting suggested only by soft pen strokes, not readable words. Behind the table, a dark window shows a deep blue night with a faint reflection of the lamp.

Composition: the upper 45 percent of the image is quiet, deep navy darkness with the lamp's warm light fading upward into it, kept empty for a title. The lower half glows amber around the journal. The journal is the brightest object and reads clearly even when the image is small.

Style: modern editorial oil painting with soft visible brushwork, cinematic chiaroscuro, restrained and premium, like the jacket of a literary hardcover. Palette: deep navy (#1e2838), warm amber lamplight, cream paper, dark walnut wood. The left edge and the top edge of the image fade into solid deep navy.

No people, no hands, no faces, no text, no letters, no numbers, no logos, no borders, no frame, no vignette edge, no florals, no hearts, no candles, no sepia filter, no clutter.
```

If the tool has a separate negative or "avoid" field, paste this there too:

```
text, letters, words, numbers, watermark, signature, people, hands, faces, florals, hearts, candles, frame, border, vignette, sepia, photo-realistic, clutter, busy background
```

**Two alternates** if the table scene does not land after six tries:

- *Dusk porch.* "A wooden porch at dusk, one empty rocking chair with a closed journal and pen on its seat, a mug on the rail, warm light from the house window on the left, deep blue evening sky filling the top half of the image. Same style, palette, and negatives as above." (Warmer and more American; slightly more risk of reading as absence.)
- *The letter.* "A cream envelope and a folded handwritten letter, pen strokes only, no readable words, lying on dark navy linen beside a fountain pen and one faded photograph, lit from the upper right, top half of the image plain dark navy linen. Same style and negatives." (Cleanest at thumbnail; less warmth.)

## 3. Picking the output

Keep a candidate only if all seven are true:

1. The top 40 percent is dark and quiet. If a lamp, window or glow sits where the title goes, discard.
2. The journal reads as a journal at 160 px wide. Shrink the image to check.
3. No readable text, letters or near-letters on the pages or photographs. (Garbled text is the number-one AI tell; KDP reviewers and buyers both notice.)
4. No hands, no people, no reflections of people in the window.
5. The pen is one pen. The glasses have two lenses. The cup has one handle. Count things.
6. The lamp light is warm, not green or magenta.
7. The left edge is nearly solid navy, so it can feather into the spine.

## 4. Preparing the art

1. **Crop** to a 7.25 : 10.25 ratio (that is 7 x 10 plus bleed). From a 2:3 image, keep the full width and trim equal amounts off the top and bottom.
2. **Upscale** to at least **2175 x 3075 px** for the paperback and **2400 x 3425 px** for the hardcover (Photoshop Super Resolution, Topaz, or the model's own HD upscale). A painterly image upscales cleanly; a photographic one does not, which is one reason for the style.
3. **Color:** leave in RGB. KDP converts. Do not push saturation; matte laminate flattens everything about 10 percent, so the print is always a little duller than the screen.
4. **Scrim:** in Illustrator, lay a rectangle over the top of the art with a vertical gradient, black at 60 percent opacity at the top edge fading to 0 percent at 42 percent of the cover height. This guarantees the title reads on every print, whatever the model did with the sky.

## 5. Paperback wrap — Illustrator setup

**Document:** 14.885 x 10.250 in, RGB, 300 ppi (4466 x 3075 px). No document bleed; the bleed is already in those numbers.

| Zone | Left edge | Width | Notes |
|---|---|---|---|
| Bleed | 0 | 0.125 in all round | Art and navy must run to the document edge |
| Back trim | 0.125 in | 7.000 in | |
| Spine | 7.125 in | 0.635 in | 254 pages, cream (KDP calculator) |
| Front trim | 7.760 in | 7.000 in | |
| Safe zone | 0.5 in inside every trim edge | | KDP minimum is 0.25; 0.5 keeps type off the fold and the trim variance |

**Layers, bottom to top:**
1. Navy rectangle `#1e2838`, full document.
2. Front art, placed so it covers x = 7.760 to 14.885 and the full height (7.125 x 10.25 in). Scale to height, crop width.
3. Feather: a 0.6 in wide rectangle at x = 7.760, full height, gradient navy 100 percent on the left to navy 0 percent on the right. (Makes the spine join invisible.)
4. Scrim gradient (section 4, step 4) over the front only.
5. Type (below).

### Front text, positions measured from the front trim edges (x from 7.760 in, y from 0.125 in)

| Element | Text | Font | Size / tracking | Color | Position |
|---|---|---|---|---|---|
| Title | WHAT I WANT / YOU TO KNOW (two lines, caps) | Playfair Display Bold | 54 pt, tracking 40 (0.04 em), leading 58 pt | `#efe7d6` | Centered on the trim; top of the cap height at 0.85 in from the top trim. Block is 5.9 in wide; it sits inside the safe zone with 0.55 in to spare each side. |
| Tagline | *My stories. My memories. My words.* | EB Garamond Italic | 17 pt | `#efe7d6` at 95 percent | Centered; baseline 2.95 in from top trim (0.25 in under the title) |
| Author | Joshua Caleb Green | EB Garamond Medium, small caps | 14 pt, tracking 140 | `#efe7d6` | Centered; baseline 0.82 in above the bottom trim |
| Descriptor | A GUIDED LEGACY JOURNAL FOR PARENTS AND GRANDPARENTS | Inter Medium, caps | 8 pt, tracking 220 | `#efe7d6` at 90 percent | Centered; baseline 0.52 in above the bottom trim |

Add a soft drop shadow to the title and tagline: black, 55 percent, blur 0.06 in, no offset. It is invisible at full size and saves the title on any print that comes out lighter.

Nothing else goes on the front. No "200 prompts" badge, no series line, no imprint. The thumbnail has one job.

### Spine (x = 7.125 to 7.760 in, text rotated 90 degrees clockwise, reads top to bottom)

| Element | Font | Size | Position |
|---|---|---|---|
| WHAT I WANT YOU TO KNOW (caps) | Playfair Display Bold | 15 pt, tracking 80 | Starts 0.55 in from the top trim; centered on the spine width |
| Joshua Caleb Green (small caps) | EB Garamond Medium | 10 pt, tracking 140 | 0.35 in after the title, same line |
| W (imprint mark) | Playfair Display Bold | 9 pt, 75 percent | Upright, centered, 0.45 in above the bottom trim |

Keep every spine character at least 0.0625 in from the spine edges (KDP's rule). At 15 pt caps the text is 0.2 in tall on a 0.635 in spine, so it has 0.2 in each side.

### Back (positions from the back trim edges, x from 0.125 in)

Ground is the flat navy. No art on the back; the lower half is deliberately empty for the barcode.

| Element | Text | Font | Size | Position |
|---|---|---|---|---|
| Headline | Some things are too important to leave unsaid. | Playfair Display Bold | 23 pt, leading 27 | Left edge 0.85 in from the left trim, top 0.95 in from the top trim, column 5.1 in wide |
| Body (four paragraphs, verbatim from `06-cover/back-cover-copy.txt`) | *below* | EB Garamond Medium | 12.5 pt, leading 19 | Same column, 20 pt under the headline, 11 pt between paragraphs |
| Closing line | Write it while you're here. Keep it forever. | Playfair Display Bold | 15.5 pt | Same column, 18 pt under the body |
| Imprint | WORDS TO KEEP | Inter Medium, caps | 7.5 pt, tracking 260, 75 percent | Left edge 0.85 in, baseline 0.62 in above the bottom trim |
| Barcode | leave empty | | 2.0 x 1.2 in | Lower right of the back: 0.35 in from the right trim and 0.35 in from the bottom trim. KDP prints the barcode there. |

Body text, verbatim:

```
You know some of the stories. You know the person, or the version they've shown you. This book is for the rest.

What I Want You to Know is a guided legacy journal for a parent or grandparent to fill in by hand, for the people who will keep it. It starts with the house they grew up in and ends with a letter. In between are the questions nobody thinks to ask: what they were afraid of, what they changed their mind about, what they never said, what they hope you'll forgive, and what to do on the days you miss them.

Two hundred prompts, one to a page, with room to actually write. Pages where the family adds questions of their own. And a section near the end where the writer stops answering and speaks directly to you.

Their memories. Their wisdom. Their handwriting. Kept, for the people who will want it most.
```

Set the book title in the second paragraph in italic.

## 6. Hardcover wrap — Illustrator setup

KDP's calculator numbers for 254 pages at 7 x 10 (already confirmed in the Previewer for the current hardcover):

| | Value |
|---|---|
| Document | 16.399 x 11.417 in (4920 x 3425 px at 300 ppi) |
| Wrap (folds around the board) | 0.591 in all round |
| Back panel | x 0.591 to 7.788 in, y 0.591 to 10.827 in (7.197 x 10.236) |
| Spine | x 7.788 to 8.612 in (0.824 wide; safe area 0.699 x 9.986) |
| Front panel | x 8.612 to 15.809 in; the first 0.394 in of it (x 8.612 to 9.006) is the hinge |
| Visible front face | x 9.006 to 15.809 in (6.803 wide) |
| Barcode (if KDP needs it) | 2.0 x 1.2 in, right edge 0.25 in left of the back hinge (x 7.144), bottom 0.375 in above the bottom wrap line (y 10.451) |

**Layers:** navy full document; front art placed from the spine edge (x 8.612) to the document edge (x 16.399) and the full height, scaled to 11.417 in tall; feather rectangle 0.7 in wide at x 8.612, navy to transparent; scrim; type.

**Front text:** identical fonts and colors to the paperback, centered on the *visible face* (center line x = 12.408 in), not on the panel. Title 52 pt, cap-top 0.85 in below the top wrap line (y 1.44 in). Tagline baseline y 3.54 in. Author baseline 0.82 in above the bottom wrap line (y 10.0 in). Descriptor baseline 0.52 in above it (y 10.3 in).

**Spine:** same text, title 16 pt, centered on x = 8.200 in; starts 0.55 in below the top wrap line. Everything inside the 0.699 x 9.986 safe area.

**Back:** same column as the paperback, left edge at x 1.216 in (0.625 in inside the panel), top at y 1.54 in, 5.1 in wide. Imprint baseline at y 10.2 in. Keep the barcode rectangle clear.

## 7. Export and upload

1. **Export:** File > Save As > Adobe PDF, preset *PDF/X-1a* or *High Quality Print*, no marks, no document bleed settings (the bleed is in the page size), fonts embedded or outlined, images at 300 ppi. One PDF per format. Check the PDF's page size is exactly 14.885 x 10.25 (paperback) and 16.399 x 11.417 (hardcover).
2. **Thumbnail test before upload:** export the front only as JPG, shrink to 160 px wide, put it next to `front-thumb-160.png`. The title must read and the journal must be recognisable.
3. **KDP, paperback (live):** Bookshelf > paperback > Edit print details > Cover > upload the new PDF > Launch Previewer > approve > Publish. The book stays on sale with the old cover until the new one clears review (usually under 72 hours). The Amazon product image updates on its own a day or two later.
4. **KDP, hardcover (in review):** nothing can be changed while it is in review. When it goes live, repeat step 3 on the hardcover.
5. **AI disclosure:** the current answers say the cover has no AI imagery. The new cover art is AI-generated, so on each format's Content page set the AI-generated content answer for **images** to yes, "some" or "all" as applies, with "edited extensively" if you repaint in Illustrator. Text answers stay as they are. (This disclosure is not shown to buyers.)
6. **Amazon A+ and carousel:** the hero banner and infographic in `marketing/amazon/AMAZON_CONVERSION.md` are specified "in the cover's colors"; they still are. Re-shoot image 1 (cover on white) once the new printed copy arrives.

## 8. Fonts

All three are free under the SIL Open Font License, from fonts.google.com. Install the desktop files:

- **Playfair Display** (Bold, 700) — title, back headline, closing line, spine.
- **EB Garamond** (Medium 500, Italic 400) — tagline, author, body. Already used inside the book.
- **Inter** (Medium 500) — descriptor and imprint. Already used inside the book.

The title face changed from Cormorant Garamond to Playfair Display on purpose. Side-by-side at 160 px, Cormorant's thin strokes vanish and Playfair's stay solid. Cormorant remains the interior's part-title face; the two are cousins and sit well together.
