# PDF size: initial audit and deferred optimization

Requested September 11, 2026. Cloud execution remains the priority. Andrew wants smaller downloads if possible, with **no visible quality loss**. This was a read-only inspection and in-memory compression measurement; no PDF was rewritten or published.

## What takes up space

Source: `output/pdf/week-in-hazel-001-woodcut.pdf`, 28,589,016 bytes (28.59 decimal MB; 27.26 MiB), 11 pages.

| Component | Stored bytes | Share |
| --- | ---: | ---: |
| Six images: cover, four stamp-treated screenshots, comic | 24,579,866 | 86.0% |
| Other streams: page drawing/text commands and font data | 3,972,868 | 13.9% |
| Remaining PDF structure | 36,282 | 0.1% |

Each of the six decoded RGB images matches an original asset in `output/week-in-hazel/assets/` by SHA-256 of its pixels. There are six distinct image streams, rather than repeated copies of the same large image.

The textured images are much larger than the clean UI captures even when their resolution is lower. For example, the Cards stamp plate occupies 3,522,982 bytes at 1630 × 965 pixels in the illustrated PDF; its clean RGB plate occupies 180,635 bytes at 2456 × 1454 in the clean PDF, plus a small alpha mask. The full clean edition is 14,520,065 bytes. Fine paper and ink variation appears to account for much of the difference; preserving that texture is part of preserving the approved aesthetic.

## Measured lossless headroom

The illustrated PDF's images use `/ASCII85Decode` around `/FlateDecode`. That outer text encoding adds size to already compressed binary image data. Its eleven page-content streams are also uncompressed after composition.

An in-memory audit decoded each stream and measured `zlib.compress(decoded_data, 9)`. It counted only streams with no decoding parameters and either no filter or a Flate filter, and retained the original size whenever recompression was larger. No image was resized, quantized, converted to JPEG, or otherwise changed.

- Removing the image encoding overhead and recompressing the exact decoded bytes saves a projected **4,920,416 bytes**.
- Compressing/recompressing the remaining eligible streams saves another projected **2,731,766 bytes**.
- Total projected saving: **7,652,182 bytes, or 26.8%**.
- Projected size: about **20.94 MB / 19.97 MiB**, before small changes to PDF object bookkeeping.

These are stream-size measurements, **not the size of a completed, verified optimized PDF**. The projected method preserves the decoded bytes exactly; implementation still needs to prove that a rewritten file retains the page structure, links, metadata, and rendering.

Flate compression and page-content compression are documented as lossless in [pypdf's file-size guide](https://pypdf.readthedocs.io/en/stable/user/file-size.html). [qpdf's optimization options](https://qpdf.readthedocs.io/en/stable/cli.html#optimizing-file-size) provide another candidate for a final packaging pass. Do not use a generic image-optimization preset without checking whether it converts images to lossy JPEG.

## Follow-up after the cloud trial

1. Implement a lossless packaging pass on a separate candidate file. Prefer eliminating ASCII85 overhead and compressing the final composed page streams. Evaluate additional lossless image prediction or object deduplication only if useful.
2. Verify every decoded image against its source, compare page count, dimensions, text and links, and render original/candidate pages with the same engine for pixel comparison. Inspect any differences before adoption. Preserve the approved original.
3. If the gain is useful, integrate packaging and size reporting into the cloud build and update the publication workflow. Record input/output sizes and verification results.

Near-lossless compression remains an optional later experiment. It cannot promise unchanged pixels and must not introduce visible damage to small code, punctuation, fine strokes, or the stamp texture. Pursue the measurable lossless saving first. Published PDFs remain unchanged.
