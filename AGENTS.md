# Working on Week in Hazel

Read `README.md` for repository and deployment status. Before editorial production, read `output/week-in-hazel/PRODUCTION.md`, `EDITORIAL.md`, `AUDIENCE.md`, `NUMBERING.md`, both ledgers, and recent issues. Preserve the approved visual example and the light Cards stamp exemplar. Do not recycle old copy or art into a new reporting week.

This is the magazine repository, not the Hazel application checkout. Git-based research must use a separate Hazel checkout. In particular, `analyze.py` reads Git objects from its working directory; running it in this repository would analyze the wrong history. Keep each issue's research in a fresh dated directory.

The existing local weekly automation still reads the original production kit in the sibling Hazel checkout. Reconcile later work before migrating it. Do not create a duplicate schedule or assume a push here changes the active automation. `docs/CLOUD-MIGRATION.md` describes a proposed migration, not an installed workflow.

Public editions belong at `https://andrewblinn.com/hazel/weekly/`, deployed through `disconcision/disconcision.github.io`. Follow `output/week-in-hazel/web/README.md`. The imported `site/hazel/weekly/` is a web archive copy; publishing requires updating the website repository. Keep changes scoped to that archive and preserve the separate `/hazel` redirect. Each edition needs the prominent red AI disclosure and a complete, unframed cover illustration above its title.

Keep authentic screenshots, generated treatments, exact prompts, source maps, editable copy, PDFs, and issue/image ledgers together. Earlier revisions are historical evidence, not current instructions. Preserve current editions when adding new ones. Do not infer AI assistance from style or activity volume.

For portability work, replace host-specific runtime paths with documented configuration and verify the actual rendering engine. For content or layout changes, follow the production guide's PDF rendering and visual inspection steps. For a byte-preserving import, verify checksums rather than regenerating approved artifacts.
