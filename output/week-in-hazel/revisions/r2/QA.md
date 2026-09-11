# Issue 001, revision 2: final verification

Verified 2026-09-11T06:23:45.817294+00:00.

## Correction to revision 1

The previous QA note incorrectly described the screenshot path as native HiDPI fidelity. Inspection found JPEG bytes under PNG filenames, small crops and JPEG encoding preserved in the original PDF. That claim is withdrawn. Revision-1 QA and files are archived in revisions/ as historical records, not current evidence. See REVISION-NOTES.md.

## Final artifacts

- week-in-hazel-001.pdf: 10 pages, 2143 extracted words, 38 HTTPS links, zero off-page text characters.
- week-in-hazel-001-woodcut.pdf: 10 pages, 2150 extracted words, 38 HTTPS links, zero off-page text characters.
- week-in-hazel-001-style-lab.pdf: 4 pages, 370 extracted words, 6 HTTPS links, zero off-page text characters.

Rendered all 24 final pages with Poppler and visually inspected every page. Reviewed the screenshot pages at higher resolution; checked all edges, frames, source/caption separation, drop-cap wrapping, columns, graph labels, stats and comic lettering. No visible clipping or overlap remained.

All three clean screenshot assets are actual PNGs, verified by decoding. Their native RGB pixel bytes are exactly identical to the decoded image data embedded in the clean PDF. The two clean plates in the style lab also match exactly. No PDF image uses DCT/JPEG compression. This verifies both native resolution and absence of lossy re-encoding, not just a filename. Effective print resolution is 378, 407 and 503 pixels per inch.

The matching woodcut edition has intentionally generated facsimiles on pages 2, 5 and 6. Their overall layouts and visible results were compared with the clean captures; small glyph, card and UI details are not guaranteed exact. For example, the Fumola result icon has two bars instead of three. Captions identify the treatments, and the colophon names the clean edition as the exact reference. No generated plate supplies technical evidence.

Reopened all three PDFs with pypdf and pdfplumber. Page counts, image encodings, pixel fidelity, link format, page bounds and placeholder/replacement-glyph checks pass. Verification source is verify_pdf.py; file sizes and SHA-256 digests are in verification.json. These tests check embedded links, not future availability of external destinations.

The weekly source snapshot and activity counts are unchanged from the previously reproduced analysis. The new 344-issue open backlog is separately sourced and timestamped at revision retrieval; 12 opened and 4 closed remain fixed-window flows. The page-5 diagram now derives from the page-2 Cards example and inspected CanvasGraph.re rules. It is explicitly an explainer, not the unavailable preview UI.

Agent attribution remains a declared trailer count, separate from unverified signature headers; absent trailers mean unknown assistance. Feature-branch merges and shared-dev merges remain distinct, reported regressions/benchmarks stay attributed, and live branch screenshots are retrieval-time observations.

The weekly editorial charter includes lossless capture, print fidelity, edge/framing, two-column pacing, purposeful diagrams, optional-facsimile rules and the existing anti-repetition policy. The issue and image ledgers record this revision. No Hazel application source changed and nothing was externally distributed.
