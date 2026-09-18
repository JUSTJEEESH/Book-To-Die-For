# Manuscript format

`MANUSCRIPT.md` is the single source of truth for the interior. It is plain text with page tags so
the Stage 7 build script can lay it out without anyone retyping it.

| Tag | Meaning |
|---|---|
| `@@ page <kind>` | A front-matter or closing page. Kinds: half-title, title, copyright, given, blank, letter-opening, howto, ten, permission, contents, in-my-own-hand, for-the-reader, anything-else |
| `@@ opener <PART LABEL> \| <Title>` | Section opener page. Paragraphs that follow are the introduction. |
| `@@ prompt` | Full-page prompt. Next line is the prompt. A line starting with `>` is the sub-line. |
| `@@ prompt *` | Marked prompt ("the questions nobody thinks to ask"). |
| `@@ spread` / `@@ spread *` | Two-page prompt. |
| `@@ quick <Heading>` | Quick-ones page. Lines starting with `-` are the items. |
| `@@ finish <Heading>` | Finish-these-sentences page. Lines starting with `-` are the stems. |
| `@@ family` | A question from your family page. |
| `@@ special <kind>` | Special page. Kinds: family-tree (2pp), important-people (2pp), family-sayings (1p), songs (1p), recipe (2pp). Paragraphs that follow are its instructions. |
| `@@ photo` | An unruled page: "For a photograph, a drawing, or anything else." |
| `@@ letter <Heading> \| <pages>` | A letter page set. |
| `@@ skipline` | (Part Six only) Marks that every prompt page in this part carries the skip line. |

Text conventions: no em-dashes anywhere in the book. Sentences end. Sub-lines are short.
