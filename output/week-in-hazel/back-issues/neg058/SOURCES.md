# Issue -058 sources

Reporting window: 2025-07-18T00:00:00Z through 2025-07-25T00:00:00Z (end exclusive). Historical dev head: `790b84e568197eb668591c4b05903aaeb6de20a9`. Retrieval: 2026-09-12 UTC.

## Lead and feature sources

- [#1805 Backpack II](https://github.com/hazelgrove/hazel/pull/1805): derived local/global backpacks, ambiguous polymorph gating, delayed trailing-keyword expansion, amorphous keyword prefixes, removed legacy actions, display changes and future work. Merged into `dev` at 2025-07-24T20:19:14Z.
- [#1033 Unused Variable Warnings](https://github.com/hazelgrove/hazel/pull/1033) and [#1825 revert](https://github.com/hazelgrove/hazel/pull/1825): warning semantics, hole-in-scope qualification, review and same-day removal from `dev`.
- [#1808 Retain/restore projector placements](https://github.com/hazelgrove/hazel/pull/1808): `^^projector(...)` syntax and insertion trigger; merged into `dev` at 2025-07-23T22:01:53Z.
- [#1267 Polymorphic equality](https://github.com/hazelgrove/hazel/pull/1267): comparable shapes, gradual holes and incomparable arrows; merged into `dev` at 2025-07-22T22:53:10Z.
- [#1799 Toggle Focus](https://github.com/hazelgrove/hazel/pull/1799), [#1818 type application normalization](https://github.com/hazelgrove/hazel/pull/1818), and [#1822 selection decoration](https://github.com/hazelgrove/hazel/pull/1822): smaller dev landings.

## Reports and open work

- [#1827 scrollbar under top bar](https://github.com/hazelgrove/hazel/issues/1827), [#1810 precedence](https://github.com/hazelgrove/hazel/issues/1810), [#1813 wildcard coverage](https://github.com/hazelgrove/hazel/issues/1813), [#1815 list consistency](https://github.com/hazelgrove/hazel/issues/1815), [#1819 duplicate scratchpad names](https://github.com/hazelgrove/hazel/issues/1819), [#1820 builtin ascription/application](https://github.com/hazelgrove/hazel/issues/1820), [#1821 old operators](https://github.com/hazelgrove/hazel/issues/1821), [#1823 projector-off hotkey](https://github.com/hazelgrove/hazel/issues/1823), and [#1824 ExplainThis wording](https://github.com/hazelgrove/hazel/issues/1824).
- [#1804 Structural Insertion and Delete](https://github.com/hazelgrove/hazel/pull/1804) and [#1812 HTML Projector](https://github.com/hazelgrove/hazel/pull/1812) opened during the week and were not counted as landed features.

## Images

- `assets/originals/unused-variable-warnings.png`: authentic 1151x1366 PNG from a dated #1033 review image (`77e98461-fe78-457c-a2af-16ab64461247`).
- `assets/originals/backpack-scrollbar-regression.png`: authentic 1354x666 RGBA PNG attached to #1827 (`36f275b4-a8b5-48db-a954-d54c9bc7a3e1`).
- Corresponding `*-stamp.png` files are generated facsimiles. They are illustration, not new technical evidence. Exact prompts are in `PROMPTS.json`.

## Metrics and limitations

`research/analyze.py`, `metrics.json` and `period-dev-commits.tsv` reproduce the cutoff-dev graph census from a separate Hazel checkout. `selected-github.json` records selected authenticated GitHub retrieval. Mutable PR prose is retrieval-time evidence. Surviving refs cannot reconstruct deleted branches or push events. The screenshot originals are historical attachments; the cloud trial did not produce a fresh native PNG or complete a Hazel application build. See `research/cloud-build-check.md` and `QA.md`.
