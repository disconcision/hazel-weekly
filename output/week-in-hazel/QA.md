# Issue 001 — revision 5 QA

Final verification: 2026-09-11T08:22:16.078579+00:00. Revision-4 PDFs, source and QA are retained in revisions/r4/.

## Automated checks

- week-in-hazel-001.pdf: 11 pages, 2864 extracted words, 46 HTTPS links, zero off-page characters.
- week-in-hazel-001-woodcut.pdf: 11 pages, 2869 extracted words, 46 HTTPS links, zero off-page characters.
- week-in-hazel-001-style-lab.pdf: 4 pages, 346 extracted words, 6 HTTPS links, zero off-page characters.

All verify_pdf.py checks pass: page counts, lossless image encoding, decoded screenshot pixels, HTTPS link format, page bounds, placeholder/replacement text and browser height guards. SHA-256 hashes and file sizes are in verification.json. Link availability was not exhaustively retested.

All four clean screenshot plates retain pixel-for-pixel identical decoded native RGB data. The two style-lab plates also match. No PDF image uses DCT/JPEG compression. Effective clean print resolution: Cards 431.3 ppi, RunningSums 503.2 ppi, Fumola 407.2 ppi, Constellation 314.4 ppi. Placements and assets remain unchanged from revision 4.

## Typography and visual proof

Paragraphs are now composed in actual Chrome 153.0.8010.36 HTML/CSS. Computed text-wrap is pretty; each main edition has 58 body paragraphs, ten of which change their layout in the measured pretty-versus-normal-wrap comparison. The six style-study body paragraphs have no difference in that comparison. Conservative hyphenation, font kerning and natural drop-cap flow also contribute. The old recursive-ascription paragraph improves with ordinary browser wrapping too; its improvement is not attributed exclusively to pretty. The browser comparison is retained at research/revision5-browser-proof.png with HTML and a reproducer.

Rendered and inspected all 26 pages with Poppler, then re-rendered and inspected both changed Wasm pages after the final code-identifier and numeric-range fix. Checked paragraph gaps, long compounds, drop-cap wraps, subheadings, source lines, chart geometry, screenshot edges and caption clearances. No visible overlap or clipping remains. Browser measurement reports zero overflows; bounds checks find zero off-page characters.

Compared all four style-study pages against the original issue-1 studies. Restored independent full-leading paragraph spacing and original ReportLab display-type placement; kept the approved rough scraps and authentic sharp screenshots. The HTML body layer is composited over native PDF artwork, without rasterizing the latter. Retained HTML files contain the text layer, not the complete illustrated magazine.

## Audience and reporting

Astra made the revision-5 pass using the saved source cache and three revision-4 reporting audits; no new reporting agents were assigned. The masthead gives concise contribution credits. Earlier-draft history, absent-source commentary, file-format discussion and future-editor assignments are absent from the published issue. The closing page offers technical questions; these are editorial synthesis, not new reported decisions. Readiness, merge targets, benchmark scope and attribution remain. AUDIENCE.md and PRODUCTION.md carry the reusable reader standard.

No full reharvest, feature execution or benchmark rerun occurred in this revision. Weekly counts and capture dates remain unchanged. The total word count is lower than revision 4 because production chatter and redundant phrasing were removed; both main editions remain eleven pages. No percentage-growth claim is made for this pass.

All screenshot and generated-art assets are unchanged. Known facsimile limits remain: small glyph/card details can drift, and Fumola’s result icon differs from the native UI. The clean plates are the exact-content reference. Woodcut plates remain borderless.

## Carried-forward local-build provenance

The exact captured agent-canvas head, 25c6c57790e89dfd62ca04792f16fa1a3864cdc9, built successfully with the development profile in an isolated worktree, with no tracked source edits. The hosted URL’s 404 and the release workflow’s two warning-as-error failures are documented in SOURCES.md and saved logs. Scorekeeper and Counter App loaded; graph and definition selection were inspected. A blank graph appeared once when switching demos with a definition open and recovered after reload; no claim of general stability or diagnosed regression is made. No LLM session was run, and motion semantics are attributed to code/tooltips.

The weekly automation remains unchanged. No tracked Hazel source was changed and nothing was published or sent to other people.
