# Portfolio — the four books after the flagship

Built in this order. Each folder holds its brief, manuscript, listing, back cover copy, and build.

| # | Book | Folder | Status | Target |
|---|---|---|---|---|
| 1 | The Stories I Made Up | `01-stories-i-made-up/` | Interior built (116 pp), placeholder wrap built, listing written. Awaiting cover art. | Live by Oct 20, 2026 |
| 2 | Still Me | `02-still-me/` | Not started | Live by Jan 2027 |
| 3 | Lo Que Quiero Que Sepas | `03-lo-que-quiero-que-sepas/` | Not started | Live by Mar 1, 2027 |
| 4 | The Words We Brought With Us | `04-words-we-brought-with-us/` | Not started | Live by mid-Apr 2027 |

Cover prompts and KDP dimensions for all four: `COVER-PROMPTS-AND-DIMENSIONS.md`.

## Build commands

```
# interior
python3 05-interior/build_interior.py --manuscript 09-portfolio/01-stories-i-made-up/MANUSCRIPT.md --out 09-portfolio/01-stories-i-made-up/build

# paperback wrap (placeholder or final; drop finished art in via Illustrator, or pass the same title/ink to this script)
python3 06-cover/build_cover.py --no-concepts --title "The Stories<br>I Made Up" --tag "Every story I ever told you, written down." --back 09-portfolio/01-stories-i-made-up/back-cover-copy.txt --ink "#1e2748" --spine 0.29 --name paperback-wrap --out-dir 09-portfolio/01-stories-i-made-up/build
```

Spine for cream paper = pages x 0.0025 in. Confirm in KDP's Cover Calculator before upload.
