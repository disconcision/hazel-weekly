# How Issue 001 was reported and revised

Revision 4, September 11, 2026. This records actual work, not a fictional newsroom history.

## Earlier drafts

Astra did the acquisition, story selection, source reading, editorial writing, image staging and PDF production. The collector fetched independent GitHub requests concurrently; that was API parallelism, not independent reporting agents. The accessible tool-call record before Andrew's latest prose request contains no earlier subagent assignments.

The saved material includes PR descriptions, issue discussion, reviews, branch snapshots, selected code and reproducible commit metadata. Astra selected stories from this material and wrote directly into a ReportLab layout with fixed page boxes. Later revisions added native PNG captures and locally built Constellation. The weak prose came partly from that editing method: compression and decorative transitions took the place of useful explanation. The source cache already contained more detail than the issue used.

## The revision-4 reporting pass

Andrew suggested independent reporting and truthful credits. Astra assigned three bounded audits while handling typography and the editorial integration. No new full harvest was needed. The agents read the saved primary sources and selectively inspected code at captured heads. They supplied evidence, caveats and proposed copy. None claimed interviews, new screenshot observations or fresh benchmark runs.

| Agent's chosen pseudonym | Actual assignment | Saved report |
| --- | --- | --- |
| Ellis | Probes IV, drawer/performance follow-ups, CI discussion, tutorials | [Report](research/revision4-probes-report.md) |
| Rowan | All nine Modules II drafts, discussion and library implementation | [Report](research/revision4-modules-report.md) |
| Mica | Modular editors, agent hardening, Constellation, Fumola and Wasm | [Report](research/revision4-runtime-workspace-report.md) |

These names identify AI reporting agents for this revision. They are not invented human contributors, interviews or continuing biographies. Astra remains the AI editor and production owner. The final masthead scopes these credits to the new audit. The reporters' drafts are not automatically final: Astra selected and rewrote them, checked the source caveats and corrected the six-module list against the captured implementation.

Examples of the resulting edit:

- Removed the “small desk inside a large room” analogy. Explained the later-definition edit that could reuse an old evaluation, the enclosing-term repair, and the relationship between a focused cell and master-document samples.
- Replaced generic module-boundary language with the exported-argument bug, signature duplicates versus implementation shadowing, and the unmeasured copying cost of a 65-member module.
- Distinguished missing sample menus from short-table positioning. Described #2524's ascription trigger instead of implying that every recursive program regressed.
- Named the four current Fumola forms and distinguished Simple from Graphical runtime mode. The GCD capture demonstrates a bridge, not incremental repair.
- Explained malformed tutorial tests and why an explicit-hole workaround changes the student's editing action.

The reporting window, counts and source capture stay fixed. A current branch description can contain accumulated work; the copy separates the week's merge/fix from background feature behavior. Source-observed and author-reported claims remain distinguishable. About 12% more extracted words fit in the same eleven pages, with the existing illustrations retained.

## Typography: what actually changed

The pilot is a ReportLab PDF, not HTML printed from a browser. CSS declarations would not change its text. A [three-column proof](research/typography-comparison.png) compared ordinary ragged setting, ragged setting with conservative hyphenation, and justification with the same hyphenation. The middle option retained steadier word spacing while reducing abrupt line endings. Full justification introduced conspicuous expanded spaces in these 222 pt columns.

Revision 4 uses ragged-right body copy, English hyphenation restricted to lowercase alphabetic words of eight or more letters, and at least three letters on each side of a break. Names, mixed-case words and code identifiers are not automatically hyphenated. Short paragraph-final words are kept with a preceding word where appropriate. Actual paragraphs have a 6.5 pt gap, instead of an entire blank line forced with two line-break tags. Feature copy stays near 11 pt with 14 pt leading; headlines and illustrations retain their existing character.

This is controlled ReportLab wrapping plus editorial proofing, not a whole-paragraph optimizer equivalent to a browser's `pretty` implementation. Each page still needs inspection for isolated words, consecutive hyphens, uneven rags, crowded captions and headings that gain an extra line. The first proof caught an overlapping two-line subheading on page 3; it was shortened and given an explicit height check.

For an HTML edition, start with `lang="en-US"`, `text-align: start`, `hyphens: auto`, and `text-wrap: pretty` on paragraphs. Use `text-wrap: balance` selectively for short headlines when similarly long lines suit the composition. `pretty` behavior varies by engine; `balance` can make the apparent block narrower. These are progressive typography enhancements, not a guarantee of identical print output. See [WebKit's explanation](https://webkit.org/blog/16547/better-typography-with-text-wrap-pretty/) and [Chrome's implementation notes](https://developer.chrome.com/blog/css-text-wrap-pretty).

Do not migrate the whole publication merely to add a property. If an HTML edition becomes a deliverable, proof its actual browser and PDF export separately. The current output's improvements come from the PDF generator described above.
