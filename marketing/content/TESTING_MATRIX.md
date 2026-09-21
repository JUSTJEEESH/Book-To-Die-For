# Testing Matrix

Every major concept gets several versions before the engine decides anything about it. The matrix
is the same for every concept; the versions are made, posted at least three days apart on the same
platform, and compared in `../WEEKLY_MARKETING.md`.

## The eight versions

| Version | Treatment | What it tests |
|---|---|---|
| A | Emotional | Quiet, slow, the tender read of the prompt |
| B | Funny | The same prompt with the comic angle (there almost always is one) |
| C | Curiosity | The prompt withheld until the end; the hook is a question |
| D | Cinematic AI | An AI-generated conceptual sequence (`../ai-video/AI_VIDEO_IDEAS.md`), clearly conceptual |
| E | Simple text | Cream type on ink, nothing else |
| F | Real photograph | A real, permissioned old photograph with the prompt over it |
| G | Creator to camera | A creator (or the team, hands only) reading the prompt to a parent |
| H | Question only | The prompt alone. No hook, no framing, no CTA |

Not every concept needs all eight. The minimum is three: E (the baseline), plus the two the concept
most obviously wants.

## Worked example: "Your dad was 17 once."

| Version | Execution |
|---|---|
| A | Slow push on a real 1970s photo (permissioned); text: "Your dad was 17 once. He had a first car. Someone he loved. A plan that didn't work out. How much of that do you know?" |
| B | "Your dad was 17 once. Legally." Then three of Part Two's funny prompts, fast. |
| C | Black screen: "There's a version of your father you've never met." Reveal at 8 s: "He was 17." Then the prompts. |
| D | AV-01 "Dad Was 19" (the multi-decade cinematic montage). |
| E | Text: "Your dad was 17 once." Hold. Then "Describe your bedroom at sixteen. What was on the walls. What was hidden, and from whom." |
| F | One real photograph, a young man, 1978; the prompt "What did you look like? Be honest." |
| G | A creator asks her father "what was on your bedroom walls at sixteen?" and films the answer. |
| H | "Describe your bedroom at sixteen." Nothing else. |

## What "strongest response" means

Judged in this order, because each one is a stronger signal than the one before it:

1. Attributed purchases (Amazon Attribution), if the post carried a link.
2. Shares and sends (the "send to Mom" behavior the brand exists for).
3. Saves.
4. Comments containing a story (not just an emoji).
5. Watch-through (average percentage watched).
6. Views.

A version that wins on views and loses on shares did not win.

## Decision rules

- After three posts of a concept: keep the version with the best rank on the list above; retire the rest of that concept for 30 days.
- After a version wins twice on different concepts, it becomes the default treatment for that pillar.
- The Cinematic AI version (D) only proceeds to an ad if it beats E on shares. AI is expensive; text is free.
- Real footage (G) that wins organically goes to the creator program for more of the same.

## Logging

Each version is a row in `../CONTENT_DATABASE.md` (same concept ID, suffix the version letter:
C-01-E, C-01-A) and, if it is a test with a hypothesis, a row in `../experiments/EXPERIMENTS.md`.
