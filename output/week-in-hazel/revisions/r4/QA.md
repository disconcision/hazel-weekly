# Issue 001 — revision 4 QA

Final verification: 2026-09-11T07:39:49.639882+00:00. Revision-3 PDFs, source and QA are retained in revisions/r3/.

## Automated checks

- week-in-hazel-001.pdf: 11 pages, 2977 extracted words, 46 HTTPS links, zero off-page characters.
- week-in-hazel-001-woodcut.pdf: 11 pages, 2985 extracted words, 46 HTTPS links, zero off-page characters.
- week-in-hazel-001-style-lab.pdf: 4 pages, 363 extracted words, 6 HTTPS links, zero off-page characters.

All verify_pdf.py checks pass: page counts, lossless encoding, decoded screenshot pixels, link format, page bounds and placeholder/replacement text. SHA-256 and file sizes are in verification.json. Link availability was not exhaustively retested.

Compared with revision 3: clean 2669 → 2977 words (+11.5%); woodcut 2676 → 2985 (+11.5%). Counts include captions, labels, credits and folios. Both issues remain eleven pages.

All four clean screenshot plates retain pixel-for-pixel identical decoded native RGB data. The two style-lab plates also match. No PDF image uses DCT/JPEG compression. Effective clean print resolution: Cards 431.3 ppi, RunningSums 503.2 ppi, Fumola 407.2 ppi, Constellation 314.4 ppi. The Cards placement shrank to 410 pt wide; no image was resampled.

## Visual proof

Rendered all 26 pages with Poppler and inspected each clean, woodcut and style-lab page. Re-rendered and inspected the final changed pages after corrections. Checked body line endings, paragraph gaps, drop-cap wraps, subheads, source lines, chart geometry, screenshot edges and caption clearances. The first proof caught a wrapped page-3 subheading overlapping the paragraph; the final heading fits and has a height guard. A final single-word ending in the lead was joined to its preceding word. No visible overlap or clipping remains.

Compared three paragraph treatments at the actual column width before selecting ragged-right plus conservative hyphenation. The comparison is saved as research/typography-comparison.png. This is a PDF typesetting comparison, not a test of CSS pretty or a browser-support claim.

## Reporting and provenance

Three bounded reporting audits are saved and linked in PROCESS.md. The masthead credits those actual revision-4 contributions and distinguishes them from Astra’s solo original research. The editor integrated the copy, checked source qualifications and confirmed the six-module list against captured implementation. No full reharvest, new feature execution or benchmark rerun occurred in this prose revision. Weekly counts and their capture remain unchanged.

All screenshot and generated-art files are unchanged. Known facsimile limits remain: small glyph/card details can drift, and Fumola’s result icon differs from the native UI. The clean plates are the exact-content reference. Woodcut plates remain borderless.

## Carried-forward local-build provenance

The exact captured agent-canvas head, 25c6c57790e89dfd62ca04792f16fa1a3864cdc9, built successfully with the development profile in an isolated worktree, with no tracked source edits. The hosted URL’s 404 and the release workflow’s two warning-as-error failures are documented in SOURCES.md and saved logs. Scorekeeper and Counter App loaded; graph and definition selection were inspected. A blank graph appeared once when switching demos with a definition open and recovered after reload; no claim of general stability or diagnosed regression is made. No LLM session was run, and motion semantics are attributed to code/tooltips.

The production brief and continuity/image ledgers record the new page, local fallback, borderless facsimiles, rough scraps and preferred Cards stamp exemplar. The weekly automation remains unchanged. No tracked Hazel source was changed and nothing was published or sent to other people.
