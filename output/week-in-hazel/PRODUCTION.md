# Make the next Week in Hazel

This is the reusable production brief. Give an editor this Markdown, the example issue, and read access to hazelgrove/hazel. It is a working guide, not an installed Codex skill. The example demonstrates the voice and visual system; its stories, page assignments and metaphors are not a template to repeat.

## Start with these references

- **Worked example:** [Issue 001, revision 5, illustrated edition](../pdf/week-in-hazel-001-woodcut.pdf). Eleven pages, September 4–10, 2026 UTC. Use its visual restraint, source-linked writing and distinction between landed work and experiments.
- **Exact UI reference:** [matching clean edition](../pdf/week-in-hazel-001.pdf). The same reporting, with authentic lossless PNGs.
- **Default published screenshot treatment:** [Cards stamp facsimile](assets/probes-cards-woodcut.png), compared with [its original capture](assets/probes-cards-clean.png). Use this light stamped treatment for future zines and the proposed History of Hazel. Andrew explicitly reaffirmed this after reviewing the back issues. The much more heavily woodgrained [RunningSums treatment](assets/modular-focus-woodcut.png) is a contrast example, not the future target. Preserve the authentic PNG as the underlying evidence. Existing back issues are unchanged unless a revision is requested.
- **Editorial continuity:** [EDITORIAL.md](EDITORIAL.md), [issues.json](issues.json), [image-ledger.json](image-ledger.json). Read these before selecting stories. Inspect the last four issues and each topic's last appearance.
- **Evidence and mechanics:** [SOURCES.md](SOURCES.md), [collect.py](collect.py), [analyze.py](analyze.py), [build_zine.py](build_zine.py), [verify_pdf.py](verify_pdf.py). Code in this kit is a worked implementation, not a substitute for fresh reporting.

When these files travel, preserve the relative paths or update this reference list. Keep the example PDF and the Cards exemplar with the guide; prose alone cannot describe the desired degree of roughness precisely.

## Audience first

Read [AUDIENCE.md](AUDIENCE.md) before writing or revising. The readers are the people doing this work and a small circle of other Hazel contributors. Assume familiarity with Hazel while explaining changes outside a reader’s specialty. Every visible paragraph must make sense to someone who has never seen the production conversation. Draft history, missing data sources, renderer mechanics and instructions to a future editor belong in this kit. Preserve source and status qualifications that affect what a colleague can conclude or try. Keep credits brief and captions focused on what the example shows.

## The assignment

Make a small weekly magazine that Hazel contributors will want to read. Aim for roughly ten or eleven pages and 2,800–3,300 extracted words in a busy week, including captions and labels; the useful measure is whether the prose explains concrete consequences. A quieter week earns a shorter issue. Keep a major screenshot when it earns its space, but do not let images turn the reporting into captions. The current pilot fits detailed reporting into eleven pages. Its modestly reduced Cards plate and compact Modules map leave room for concrete explanation at legible body size.

Lead with a consequential merge into shared dev. Then select a few experiments, a small review or contributor interaction, an overlooked detail and a statistical view. Read PR descriptions, comments, reviews, issues and current branch code. Feature branches matter even without PRs, but their status changes the emphasis. This is selection, not a changelog dump.

Write with curiosity, affection and dry humor. Let the weirdness live in original illustrations and fictional comics. Write the trigger, behavior, consequence and status before adding stylistic flourishes. Keep occasional jokes, but remove ornamental conclusions and aphorisms that could describe almost any software project. A small concrete example usually deserves the space more. Do not invent dialogue, quotes, motives or personalities for contributors. A recurring contributor is someone whose work develops across issues, not a mascot or a repeated bio.

## Reporting workflow

1. Choose the next uncovered seven-day UTC window, ending Friday 00:00 UTC. The next issue after the pilot ends September 18, 2026 at 00:00 UTC. Do not regenerate an already covered window because a scheduler woke up. Use two or three earlier weeks for context, excluded from period counts.
2. Save a new dated research directory. Fetch remote refs without changing the user's checkout. Harvest paginated GitHub PRs/issues, reviews, discussion and a branch snapshot. The collector and analyzer examples are in README.md. Never reuse an old research directory for a new capture.
3. Read beyond the headline description. Follow corrections, review arguments and stacked dependencies; inspect code for selected claims. An edited PR body is retrieval-time evidence, not a perfect historical record. A recent commit timestamp does not establish a push event.
4. Build a story budget before typesetting. For each candidate, record its source links, status, concrete change, why a contributor should care, last coverage, fresh angle and possible image. A report without those answers may be only a brief.
5. For a substantial issue, assign bounded topic audits to reporting agents when available, while the editor does independent production or synthesis work. Ask for sourced findings, caveats and draft copy; keep their reports. The editor verifies and integrates, rather than stitching summaries together. Credit actual contributions only, with optional explicitly labeled AI pseudonyms. [PROCESS.md](PROCESS.md) distinguishes the pilot’s solo research from revision 4’s three real reporting audits. Add substance by explaining a small program, an interaction, a consequence, a design boundary or a review that changed the work. Do not pad with repeated experimental caveats, lists of internal filenames or generic praise. In the example, the name-and-age module scenario and six malformed tutorial tests are the kind of detail that earns more text.
6. Stage and capture images, write source-grounded copy, then typeset. Keep primary source links near the relevant reporting and fuller provenance in SOURCES.md. Label staged examples, measured versus reported results, and generated images.
7. Render every page, inspect the result, correct it, validate the final PDF, and update the ledgers. Produce the readable HTML edition and publish the PDF, cover and HTML to **andrewblinn.com/hazel/weekly/** as part of the weekly task, following [web/README.md](web/README.md). Verify the updated archive and live issue, then report completion with its URL and local PDF. This routine publication is authorized; do not send Slack/email messages or publish elsewhere without separate authorization.

## Status vocabulary and counts

Say **merged into dev**, **merged into a named feature branch**, **open PR**, **draft**, **branch only**, or **reported issue**, as appropriate. Verify base branches and merge timestamps. A large stacked diff is not all new work. A proposed fix does not make a reported regression resolved. If a preview fails, check the exact URL and deployment log, then try a local build in an isolated checkout. A 404 is evidence about one URL, not the feature’s existence. Use a labeled source-derived explainer only when running the feature is genuinely unavailable; never invent a screenshot.

Preserve the denominators: SHA-distinct reachable commit objects, committer timestamp window, merges, rebases/cherry-picks, the captured branch set and sampling limits. Separate declared agent co-author trailers from cryptographic signatures and bot identities. No trailer means assistance unknown. Do not estimate agent use from writing style, speed or volume. Never turn the count into productivity or percentage of code written by AI.

Issue openings/closures are flows within the fixed week. Outstanding issues are a stock at a stated retrieval time unless historical state is actually reconstructed. Put these counts beside issue reporting. Put a benchmark beside its workload, scope and attribution. The chart must remain numerically exact even when it looks printed by hand.

## Visual grammar

Use the example as the primary visual reference. Warm ivory paper, forest-black type, moss green, vermilion accents, occasional muted yellow and red paper slips. Linux Libertine supplies body and literary headlines; Rubik supplies a few bold statistical/cover forms; Liberation Mono supplies labels and code. In the pilot: page 540×720 pt, 36 pt margins, two 222 pt columns with a 24 pt gutter. Body around 11 pt with 13.5–14.5 pt leading. These are a coherent starting system, not immutable page coordinates.

- **Screenshot frames:** woodcut/stamp plates have **no added border, mat or corner marks**. The printed image is enough. Clean plates may use one green outer rule, small red corners and one narrow 4 pt cream mat; no inner rule or nested bands. Keep furniture outside authentic pixels.
- **Paper boxes:** filled scraps with uneven cut angles, nicked edges and asymmetry in their overall shapes. Tidy dog-ears and folded-corner icons are too neat; omit them. A modest paper shadow can help. Fine sparse ink flecks can suggest the printed surface. No default enclosing outline. Use the same treatment for issue counts, Modules reading-map cards, the Fumola note, chart counters and the dark benchmark strip. Leave text and numbers clear.
- **Diagram:** place it on the same paper slip, without a separate enclosing green rectangle. Keep source-derived relationships exact; slightly bowed pen strokes, quiet node cards and irregular paper give it affinity with the art. The illustration must explain a specific program or relationship. Do not add nodes to fill space.
- **Chart:** retain exact bar heights, stack boundaries and common baseline. Put light texture inside the fills; never shift quantitative endpoints to imitate a hand drawing. Label counts clearly and keep the legend consistent.
- **Drop caps:** use selectively at feature openings. Reserve the actual wrapped-line height and enough width for broad initials; never let the fourth line collide with the initial or its rule.
- **Page rhythm:** favor two columns for sustained copy. Use a full-width image or brief introduction when it earns emphasis. Avoid large unassigned bands. A little roughness should join the page elements together, not make every edge compete.

The pilot builder's `paper_patch`, `sketch_line`, `ink_bar` and `image` methods implement this grammar as vector page furniture. Preserve exact diagram labels and numerical geometry in code. New ImageGen calls are useful for conceptual art and comics, not necessary for every box.

## Paragraph typography

The current generator uses HTML/CSS in an isolated headless Chrome session for paragraphs, captions and drop-cap flow. Body text uses `text-wrap: pretty`, `hyphens: auto`, `hyphenate-limit-chars: 8 3 3`, normal kerning and common ligatures, with `lang="en-US"`. Keep code identifiers and names from inappropriate hyphenation. Ordinary word spacing and a ragged edge remain the default. `pretty` is browser-dependent; test the real engine, not just the existence of a CSS declaration. The worked build records the engine and compares the paragraph layout with ordinary wrapping in typesetting/metrics.json.

ReportLab retains the artwork, numerical chart geometry, labels and deliberately set display type. Chrome's text PDF is composited over that artwork without rasterizing it. This keeps the native PNG screenshots lossless. `build_zine.py`, `browser_layer.py` and `browser_typeset.cjs` form the generator. It runs a measurement pass and then builds with measured text heights; overflow blocks the final composition. The retained typesetting HTML is the text layer, not a complete browser edition of the illustrated magazine.

Use about 7 pt between ordinary paragraphs. Give the style studies their own full-leading spacing and preserve their original large display forms. Do not impose a body-density adjustment on every visual treatment. Short headings may use deliberately chosen line breaks; body paragraphs should flow. `text-wrap: balance` is an option for selected short headings in a future all-browser design, not a blanket paragraph rule.

Do not solve overflow by shrinking all the type. Rebudget a title, compress oversized furniture, move a paragraph, or add a page. Render every page and inspect the actual text. A height check must include subheadings as well as body boxes. Check drop-cap flow, long compounds, short last lines, consecutive hyphens and space around captions. Compare against the approved original art direction as well as the preceding revision.

## Screenshots and the preferred stamp treatment

Compose a photograph, not a window dump. Andrew authorizes scrolling, zooming, choosing panels, editing disposable scratch code, adding probes and rich literals, and staging examples. First write the sentence the image should make obvious. Then arrange source, relevant values and just enough UI context to establish the scene. Keep the staged source and build/branch provenance. Do not modify the repository just to dress a screenshot when a scratch document will do.

Inspect the full-resolution capture and all four edges. Exclude accidental sidebar slivers, cut-off headings, selection tools and empty panels. Aim for at least 300 pixels per printed inch, preferably 400 or more. Verify encoding from decoded bytes: the browser tool once returned JPEG despite a PNG filename. Export a real PNG through a native browser screenshot path if necessary. Firefox's built-in region screenshot at 180% zoom worked for the pilot. Never upscale or re-save an old JPEG and describe it as a new lossless capture.

Apply the light stamp treatment by default to published screenshots. First capture and verify the authentic high-resolution PNG, then use it as **content reference**, and the Cards stamp image as **style reference only**. Request exact code, punctuation, values, line breaks and UI geometry. The three original prompts were customized to their subjects but shared the same art direction; that did not produce a uniform texture level. The selected Cards image, not prompt similarity, is the visual standard. Use no added border, mat, corner marks or heavy woodgrain.

Prompt starting point, to adapt to the actual capture (the new Constellation plate uses a subject-specific version recorded in WOODCUT-PROMPTS.json):

> Reproduce reference 1 as faithfully as a meticulous stamp-maker reproducing a software screenshot. Reference 2 supplies only the restrained printed quality: slightly irregular ink edges, light pigment variation, warm pale paper, sparse fine grain and limited moss green/vermilion. Preserve every code character, label, value, card detail, line break and UI relationship from reference 1. Keep its aspect ratio and complete crop. Text and values must remain crisp and readable. The pale background should stay quiet, with no heavy horizontal woodgrain, dark bands, thick carved outlines, invented decoration or changed UI. Do not import subjects from reference 2. Favor the lightly stamped Cards exemplar over the heavily woodblocky RunningSums example.

Inspect the generated result against the original. Small glyphs can drift even with this prompt. Retain and link the clean capture, identify the treatment in a compact illustration note, and never treat its apparent output as new technical evidence. Record the actual prompt, input references, selected output and known limits. If the treatment changes meaningful content or reduces readability, correct it before publication; use a clearly recorded clean-image exception when exact details cannot survive the treatment. Do not silently skip the treatment because the original PNG is already sharp. Do not regenerate existing issues unless requested.

## Continuity without repetition

Read issues.json and image-ledger.json. For every returning subject, name what changed since its last visit. Prefer mostly new developments or new angles. A status change, new interaction, measured result, resolved design question, consequential failure or revealing review can earn a return. Routine activity gets a sentence and a link, not a recycled feature. A new capture of the same unchanged example is still repetition.

Bring a dormant topic back after roughly two or three months when there is a meaningful development or a useful retrospective. Give new readers a brief reintroduction. Keep a deferred-leads list and triggers for returning. Reviewers, documentation work and quiet fixes deserve attention alongside prolific committers. Keep visual compositions and comic premises fresh; the cabinet tree is not the mascot of every issue.

## Handoff and final verification

Deliver the PDF plus editable source, raw/selected research, source map, exact prompts, original captures, generated images, staged examples and updated ledgers. Keep prior issues and revisions; new weekly filenames must not overwrite them. Record dates, branches/SHAs, observed outputs and any source limits. Slack is optional additional context when connected and scoped; GitHub-only production can proceed.

Render every final page with Poppler and inspect it at reading size and enlarged for code, captions, irregular paper edges and image crops. Confirm no overlap or clipping, consistent folios, correctly directed diagram arrows, clear status and comparable chart definitions. Reopen the PDF, verify page count/text/links, and compare decoded embedded screenshot pixels with the native clean PNGs. A file extension or an attractive thumbnail is not enough. Keep a short honest QA record, including known limitations.

The weekly schedule already exists in Codex; this guide does not create another automation. EDITORIAL.md is its entry point and links here. Formal skill packaging can follow a review of this final draft; the current deliverable is portable production Markdown plus a worked example.

The [web archive handoff](web/README.md) records the personal-site destination, HTML builder and publication checks. Andrew selected **andrewblinn.com/hazel/weekly/** in place of hazel.org. Use the prominent red disclosure banner: “All content is fully AI-generated from the Hazel Git repository and GitHub data.” The second line reads “Reporting, writing and illustrations are all AI-produced.” The tagline is “A small digest for the hazelnut community.” Open HTML editions with large, unframed cover illustrations above their titles. Publish each new weekly issue here as part of the authorized recurring task; confine changes to that path and preserve other navigation and the `/hazel` redirect.

## Issue numbers and historical editions

Follow [NUMBERING.md](NUMBERING.md). Issue numbers are fixed to reporting weeks; Issue 001 anchors September 4-10, 2026, with 000 and negative numbers before it. Back issues retain their historical window, identify themselves as retrospectives and use period evidence.

## Historical calibration editions

[Back-issue kit](back-issues/README.md): Issues -100, -060 and -019 include exact-head build provenance, archived reporting, per-issue copy, new art, and a builder derived from this R5 system. Use `back-issues/analyze_periods.py` for the cutoff-dev census. Its denominator differs from the pilot's all-ref census; do not plot them as a like-for-like trend without recomputation.

Historical screenshots use isolated detached worktrees and fresh browser profiles. Stage concrete programs, preserve source PNG dimensions, and verify visible controls against the claimed readiness. An absent API key is acceptable when the feature being shown is configuration or availability; it does not establish a successful agent task. Do not configure secrets or spend API credits just to decorate an article.
