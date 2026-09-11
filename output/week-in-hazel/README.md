# Week in Hazel — pilot production kit

Pilot coverage: **2026-09-04 00:00 UTC through 2026-09-11 00:00 UTC (exclusive)**. Context: August 21-September 3. GitHub was harvested and screenshots were composed September 11 UTC. Source records are a snapshot, not an event-perfect reconstruction of mutable PR prose.

- `../pdf/week-in-hazel-001.pdf`: eleven-page main issue, revision 5, with clean lossless PNG plates.
- `../pdf/week-in-hazel-001-woodcut.pdf`: matching eleven-page edition with ImageGen woodcut facsimiles of those same four captures.
- `../pdf/week-in-hazel-001-style-lab.pdf`: four pages, two thematic art directions. These are two-page studies, not full alternative eleven-page issues.
- `PRODUCTION.md`: reusable brief plus worked PDF example, preferred stamp exemplar, visual grammar, reporting workflow and verification.
- `EDITORIAL.md`: editorial decisions, screenshot direction, status rules, weekly workflow and anti-repetition policy.
- `issues.json`, `image-ledger.json`: continuity for future editors.
- `SOURCES.md`: claim-to-source map and evidence caveats.
- `PROCESS.md`: actual research history, reporting credits, editorial passes and typography rationale.
- `AUDIENCE.md`: the internal Hazel reader, relevance checks, appropriate qualifications and prevention of stylistic drift.
- `browser_layer.py`, `browser_typeset.cjs`, `typesetting/`: browser paragraph composition and measured layout. Retained HTML files are text layers; the complete magazine is the PDF.
- `assets/`: authentic screenshots and original generated art; `PROMPTS.md` records the image briefs.
- `research/`: raw GitHub responses, branch snapshot, commits and reproducible metrics.
- `collect.py`, `analyze.py`: read-only GitHub acquisition and commit analysis.
- `build_zine.py`: editable ReportLab layout/prose source for the pilot.

Rebuild the pilot with the bundled Python environment, with reportlab, Pillow, pypdf and the bundled Node Playwright package, plus installed Google Chrome. The font path in the builder points at the bundled LibreOffice fonts. On another machine, adjust it to licensed copies of Linux Libertine, Rubik and Liberation Mono.

```sh
/Users/andrewblinn/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 output/week-in-hazel/build_zine.py
```

The collector requires authenticated `gh` and the Hazel checkout. Use a fresh dated output directory for each future window. Do not reuse the pilot's `research/` directory or overwrite prior issue PDFs. Run `git fetch origin` first; do not check out feature branches in the user's working tree. Future editorial copy must be researched and written anew; the builder is not an automatic summarizer. See the charter for the full scheduled agent workflow.

No Hazel application source was modified, no changes were committed, and no GitHub or Slack messages were sent. Browser examples changed a scratchpad and added a probe to the local stored Mega 1k demonstration; those are editorial staging, not repository edits.

Example harvest for the next issue (run from the Hazel repository; execute at or after its cutoff):

```sh
git fetch origin
python3 output/week-in-hazel/collect.py --since 2026-08-28T00:00:00Z --until 2026-09-18T00:00:00Z --out output/week-in-hazel/issues/2026-09-18/research
python3 output/week-in-hazel/analyze.py --research output/week-in-hazel/issues/2026-09-18/research --start 2026-09-11T00:00:00Z --end 2026-09-18T00:00:00Z
```

The wider `--since` in acquisition supplies three weeks of context. Analysis uses only the issue's seven-day window. If a branch was pushed between fetch and acquisition, fetch again before analysis so every sampled tip is present locally. The collector resumes cached snapshots and does not silently refresh their timestamps; start a new directory for a new capture. Inspect discussions and current code independently after acquisition.

## Weekly schedule

The active Codex heartbeat **Week in Hazel — weekly zine** (id `week-in-hazel-weekly-zine`) runs Fridays at 9:00 a.m. local time; the current host timezone is America/Los_Angeles. It is attached to this task. The first new reporting window ends September 18, 2026, at 00:00 UTC; an earlier scheduler wakeup skips the already completed pilot. It delivers a new local PDF and readable HTML edition, and publishes each completed issue to **https://andrewblinn.com/hazel/weekly/** with an updated archive. This routine publication is authorized as part of the weekly task; Slack/email distribution and publication elsewhere remain outside its scope. Follow [the web archive guide](web/README.md) for the red disclosure banner, cover-led reading pages, publication checks and failure recovery. The live schedule is managed in Codex Automations, not by this file.

The revised editions use genuine PNG exports at native dimensions (847–3271 pixels wide, placed at 314–503 pixels per printed inch), placed directly with lossless PDF compression. Files ending `-clean.png` are the authentic captures; `-woodcut.png` are generated facsimiles. The older unsuffixed screenshot files and `-full.png` files contain JPEG bytes despite their extensions and are retained only as deprecated revision-1 evidence. They are never used by the revised builder. `REVISION-NOTES.md`, `QA.md` and `verification.json` explain the correction and final checks. Previous PDFs and builder are in `revisions/`; the exact new ImageGen prompts are in `WOODCUT-PROMPTS.json`.

Revision 3 removes every added frame from woodcut plates, uses irregular paper scraps and interior chart texture, expands the reporting, and adds a full Constellation page from a successful local build. Clean plates retain a single narrow frame. The selected Cards facsimile is the preferred light-stamp exemplar; the other generated assets have not been regenerated. This is production Markdown plus an example, not an installed skill. The revision-2 PDFs and source are preserved under `revisions/r2/`.

## Local Constellation preview

The isolated checkout is `/Users/andrewblinn/.codex/worktrees/week-in-hazel-canvas`, at `25c6c57790e89dfd62ca04792f16fa1a3864cdc9` (the captured `agent-canvas` head). No tracked source changes were needed.

```sh
cd /Users/andrewblinn/.codex/worktrees/week-in-hazel-canvas
opam exec --switch=editor-output -- dune build src --profile dev -j 4
cd _build/default/src/web/www
python3 -m http.server 8917 --bind 127.0.0.1
```

The preview is `http://127.0.0.1:8917/` while the server runs. Choose Documentation → Constellation. Setup used the existing `editor-output` opam switch, a symlink to the main checkout’s node_modules and `make setup-instructor` in this isolated checkout. Build and failed-hosted-deployment logs are saved under research/. See SOURCES.md for the precise 404 diagnosis and observed behavior.

Revision 4 deepens the prose by about 12%, keeps eleven pages, adds conservative hyphenation and paragraph spacing, and credits three actual reporting audits. See PROCESS.md. The revision-3 outputs and production files are preserved in revisions/r3/.

Revision 5 removes production commentary from the publication, turns the last page into open technical questions, and actually applies `text-wrap: pretty` in Chrome. Artwork, display type and native screenshot pixels remain in the PDF art layer. The entry command runs both measurement and composition. Revision-4 files are preserved in revisions/r4/. See AUDIENCE.md and the current PRODUCTION.md; Pyphen remains a dependency only for the archived revision-4 generator.

The [retrospective calibration set](back-issues/README.md) adds three full back issues with a permanent [numbering convention](NUMBERING.md), historical builds and production lessons. Issue 001 remains the current pilot; historical production does not advance the weekly schedule.
