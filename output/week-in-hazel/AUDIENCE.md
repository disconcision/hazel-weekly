# Audience and editorial viewpoint

Week in Hazel is primarily for the small internal Hazel community. Andrew, Alexander, Matthew, Cyrus and the other contributors are potential readers, not remote subjects being introduced to the public. A reader may know one subsystem intimately while having missed another team's recent work. Write for that technically capable colleague.

The issue should help that reader learn what landed, understand a useful experiment, recognize a blocker or design question, and find something worth trying or discussing. It should also be an enjoyable magazine: distinctive typography, an occasional dry joke, strong examples, and art with its own personality.

## The reader's question

For every paragraph, caption and note, ask: **Would this mean something to a Hazel contributor who has never seen our editing conversation?**

Useful material includes a changed interaction, an illustrative program, a consequential review comment, an implementation choice that explains behavior, a feature's readiness, and the scope of a benchmark. Assume familiarity with Hazel, PRs, probes, livelits and normal development practice. Explain the unfamiliar work inside this particular branch; do not spend space explaining what a repository or a developer is.

Use names naturally. First names are generally enough after an unambiguous introduction. Contributor sections should reveal the work and connections between efforts, not invent personalities, repeat biographies, or praise colleagues from a distant outsider's viewpoint.

## Keep production records out of the issue

Earlier draft history, agent assignment chronology, absent data sources, image export mechanics, renderer choices, failed first attempts and instructions for future editors belong in the production kit. They do not belong in a reader's masthead or feature unless the production event itself is the subject of a story.

For this issue, remove phrases such as “earlier revisions had no reporting-agent bylines,” “no Slack source used,” “native PNG” and “all pixels retained.” The magazine credits its actual editorial contributors briefly. PROCESS.md can give the complete history.

The same rule applies less obviously to the closing page. “Revisit this when…,” “show the corrected interaction” and “bring it back in a brief” are assignments to an editor. Replace them with the open technical questions and consequences that a contributor can think about now. Keep coverage planning in issues.json and EDITORIAL.md.

Captions should first identify what is visible and what it explains. A short branch or demo label is often enough. Keep one compact illustration credit that tells readers when screenshots are generated reproductions and points to the exact-UI edition; repeated image-tool and file-format commentary distracts from the feature.

## Qualifications must serve interpretation

Keep draft/open/merged status, the merge destination, the benchmark's workload and attribution, and the date of a changing count. These change what a reader can conclude or act on. Prefer source attribution in the sentence: “the report traces…,” “the PR's headless benchmark…,” or “the animation code…”. Do not replace these with unqualified assertions.

A qualification about the editor's own process is usually less useful. “We have not rerun every test” can become a clear attribution to the author’s result. “We did not run an LLM session” can become a source-grounded account of what the animation code and controls implement. Preserve observations such as a graph going blank, because they affect someone trying the branch. Keep untested hypotheses visibly framed as questions or interpretations.

## Preserve a magazine's voice

Audience awareness is not a request to make the zine bland. Keep playful titles, expressive type, warm rhythm and the fiction department. Put detailed explanation in the article and let illustrations, headlines and selected display passages carry more of the literary register. A memorable image should make a particular feature clearer; an interchangeable aphorism should be cut.

## Prevent revision drift

Compare new pages with the approved visual reference, not only with the immediately preceding draft. Review content changes separately from art direction. A request for denser reporting should not silently tighten every paragraph in a spacious style study. Keep display typography, body typography, captions and study layouts independently controlled. Judge the composition as a whole after local fixes.

Before release, read the issue straight through as a Hazel colleague. Check that every visible word belongs to the publication rather than the production conversation. Then proof the actual rendered pages. Browser CSS can improve line breaks, but it cannot choose the audience or restore an editorial voice for us.
