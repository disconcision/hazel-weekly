# Week in Hazel

A small digest for the hazelnut community.

**All content is fully AI-generated from the Hazel Git repository and GitHub data.** Reporting, writing and illustrations are all AI-produced.

Read the magazine at **[andrewblinn.com/hazel/weekly](https://andrewblinn.com/hazel/weekly/)**. This repository holds its editorial guides, reporting evidence, original artwork and screenshots, editable builders, finished PDFs, and a copy of the HTML archive.

## Start here

- [Production brief](output/week-in-hazel/PRODUCTION.md): the assignment, visual language, reporting and verification process.
- [Editorial guide](output/week-in-hazel/EDITORIAL.md) and [audience](output/week-in-hazel/AUDIENCE.md): write for the people working on Hazel.
- [Issue ledger](output/week-in-hazel/issues.json), [image ledger](output/week-in-hazel/image-ledger.json), and [numbering](output/week-in-hazel/NUMBERING.md): continuity across weeks.
- [Preferred screenshot treatment](output/week-in-hazel/assets/probes-cards-woodcut.png), with its [authentic PNG](output/week-in-hazel/assets/probes-cards-clean.png): a light stamp texture, with no added frame.
- [Web publication guide](output/week-in-hazel/web/README.md): HTML editions, the disclosure banner, and the existing personal-site destination.
- [Cloud migration assessment](docs/CLOUD-MIGRATION.md): what is portable now and what still needs work.
- [PDF size audit](docs/PDF-SIZE.md): measured lossless compression headroom, deferred until after the cloud trial.

## Editions

Issue numbers follow reporting weeks, not the order in which editions were produced. Issue 001 anchors September 4–10, 2026; the previous week is 000, with negative numbers before that. Retrospectives retain their historical dates.

| Issue | Reporting week (UTC) | Edition | PDF | HTML |
| --- | --- | --- | --- | --- |
| 001 | September 4–10, 2026 | The cabinet is open. | [Illustrated PDF](output/pdf/week-in-hazel-001-woodcut.pdf) | [Read](https://andrewblinn.com/hazel/weekly/issues/001/) |
| -019 | April 17–23, 2026 | At the same table. | [PDF](output/pdf/week-in-hazel-neg019.pdf) | [Read](https://andrewblinn.com/hazel/weekly/issues/neg019/) |
| -060 | July 4–10, 2025 | Another seat at the desk. | [PDF](output/pdf/week-in-hazel-neg060.pdf) | [Read](https://andrewblinn.com/hazel/weekly/issues/neg060/) |
| -100 | September 27–October 3, 2024 | New roots. | [PDF](output/pdf/week-in-hazel-neg100.pdf) | [Read](https://andrewblinn.com/hazel/weekly/issues/neg100/) |

The pilot also has a [clean screenshot edition](output/pdf/week-in-hazel-001.pdf) and [style studies](output/pdf/week-in-hazel-001-style-lab.pdf). Earlier revisions are retained as production history; use the current production brief and approved edition when making new issues.

## Repository layout

```text
output/week-in-hazel/   Editorial kit, builders, research, assets, and ledgers
output/pdf/             Finished PDFs
site/hazel/weekly/      Complete copy of the published web archive
docs/                   Import provenance and cloud migration notes
```

The original `output/` layout is preserved so relative asset links and PDF destinations keep working. This repository does not contain Hazel application source. Keep a separate checkout of [hazelgrove/hazel](https://github.com/hazelgrove/hazel) for commit analysis and application builds.

To preview the copied web archive locally, run this from the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory site
```

Then open `http://localhost:8000/hazel/weekly/`.

The existing PDF builders use Python, ReportLab, Pillow, pypdf, Node, Playwright, Chrome, and Linux Libertine/Rubik/Liberation Mono fonts. Some runtime and font paths still point to the original Mac installation. They are preserved working examples, not yet a portable cloud build. The collector needs `gh`; the analyzer must run with the **Hazel checkout as its working directory**, because it reads Hazel's Git objects. Use absolute paths to this repository's scripts and new research directories when running it there.

## Automation and deployment status

Imported September 11, 2026. This is the project repository and a starting point for cloud migration. **Creating it did not move or activate a scheduled job.** The existing Friday 9 a.m. America/Los_Angeles Codex task still runs locally and reads the original production kit in the sibling `hazel` checkout. Until that task is migrated, reconcile any newer issues and ledgers from that working kit before using this repository for production.

The live website remains in [disconcision/disconcision.github.io](https://github.com/disconcision/disconcision.github.io), deployed from `master`. This repository's `site/` directory is a complete imported copy of the archive, not a second deployment. Publishing a commit here does not update the website. Keep website changes confined to `hazel/weekly/` and preserve the existing `/hazel` redirect and all other navigation.

The import includes the finished issues and retained revisions without changing their bytes. [The import manifest](docs/import-manifest.json) records paths, sizes, checksums, and the source website commit. Local credentials, browser profiles, dependency installations, Hazel worktrees, and automation configuration are not included.
