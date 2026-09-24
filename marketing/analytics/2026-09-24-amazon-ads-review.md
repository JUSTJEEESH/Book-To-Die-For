# Amazon Ads review: 2026-09-24

Source: the three CSVs in this folder (campaign, search term, targeting exports from the Amazon Ads
console). Campaigns started 2026-09-21, so this covers three days.

## What the data says

| Campaign | Type | Budget/day | Impressions | Clicks | Spend | Sales |
|---|---|---|---|---|---|---|
| AUTO / Discovery / Paperback | Automatic | $8 | 1,523 | 1 | $0.24 | 0 |
| EXACT / High Intent / Paperback | Manual, exact | $8 | 0 | 0 | $0.00 | 0 |

Auto campaign by targeting group:

| Group | Bid | Impressions | Clicks |
|---|---|---|---|
| Substitutes (competitor product pages) | $0.40 | 1,486 | 1 |
| Close match (searches like the listing) | $0.60 | 24 | 0 |
| Complements | $0.20 | 9 | 0 |
| Loose match | $0.40 | 4 | 0 |

Search term report: one row, the ASIN that produced the single click (a substitute placement on a
competitor's page). Amazon's search term report only lists terms that earned a click, so there is
no search visibility yet.

## Diagnosis

This is not a sales problem yet. It is a delivery problem. Total spend across two campaigns in
three days is 24 cents against a $48 budget. Nothing has been tested.

1. The manual exact campaign has zero impressions. Either its keyword bids are under Amazon's
   floor for those terms, or the keywords are not yet relevant enough to a one-image, zero-review
   listing for Amazon to serve them.
2. The auto campaign is almost entirely serving on competitor product pages (substitutes), where
   our thumbnail sits under a book with hundreds of reviews. Search placements (close match) got
   24 impressions at a $0.60 bid, which means the bid is losing the auction.
3. One click in 1,486 impressions is a 0.07% click rate. Books normally see 0.3% to 0.5%. The
   sample is too small to conclude, but on competitor pages a cover with no reviews will always
   click poorly.
4. Any click lands on a page with one image and no reviews. Until the listing is fixed, ad spend
   is for learning search terms, not for sales.

## Changes to make now

| Where | Change | Why |
|---|---|---|
| Auto, close match | $0.60 to $1.00 | Search placements are the ones we want to learn from |
| Auto, loose match | $0.40 to $0.65 | Same |
| Auto, substitutes | $0.40 to $0.55 | Keep learning which competitor pages convert, without buying most of the traffic there |
| Auto, complements | leave at $0.20 | Low value for a book |
| Manual exact | Open the campaign, read the suggested bid next to each keyword, set each to the suggested median (expect $0.75 to $1.25). If a keyword shows no suggested bid, it has no search volume; replace it. | Zero impressions means the bids never entered the auction |
| Both | Budget $10/day is fine. Do not raise it until the listing has images and 10 reviews. | Spend without a converting page is waste |
| Both | Bid strategy stays "dynamic, down only" | Correct for a launch |

## What to judge, and when

- After 14 days and at least $50 of spend: which search terms got clicks (search term report), click
  rate by placement, and whether any click produced a detail page view that became a sale.
- Do not judge sales before then, and not until the listing carousel and A+ are live.
- Success in the next two weeks is: impressions in the thousands per day on search placements, click
  rate above 0.3%, and a list of 20 search terms with clicks to move into the manual campaign.

## Still needed from the console

The keyword list and bids inside the manual exact campaign (Targeting tab, export), and the
Placement report, so the search vs. product page split is exact rather than inferred.

## Addendum: the manual campaign's keywords (export received later the same day)

36 targets: 12 keywords, each in broad, phrase, and exact, every one bid at $0.55. Amazon's own
suggested bids show why the campaign is nearly silent:

- 13 of 36 targets are bid **below Amazon's low suggested bid**, so they never enter the auction.
- 15 more are under the median.
- Total impressions across all 36: 47, almost all from the four broad terms that happened to clear.

### Bid changes (apply in the console, Targeting tab)

| Keyword | Match | Now | Set to |
|---|---|---|---|
| memory book for parents | Exact | 0.55 | 0.80 |
| memory book for grandparents | Exact | 0.55 | 0.70 |
| grandparent memory book | Exact | 0.55 | 0.75 |
| parent memory book | Exact | 0.55 | 0.60 |
| life story journal | Exact | 0.55 | 0.65 |
| legacy journal | Exact | 0.55 | 0.60 |
| legacy journal for grandparents | Exact | 0.55 | 1.00 (Amazon says 1.40; cap it, watch it) |
| legacy journal for parents | Exact | 0.55 | 0.45 |
| grandparent legacy journal | Exact | 0.55 | 0.70 |
| family memory journal | Exact | 0.55 | 0.65 |
| family legacy journal | Exact | 0.55 | 0.45 |
| parent legacy journal | Exact | 0.55 | 0.40 |
| every Phrase target | Phrase | 0.55 | pause |
| every Broad target | Broad | 0.55 | pause in this campaign (see below) |

The low-suggested-bid keywords (family legacy journal, parent legacy journal, legacy journal for
parents at about $0.40) are cheap because almost nobody searches them. Keep them at the suggested
bid and expect little.

### Structure

The campaign is named "EXACT | High Intent" and should be exactly that: exact match only. Broad and
phrase in the same campaign compete with the exact terms for the same $8 and blur the search term
report. Move broad match to a second manual campaign, "BROAD | Research | $6/day", with the five
highest-volume roots only: memory book for parents, grandparent memory book, life story journal,
legacy journal, memory book for grandparents, each at Amazon's median.

### Keywords that are missing

Every keyword in the campaign is a category word. None of them is how a daughter types. Add these
as exact match, at the suggested median once the console shows it:

memory journal for mom · mom memory book · dad memory book · memory journal for dad · grandma
memory book · grandpa memory book · questions to ask your parents · questions to ask grandparents ·
mom life story book · dad life story book · gifts for mom who has everything · gifts for dad who has
everything · 70th birthday gift for mom · 80th birthday gift for dad · retirement gift for dad ·
new grandparent gift · life story book for grandparents · family history journal · grandparents
journal to fill in · mom journal to fill in

Never a competitor's brand name.

### What good looks like in fourteen days

Manual campaign: 300 to 800 impressions a day, click rate above 0.3%, spend near budget, and a search
term report with at least 20 rows. Auto campaign: close match carrying more impressions than
substitutes. Then, and only then, judge purchases, and only if the listing has its images and A+ by
then.
