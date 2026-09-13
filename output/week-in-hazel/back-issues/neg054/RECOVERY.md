# Week in Hazel -054: interrupted cloud trial

**Status: incomplete. No finished PDF, illustrated HTML edition, or verified download package. Nothing published.**

## Identity

- Input main: cd6897cfe18e6c4127a66bab6b360f609669465a.
- Fresh branch: codex/cloud-trial-neg054.
- Selected week: August 15–21, 2025 UTC; end exclusive August 22 00:00 UTC.
- Calendar issue: 1 + (2025-08-15 - 2026-09-04).days // 7 = -54.
- Historical Hazel dev head: defc38690ed8035ae8950d148523ee0b25c22021.
- Next first-parent integration: 72e8d10bc326cc8d4c3d747dd1b68c19a5eb8199 at August 22 01:28:28Z, after cutoff.
- Excluded editions: 001, -019, -058, -060 and -100.

## Failure and persistence limits

The cloud execution environment disconnected during dependency setup on September 12, 2026. Subsequent commands and browser access failed with `409 Conflict, environment_offline: Environment is not connected`. A September 13 environment update explicitly marked it failed. This was not an approval rejection.

Local research, native historical screenshots, a generated cover, comic and completion treatment were produced before the outage. Their files became inaccessible. An artwork upload and a later larger recovery upload were interrupted, with no confirmed resulting commit. This file is the compact recovery record; it does NOT claim that those assets or raw records are present on the branch. No PDF was authored or rendered. No final visual QA or downloadable package verification passed.

## Verified editorial findings

Working title: **Rows, with names.** Lead with tables as lists of labeled tuples, followed by character editing, completion, proofs, persistence and unresolved probe reports. Two actual bounded AI reporting agents audited tables/proofs and editing/reports while the editor worked on production. No interviews or contributor dialogue were invented.

1. [Tables #1555](https://github.com/hazelgrove/hazel/pull/1555) merged into dev August 20 18:43:07Z at adc176b304faabb7274a2ee5500eedbe0927d716. The PR body contains stale names. Merged code uses group_by_label, to_lvs, from_lvs, project_labels, select_labels, omit_labels and omit_all_labels. Dot projection broadcasts over lists of tuples. The gradebook example extracts final scores; the leaderboard groups by level then projects desert scores. Read the period [Tables document](https://github.com/hazelgrove/hazel/blob/adc176b304faabb7274a2ee5500eedbe0927d716/src/web/init/docs/Tables.ml) and [builtin definitions](https://github.com/hazelgrove/hazel/blob/adc176b304faabb7274a2ee5500eedbe0927d716/src/language/builtins/BuiltinsTupleOperations.re).
2. [Delimiter editing #1865](https://github.com/hazelgrove/hazel/pull/1865) merged dev August 20 23:12:59Z. Editing inside polytile delimiters follows ordinary character insertion/deletion. Tests cover then becoming thxen and else becoming lse then else again. Keywords expand immediately, including the temporary let while typing letter. No quantified reliability improvement is established.
3. [Completion #1883](https://github.com/hazelgrove/hazel/pull/1883) merged dev August 20 22:56:31Z. It filters shadowed context entries and puts leading-form suggestions in the sorted candidate list. Andrew's [August 20 reduction](https://github.com/hazelgrove/hazel/issues/1875#issuecomment-3206826977) shows a local tl : Float wrongly treated as callable. #1880 (p becomes pause) and #1881 (let suggested in type position) close with this merge.
4. Crucial caveat: #1883's title names [#1882](https://github.com/hazelgrove/hazel/issues/1882), but its actual closure set is #1875/#1880/#1881. #1882 remains open at cutoff; the later explanation at August 22 01:17:30Z is outside the week.
5. [Reflexivity #1859](https://github.com/hazelgrove/hazel/pull/1859) merged dev August 20 18:07:25Z. Proof steps are experimental and off by default. The expression matcher handles term-binder alpha-equivalence; do not confuse its limits with those of the separate replacement function. Ordinary green steps suppress competing purple reflexivity candidates at the same expression.
6. [Theorem capture #1871](https://github.com/hazelgrove/hazel/pull/1871) merged August 21 09:42:33Z into theorem-capture, NOT dev. Named theorems have captured context and their own proof steppers; forall remains deliberately indeterminate in ordinary evaluation.
7. [Stepper persistence #1869](https://github.com/hazelgrove/hazel/pull/1869) merged dev August 20 18:07:47Z. Persisted step-kind chains reconstruct derived fields; this is not a full live evaluator-cache snapshot.
8. [TermData #1884](https://github.com/hazelgrove/hazel/pull/1884) merged dev August 20 23:19:41Z, the cutoff head. Term range, base segment and root piece come together; indication arms use that information. The reported marginal efficiency benefit has no timings.
9. [Flat-map #1866](https://github.com/hazelgrove/hazel/pull/1866) fixes chunk order: flat_map([1,2], fun x -> [x,x]) expects [1,1,2,2], replacing the old test's [2,2,1,1]. [#1867](https://github.com/hazelgrove/hazel/pull/1867) repairs transitions through ascribed deferrals. [#1878](https://github.com/hazelgrove/hazel/pull/1878) aligns text-projector stripes with --line-height instead of fixed 1.47em.
10. Open reports at cutoff include duplicated scrutinee probe samples #1885, viewport scrolling #1886, inspector mismatch #1887, persistent probe-selection crash #1888, stray arms #1889 and typing 1= crash #1893. Closures of #1887/#1888/#1893 just after August 22 01:28Z are too late for this issue.

Counts verified from GitHub records: **9 PR openings, 12 merges (10 dev, 1 equality, 1 theorem-capture), 9 issue openings**. The 18 PRs in the union of openings/merges are 1555, 1758, 1859, 1865, 1866, 1867, 1869, 1871, 1873, 1876, 1877, 1878, 1879, 1883, 1884, 1890, 1891, 1892. No historical backlog, push total, productivity metric, or AI-assistance inference. Final cutoff-dev commit census remains uncomputed.

## Authentic screenshot sources

- Completion: [original PNG](https://github.com/user-attachments/assets/af300993-3f21-4ef0-ae92-4cd08d27d538), from the dated August 20 reduction above. Downloaded and decoded before outage: 792 x 266 PNG. Print about 2.5 inches wide for 317 ppi. Generated treatment was inspected; exact original remains evidence.
- Duplicated probes: [original PNG](https://github.com/user-attachments/assets/e70ef90e-fcf5-4019-884a-9e97ea217266), [#1885](https://github.com/hazelgrove/hazel/issues/1885), opened August 20 23:30:45Z. Downloaded/decoded 978 x 426 PNG. Print about 3.2 inches for 306 ppi. Unfinished qsort, badge 2 on xs and two identical samples. The treatment call failed before reading references.
- Reflexivity: [author PNG](https://github.com/user-attachments/assets/91d64a83-6079-44f6-8ab6-b1feb0aa807e), 1051 x 583, 37,305 bytes, SHA-256 4838210b30bec36a30ff8f2393402f0109d96145fc1ab6f27cd2977f347fec33. It shows the older self-equality label; exact capture revision/time unknown. Do not present as a rebuilt cutoff screenshot.

These were genuine historical PNGs, not fresh cloud captures. Their original local downloads are inaccessible and not attached to this record.

## Artwork recovery

Built-in ImageGen produced and displayed three assets in the conversation, all currently inaccessible as local files:
- Cover: exec-4dc0fb98-e6be-4209-83e2-ee648184f76b.png. Linocut beetle workshop, continuous paper ribbon of compartmented rows, berry/leaf/stone fields with blank label tabs, folding into a table-like grid. Forest-black, warm ivory, moss/vermilion/ochre; no title or writing.
- Comic: exec-4427117c-ec54-43d4-83aa-b3da9c0036bb.png. Three panels: beetle shipping clerk offers an absurd padded lift; caterpillar with a tray of labeled jars chooses an ordinary conveyor. Exact dialogue: "Special handling?" / "Same conveyor." / "Keep the labels." No other lettering. Visually inspected.
- Completion stamp: exec-fe4eb233-12d5-42b8-b089-a07179039fff.png. Authentic completion PNG as content reference; existing probes-cards-woodcut.png as style only. Complete crop, three code lines, crisp syntax, light ink variation and quiet paper; no frame or heavy woodgrain. Visually inspected against original.

These descriptions are recovery briefs, not the verbatim full prompts. Full original prompts remain in the conversation. Recover the images there if supported; otherwise regenerate and record new prompts/output provenance. Do not claim these files are downloadable from this branch.

## Setup progress

The missing-header problem was resolved using official Debian packages extracted with dpkg-deb -x into a user-space sysroot: libgmp-dev 6.3.0+dfsg-3, libffi-dev 3.4.4-1, m4 1.4.19-3, pkgconf-bin/libpkgconf3 1.8.1-1. A C program including gmp.h and ffi.h compiled, linked with -lgmp -lffi and ran. pkg-config resolved GMP 6.3.0, libffi 3.4.4, OpenSSL 3.0.13 and zlib 1.3. npm ci at cutoff Hazel passed.

The old trial's isolated opam 2.5.2 / OCaml 5.2.0 setup was reused. After actual headers were verified, opam install ./hazel.opam.locked --deps-only --with-test --with-doc --no-depexts -y passed solving. Tar then failed trying to restore uid 22367/gid 32771. Proposed correction TAR_OPTIONS=--no-same-owner was not successfully run before disconnection. Full Hazel build remains unverified.

Cloud screenshot recheck returned 87,042 JPEG/JFIF bytes. Playwright Chromium archive timed out repeatedly. Official Debian chromium-headless-shell_150.0.7871.100-1~deb12u1_amd64.deb downloaded (57 MiB observed), but extraction/ldd/runtime results were not returned before outage. No fresh native PNG capability was established.

Public Git fetch worked. Normal authenticated push --dry-run failed for missing username; GitHub branch creation worked. The prior trial's PDF exceeded the connector's 16 MiB base64 request ceiling. This trial never reached PDF authoring, so its export path was not tested.

## Continue in a working environment

Clone this branch and preserve the selected week. Read current production guides and approved visual examples. Restore or regenerate this issue's assets; retrieve primary records and period source; run a SHA-distinct cutoff-dev census with explicit UTC committer filtering. Finish roughly nine pages, genuine staged PNGs when possible, light treatments, source maps, editable copy and cover-led HTML with the red disclosure and stable linked headings. Render and inspect every PDF page, then save complete PDF/HTML/source packages and retrieve their bytes to verify delivery.

Keep everything unpublished. Do not merge, alter site/, modify production ledgers as if this incomplete issue were covered, or change schedules. The previous trial branch and all prior editions remain untouched.
