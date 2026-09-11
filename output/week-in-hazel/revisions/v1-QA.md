# Issue 001: final verification

Verified September 11, 2026 UTC.

- The main issue has 10 pages and 1,917 extracted words, including captions, labels and source links. The style lab has four pages: two two-page art-direction studies.
- Rendered both final PDFs with Poppler and visually inspected every page. Checked typography, page boundaries, spacing, captions, sources, charts, comic lettering and all three screenshot compositions. No visible clipping or overlap remained.
- Corrected a browser screenshot pixel-scale mismatch during proofing. Final layouts use native HiDPI captures with PDF clipping; the retained crop assets record the intended framing. Source code and runtime values are readable at the designed page size.
- Reopened both PDFs with pypdf and pdfplumber. Page counts are correct; no replacement glyphs, placeholder copy or off-page text characters were found. There are 38 HTTPS link annotations in the main issue and six in the style lab. These checks validate the embedded link format; they are not a promise that external URLs will remain available.
- Re-ran analysis against the saved branch and GitHub snapshot. Every metric matched the previously typeset values, including daily totals. Also exercised a different date window to verify that the reusable analyzer derives its daily labels and totals from the requested bounds.
- Source mapping is in SOURCES.md. Merged-to-dev and merged-to-feature-branch work are distinct. Benchmarks are attributed, live screenshot observations are labeled, and generated art is identified as editorial fiction or illustration.
- The agent-credit chart measures declared co-author trailers among SHA-distinct commit objects. Cryptographic signature headers are counted separately and were not independently verified. Missing trailers do not establish absence of assistance.
- The Constellation preview returned 404, so the issue uses a labeled schematic based on inspected source. The Fumola screenshot demonstrates a working bridge, not incremental reuse or performance. No Slack material was available.
- The weekly heartbeat is active. The issue and image ledgers mark the pilot ready and identify return triggers for future coverage. The next new issue ends September 18, 2026, at 00:00 UTC.

See verification.json for machine-readable page, word, link and file-size checks. No Hazel application source was changed, and no external distribution was performed.
