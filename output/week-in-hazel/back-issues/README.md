# Back-issue calibration set

Three full retrospective editions, produced September 11, 2026. This set tests the Week in Hazel process against different kinds of busy weeks, not merely the three largest commit totals.

| Issue | Reporting week (UTC) | Editorial center | PDF |
|---|---|---|---|
| -100 | September 27-October 3, 2024 | Bonsai migration, labeled tuples, warning policy | `../../pdf/week-in-hazel-neg100.pdf` |
| -060 | July 4-10, 2025 | Assistant landing, gated Compose mode, indentation, first reports | `../../pdf/week-in-hazel-neg060.pdf` |
| -019 | April 17-23, 2026 | Elastatics, compact function syntax, keyboard focus, pretty printer | `../../pdf/week-in-hazel-neg019.pdf` |

[Numbering](../NUMBERING.md) anchors 001 to September 4-10, 2026. The immediately preceding week is 000; weeks before that descend through -001, -002, etc. Calendar gaps keep their numbers. These artifacts are retrospective editions, not claims that the magazine existed in 2024.

## What the calibration found

1. **Merged implementation is not necessarily enabled UI.** The July assistant merge includes Task Completion machinery, but its historical `AssistantView.re` explicitly disables the Compose button. The local build confirmed it. The lead was corrected to distinguish the landed code from the public mode. Future reporting must check flags, controls and entry points as well as PR state.
2. **Today's graph leaks later landings into a historical census.** A first screen of today's reachable dev history found 60, 122 and 137 date-matching objects for these weeks. Restricting the census to each actual week-end dev revision gives 17, 41 and 65. Selection-screen counts remain in `selection.json`; the magazine uses only cutoff-head counts. These totals are not directly comparable to the pilot's all-remote-ref census.
3. **GitHub prose is mutable.** A current PR title/body may describe later revisions or stale design. The keyboard-focus body still refers to an abstraction subsequently removed in its dated discussion; the function-syntax implementation is more precise than its old shorthand explanation. Period code and dated comments take precedence.
4. **A merge has a destination.** The 2024 tuple change merges into `labeled-tuple-rewrite`, not dev. Each story labels that distinction. Later merges of #1405, #1765, #2222 and other open work are not imported into the covered week.
5. **Trailers, signatures and bot PR authorship are separate evidence.** Zero tracked trailers does not establish zero AI assistance. The April Copilot-authored PR would be missed by a Claude-trailer census. Signature presence is counted but cryptographic validity is not claimed.
6. **Historical builds are feasible.** All three exact dev heads built in detached worktrees with the existing editor-output opam switch. No historical tracked source was patched. Each screenshot uses a staged scratch program in that rebuilt UI. The assistant shot sends no model request and visibly has no configured API key.
7. **Length should follow the week's substance.** The two earlier issues use seven pages; April uses eight. Native screenshots explain observable behavior; source-derived diagrams explain architecture. Each issue has a fresh cover and a source-inspired fictional comic. The copy does not add biographies or filler to equalize page counts.
8. **Generated incidental lettering needs its own proof pass.** The first comic images added unwanted motivational slogans to props despite the prompts. An image-edit pass removes that writing, retaining the actual dialogue and scene. Future prompts and QA should treat every readable word in an illustration as publication copy.

## Reproduce or revise

- `neg*/copy.json`: editable article text, captions, source links and page structure.
- `build.py`, `layout.py`, `browser_layer.py`, `browser_typeset.cjs`: local edition builder derived from the approved R5 system. The pilot builder is unchanged.
- `analyze_periods.py`: regenerate historical metrics from git plus the archived GitHub metadata.
- `stage.cjs`: stage screenshot programs through actual UI events in isolated browser profiles. It expects local servers on ports 8920-8922 and the historical checkouts below.
- `ART-PROMPTS.json`, `COMIC-PROMPTS.json`, `COMIC-CLEANUP.md`: original art direction and correction history.
- `neg*/research/`: saved PR metadata, dated comments/reviews, issue records, metrics, screenshot programs and build provenance.
- `typesetting/`: generated editable HTML paragraph layers and browser-measured geometry.
- `QA.md`: release checks and limitations.

Run the builder with the bundled Python runtime:

```
/Users/andrewblinn/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 output/week-in-hazel/back-issues/build.py
```

It measures browser paragraphs, runs a second placement pass and rejects overflow. Body text uses `text-wrap: pretty` and controlled hyphenation, with ragged right columns. Cover/display type and artwork are native PDF objects; screenshots remain lossless PNG images. No global shrinking was used to make the articles fit.

Historical heads and worktrees are recorded in `selection.json` and each `research/build-provenance.json`. The week-end graph is reconstructed from the first-parent dev integration history. Surviving history cannot reconstruct every deleted private branch or historical push event. No historical outstanding-issue backlog is invented from today's count. Closed-issue totals are omitted because a current last-closure timestamp does not establish the complete closure/reopening flow.

These back issues are added to the date-indexed coverage and image ledgers. They do not advance the current weekly cutoff, renumber Issue 001, or change the existing automation.
