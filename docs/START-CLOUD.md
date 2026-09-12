# Start a cloud trial yourself

This repository contains the editorial instructions, examples, source evidence, assets, builders, and ledgers needed to brief a new agent. It does **not** yet provide a fully working, unattended cloud installation. The first trial produced and pushed substantial work, but exposed build, capture, and large-file export problems. The next task should inherit those findings rather than rediscover them.

## Start in the interface

1. Open [ChatGPT on the web](https://chatgpt.com/) using the same account as the desktop app. Starting here makes the cloud execution choice explicit without relying on the confusing local Hazel sidebar entry.
2. Create a ChatGPT project named **Week in Hazel**, then start a new conversation inside it and select **Work**. An existing ChatGPT project is also fine. This project organizes conversations; the GitHub repository supplies the production files.
3. Open the model control and choose **GPT-6 Astra**, then set effort to **Extra High**. Select these in the interface before sending the prompt; mentioning a model in the prompt does not configure it. Astra was available in the account's web Work model picker when checked September 11, 2026, Pacific time.
4. Make the connected GitHub plugin available to the task. The previous cloud task could read Hazel and write branches in `disconcision/hazel-weekly` through that connection; a normal shell Git session did not automatically inherit those credentials. Do not paste tokens into the conversation or repository.
5. Paste the prompt below. Keep this first manually launched task unscheduled and unpublished. Find the new project and conversation on the phone and desktop before considering the eventual automation handover complete.

For a desktop start, select **ChatGPT**, create a Work conversation, and choose **Cloud** from the composer control labeled **Work locally**, when available. Check the model and effort there too. The earlier desktop sidebar visibility problem remains unconfirmed; creating a project yourself may clarify the navigation but is not a verified synchronization fix.

These steps follow the official [quickstart](https://learn.chatgpt.com/docs/quickstart) and [Work guide](https://learn.chatgpt.com/docs/get-started-with-work). No repository-oriented Codex cloud environment needs to be created for this Work trial.

## Copy this prompt

```text
Produce a new retrospective Week in Hazel issue as a cloud production trial.

Retrieve https://github.com/disconcision/hazel-weekly and start from its current main branch. Read AGENTS.md, README.md, docs/START-CLOUD.md, and docs/CLOUD-TRIAL.md, then follow the production, audience, numbering, visual-example, and ledger references they specify. The reporting repository is https://github.com/hazelgrove/hazel. Do not depend on my Mac or on prior conversation context.

First inspect the previous trial branch codex/cloud-back-issue-trial, especially output/week-in-hazel/back-issues/neg058/QA.md, PERSISTENCE.md, and research/cloud-build-check.md. Reuse useful setup work after reviewing it. Check the recorded Hazel build, native PNG capture, and PDF export failures early; resolve routine setup problems with the available hosted tools and retain exact commands and outcomes.

Choose a substantial uncovered historical week in the two years before September 11, 2026. Exclude issues 001, -019, -058, -060, and -100, plus any subsequently covered weeks. Calculate the calendar issue number. Produce the illustrated PDF, cover-led HTML, fresh cover/comic, light Cards-style screenshot treatments with authentic PNG originals, research, editable sources, prompts, and QA specified by the brief.

Save this new trial on a fresh codex/cloud-trial-<issue-slug> branch, preserving the old trial branch. Return direct links to the PDF, HTML/assets package, and branch. Verify that exported files are actually retrievable; creating files inside the VM is not delivery. If any stage remains blocked, save useful work and report the exact limitation without claiming a complete migration.

Keep the issue unpublished. Do not merge into main, alter the website, or create or change any schedule. The local weekly publisher remains active until a separate, verified handover. Proceed with the trial; do not stop at a plan.
```

The fresh branch name and additional exclusion above override the original trial's fixed branch name and exclusion list. This is a fresh editorial trial with reusable infrastructure, not authorization to overwrite Issue -058.

## What the first trial saved

Verified through a remote Git fetch on September 11, 2026, Pacific time (September 12 UTC):

- Branch: [`codex/cloud-back-issue-trial`](https://github.com/disconcision/hazel-weekly/tree/codex/cloud-back-issue-trial).
- Commit: [`daace136f1cff30b1f552efcc6f0080663239a97`](https://github.com/disconcision/hazel-weekly/commit/daace136f1cff30b1f552efcc6f0080663239a97).
- Candidate: **Issue -058**, July 18–24, 2025 UTC. The branch contains prose, HTML, a fresh cover and comic, two original historical PNGs and their treatments, research, prompts, proposed ledgers, a builder, and portability changes. Nothing was merged or published; no PR existed at verification.
- The agent's QA reports an eight-page PDF, 18,019,306 bytes. **The PDF is absent from the remote branch.** Its upload exceeded the connector's 16 MiB request-body limit after base64 encoding. This is a connector transport limit, not GitHub's ordinary Git file-size limit.
- The conversation currently ends with a **network error**. Although its committed notes refer to a downloadable bundle, a delivered bundle link was not visible when checked. Treat that export as unverified; the builder and source assets are preserved.
- The QA reports successful OCaml 5.2.0 and npm setup, followed by missing `libgmp-dev` and failed apt privilege operations. Chromium downloads timed out, and the connected browser emitted JPEG. These are recorded trial failures, not proof that all supported solutions have been exhausted.

Read the committed [QA](https://github.com/disconcision/hazel-weekly/blob/codex/cloud-back-issue-trial/output/week-in-hazel/back-issues/neg058/QA.md) and [persistence note](https://github.com/disconcision/hazel-weekly/blob/codex/cloud-back-issue-trial/output/week-in-hazel/back-issues/neg058/PERSISTENCE.md) for evidence. A finished-looking issue alone does not establish that weekly jobs can independently build, stage, capture, save, and publish Hazel work.

## What is already in the production kit

`AGENTS.md` and `README.md` point to the current production and editorial guides, audience definition, issue numbering, coverage/image ledgers, screenshot exemplar, approved PDFs, and web publication requirements. No previous conversation needs to be uploaded. Follow the current guides rather than treating every retained draft as an instruction.

The standalone repository is locally cloned at `/Users/andrewblinn/Dropbox/projects/hazel-weekly`. Cloud work must retrieve its GitHub copy. The local automation still reads the older sibling Hazel production directory, so reconciliation and the single-publisher handover remain required before recurring cloud production.
