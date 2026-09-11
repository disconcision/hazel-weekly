# Week in Hazel: editorial charter

The deliverable is a small, engaging magazine for people who work on Hazel. An agent owns selection, reporting, writing, images, layout, and verification. Aim for about 8-12 minutes of reading, roughly 1,500-2,200 words in 8-12 visually paced pages. Adjust to the news. A quiet week should produce a shorter issue. The pilot is a starting direction, not a permanent template.

## Voice and judgment

Curious, affectionate, technically literate, occasionally strange. A handmade literary/science zine, with good typography and a little dirt on its cuffs. Humor comes from recognizable work and invented abstractions, not jokes at a contributor's expense. Do not invent quotations, motivations, conversations, outcomes, or personalities. A playful headline can coexist with precise status. Prioritize a story people want to read, while preserving the facts that determine whether they can use or rely on the work.

Lead with major changes merged into the shared development branch. Select a few interesting experiments, a small contributor story or interaction, one overlooked detail, and a compact statistical view. Read past PR descriptions into current comments, reviews, code and demos. Older prose can be stale. Reported benchmark numbers stay attributed and scoped to their workloads; distinguish them from our own observations.

## Status is part of the story

- MERGED INTO DEV: verify merged_at and base branch, plus default-branch reachability where needed.
- MERGED INTO FEATURE BRANCH: name that branch. A merged badge alone does not mean Hazel's main build has it.
- OPEN PR: reviewable work, not necessarily a merge candidate. Respect textual warnings such as “spike.”
- DRAFT: explicitly experimental; note dependencies and what is unresolved.
- BRANCH ONLY: check for matching PRs, record the sampled SHA, and use tentative language.
- REPORTED ISSUE: explain the visible effect and its reported status. Do not turn a proposed fix or an isolated branch into a shipped fix.

Large stacked diffs are not independent features or fresh lines of implementation. A branch that only merged dev is not automatically a new story. Distinguish a real development event from an updated_at timestamp, a rebase, or a bot comment.

## Make photographs, not window dumps

The user explicitly authorizes composing screenshots: scroll, choose the scale/zoom, open or close panels, set up examples, edit scratch code, place probes and rich literals, and arrange the view to explain the feature. Use fresh disposable scratch documents or isolated browser profiles when possible. Keep staged source with the issue.

Before capturing, write the one sentence the image should make obvious. Remove unrelated panels and dead space; place the relevant source, probe, result and contextual navigation in one readable view. Crop at capture time when appropriate. Preserve enough genuine UI context to establish what is being shown. Check at the final printed size: if a reader cannot read the relevant labels, use a tighter shot, fewer lines, or a larger panel. Avoid empty sidebars and mostly blank editor screenshots.

Every image gets a caption saying what to notice, which build it came from, whether the example was staged, and what it does not establish when that matters. Never pass a generated mockup off as a screenshot. If a branch preview is unavailable, use a clearly labeled conceptual illustration or schematic and say what was inspected. Avoid generating pictures of real contributors; represent concepts and fictional characters instead.

Use real screenshots, a few deliberate diagrams, and original image generation. One short alt-comic can be a recurring feature, with fresh imagery and a new premise. Save prompts, tool provenance and assets. Do not reuse the pilot's drawer tree and moth as the default picture every week.

## Print quality and page composition

Inspect the file signature and decoded dimensions, not the extension. The pilot revision exposed JPEG bytes saved under `.png` names by the browser tool path. A PNG filename is not proof of lossless capture. Never upscale those bytes or convert an old JPEG and call it a new lossless capture. Use an actual browser PNG export when the tool returns JPEG; Firefox’s built-in screenshot selection at 180% zoom worked for revision 2. Keep native files and staged source. Aim for at least 300 pixels per printed inch for UI plates, preferably 400 or more; inspect the actual embedded PDF image for downsampling or recompression.

Inspect all four edges at full resolution before placing a shot. Exclude accidental slivers of sidebars, selection overlays and clipped titles. Retain intentional context, such as an outline connected to its selected definition. Frames are page furniture: a restrained paper mat, fine rule and occasional spot-color corner can tie screenshots to the illustration without damaging the actual capture. Do not bake distress or fake UI into the clean image.

Prefer two columns for sustained prose. Place statistics beside the reporting they illuminate: issue flow/backlog with follow-up reports, benchmark numbers with their scope. Keep breathing room around strong images but avoid whole unused page bands. A selective ornamented initial can open a feature or a small contributor story; check its letter width and every wrapped line. Add diagrams only when they explain a specific relationship in the article. In revision 2, the canvas explainer derives from the same Card/Hand insertion-sort example on page 2 instead of an unrelated generic network.

ImageGen woodcut facsimiles are an optional art-direction experiment, not the new default. Keep a matching clean edition when exploring them. Supply the authentic PNG as the content reference and the issue art only as style reference; request unchanged code, values and composition. Inspect all visible code and labels, disclose that the plate is a generated facsimile, and retain the original as the reference for exact syntax. Small glyph and card details can drift even when the overall reproduction looks close. Do not present either the generated image or its apparent values as new evidence. Record prompts, selected output, fidelity limits and any rejected variants in the image ledger.

## Novelty, callbacks and returning characters

Before assigning stories, read every recent entry in issues.json and image-ledger.json; inspect the last four issues and the last appearance of each proposed feature. Keep a longer archive, not just a rolling weekly memory.

For each story answer: **What has changed since our last visit, and why is this worth a reader's time now?** Record its new contribution in the issue ledger. A changed status (draft to merged), a new interaction, measured result, resolved design question, revealing review, or consequential failure can earn a return. Mere ongoing activity does not.

- As a default, spend at least two-thirds of editorial space on new developments, new angles, or first coverage. This is a judgment aid, not a quota that should suppress a major continuing story.
- Use one or two sentences and a link for a routine callback. Do not retell the previous feature or reuse its entire screenshot.
- A major story may lead in consecutive weeks if there is a substantial new event; name that event immediately.
- Contributors recur through evolving work and interactions, not repeated biographies or fixed caricatures. Rotate attention beyond the busiest committers; reviews, tests, docs and quiet fixes count.
- Each image ledger entry records the concept, example, composition and build. A fresh screenshot of the same unchanged view is still repetition. Prefer a new example, a before/after, a changed state or a detail we did not show before.
- Revisit work after roughly 8-12 weeks of no coverage when a meaningful new development or a useful retrospective justifies it. Introduce it again briefly for new readers; do not assume the archive has been memorized. Dormancy alone is not news.
- Keep a “not this week” list with why an interesting lead was deferred and what could make it timely.

The pilot has no previous issue to avoid repeating. Style studies are alternatives within the pilot, not separate weekly coverage.

## Sources and counts

Default issue window: seven completed UTC days ending Friday 00:00 UTC. Friday morning publication uses that fixed cutoff, with two earlier weeks for context. Write exact start/end and the retrieval time. Mutable PR prose, draft state and live demos are observations at retrieval; do not imply perfect historical reconstruction. Label anything arriving after cutoff as a later note, and keep it out of period counts.

Keep raw paginated GitHub records, refs, sampled commits, analytical definitions and a source map under the dated issue. Deduplicate shared commits by SHA. Describe rebases/cherry-picks and merges in the denominator. A commit's committer timestamp is not a push timestamp; a recent branch tip does not count pushes. GitHub Events is capped and cannot be the sole activity history. Never label commit volume as productivity, impact, human effort, or AI code share.

Track declared agent co-author trailers separately from cryptographic signature headers and GitHub bot identities. No trailer means assistance is unknown. A Claude credit is a declaration, not a verified measure of labor. Zero OpenAI trailers does not establish zero Codex/ChatGPT use. Do not infer agent use from prose style, speed or volume. Counts across weeks must use comparable definitions, with methodology changes called out.

## Weekly production

1. Compute the next uncovered window. If its issue already exists, do not regenerate or overwrite it merely because the scheduler ran. The pilot covers 2026-09-04 through 2026-09-10; the next issue ends 2026-09-18T00:00:00Z.
2. Read this charter and the two ledgers. Harvest GitHub for the current window plus context, and fetch remote refs without changing the user's checkout. Save a dated immutable source snapshot. Review issues, PR descriptions, discussions, reviews, changed code, branches and meaningful external dependency changes.
3. Create a source-grounded story budget. Pick the lead and several smaller stories. Record evidence, statuses, relationships, editorial angle, the last time each was covered, and outstanding uncertainty.
4. Stage new screenshots. Generate fresh editorial art as appropriate. Capture build/source provenance, visible results and staged code. Keep screenshots authentic.
5. Write the issue; put source links close to claims. Keep technical explanation proportional to what a Hazel contributor needs to understand. Author the PDF using the PDF skill and retain editable source. The pilot builder is useful layout code, but its prose and page assignments must be replaced, not rerun for a new date.
6. Render every page to images and visually inspect all of them, at actual size for captions and code. Correct overflow, cramped text, unreadable screenshots, misleading status and stale numbers. Validate page count, extracted text, hyperlinks, exact reporting window and metric consistency.
7. Save the new issue under a new filename, update the issue and image ledgers, and notify Andrew when it is ready. Do not post to Slack, email people or publicly publish unless separately authorized. The request authorizes production, not distribution to other people.
8. If a source is temporarily inaccessible, continue with usable evidence and state the limit. Do not quietly substitute invented details. Stay quiet on scheduled runs with no new uncovered reporting window; notify on completion, material failure or required action.

## Additional inputs

Slack is supported by a plugin but was not connected for the pilot. Development channels, design threads, demo announcements and meeting notes would add the reasons behind changes. Prefer explicit channel scope and preserve the source's audience; private discussion should not silently become public magazine copy. An optional demo/example bank and preferred names/pronunciations would also help. Do not block weekly work on these additions.

An agent disclosure convention could improve future counts: consistent optional Co-authored-by trailers, plus a short human-written assistance note when useful. Treat missing disclosure as unknown, never a compliance failure. No repository policy change has been made here.
