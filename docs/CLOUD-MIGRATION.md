# Moving weekly production off the Mac

Assessment: September 11, 2026. This document records a proposed migration. No cloud environment, paid API use, deployment workflow, or replacement schedule has been activated.

## What exists now

The editorial process, source snapshots, issue/image ledgers, artwork, screenshots, PDF builders, finished issues, and HTML archive are now in this repository. The initial import preserves the existing files and relative layout. The active weekly Codex automation remains local and continues to use the original production kit in the sibling Hazel checkout.

Local scheduled tasks require the computer to be on and the Codex app running. Web scheduled tasks are a separate capability, available when enabled for the account/workspace; they do not preserve this local checkout between runs. See the official [scheduled-task documentation](https://learn.chatgpt.com/docs/automations).

## Two possible execution routes

**Codex cloud:** connect this repository, create an environment, and install the required tools through its setup. Codex runs repository tasks remotely. Before choosing it for the whole magazine, test its browser capture, image editing/generation, artifact handling, and recurring execution together. The documentation does not establish that this existing desktop heartbeat can simply be transferred with all the same tools. See [Codex cloud](https://learn.chatgpt.com/docs/cloud) and [cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environment).

**A scheduled hosted CI runner running Codex:** a GitHub-hosted job could check out the production and Hazel repositories, run the editorial agent with the saved brief, render the outputs, and publish to the existing website repository. OpenAI provides a [Codex GitHub Action](https://learn.chatgpt.com/docs/github-action) that runs Codex CLI in CI and requires an OpenAI API key. A full magazine workflow would still need screenshot and image-generation tools, dependency setup, persistence, and a measured per-run budget. This is a proposed architecture, not something this repository currently runs.

The second route gives explicit control over the long visual-production pipeline. The first may be simpler if an end-to-end trial confirms the required tools and scheduling are available. Validate those capabilities before choosing a scheduler.

## Remaining work

1. **Make the renderer portable.** Replace absolute Mac paths in the current builders and browser layers. Pin Python/Node packages and the browser, supply the font files with their licenses, and document Poppler installation. The copied web archive already includes its licensed web fonts, but the PDF builder needs additional font faces. Confirm `text-wrap: pretty` and the measured composition pass on the actual cloud browser.
2. **Provision Hazel separately.** GitHub harvesting uses `gh`; commit analysis needs the appropriate Hazel refs and objects. Feature screenshots may require historical or branch builds with OCaml/opam, dune, and JavaScript dependencies. The current examples borrowed a local opam switch and dependency tree, which a fresh cloud job will not have.
3. **Replace desktop-only capture steps.** Supply a browser the agent can operate in the cloud, stage disposable programs and probes, and save genuine high-resolution PNGs. Preserve the ability to choose zoom, panels, and crop deliberately. Check that the same feature can actually be built and demonstrated there.
4. **Validate image production.** Confirm access to image generation and reference-image editing in the chosen execution environment. Do not assume the desktop tool automatically exists there. A separate image API may be needed. Carry the light Cards stamp exemplar, original PNGs, actual prompts, and visual QA into the trial.
5. **Save durable state and publish deliberately.** Persist new research, assets, editable copy, PDFs, and both ledgers back to this repository or a documented artifact store. Cloud container caches are not the archive. Configure the required GitHub access to read Hazel, save production work here, and update only the authorized website path. The local `gh` login does not travel with this repository. Codex cloud secrets are available during setup and removed before the agent phase; design the integration around supported authentication rather than copying secrets into tracked files.
6. **Make scheduled runs recoverable.** Key production to the completed reporting window, check the issue ledger, prevent overlapping runs, and save a checkpoint before publication. Retry publication of an existing issue after a failure. Record the published website commit and URLs only after verification. Keep retrospectives separate from the current weekly cutoff.

## Proposed cutover

Run one complete cloud trial before changing the existing automation: acquire a bounded source window, build a representative Hazel feature, compose and capture a screenshot, apply the approved stamp treatment, produce original art, render and inspect a PDF, and build the readable HTML edition. Compare the result with Issue 001 and confirm the archive links and disclosure. Use an unpublished trial artifact so the experiment does not consume an issue number or duplicate an existing edition.

Once the chosen environment can do that reliably, reconcile any newer local issues and ledgers into this repository, configure the weekly schedule, and retire the old local schedule as one coordinated change. Keep the current Friday schedule until the replacement is tested. The existing public website address can stay the same throughout.

## Deferred: smaller PDFs

After the cloud execution trial, evaluate a lossless PDF packaging pass. Andrew requested no visible quality loss and explicitly prioritized the cloud work. The [initial file-size audit](PDF-SIZE.md) finds that images dominate Issue 001, with a projected 26.8% saving from removing encoding overhead and compressing unchanged stream data. This estimate has not yet been validated in a rewritten PDF; published editions are unchanged.
