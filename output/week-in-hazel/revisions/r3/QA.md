# Issue 001 — revision 3 QA

Final verification: 2026-09-11T07:12:18.786300+00:00. Prior revision-2 artifacts and QA are retained in revisions/r2/.

## Automated checks

- week-in-hazel-001.pdf: 11 pages, 2669 extracted words, 43 HTTPS links, zero off-page characters.
- week-in-hazel-001-woodcut.pdf: 11 pages, 2676 extracted words, 43 HTTPS links, zero off-page characters.
- week-in-hazel-001-style-lab.pdf: 4 pages, 370 extracted words, 6 HTTPS links, zero off-page characters.

`verify_pdf.py` checks page counts, image encoding, decoded image pixels, link format, page bounds and replacement/placeholder text. All pass. File sizes and SHA-256 values are recorded in verification.json. Link targets were not exhaustively availability-tested.

Four authentic PNG plates embed with pixel-for-pixel identical decoded RGB data in the clean PDF. The style lab’s two plates also match. No image in any of the three PDFs uses DCT/JPEG compression. Print resolution: Cards 409.3 ppi; RunningSums 503.2 ppi; Fumola 407.2 ppi; Constellation 314.4 ppi. Native graph dimensions are 847×1125 at 194 pt printed width; it was not upscaled.

## Visual inspection

Rendered all 26 pages using Poppler. Inspected every woodcut page and all four style-lab pages at reading resolution; inspected all four clean screenshot pages individually and compared the remaining shared clean layouts as a contact sheet. Checked borders, image edges, captions, drop-cap wraps, column flow, folios, callout interiors and chart endpoints. No visible overlap or clipping remained. Woodcut plates have no added frames; clean plates use one narrow green frame with red corner strokes. Paper scraps have irregular cut edges without page-peel corners.

All four facsimiles were compared with authentic captures. The new Constellation plate retains the named nodes, four integer nodes, function arrow directions and two test dots. Its typography, grain and small marks vary. Existing Cards/Fumola/RunningSums facsimiles were not regenerated. Known pre-existing differences include small card details and Fumola’s result icon changing from three bars to two. Generated images never supply technical evidence.

## Reporting and local build

The fixed weekly metrics remain unchanged. The 344-issue backlog is a separately timestamped September 11 stock; 12 opened/4 closed are weekly flows. New text is grounded in saved PRs and tracked code; the revised eleven-page issue adds substantive Constellation coverage and removes the old source-derived schematic.

The exact captured agent-canvas head, 25c6c57790e89dfd62ca04792f16fa1a3864cdc9, built successfully with the development profile in an isolated worktree, with no tracked source edits. The hosted URL’s 404 and the release workflow’s two warning-as-error failures are documented in SOURCES.md and saved logs. Scorekeeper and Counter App loaded; graph and definition selection were inspected. A blank graph appeared once when switching demos with a definition open and recovered after reload; no claim of general stability or diagnosed regression is made. No LLM session was run, and motion semantics are attributed to code/tooltips.

The production brief and continuity/image ledgers record the new page, local fallback, borderless facsimiles, rough scraps and preferred Cards stamp exemplar. The weekly automation remains unchanged. No tracked Hazel source was changed and nothing was published or sent to other people.
