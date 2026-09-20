# Portfolio — the four books after the flagship

Built in this order. Each folder holds its brief, manuscript, listing, back cover copy, and build.

| # | Book | Folder | Status | Target |
|---|---|---|---|---|
| 1 | The Stories I Made Up | `01-stories-i-made-up/` | Interior built (116 pp), placeholder wrap built, listing written. Awaiting cover art. | Live by Oct 20, 2026 |
| 2 | Still Me | `02-still-me/` | Interior built (100 pp, 8.5 x 11, with a 3,800-word guide), placeholder wrap built, listing written. Awaiting cover art. | Live by Jan 2027 |
| 3 | Lo Que Quiero Que Sepas | `03-lo-que-quiero-que-sepas/` | Interior built (256 pp, Spanish labels throughout), wrap built (same cover as the flagship), listing written. **Needs the native editor's pass before publishing.** | Live by Mar 1, 2027 |
| 4 | The Words We Brought With Us | `04-words-we-brought-with-us/` | Interior built (104 pp), placeholder wrap built, listing written. Awaiting cover art. | Live by mid-Apr 2027 |

Cover prompts and KDP dimensions for all four: `COVER-PROMPTS-AND-DIMENSIONS.md`.

## Build commands

```
# interior
python3 05-interior/build_interior.py --photo-fill --manuscript 09-portfolio/01-stories-i-made-up/MANUSCRIPT.md --out 09-portfolio/01-stories-i-made-up/build

# paperback wrap (placeholder or final; drop finished art in via Illustrator, or pass the same title/ink to this script)
python3 06-cover/build_cover.py --no-concepts --title "The Stories<br>I Made Up" --tag "Every story I ever told you, written down." --back 09-portfolio/01-stories-i-made-up/back-cover-copy.txt --ink "#1e2748" --spine 0.29 --name paperback-wrap --out-dir 09-portfolio/01-stories-i-made-up/build
```

Spine for cream paper = pages x 0.0025 in. Confirm in KDP's Cover Calculator before upload.

```
# Still Me (8.5 x 11, with the flowing guide section)
python3 05-interior/build_interior.py --photo-fill --manuscript 09-portfolio/02-still-me/MANUSCRIPT.md --out 09-portfolio/02-still-me/build --trim-w 8.5 --trim-h 11 --extra-css 09-portfolio/02-still-me/stillme.css
python3 06-cover/build_cover.py --no-concepts --title "Still Me" --tag "A life-story book, filled in together." --back 09-portfolio/02-still-me/back-cover-copy.txt --ink "#e9e2d3" --text "#2b3a34" --trim-w 8.5 --trim-h 11 --spine 0.25 --name paperback-wrap --out-dir 09-portfolio/02-still-me/build
```

The build now supports `@@ flow FILE | LABEL | Title` for flowing prose sections (paginated by
Chromium with running feet and continuous page numbers, spliced into the interior with poppler),
`--trim-w/--trim-h` for other trim sizes, and `--extra-css` for per-book type overrides.

```
# Lo Que Quiero Que Sepas (Spanish labels via --lang es)
python3 05-interior/build_interior.py --photo-fill --lang es --manuscript 09-portfolio/03-lo-que-quiero-que-sepas/MANUSCRIPT.md --out 09-portfolio/03-lo-que-quiero-que-sepas/build
python3 06-cover/build_cover.py --no-concepts --title "Lo Que Quiero<br>Que Sepas" --tag "Mis historias. Mis recuerdos. Mis palabras." --back 09-portfolio/03-lo-que-quiero-que-sepas/back-cover-copy.txt --ink "#1e2838" --spine 0.64 --name paperback-wrap --out-dir 09-portfolio/03-lo-que-quiero-que-sepas/build
```

```
# The Words We Brought With Us
python3 05-interior/build_interior.py --photo-fill --manuscript 09-portfolio/04-words-we-brought-with-us/MANUSCRIPT.md --out 09-portfolio/04-words-we-brought-with-us/build
python3 06-cover/build_cover.py --no-concepts --title "The Words<br>We Brought<br>With Us" --tag "The words, the sayings, and the songs we still say." --back 09-portfolio/04-words-we-brought-with-us/back-cover-copy.txt --ink "#1f3a2f" --spine 0.26 --name paperback-wrap --out-dir 09-portfolio/04-words-we-brought-with-us/build
```
