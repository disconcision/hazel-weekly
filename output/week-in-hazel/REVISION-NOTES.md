# Issue 001, revision 2

The original screenshot path returned JPEG bytes. I saved them under PNG extensions without validating the format, used small crops, and preserved their JPEG encoding in the PDF. The earlier QA claim of native HiDPI fidelity was wrong. This was a capture/export and verification mistake, not an intrinsic PDF limitation. The tool’s screenshot method did not expose a format selector; native browser export supplied real lossless PNGs.

All three plates were recaptured through Firefox’s built-in screenshot UI at 180% zoom, with tighter compositions and intentional panels. The native PNGs are 2456×1454 (Cards), 2647×1051 (Fumola) and 3271×1256 (modular editors), about 378, 407 and 503 pixels per inch at the 6.5-inch printed width. No upscaling or image retouching was used. ReportLab embeds them losslessly, without resampling. The dark left-edge sliver in the Cards plate is gone. The tiny playing-card artwork remains intentionally pixel-art in the application.

The clean and woodcut editions share the ten-page layout. Three ImageGen edits use each new capture as the content reference and the cabinet illustration as the style reference. These are attempts at faithful engraved reproductions, not pixel-exact screenshots. The Fumola result icon becomes an equals-like mark instead of its original three-bar form; card details and other small glyphs vary. Overall program layout and the stated results remain recognizable. The clean plates and saved Fumola source are authoritative for exact syntax. No generated plate is used as evidence.

Added restrained double-mat frames and selective ornamental initials, moved issue flow plus a separately timestamped open backlog to page 3, expanded two-column reporting and the closing bookmarks, and made the statistics methodology easier to scan. The page-5 diagram now explains Card + Hand → (Card, Hand) → insert → Hand and sort : Hand → Hand, using the page-2 program and inspected CanvasGraph extraction rules. It remains explicitly an editorial explainer, since the canvas preview was unavailable. The original schematic was too generic to earn its space.

The four-page Field notes / Night shift style lab also uses the clean PNGs and new frames. The weekly charter now contains format verification, edge inspection, print-resolution checks, layout direction and optional-facsimile rules. Existing continuity and anti-repetition policies remain in force. The active weekly schedule is unchanged.

The built-in ImageGen tool made all three selected facsimiles; exact prompts are in WOODCUT-PROMPTS.json. The first output for each was selected. Source captures, generated outputs and their provenance are in image-ledger.json. No Hazel application code was changed, and nothing was distributed externally.

## Revision 3 — final refinement

Woodcut screenshots now have no added border or mat. Clean plates retain one green rule, red corner strokes and a single 4 pt cream mat. Callouts use uneven angles and nicked edges with sparse ink texture; the tidy folded corners are gone. Chart texture stays inside exact numerical boundaries. The existing three facsimiles are unchanged.

Expanded the reporting through concrete drawer behavior, the Modules greeting/interface example and explicit join boundary, agent probe settling, and six malformed tutorial hidden tests. Reduced the Cards plate to six inches wide, giving about 409 ppi.

The issue is now eleven pages. Constellation has a dedicated page with a real, tightly cropped Scorekeeper graph and reporting on canvas mode, sample interactions, module hull timing and camera behavior. The old schematic is removed. The hosted preview URL returned 404, and the latest release deployment failed on two unused-code warnings. An isolated development build of the exact captured branch head succeeded without source patches. That distinguishes a failed preview URL from an unobservable feature; see SOURCES.md and the saved logs.

One new stamp plate was generated for Constellation using the lightly stamped Cards image as its style reference. It preserves the visible named nodes, arrows and test dots; it is still a generated facsimile, not technical evidence. Original existing facsimiles were not regenerated. Built-in ImageGen was used; the executed prompt is in WOODCUT-PROMPTS.json.

PRODUCTION.md is the portable generation brief, tied to this revision as its worked example. It records borderless stamp images, irregular paper shapes, stronger coverage and the local-build fallback. Cards remains the primary style exemplar; RunningSums is a contrast example. No installed skill was created. Prior revision-2 PDFs and source are preserved in revisions/r2/.

## Revision 4 — concrete reporting and a typography pass

- Eleven-page clean and woodcut editions retained, with about 12% more extracted words than revision 3. Cover, comic and four screenshot assets unchanged; the Cards plate is slightly smaller to accommodate the expanded lead.
- Three real AI reporting agents audited the saved evidence. The masthead credits Ellis, Rowan and Mica for this revision, with Astra as editor. Earlier editions did not use reporter agents. Full scope and reports are linked from PROCESS.md.
- Rewrote the feature copy around observed behavior, concrete failures, design boundaries and source-attributed limits. Removed the desk/room passage, “tiny betrayal,” “keep the fence,” and other decorative conclusions. Tutorial, module, evaluation, Fumola and benchmark explanations are more specific.
- Body text stays ragged-right. Added conservative dictionary hyphenation, short-ending protection and smaller true paragraph gaps. Retained approximately 11 pt feature text and the established visual grammar. Compared against justification, then proofed the actual pages.
- Earlier revision-3 PDFs, source and production records are preserved in revisions/r3/. No new screenshot generation, application edits, GitHub messages, metric refresh or schedule change was performed for this prose revision.

## Revision 5 — internal readers, browser paragraphs, preserved art direction

- Audited every article, caption and note for the internal Hazel audience. Removed draft-history language, absent-source statements, file-format commentary and editorial assignments from the published issue. Credits are concise; readiness, benchmark scope and source attribution remain.
- Replaced the closing editorial plan with four technical questions: probe metadata lifetime, nested module narrowing, copied runtime state and legibility across agent edits. The existing continuity rules remain in the kit.
- Paragraphs now use Chrome HTML/CSS with `text-wrap: pretty`, hyphenation, kerning and natural float flow for drop caps. The generator measures and checks actual browser geometry. The original ReportLab display type and artwork are retained, and the clean PNGs remain byte-for-byte equivalent after decoding from the final PDF.
- Restored independent spacing for the style studies and deliberate display-line arrangements. Compared with the original studies rather than treating the preceding draft as the sole visual baseline.
- No new feature harvest, screenshot generation, benchmark run, repository-source change, publication or schedule change. Prior revision-4 files are archived in revisions/r4/.
