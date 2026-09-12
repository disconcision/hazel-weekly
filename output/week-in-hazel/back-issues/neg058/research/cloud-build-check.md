# Cloud build and capture check

Trial date: 2026-09-12 UTC. Historical source revision: `790b84e568197eb668591c4b05903aaeb6de20a9`.

## Dependency inventory

- Present initially: Git 2.51.1, GCC 13.3.0, GNU Make 4.3, Node 24.19.0, npm, Python 3.12.14.
- Absent initially: `opam`, `ocamlc`, `dune`, `m4`, `pkg-config`.
- System libraries present at runtime included libgmp, libssl, libz and libffi, but the development headers/package metadata required by the opam depext checks were not present; `libgmp-dev` was the first reported blocker.

## Commands and actual results

1. Downloaded the official opam 2.5.2 x86_64 Linux static binary from the GitHub release. `opam --version` returned `2.5.2`.
2. Initialized an isolated root with `opam init --bare --disable-sandboxing -y default https://github.com/ocaml/opam-repository.git`. Result: success.
3. Created an isolated OCaml 5.2.0 switch with `opam switch create ... ocaml-base-compiler.5.2.0 -y`. Result: success; OCaml 5.2.0 installed from source.
4. Ran `npm ci` at the historical Hazel revision. Result: success; 71 packages installed.
5. Ran the revision's `make deps`. Repository initialization and update succeeded, including the historical opam archive repository. Dependency solving then failed with exit code 20: `deps-of-hazel -> conf-gmp >= 5 depends on the unavailable system package 'libgmp-dev'`.
6. Ran `make dev` in the same switch. Result: exit 127 because `dune` was not installed after the dependency step failed.

The environment's apt transport could not repair the system layer. `apt-get update` failed because its `_apt` privilege drop could not call `setgroups`, `setegid`, or `seteuid`, and it could not write the apt cache. The smallest build setup is a cloud image (or allowed package layer) with `libgmp-dev`, `libffi-dev`, `libssl-dev`, `zlib1g-dev`, `pkg-config`, and `m4`; then rerun `make deps` and `make dev` in the isolated OCaml 5.2.0 switch. The trial does not establish that a future weekly job can build a fresh Hazel branch.

## Hosted browser and native PNG

The connected Chrome browser loaded `https://hazel.org/build/backpack-2/` successfully. Its screenshot API returned 87,159 bytes beginning `ff d8 ff e0 ... JFIF`, i.e. JPEG, even when saved without an extension. That does not satisfy the native lossless PNG requirement.

An attempted Playwright Chromium install (`npx playwright install chromium`) retried the 153.0.8010.12 archive three times; each request to `https://cdn.playwright.dev/builds/cft/153.0.8010.12/linux64/chrome-linux64.zip` timed out after 30 seconds without downloading data. A direct five-minute-capable `curl` attempt to the same URL also transferred zero bytes for 33 seconds before being stopped. `apt-get update` was unavailable for the privilege reasons above. The smallest capture setup is either (a) a preinstalled Chromium/Firefox executable exposed to hosted Playwright, or (b) network access to the Playwright browser archive plus required shared libraries. The browser must then be exercised with a true PNG output and the file signature verified.

For this editorial candidate, the screenshot originals are authentic historical PNG attachments from dated Hazel GitHub discussions. They are valid evidence for the article but do not demonstrate fresh cloud staging or capture.
