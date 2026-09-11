# Back-issue release checks

All three PDFs were built and visually inspected, including every page and a full-size proof of each final comic page after the lettering cleanup. Source PNGs are embedded losslessly. The Python verification compares each embedded screenshot's decoded RGB bytes with its source image, rather than merely checking the filename extension.

| Issue | Pages | Extracted words | Screenshot pixels | PDF |
|---|---:|---:|---|---:|
| -100 | 7 | 2,113 | 2190 x 810 | 13.3 MB |
| -060 | 7 | 2,135 | 3345 x 1530 | 12.6 MB |
| -019 | 8 | 2,403 | 2100 x 930 | 13.6 MB |

- Zero body-text overflows in browser-measured allocations.
- Zero off-page PDF characters, replacement characters or placeholder markers.
- Every paragraph layer uses `text-wrap: pretty`; its line placement measurably differs from ordinary wrapping in 7, 9 and 7 body paragraphs respectively.
- All PDF images use lossless filters; no JPEG/DCT images.
- Each source screenshot appears once and matches the embedded pixels exactly.
- Linked source annotations point to the Hazel repository.
- Correct signed issue identifiers, reporting dates, folios, retrospective labels and actual editorial credits.
- All three historical dev builds exit successfully. Staged programs produce the visible historical results; the assistant screenshot deliberately shows its actual disabled Compose control. No AI service request was sent.
- Source-based figures describe the associated article's actual distinction or flow. The label-placement figure is a statement of review/test properties, not an executed branch demo.
- The final art pass removes prominent unrequested slogans. Inspect the retained original and correction prompts if revising the art.

Full structural checks, dimensions, PDF hashes and browser version are in `verification.json`. `verify.py` reproduces these checks. The first proof found two long cover decks, one long indentation spread and two small column overflows; local edits resolved them without shrinking the publication as a whole.

## Scope limits

The GitHub snapshot is current retrieval with historical filtering; mutable PR prose cannot alone establish past contents. No claim is made to reconstruct all branch pushes, deleted refs, issue reopenings, the historical outstanding backlog, or an exhaustive development census. Historical graphs and the pilot's all-ref graph have different denominators. Co-author trailers and signature-header presence are declarations/metadata, not a complete measure of agentic work.

The current Issue 001 output and its next weekly cutoff are preserved. No automation schedule, remote repository state or publication endpoint was changed.
