# Publishing Guide — Getting WHAT I WANT YOU TO KNOW onto Amazon

A step-by-step path from the files in this repo to a live listing. Each step says what you do, what
you need from the repo, and what to send back so the files can be finalized. Estimated calendar time
from Step 1 to a live paperback: three to four weeks, most of it waiting on the proof and on KDP review.

Files you will upload (all ready now):

| File | Path | Used at |
|---|---|---|
| Interior PDF | `05-interior/build/interior.pdf` | Step 6 |
| Paperback cover PDF | `06-cover/build/paperback-wrap.pdf` | Step 6 |
| Hardcover cover PDF | built in Step 9 to KDP's numbers | Step 9 |
| Description, keywords, categories | `07-amazon/STAGE-10-amazon-listing-and-launch.md` | Step 5 |

---

## Step 1. Open the account (day 1, about an hour)

1. **KDP account.** Sign in at kdp.amazon.com. Since you already publish on KDP, confirm the
   Account page is complete: publisher information, bank account, and the tax interview. Nothing
   else is needed before you start.
2. **Amazon Author Central.** At author.amazon.com, add Joshua Caleb Green as an author profile if it
   is not there already, with a short biography and a photograph. Books attach automatically.

## Step 2. ISBNs: let KDP assign them (no cost, no waiting)

KDP gives a free ISBN to each print format when you set it up, and that is what to use here.
On the Content page you click "Assign me a free KDP ISBN," and the number appears immediately.
The paperback and the hardcover each get their own.

What the free ISBN means, so the choice is deliberate:

- The Amazon product page lists the publisher as "Independently published." The copyright page
  inside the book still says Words to Keep, and the series name still appears on the listing.
- The ISBN can only be used for the KDP edition. If you ever print the same edition through another
  printer, that printer would need its own ISBN. That is a bridge to cross later, if ever.
- Expanded Distribution works with the free ISBN.

The copyright page has been built without an ISBN line, so the interior file is ready to upload as is.
The barcode KDP prints on the back cover carries the number. If you would like the ISBN printed on
the copyright page as well, send the number after KDP assigns it and the interior will be rebuilt;
it is a one-line change.

Buying your own ISBNs from Bowker is only worth it if you want "Words to Keep" shown as the publisher
on Amazon, or plan to sell the same edition outside Amazon. Neither is needed to launch.

## Step 3. Decide the publication date (day 1)

Pick a date about four weeks out. That leaves time for the proof (Step 7). KDP paperbacks cannot
be pre-ordered; the book goes live when you press Publish, and the release date you enter is what
shows on the page.

## Step 4. Confirm the spine (five minutes)

The interior is 254 pages. Spine width for KDP paperback on cream paper is page count multiplied
by 0.0025 inches, which is 0.635 inches. Confirm it in KDP's Cover Calculator
(kdp.amazon.com/cover-calculator) using: Paperback, Black & white, Cream, 7 x 10, 254 pages. The
calculator's full cover size should read 14.885 x 10.25 inches, which is what the cover file is.
If the numbers differ, send them back and the cover is rebuilt with:

```
python3 06-cover/build_cover.py --no-concepts --spine <spine> --bleed 0.125
```

## Step 5. Create the paperback in KDP: "Paperback Details" page (thirty minutes)

On the Bookshelf, choose **Create** and then **Paperback**. Fill the first page from the listing
document. Field by field:

| Field | Enter |
|---|---|
| Language | English |
| Book title | What I Want You to Know |
| Subtitle | A Guided Legacy Journal for Parents and Grandparents to Leave Their Stories, Memories, and Words to the People They Love |
| Series | Create a series: **Words to Keep**, this is Book 1 |
| Edition number | Leave blank (first edition) |
| Author | Joshua Caleb Green |
| Contributors | None |
| Description | Paste the HTML description from the listing document. KDP's editor accepts the bold, italic, and list tags used there |
| Publishing rights | I own the copyright and hold necessary publishing rights |
| Primary audience | Sexually explicit: No. Reading age: leave blank or 18 and up |
| Primary marketplace | Amazon.com |
| Categories | Choose three, as close as KDP's current browse tree allows to the three in the listing document |
| Keywords | The seven backend keyword strings from the listing document, one per box |
| Adult content | No |

**"Does your book classify as any of these types?" (low-content, large-print).** Leave both unchecked.

- *Large-print* means the book's text is 16 point or larger throughout. Our prompts are 21 point but
  the introductions, letters, and front matter are 12.5 to 13 point, so the book does not qualify.
  Checking it would add a "Large Print" label the book can't honor.
- *Low-content* is defined by KDP as "minimal or no content on the interior pages, generally
  repetitive, and designed to be filled in." KDP's examples include prompt journals, so read this
  carefully. Checking it removes four things this launch depends on: the free KDP ISBN, Expanded
  Distribution, series creation (the Words to Keep series page), and Look Inside unless you supply
  your own ISBN. This book has about 3,800 words of original written text: thirteen section essays,
  an opening letter, a giver's guide, instructions, 202 individually written prompts with sub-lines,
  and an index. It is not repetitive and not minimal, and comparable guided journals on Amazon
  carry Look Inside and series pages as ordinary books. Leave it unchecked.
- If KDP's review disagrees and asks you to reclassify it as low-content, the fallback is: buy one
  ISBN from Bowker (myidentifiers.com) so Look Inside stays on, accept that Expanded Distribution
  and the series page are unavailable, and republish. Tell me if that happens and I will adjust the
  copyright page and the launch plan.

**The AI content question.** KDP asks whether AI tools were used to create the text, images, or
translations, and distinguishes "AI-generated" (created by an AI tool, even if edited afterward)
from "AI-assisted" (you wrote it, AI helped edit or check). Answer it truthfully: the prompts and
the book's text were drafted by an AI tool and then edited and approved by you, which is
"AI-generated" text under KDP's definition, with edits. The cover is typeset by code from your
specifications and uses no AI-generated imagery. KDP permits AI-generated content when it is
disclosed and meets content guidelines; the disclosure is not shown on the product page. Answering
it wrongly is the one thing on this page that can get an account suspended, so answer it as it is.

Save and continue.

## Step 6. "Paperback Content" page (thirty minutes)

| Field | Enter |
|---|---|
| ISBN | **Assign me a free KDP ISBN.** Copy the number it gives you |
| Publication date | The date from Step 3 |
| Print options | Black & white interior with **cream** paper; trim **7 x 10 in**; **No bleed**; cover finish **Matte** |
| Manuscript | Upload `interior.pdf` |
| Book cover | Choose "Upload a cover you already have (print-ready PDF)" and upload `paperback-wrap.pdf`. Leave "barcode" to KDP; the white reserve on the back cover is where KDP places it |
| AI-generated content | Answered in Step 5 |
| Book preview | Launch Previewer |

**In the Previewer**, check these specifically:

1. Page 1 is the half title on a right-hand page, and Part One's opener (page 15) is on a right-hand page.
2. Every two-page spread prompt starts on a left-hand page.
3. No warnings about text outside the safe zone. The running foot sits 0.42 inches from the bottom trim, inside KDP's requirement.
4. The cover previewer shows the spine text centered on the spine with no overlap onto the panels.

If the previewer flags anything, note the exact message and send it back here.

Approve the preview. KDP reports the printing cost on the next page. At 254 pages it should be about
$5.32 for US orders (7 x 10 is a large-trim size, priced at about $1.00 plus $0.017 per page).

## Step 7. Order a printed proof before publishing (one week of waiting)

On the "Paperback Rights & Pricing" page, do not publish yet. Set the price first (Step 8), then
click **Request printed proofs**. You pay the print cost plus shipping. The proof arrives with a
"Not for resale" band across the cover.

When it arrives, check with a pen in hand:

- Write on a prompt page near the middle of the book. Does the gutter margin let you write comfortably to the inner edge? It should.
- Are the gray writing lines visible under a lamp without being dark? If too faint, they will be raised from 39% to 45% and the interior rebuilt.
- Does the cover's ink color print deep, not purple or washed out? Matte laminate darkens slightly; that is expected.
- Is the spine text centered?
- Flip through every page once. Look for anything unexpected.

Send back a photograph of one written-on page and of the spine, plus any notes. Corrections are a
rebuild and a re-upload, and KDP lets you replace files before and after publishing.

## Step 8. "Paperback Rights & Pricing" page (ten minutes)

| Field | Enter |
|---|---|
| Territories | All territories (worldwide rights) |
| Primary marketplace | Amazon.com |
| Pricing | **$17.99** for launch. Change to $19.99 after fourteen days. The royalty shown should be about $5.47 at $17.99 and $6.67 at $19.99 |
| Other marketplaces | Let KDP convert automatically |
| Expanded Distribution | **Enable.** It lists the book with bookstore and library wholesalers at a 40% royalty. At $19.99 that clears about $2.68 per copy |
| Release date | Confirm |

Press **Publish**. KDP review takes up to 72 hours; usually less than 24. You receive an email when
the book is live. The product page appears without images or reviews for the first day or two.

## Step 9. Hardcover (after the paperback is approved)

1. On the Bookshelf, under the paperback, choose **Create hardcover**. KDP copies the details; check them.
2. Print options: Black & white, cream, 7 x 10, no bleed, matte.
3. ISBN: assign a free KDP ISBN for the hardcover (it gets its own).
4. **Cover:** upload `06-cover/build/hardcover-wrap.pdf`. It is built to KDP's calculator numbers
   for Hardcover, Black & white, Cream, 7 x 10, 254 pages: full cover 16.399 x 11.417 in, panels
   7.197 x 10.236, wrap 0.591, hinge 0.394, spine 0.824 with a 0.699 safe area, margin 0.125.
   If the calculator ever shows different numbers (a page-count change), rebuild with:
   ```
   python3 06-cover/build_cover.py --no-concepts --hardcover --full-w <full width> --full-h <full height> --panel-w <front cover width> --panel-h <front cover height> --hinge <hinge> --hc-spine <spine> --hc-wrap <wrap>
   ```
   The script checks that two wraps plus two panels plus the spine equal the full width and stops if they don't.
5. Upload the same interior PDF. Preview. Order a proof. Price at **$28.99**. Publish.

KDP links the two formats on one product page automatically when title, author, and subtitle match.

## Step 10. The product page, after it goes live (week 1)

1. **A+ Content.** In KDP, open Marketing, then A+ Content, and build the seven modules from the
   listing document. A+ needs photographs of the real proof, so shoot those first (Step 11). A+ takes
   up to seven days for Amazon to approve.
2. **Author page.** In Author Central, confirm the book has attached to the profile.
3. **Look Inside.** Amazon enables it automatically for print books within a week or two.
4. **Series page.** Confirm the Words to Keep series page exists (KDP, Bookshelf, series).

## Step 11. Photographs (week 1)

Use the printed proof, never a mock-up. Seven images are specified in the listing document.
Handwriting in the photographs should be real. Ask a parent or grandparent to fill in two prompts
and the giver's page, and photograph those. KDP's image uploader accepts JPG at 2,000 pixels on the
long side or larger.

## Step 12. Reviews and the first ads (weeks 1 to 4)

Follow the twelve-week plan in the listing document. The first three actions:

1. Give copies to twenty-five early readers now, and ask them to review honestly once the page is
   live. Amazon allows reviews of gifted copies when the reviewer says so and the gift was not
   conditional on a positive review. Do not ask family members who share your household; Amazon
   removes those.
2. Turn on an automatic Sponsored Products campaign from the KDP Marketing tab on the day the
   book goes live, at a $10 daily budget, to learn which searches convert.
3. At twenty reviews, start the manual keyword campaign and the competitor-targeting campaign
   described in the listing document.

## Step 13. Updating the book later

Any change to the text is an edit to `04-manuscript/MANUSCRIPT.md`, a rebuild, and a re-upload of
the interior in KDP. If the page count changes, the spine changes and the cover is rebuilt. KDP
re-reviews updated files within 72 hours and the listing stays live meanwhile.

---

## What to send back, in order

1. The chosen publication date (Step 3), and the ISBN only if you want it printed inside.
2. Any Previewer messages (Step 6).
3. Photographs and notes from the proof (Step 7).
4. The hardcover template numbers (Step 9).

## Costs to expect

| Item | Approximate |
|---|---|
| Paperback proof, shipped | $10 |
| Hardcover proof, shipped | $15 |
| Twenty-five early-reader copies at author price | $100 to $150 plus shipping |
| First month of Amazon ads | $300 |

No fee to publish on KDP. Author copies are sold at the print cost.
