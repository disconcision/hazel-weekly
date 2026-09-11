# Revision 4 reporting: workspace, Constellation, and runtimes

**Reporter:** Mica, an AI reporting-agent pseudonym; actual role: runtime and workspace reporting audit for editor Astra. This credit describes the new revision-4 audit, not the process that produced earlier editions. Use a small masthead credit if desired; no fictional biography or human authorship is implied.

**Method:** I read the existing issue prose, the saved bodies/reviews/comments for PRs #2469, #2427, #2505, #2492, #2504, #2509 and #2490, and the existing source/observation notebook. I selectively checked the actual downstream-evaluation fix, the canvas sample-routing fix, CanvasGraph's extraction rules, and current Fumola documentation at the captured branch SHAs. I did not refresh GitHub counts, run benchmarks or tests, browse the app, or repeat the screenshot sessions. Direct observations below remain Astra's recorded September 11 inspection.

## Ten concrete findings worth keeping

1. **The modular-editor feature is a context-preserving editing view.** Its outline opens definitions as header/body cells, but probes can collect calls outside the open cell and the master document supplies the result and tests. This explains precisely what the Mega 1k screenshot demonstrates. Pins/collapse and cell navigation are part of the ongoing draft, not necessarily new this week. [PR #2469](https://github.com/hazelgrove/hazel/pull/2469).
2. **A specific correctness repair gives that promise substance.** Previously, an edit after the first definition could leave the incremental evaluator reusing an old result: an ancestor's elaborated term omitted the changed suffix. `46bdb6b16e` includes the whole suffix in each relevant root and adds a regression test. The commit is dated September 8 UTC; the PR's September 9 addendum records its transfer from aria-demo. [Commit](https://github.com/hazelgrove/hazel/commit/46bdb6b16e).
3. **The performance review distinguishes a dirty dependency set from “only one item.”** The saved Codex review reports a Mega 4k surgical edit analyzing 16 of 891 items in 56 ms versus an 872 ms cold pass, under a headless harness. It also identifies an approximately 27 ms whole-text autosave floor at 4k despite 3–10 ms per-item writes. The body now acknowledges the latter. These are reviewer/author measurements and background for the design; do not turn them into measured browser speed or a fresh benchmark. [Review comment](https://github.com/hazelgrove/hazel/pull/2469#issuecomment-5486808215).
4. **Agent hardening has more content than merely “wait for probes.”** The open PR waits for evaluation in 150 ms checks, bounded at about ten seconds; supports owner/member paths in edit, view and probe tools; and moves persistence to per-chat records. Its description reports a fresh chat shrinking from roughly 152 KB to 2 KB. These changes arose during trials generating user-defined livelits. [PR #2427](https://github.com/hazelgrove/hazel/pull/2427).
5. **Constellation has a legible, specific visual vocabulary.** From cached statics, type aliases become nodes, functions become arrows between input/output types, values attach to their types, and tests attach to functions mentioned in the test. Multi-input functions have product nodes; builtin types use small local terminals. This is a type-oriented architectural graph, not evidence of a measured runtime execution trace. [CanvasGraph at the captured head](https://github.com/hazelgrove/hazel/blob/25c6c57790/src/web/app/canvas/CanvasGraph.re).
6. **The new main canvas mode and its value wells are practical editing work.** Canvas mode opens a selected definition below the graph and restores the full program on exit. The sample-routing fix sends clicks/arrow navigation to the whole-program editor whose values the wells display, rather than the active definition cell; it also outlines the selected sample. These before/after details explain the change better than a metaphor about a desk. [Mode](https://github.com/hazelgrove/hazel/commit/b1d83917ce), [restore/dismiss](https://github.com/hazelgrove/hazel/commit/8006692914), [sample fix](https://github.com/hazelgrove/hazel/commit/73325cb58c).
7. **Motion is implemented and source-grounded, but the magazine did not observe an LLM session.** Pace separates an edit burst into travel, act and settle; follow handles camera attention. Week commits synchronize module hulls with their nodes and keep the camera steady when the program remains visible. Attribute this to source and tooltips. The local inspection exercised Scorekeeper/Counter App and definition selection. A demo switch with a definition open once blanked the graph; reload recovered it. [Hull timing](https://github.com/hazelgrove/hazel/commit/03f4c2badc), [camera hold](https://github.com/hazelgrove/hazel/commit/a5b6dbf4c6), [toolbar code](https://github.com/hazelgrove/hazel/blob/25c6c57790/src/web/app/canvas/CanvasSidebar.re).
8. **Fumola's current API has four named roles.** `fumola_new` declares a runtime/mode; `fumola_put_force` evaluates within a named thunk; `fumola_eval` runs without an enclosing force; `fumola_with` passes a Hazel value as `input` and returns a Fumola result. The current docs explain first-order values crossing, with holes and functions refused. The old PR's two-form `thunk`/`editor` names are obsolete at the captured head. [Overview](https://github.com/hazelgrove/hazel/blob/583e84d07b/hazel-programs/docs/reference/fumola-0-overview.hz), [input example](https://github.com/hazelgrove/hazel/blob/583e84d07b/hazel-programs/docs/reference/fumola-5-input.hz).
9. **Runtime mode is a substantive limit on the incremental story.** The docs say runtimes default to Simple, which has a store/cached thunk results but no graph to inspect or repair. Graphical records the dependency graph and event history. A documentation example displays its events as a Hazel table. Neither the GCD/cell screenshot nor the reporter audit establishes repair/reuse. The overview itself describes graphical records as what repair “will need”; avoid presenting completed Adapton repair as a demonstrated result. [Runtime demo](https://github.com/hazelgrove/hazel/blob/583e84d07b/hazel-programs/docs/reference/fumola-6-runtimes.hz), [overview](https://github.com/hazelgrove/hazel/blob/583e84d07b/hazel-programs/docs/reference/fumola-0-overview.hz).
10. **The loader merges solve reproducibility problems, with a bounded claim.** #2504 tries local assets, fumola.org and the older Pages origin; #2509 reads a manifest and selects a matched glue/Wasm pair at content-addressed URLs, falling back to stable assets. Both merged into the Fumola feature branch, not dev. The selected version can be reported, but Hazel still does not lock the external runtime. The branch notes identify hand-written translation fixtures and skipped livelit tests as a gap in live-runtime coverage. [#2504](https://github.com/hazelgrove/hazel/pull/2504), [#2509](https://github.com/hazelgrove/hazel/pull/2509), [runtime notes](https://github.com/hazelgrove/hazel/blob/583e84d07b/docs/fumola-runtime-changes.md).

## Suggested workspace copy (~300 words)

### Edit a definition, keep the program live

Andrew Blinn's modular-editor draft lets a large program be edited through a collapsible outline. Opening a definition creates a focused cell for its header and body. The surrounding program still supplies its context, tests and result; a probe inside that definition can collect samples from calls elsewhere in the document.

Our Mega 1k capture shows `RunningSums.running_sum`, which accumulates partial sums in reverse order before reversing the list. We placed a probe on `total`. Its eight samples come from the enclosing program, whose result remains `true` below the focused editor. The small editing view is useful because it preserves those larger connections.

One of this week's fixes repairs a failure of that arrangement. Edits after the first definition could leave evaluation stuck on an old result. The incremental evaluator saw an apparently unchanged enclosing term and reused its previous answer, even though something below it had changed. Commit `46bdb6b16e` makes that term include the remaining program and adds a regression test.

The draft also reduces repeated work in analysis, drawing and persistence. A saved review measured a surgical Mega 4k edit analyzing 16 of 891 items, rather than running a full cold analysis. That supports the dependency-based approach, but it is a headless measurement, not a fresh browser benchmark. Whole-text fallback storage also leaves some document-sized work on the autosave path.

The related agent-hardening PR addresses what an assistant receives after an edit. Probe requests now wait for evaluation to settle, checking every 150 milliseconds for roughly ten seconds at most. Edit, view and probe tools can address module members through their owner/member paths. Per-chat storage reduces how much conversation state each update must handle. These remain open changes; together, they make focused editing and subsequent inspection more consistent for people and agents.

## Suggested Constellation copy (~330 words)

### A graph you can edit through

Constellation arranges a Hazel program by its types and definitions. Type aliases become nodes; functions become arrows from input to output; values attach to the types they inhabit. Tests appear beside the functions they mention. Module hulls group related definitions, while small builtin-type terminals keep common types such as `Int` from collecting every arrow in one place.

The Scorekeeper example makes that vocabulary readable. `Score` provides a base of 10, a doubling function and a cap of 50. `tally` adds the base to the bonus; `capped` limits the result. For an input of 7, the program returns 24. The graph shows the module grouping and function arrows, with passing-test dots beside `tally` and `capped`.

This week's main canvas mode makes selecting those shapes an editing action. We opened `tally` from Scorekeeper and `update` from Counter App and inspected their definitions below the graph. Leaving the mode returns to the whole program. This gives the graph a concrete navigation role: find a definition by its relationship to other types and functions, then work on its source.

The value wells needed a corresponding correction. Their samples came from the whole-program editor, but clicks and arrow keys were being sent to the active definition cell. The September 8 fix routes those actions to the editor that owns the displayed values and adds an outline around the selected sample. A separate repair keeps wells refreshing while a definition is open.

The agent animation work addresses how a series of edits is presented. Pace divides bursts into travel, act and settle; follow controls camera attention. Recent commits make module hulls move with their nodes and hold the camera steady when the program is already visible. These details come from source and toolbar text; we did not run an LLM session.

The branch remains a draft integration stack. Our local inspection also encountered a blank graph after one demo switch, recovered by reloading. Six demos now provide cases for further exploration, including nested modules, many callers and pipeline depth.

## Suggested Fumola copy (~260 words)

### A foreign runtime, with an address

Matthew Hammer's experimental Fumola integration lets a Hazel document name and use an external runtime. Livelits sharing an instance id communicate with the same store. Named thunks give successive edits a stable identity inside that runtime; separate instance ids keep their state apart.

The current branch has four entry points. `fumola_new` declares a runtime and its mode. `fumola_put_force` runs a program inside a named thunk, while `fumola_eval` runs without that wrapper. `fumola_with` sends a Hazel value across as `input`, so the boundary works in both directions. Its documentation doubles the input 21 and returns 42; holes and functions cannot be passed this way.

The choice of runtime mode matters. Simple is the default and keeps no dependency graph. Graphical records nodes, dependencies and events; one documentation example brings that event log back as a Hazel table. Our smaller screenshot verifies a GCD calculation and a named-cell read, producing `(6, 42)`. It does not demonstrate incremental repair or measure reused computation.

Two loader changes merged into the Fumola feature branch this week. One tries multiple runtime sources. The other reads a manifest naming a matched JavaScript/Wasm pair under a content-addressed URL, then reports which build loaded. This makes stale-runtime problems easier to diagnose.

Hazel still does not lock that external version. The branch's runtime notes also identify a test gap: hand-written translation fixtures exercise the boundary's expected formats, while the evaluator suite skips the four live Fumola forms. Those tests can stay green when the published runtime changes incompatibly. The loader work improves observability; end-to-end runtime coverage remains unfinished.

## Wasm: retain the corrected result, add a more concrete limitation

The current page already uses the right 3.0–4.1× range and roughly 3.5× summary. The useful amendment is why fixed precision matters: Hazel's `Int`/`Nat` require arbitrary-precision support that the spike has not ported; the successful workloads use `SInt` and `Float`. Keep the deliberate livelit deletion / not-for-merge caveat.

Suggested replacement or insertion (about 100 words):

> The successful workloads use `SInt` and `Float`, avoiding the arbitrary-precision runtime required by Hazel's ordinary `Int` and `Nat`. Matthew's corrected measurements compare the two backends with matching answers, compiler version and settings, and report 3.0–4.1× faster evaluation. Turning probe recording on did not materially separate these tiny, compute-heavy cases. That leaves the central editor question unanswered: large documents with short evaluations spend time differently. The initial cold-statics timing was also distorted by warm-up and does not support a speedup claim. This is a useful evaluator experiment; the branch still removes livelits as a shortcut and is not for merge.

Source: [latest benchmark correction](https://github.com/hazelgrove/hazel/pull/2490#issuecomment-5534741226), with fixed-precision details and the livelit caveat in the [preceding update](https://github.com/hazelgrove/hazel/pull/2490#issuecomment-5534642432).

## Integration cautions

- Keep the issue's existing time window and counts. This audit adds explanation from captured evidence; it does not make every feature in an evolving PR description a new event in September 4–10.
- The editorial voice can retain one short joke or playful headline per story. Replace metaphor where the reader needs mechanism, trigger, effect or status.
- Canvas observations are September 11 staging observations of the captured branch head, separate from the week's dated commits. The local build's unused-code warning failure belongs in production notes or a small caption, not the main feature paragraph.
- The richer Fumola explanation supersedes old `fumola_thunk` / `fumola_editor` instructions; it does not claim the newer four-form API all arrived inside the issue window.
- The credits must be scoped to this revision's actual reporting work. Astra remains editor and integration/verification owner; this audit does not independently verify previously reported live captures.
