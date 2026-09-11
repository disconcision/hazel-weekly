# Moving weekly production off the Mac

Assessment: September 11, 2026. A one-off ChatGPT Work Cloud trial has now been started. No replacement weekly schedule, separately provisioned Codex cloud environment, paid API integration, or deployment workflow has been activated.

## Current next step: the hosted back-issue trial

The app already contains two distinct projects named **hazel**: a local project connected to the Mac's Hazel checkout, and a ChatGPT project. The trial was started directly in the existing ChatGPT project using the app's ChatGPT Work Cloud task creation capability. Andrew does not need to create another project for this trial. The local project and this production conversation remain intact; no in-place conversion was attempted.

- Cloud task ID: `6aa49166-9678-83ea-a228-bcc4e5135ce7`.
- ChatGPT project ID: `g-p-6898c74753888191b5b9e8751ebbd402`.
- Starting production revision: `36c0a703e8b84014dd5030e74de712f8f16f61d7`.
- Assignment: [one new retrospective issue](CLOUD-TRIAL.md), including an actual hosted-tool capability check before production.
- The task is now titled **Produce Cloud Trial Issue**. Its actual web conversation shows repository retrieval, Node/Python and Poppler checks, and selection of Issue **-058**, July 18–24, 2025, with historical cutoff head beginning `790b84e568`. Browser access to public `hazel.org` was allowed for this chat, and the web UI then showed work continuing. Successful completion is not yet established.
- The desktop `read_thread` tool returned only the initial user brief despite substantial assistant progress being visible on the web. Do not use an empty assistant-message result or the generic active/idle flag alone to conclude that this cloud task has not started or has finished.

This is **ChatGPT Work Cloud**, which is distinct from the repository-oriented Codex cloud environment described below. The official [Work guide](https://learn.chatgpt.com/docs/get-started-with-work) describes hosted work that can continue after the desktop app closes. A [ChatGPT project](https://learn.chatgpt.com/docs/projects) organizes shared sources and conversations; the local-folder project does not automatically become a hosted filesystem. This trial reads its durable production kit from GitHub.

The cloud task must attempt the new back issue, record which tools work, and identify any exact missing connection or dependency. During the trial it cannot publish or enable recurring execution. After the result passes review, pause and verify the local schedule before activating a cloud replacement, as specified in the trial brief. There must be only one active weekly publisher.

## Access across devices is an acceptance requirement

Andrew wants a clearly discoverable project and task in the desktop client and on his phone, without depending on a special link supplied by an agent. Do not declare the migration ready until this is verified along with production and publishing.

- [Existing ChatGPT hazel project](https://chatgpt.com/g/g-p-6898c74753888191b5b9e8751ebbd402-hazel/project).
- [Produce Cloud Trial Issue](https://chatgpt.com/g/g-p-6898c74753888191b5b9e8751ebbd402/c/6aa49166-9678-83ea-a228-bcc4e5135ce7).

Both URLs were observed in the authenticated ChatGPT web UI. Expanding its sidebar showed the task as a Work conversation under **hazel**. Desktop-sidebar discovery and phone access still need confirmation. The native desktop UI could not be inspected through Computer Use because that tool blocks control of the Codex app; the app's purpose-built project/task APIs and the separate ChatGPT web UI were used instead.

The [official comparison](https://learn.chatgpt.com/docs/use-chatgpt) distinguishes the ChatGPT view, which includes Work and web/mobile conversations, from the Codex developer view. A local Hazel folder entry is a different project from the ChatGPT **hazel** project. Work Cloud and Codex share core execution machinery, but their tool access and histories are not interchangeable. The [cloud execution documentation](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-cloud-security) makes this distinction explicit. A clearly named dedicated magazine project may improve organization later; creating another project is not by itself a fix for missing desktop navigation.

An existing [desktop cloud-project synchronization report](https://github.com/openai/codex/issues/32718), filed July 13, 2026, describes projects visible on the web but missing in a desktop app version. This is related user evidence, not a confirmed diagnosis for Andrew's current app. First check the ChatGPT product view and project navigation; do not assume a reported bug applies or recreate the trial merely because a sidebar entry is missing.

## What exists now

The editorial process, source snapshots, issue/image ledgers, artwork, screenshots, PDF builders, finished issues, and HTML archive are now in this repository. The initial import preserves the existing files and relative layout. The active weekly Codex automation remains local and continues to use the original production kit in the sibling Hazel checkout.

Local scheduled tasks require the computer to be on and the Codex app running. Web scheduled tasks are a separate capability, available when enabled for the account/workspace; they do not preserve this local checkout between runs. See the official [scheduled-task documentation](https://learn.chatgpt.com/docs/automations).

## Alternative execution routes if the hosted trial needs them

**Codex cloud:** connect this repository, create an environment, and install the required tools through its setup. Codex runs repository tasks remotely. Before choosing it for the whole magazine, test its browser capture, image editing/generation, artifact handling, and recurring execution together. The documentation does not establish that this existing desktop heartbeat can simply be transferred with all the same tools. See [Codex cloud](https://learn.chatgpt.com/docs/cloud) and [cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environment).

**A scheduled hosted CI runner running Codex:** a GitHub-hosted job could check out the production and Hazel repositories, run the editorial agent with the saved brief, render the outputs, and publish to the existing website repository. OpenAI provides a [Codex GitHub Action](https://learn.chatgpt.com/docs/github-action) that runs Codex CLI in CI and requires an OpenAI API key. A full magazine workflow would still need screenshot and image-generation tools, dependency setup, persistence, and a measured per-run budget. This is a proposed architecture, not something this repository currently runs.

The CI route gives explicit control over the long visual-production pipeline. A separately configured Codex cloud environment may also be useful if the ChatGPT Work Cloud trial exposes limitations. Neither alternative is required merely to start the current hosted trial. Validate the actual capabilities before choosing a weekly scheduler.

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
