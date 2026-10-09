# Amazon Ads review: 2026-10-09 (18 days of data, since 2026-09-21)

Source: the four exports in this folder. Note: every export shows Clicks = 0 while cost accrues,
so the click column did not come through; click rate, cost per click, and conversion rate cannot
be computed from these files. Spend, impressions, purchases, and sales are intact.

## Totals

| | Spend | Impressions | Purchases | Sales | ACOS |
|---|---|---|---|---|---|
| AUTO campaign | $81.56 | 42,111 | 3 | $53.97 | 151% |
| MANUAL campaign | $90.83 | 12,311 | 1 | $17.99 | 505% |
| **Both** | **$172.39** | 54,422 | **4** | **$71.96** | **240%** |

Royalty on four paperback sales at $17.99 is about $22. The ads lost about $150 in 18 days.
Break-even ACOS at the launch price is about 30% (royalty $5.47 on $17.99). Current ACOS is eight
times that. Bids cannot close a gap that size; conversion has to, which means the listing.

## Where the money went

### Manual campaign by match type

| Match | Spend | Impressions | Purchases |
|---|---|---|---|
| Broad | $73.86 | 11,365 | 1 |
| Phrase | $14.01 | 260 | 0 |
| Exact | $2.96 | 686 | 0 |

The September review said: exact only in this campaign, broad in a small separate research
campaign at Amazon's median bid. What happened instead: broad bids were raised well above median
(memory book for parents broad at $1.60 against a $0.61 median; life story journal broad at $1.21
against $0.89), and broad took 81% of the manual spend. The exact-match terms, which carry the
buyer's intent, spent $2.96.

Three targets spent $71 and produced one sale:

| Target | Bid | Amazon median | Spend | Purchases |
|---|---|---|---|---|
| memory book for parents, broad | $1.60 | $0.61 | $33.21 | 0 |
| life story journal, broad | $1.21 | $0.89 | $22.42 | 1 |
| legacy journal, broad + phrase | $1.27 | $1.27 | $25.12 | 0 |

The manual campaign has grown to 155 targets. 39 of them have no suggested bid at all, which means
Amazon sees no search volume for the phrase; they are clutter. Several target the wrong intent:
"memory book for deceased parent" (a memorial book, bid $1.77) and "legacy journal for alienated
grandparents" are not this buyer. "this life of mine a legacy journal" is a competitor's title.

### Auto campaign by targeting group

| Group | Bid | Spend | Purchases | ACOS |
|---|---|---|---|---|
| Substitutes (competitor product pages) | $0.40 | $29.86 | 2 | 83% |
| Close match (search) | $0.60 | $50.10 | 1 | 278% |
| Loose match | $0.40 | $1.60 | 0 | |
| Complements | $0.20 | $0.00 | 0 | |

Substitutes is the best thing in either campaign. The auto search-term report shows one competitor
ASIN, 1452153817, produced a purchase; the rest of the substitute placements cost about 40 cents
each and did not.

## What to change

### Manual campaign

1. **Pause every Broad and Phrase target.** All of them. Broad has had 18 days and $74 to prove itself and produced one sale at a 125% ACOS.
2. **Delete the wrong-intent and competitor-title targets:** memory book for deceased parent (all three), memory book for deceased parent to complete (all three), legacy journal for alienated grandparents (all three), this life of mine a legacy journal (all three).
3. **Delete the 39 no-volume targets** (every row with a blank suggested bid). They do nothing and they hide the ones that matter.
4. **Set the remaining Exact bids to Amazon's median**, capped at $1.00:

| Keyword (Exact) | Now | Set to |
|---|---|---|
| memory book for parents | 0.78 | 0.96 |
| parent memory book | 0.58 | 0.96 |
| dad memory book | 0.61 | 1.00 (median 1.12, capped) |
| dad life story book | 0.62 | 1.00 (median 1.46, capped) |
| memory journal for mom | 0.80 | 1.00 |
| memory journal for dad | 0.52 | 0.60 |
| mom memory book | 0.80 | 0.82 |
| mom life story book | 1.22 | 1.00 (cap) |
| grandma memory book | 0.47 | 0.50 |
| grandpa memory book | 0.52 | 0.57 |
| grandparent memory book | 0.75 | 0.75 (leave) |
| memory book for grandparents | 0.68 | 0.68 (leave) |
| life story book for grandparents | 0.58 | 0.58 (leave) |
| life story journal | 0.61 | 0.61 (leave) |
| questions to ask your parents | 0.76 | 0.76 (leave) |
| questions to ask grandparents | 0.59 | 0.59 (leave) |
| family memory journal | 0.64 | 0.72 |
| family history journal | 0.48 | 0.48 (leave) |
| legacy journal | 0.59 | 0.60 |
| legacy journal for grandparents | 1.40 | 1.00 (cap) |
| new grandparent gift | 1.20 | 0.90 (low end; gift terms convert poorly without reviews) |
| 70th birthday gift for mom | 1.66 | 1.24 (low end) |
| 80th birthday gift for dad | 1.88 | pause until 20 reviews |
| gifts for mom who has everything | 1.81 | pause until 20 reviews |
| gifts for dad who has everything | 1.97 | pause until 20 reviews |
| retirement gift for dad | 1.63 | pause until 20 reviews |

The gift terms cost $1.60 to $2.00 a click against a page with no social proof. They are the
right terms for December, after reviews exist.

5. **Budget:** $6 a day. Exact-only will not spend more than that at these bids.

### Auto campaign

| Group | Now | Set to | Why |
|---|---|---|---|
| Substitutes | 0.40 | 0.50 | The only placement under 100% ACOS |
| Close match | 0.60 | 0.45 | $50 for one sale |
| Loose match | 0.40 | 0.30 | No sales |
| Complements | 0.20 | 0.20 | Leave |

Budget stays $8 a day.

### New: a product-targeting campaign

Create "PT | Competitor pages | $5/day", manual, product targeting, with ASIN 1452153817 at $0.55
(it already produced a sale) and the ten best-selling competitor ASINs from the category at $0.45.
This is the "substitutes" placement, bought on purpose instead of by accident. Add the ASINs that
produced clicks in the auto search-term report as they appear.

## The real problem, stated again

Four purchases from roughly $172 of clicks is a conversion problem, not a traffic problem. The
page received thousands of visits from people searching for exactly this kind of book, and almost
none of them bought. In the September review the fixes were: seven listing images, A+ Content, the
first twenty reviews. If those are not live yet, every dollar of ads is paying to show buyers a
page that cannot close them. The bid changes above cut the waste; they do not fix the page.

## Still needed

- Reviews, images, and A+ status on the listing as of today.
- An export that includes clicks (the campaign-level export, or a screenshot of the campaign
  manager with the Clicks column), so click rate and conversion can be computed.
- The manual campaign's search term report (the one uploaded covers the auto campaign only). The
  "life story journal" broad sale came from an actual search phrase; that phrase belongs in the
  exact list.
