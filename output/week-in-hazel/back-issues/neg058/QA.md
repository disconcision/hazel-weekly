# Issue -058 cloud-production QA

Verdict: **issue candidate complete; full production migration not ready**. This retrospective is unpublished. No live-site files, deployment, or scheduled task were created, enabled, changed, or disabled. The existing local Friday publisher remains the only active weekly publisher.

## Identity and cutoff

- Production input: `disconcision/hazel-weekly` at `36c0a703e8b84014dd5030e74de712f8f16f61d7`.
- Trial branch: `codex/cloud-back-issue-trial`.
- Calendar calculation: Issue 001 covers 2026-09-04 through 2026-09-11 UTC; 59 seven-day intervals earlier is Issue -058, covering 2025-07-18 through 2025-07-25 UTC (end exclusive).
- Historical Hazel cutoff: `dev` head `790b84e568197eb668591c4b05903aaeb6de20a9` at the end of the reporting window.
- Census: 61 cutoff-reachable commit objects (35 nonmerge, 26 merge), 12 PRs opened, 11 merged into `dev`, and 12 issues opened. Counts and scope are in `research/metrics.json`.

## Stage record

| Stage | Result | Evidence |
| --- | --- | --- |
| Production repository retrieval | Pass | Exact requested input revision checked out; current guides and ledgers read. |
| Hazel Git/GitHub evidence | Pass | Separate Hazel clone/worktree, portable census script, TSV/JSON snapshots, source map, dated PR/issue records. |
| Reference image generation/editing | Pass | Fresh cover and comic; two light Cards-style screenshot treatments; prompts and references retained. |
| Authentic screenshot evidence | Pass for this issue | Two original historical GitHub PNGs retained with SHA-256 hashes; treatments are explicitly labeled illustration. |
| Fresh native-PNG browser capture | **Fail** | Connected browser emitted JPEG/JFIF; Playwright Chromium archive timed out three times with zero bytes. |
| Historical Hazel build | **Fail** | OCaml 5.2.0 and npm dependencies installed; `make deps` stopped at missing `libgmp-dev`; `make dev` then lacked `dune`. |
| PDF authoring/rendering | Pass | ReportLab PDF, Poppler rendering, pypdf/pdfinfo inspection; every page visually checked. |
| HTML edition | Pass with preview limitation | Complete cover-led article, responsive single-column fallback, red disclosure, local assets and PDF. Static structure/assets pass; cloud browser blocks local `file://` URLs. |
| Durable export | Pass, with repository size exception | Review packages exported. Authenticated admin write was verified and sources/assets persisted on the trial branch; the 18,019,306-byte PDF is delivered separately because the connector rejects its 24 MB base64 request body above 16 MiB. |
| Publication/schedules | Intentionally untouched | No website or automation mutation. |

## Hazel build check Andrew requested

The historical source checkout had Git 2.51.1, GCC 13.3.0, Make 4.3, Node 24.19.0, npm 11.10.1 and Python 3.12.14. It initially lacked opam, OCaml, dune, m4 and pkg-config. The trial downloaded the official opam 2.5.2 static binary, initialized an isolated opam root, compiled OCaml 5.2.0, and completed `npm ci` (71 packages). The repository's `make deps` performed its repository setup, then exited 20 because `deps-of-hazel` requires the unavailable system package `libgmp-dev`. `make dev` exited 127 at `dune build --profile dev` because dune was not installed after the dependency solve failed.

`apt-get update` could not repair the image: its `_apt` privilege drop failed at `setgroups`, `setegid`, and `seteuid`, and apt could not execute its cache pre-invoke step. The smallest build fix is a cloud image/package layer containing `libgmp-dev`, `libffi-dev`, `libssl-dev`, `zlib1g-dev`, `pkg-config`, and `m4`; then rerun `make deps` and `make dev` in the isolated OCaml 5.2.0 switch. Until that passes, the environment has not shown it can build a feature branch or stage a fresh example.

## Native PNG capture check

The connected Chrome browser loaded the existing `https://hazel.org/build/backpack-2/` deployment. Its screenshot call returned 87,159 bytes with magic bytes `ff d8 ff e0 ... JFIF`: JPEG, not native PNG. `npx playwright install chromium` tried the Chrome-for-Testing 153.0.8010.12 archive three times; every `cdn.playwright.dev` request timed out after 30 seconds with zero bytes. A direct curl to the same archive also transferred zero bytes. The smallest fix is either a preinstalled Playwright-compatible Chromium/Firefox executable exposed to the job, or download access to that browser archive plus its shared-library dependencies. A follow-up must stage a disposable program in a freshly built historical/feature revision, capture it as PNG, and verify the `89 50 4e 47 0d 0a 1a 0a` signature.

Existing hosted builds and the two dated GitHub PNGs support this article's reporting. They do not prove that future jobs can build, stage, and capture independently. Therefore migration remains **not ready**.

## Artifact QA

- PDF: 8 pages, 540 × 720 pt, 2,169 extracted words, 35 link annotations, unencrypted, no JavaScript, no replacement characters or placeholder tokens.
- Images embedded in the PDF use lossless Flate encoding; file-size optimization is deferred as requested.
- Poppler rendered all eight pages at 150 dpi. Full-page and contact-sheet visual inspection found no clipped text, overlap, unintended frames, or broken images.
- The warning facsimile preserves the visible code/outline relationships; the scrollbar facsimile preserves the four EmojiPaint declarations and scrollbar-under-top-bar relationship. The original PNGs remain authoritative for exact pixels.
- HTML: one H1, seven article sections, three publication figures, complete unframed cover first, prominent red AI disclosure, local PDF, and six local image assets including both originals. Every referenced local file exists.
- SHA-256 (PDF): `e4ce4c1a5e115b9100c3b563c0f045d7b5c7fe2682608420d4b062ea866ab85d`.
- Exact commands and failures: `research/tool-transcript.txt`; fuller interpretation and setup: `research/cloud-build-check.md`.

## Portability and review controls

- The new Issue -058 builder discovers hosted fonts through `CODEX_PRIMARY_RUNTIME_ROOT` or `HAZEL_ZINE_FONT_DIR` and has no Mac dependency.
- Shared back-issue typography now accepts hosted Node/modules and an explicit browser executable/channel while retaining the historical Mac defaults for compatibility.
- Production `issues.json` and `image-ledger.json` were not modified. `proposed-ledger-updates.json` is the review-only change set.
- Authenticated GitHub persistence succeeded for editable files, evidence and PNG assets. Uploading the PDF blob failed exactly with HTTP 400: `MCP request body is invalid or exceeds the 16 MiB limit`; the PDF and its duplicate HTML-package copy therefore remain in the downloadable trial bundle rather than the hosted branch. The smallest remaining persistence step is to push the bundled local commit with a normal authenticated Git client (or install Git LFS and track the PDF) after review.
- The HTML is not copied into the live archive, and the website repository is untouched.
- A later handover must first review and integrate this candidate, then configure the cloud schedule paused; only after pausing and verifying the local `week-in-hazel-weekly-zine` schedule should the cloud replacement be enabled.
