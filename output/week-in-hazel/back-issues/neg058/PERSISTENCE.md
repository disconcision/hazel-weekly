# Persistence note

The authenticated GitHub connector verified account `disconcision` has `admin` permission and created `codex/cloud-back-issue-trial` from `36c0a703e8b84014dd5030e74de712f8f16f61d7`.

Editable production files, research, prompts, QA, HTML and all six PNG assets are committed on that branch. The connector rejected the finished 18,019,306-byte PDF when its base64 payload exceeded the connector's 16 MiB request limit:

`HTTP 400: MCP request body is invalid or exceeds the 16 MiB limit`

The downloadable bundle contains both PDF paths and the exact local commit. The smallest remaining repository step is a normal authenticated push of the local commit (or an approved Git LFS setup for the PDF) after review. No live-site or schedule state is involved.
