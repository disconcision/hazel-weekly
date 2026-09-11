# Week in Hazel: editorial charter

**Reader contract:** [AUDIENCE.md](AUDIENCE.md). Write for the small internal Hazel community, including the contributors named in the issue. Production history and editing instructions stay in the kit; published text must stand on its own.

Start with [PRODUCTION.md](PRODUCTION.md) and its linked current example for the complete reusable brief, visual grammar and preferred Cards stamp exemplar. This charter retains the weekly reporting and continuity policy.

The deliverable is a small, engaging magazine for people who work on Hazel. An agent owns selection, reporting, writing, images, layout, and verification. Aim for about 8-12 minutes of reading, roughly 2,200-2,500 extracted words in a busy week in 8-12 visually paced pages. Adjust to the news. A quiet week should produce a shorter issue. The pilot is a starting direction, not a permanent template.

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

Every image gets a caption saying what to notice, which build it came from, whether the example was staged, and what it does not establish when that matters. Never pass a generated mockup off as a screenshot. If a preview fails, verify the URL and deployment logs, then attempt an isolated local build. Do not use one 404 to conclude that a feature cannot be observed. If it still cannot run, use a labeled source-derived illustration and say what was inspected. Avoid generating pictures of real contributors; represent concepts and fictional characters instead.

Use real screenshots, a few deliberate diagrams, and original image generation. One short alt-comic can be a recurring feature, with fresh imagery and a new premise. Save prompts, tool provenance and assets. Do not reuse the pilot's drawer tree and moth as the default picture every week.

## Print quality and page composition

Inspect the file signature and decoded dimensions, not the extension. The pilot revision exposed JPEG bytes saved under `.png` names by the browser tool path. A PNG filename is not proof of lossless capture. Never upscale those bytes or convert an old JPEG and call it a new lossless capture. Use an actual browser PNG export when the tool returns JPEG; Firefox’s built-in screenshot selection at 180% zoom worked for revision 2. Keep native files and staged source. Aim for at least 300 pixels per printed inch for UI plates, preferably 400 or more; inspect the actual embedded PDF image for downsampling or recompression.

Inspect all four edges at full resolution before placing a shot. Exclude accidental slivers of sidebars, selection overlays and clipped titles. Retain intentional context, such as an outline connected to its selected definition. Woodcut plates have no added border, mat or corner ticks. Clean plates may retain a single green outer rule, red corners and one 4 pt cream mat. Never use double borders or nested pale bands. Do not bake distress or fake UI into the clean image.

Use filled paper scraps with uneven cut angles, visibly irregular nicked edges and sparse grain; avoid tidy folded-corner icons for callouts and counts. Do not default to outlines around boxes. Diagrams use the same paper and lightly sketched strokes. Chart endpoints and labels remain exact; texture stays inside the fills. Prefer two columns for sustained prose. Place statistics beside the reporting they illuminate: issue flow/backlog with follow-up reports, benchmark numbers with their scope. Keep breathing room around strong images but avoid whole unused page bands. A selective ornamented initial can open a feature or a small contributor story; check its letter width and every wrapped line. Add diagrams only when they explain a specific relationship in the article. Revision 3 removes the old canvas schematic and gives the locally observed Constellation graph its own page.

The default for future published screenshots, including the proposed History of Hazel, is the light stamp treatment exemplified by assets/probes-cards-woodcut.png: restrained ink, quiet paper and clear lettering. Andrew reaffirmed this after the back-issue calibration; leaving those screenshots untreated was not the desired future direction. The RunningSums image is too heavily woodblocky and must not become the standard. Use no added border or mat. Supply the authentic high-resolution PNG as the content reference and the Cards exemplar only as style reference; request unchanged code, values and composition. Inspect all visible code and labels, identify the treatment in a compact illustration note, and retain the original as the reference for exact syntax. Correct content drift or use a documented clean-image exception if meaningful details cannot remain legible. Do not silently omit the treatment. Keep original captures accessible; a second complete clean edition is optional. Record prompts, selected output, fidelity limits and any rejected variants in the image ledger. Existing editions are not being revised by this preference update.

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
7. Save the new issue under a new filename and update the issue and image ledgers. Produce the readable HTML edition and publish it with the PDF and cover art to **andrewblinn.com/hazel/weekly/**, following [the web archive guide](web/README.md). Update the featured issue and regular archive, preserve older issues and the separate retrospective section, and verify the live links before notifying Andrew. Andrew has authorized this routine archive publication as part of weekly generation; do not request approval again for each issue. Do not post to Slack, email people or publish elsewhere without separate authorization. If publication fails, retain the local deliverables and retry the same issue rather than generating a duplicate.
8. If a source is temporarily inaccessible, continue with usable evidence and state the limit. Do not quietly substitute invented details. Stay quiet on scheduled runs with no new uncovered reporting window; notify on completion, material failure or required action.

## Additional inputs

Slack is supported by a plugin but was not connected for the pilot. Development channels, design threads, demo announcements and meeting notes would add the reasons behind changes. Prefer explicit channel scope and preserve the source's audience; private discussion should not silently become public magazine copy. An optional demo/example bank and preferred names/pronunciations would also help. Do not block weekly work on these additions.

An agent disclosure convention could improve future counts: consistent optional Co-authored-by trailers, plus a short human-written assistance note when useful. Treat missing disclosure as unknown, never a compliance failure. No repository policy change has been made here.

## Revision 4: reporting before ornament

Andrew's latest direction is more contentful prose, fewer aphorisms, and roughly 10–20% greater density than revision 3. The revised pilot is about 3,000 extracted words over eleven pages. Let the art and comics carry much of the weirdness. A playful headline is fine; a paragraph must explain behavior, a design decision, a consequence or a source-backed uncertainty. Avoid metaphor as a replacement for any of those. Do not write generic praise or close every brief with a maxim.

For a substantial issue, use bounded reporting agents when available: give each a selected topic, primary-source cache and explicit output contract (facts, source links, caveats, useful draft copy). The editor should do separate useful work and then verify, select and integrate the reports. Avoid a whole-repository reharvest just to deepen already selected stories. Credit actual work only. Agent pseudonyms are optional, must be labeled as such, and must not imply human identities, interviews or past reporting that never occurred. See [PROCESS.md](PROCESS.md) and the three saved revision-4 reports for the honest pilot history.

Prefer a controlled ragged edge to blanket justification in narrow columns. See PRODUCTION.md for the paragraph spacing, conservative hyphenation and visual proofing rules. Revision 5 now applies CSS paragraph layout through a browser text layer, preserving the original PDF artwork and display typography. See the current production guide.

## Revision 5: preserving the reader’s perspective

Read the issue as a colleague who missed another branch’s week, not as the person commissioning the zine. Use the test in AUDIENCE.md on captions, credits, closing pages and qualifiers as well as feature copy. Keep coverage plans and production mechanics here. The published closing page contains open development questions, not instructions to a later editor.

Compare revised compositions with the original style studies. Keep their paragraph spacing and display type independently controlled. Richer reporting can coexist with expressive type; avoid flattening every passage into the same density or removing all literary rhythm.

## Issue numbers and historical editions

Follow [NUMBERING.md](NUMBERING.md). Issue numbers are fixed to reporting weeks; Issue 001 anchors September 4-10, 2026, with 000 and negative numbers before it. Back issues retain their historical window, identify themselves as retrospectives and use period evidence.

## Lessons from the retrospective calibration

The [back-issue set](back-issues/README.md) tests architectural, product and language-heavy weeks. Check the enabled UI and feature flags even for merged code: July 2025's assistant included Task Completion machinery while its Compose button remained disabled. Do not equate merged implementation with an available interaction.

For historical reporting, follow [NUMBERING.md](NUMBERING.md), select a cutoff development head, and use dated discussion plus period code. Current PR bodies can contain both later additions and stale explanations. Treat source-derived diagrams as explanations, not screenshots or proof that an experimental branch ran. Keep retrospective entries ordered by reporting week when planning coverage; a back issue made today is not this week's latest issue.

Inspect every readable word in generated art. Incidental writing on a mug, poster or book is still publication copy; remove unrequested slogans. The back-issue comic cleanup is recorded in [COMIC-CLEANUP.md](back-issues/COMIC-CLEANUP.md).
