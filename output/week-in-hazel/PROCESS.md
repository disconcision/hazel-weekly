# How Issue 001 was reported and revised

Production history through revision 5, September 11, 2026. This records actual work, not a fictional newsroom history.

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

These names identify AI reporting agents for this revision. They are not invented human contributors, interviews or continuing biographies. Astra remains the AI editor and production owner. Revision 4’s masthead scoped these credits to the new audit. The reporters' drafts are not automatically final: Astra selected and rewrote them, checked the source caveats and corrected the six-module list against the captured implementation.

Examples of the resulting edit:

- Removed the “small desk inside a large room” analogy. Explained the later-definition edit that could reuse an old evaluation, the enclosing-term repair, and the relationship between a focused cell and master-document samples.
- Replaced generic module-boundary language with the exported-argument bug, signature duplicates versus implementation shadowing, and the unmeasured copying cost of a 65-member module.
- Distinguished missing sample menus from short-table positioning. Described #2524's ascription trigger instead of implying that every recursive program regressed.
- Named the four current Fumola forms and distinguished Simple from Graphical runtime mode. The GCD capture demonstrates a bridge, not incremental repair.
- Explained malformed tutorial tests and why an explicit-hole workaround changes the student's editing action.

The reporting window, counts and source capture stay fixed. A current branch description can contain accumulated work; the copy separates the week's merge/fix from background feature behavior. Source-observed and author-reported claims remain distinguishable. About 12% more extracted words fit in the same eleven pages, with the existing illustrations retained.

## Revision-4 typography: what actually changed

The pilot is a ReportLab PDF, not HTML printed from a browser. CSS declarations would not change its text. A [three-column proof](research/typography-comparison.png) compared ordinary ragged setting, ragged setting with conservative hyphenation, and justification with the same hyphenation. The middle option retained steadier word spacing while reducing abrupt line endings. Full justification introduced conspicuous expanded spaces in these 222 pt columns.

Revision 4 uses ragged-right body copy, English hyphenation restricted to lowercase alphabetic words of eight or more letters, and at least three letters on each side of a break. Names, mixed-case words and code identifiers are not automatically hyphenated. Short paragraph-final words are kept with a preceding word where appropriate. Actual paragraphs have a 6.5 pt gap, instead of an entire blank line forced with two line-break tags. Feature copy stays near 11 pt with 14 pt leading; headlines and illustrations retain their existing character.

This is controlled ReportLab wrapping plus editorial proofing, not a whole-paragraph optimizer equivalent to a browser's `pretty` implementation. Each page still needs inspection for isolated words, consecutive hyphens, uneven rags, crowded captions and headings that gain an extra line. The first proof caught an overlapping two-line subheading on page 3; it was shortened and given an explicit height check.

For an HTML edition, start with `lang="en-US"`, `text-align: start`, `hyphens: auto`, and `text-wrap: pretty` on paragraphs. Use `text-wrap: balance` selectively for short headlines when similarly long lines suit the composition. `pretty` behavior varies by engine; `balance` can make the apparent block narrower. These are progressive typography enhancements, not a guarantee of identical print output. See [WebKit's explanation](https://webkit.org/blog/16547/better-typography-with-text-wrap-pretty/) and [Chrome's implementation notes](https://developer.chrome.com/blog/css-text-wrap-pretty).

Do not migrate the whole publication merely to add a property. If an HTML edition becomes a deliverable, proof its actual browser and PDF export separately. That revision's improvements came from the PDF generator described above. Revision 5 subsequently adopted the hybrid browser approach below.

## Revision 5: audience and browser typography

Astra made this editorial pass using the existing source cache and the three reporting audits. The previous credits remain credits for actual contributions to the issue; no additional reporting agents were assigned. The published masthead now gives names and roles only. Full assignment history remains here.

The audience audit found production material beyond the masthead: the closing page contained editorial assignments; captions foregrounded encoding and capture mechanics; some qualifications narrated the editor’s limitations rather than attributing the underlying claim. AUDIENCE.md records the internal-reader standard. The closing page now discusses live technical questions, and qualifications stay where they affect interpretation.

The earlier revision found `text-wrap: pretty` but did not apply it. Revision 5 uses it in actual HTML paragraphs rendered by Chrome 153.0.8010.36. A retained comparison demonstrates that browser wrapping also handles the long `recursive-ascription` compound more naturally than the old ReportLab split-drop-cap paragraph. The tested paragraphs do not all differ between `auto` and `pretty`: the specific compound improvement appears with normal browser breaking too. The full issue’s measured comparison shows ten of 58 body paragraphs changing their layout under `pretty`. This is a combined improvement from browser line breaking, hyphenation, kerning, flow and the edited prose, not a claim that one CSS property fixes every gap. See [browser comparison](research/revision5-browser-proof.png) and typesetting/metrics.json.

The primary documentation describes browser-dependent behavior: [WebKit on `pretty`](https://webkit.org/blog/16547/better-typography-with-text-wrap-pretty/), [Chrome’s implementation](https://developer.chrome.com/blog/css-text-wrap-pretty), and [Safari 26 availability](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/).

The original style studies were compared page by page with revisions 4 and 5. Their typefaces and main geometry had stayed largely intact; the shared paragraph helper had tightened the spacing, and explanatory rewrites had diluted some display passages. Revision 5 separates these rules: original display typography and art stay in ReportLab; body text uses the browser; studies keep a full-leading paragraph gap and deliberate line arrangements. This is a correction of specific drift, not a reason to reset approved images or artwork.
