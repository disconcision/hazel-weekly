# Week in Hazel web archive

The archive lives at **https://andrewblinn.com/hazel/weekly/** in
`disconcision/disconcision.github.io`, published from `master` by GitHub Pages.
Andrew changed the destination from hazel.org to his personal site on September 11, 2026.
Keep all public files under `hazel/weekly/`; do not add links from the rest of his
site or change unrelated pages. Preserve the separate `hazel/index.html` redirect
to hazel.org. The page and every HTML edition have a prominent red banner with
warm white text, with these two lines:

**All content is fully AI-generated from the Hazel Git repository and GitHub data.**

Reporting, writing and illustrations are all AI-produced.

The public tagline is **A small digest for the hazelnut community.** Pages request
`noindex` but are publicly accessible. Do not add archive links elsewhere on the site.

The initial archive contains 001 and retrospectives -019, -060 and -100. Latest
means latest reporting week, not the retrospective's production date. The public
001 PDF is the approved illustrated edition. PDF contents are copied unchanged.

`build_web.py SITE_ROOT/hazel/weekly` produces responsive HTML editions from the
finished prose and assets. Use Python with Pillow. `pilot-content.json` records
the final pilot's text nodes; the retrospective sources remain in `back-issues`.
The web layout reflows the print columns, preserves all article text and citations,
recreates numerical charts with accessible tables, and links images at their full
resolution. The pilot masthead omits its reference to a separate clean PDF because
the public archive currently offers the illustrated edition only.

Every HTML edition opens with its original cover illustration as a large,
full-width leader above the title and introduction. Show the complete image at
its native aspect ratio within the page margins: no frame, mat, cropping, rounded
corners or shadow. Link it to the complete printed cover. On desktop, set the
issue number and date beside the title/deck; on narrow screens, let them stack.
Use the current issue pages as the reference, not the superseded thumbnail layout.

`page()` is the reusable edition wrapper. A future issue supplies its own source
articles, `cover_src` and `cover_alt`; it must not reuse the pilot's prose or art.
The script's default command rebuilds the four initial editions, so extending the
archive requires adding the new issue's content to the build, not merely rerunning
the initial-issue command. Preserve existing issue URLs and published files.

Every article section must have a permanent, unique lowercase URL slug and a
linked heading: `<section id="fumola">` with a title link to `#fumola`, for
example. `article()` supplies the heading permalink and its small `#` marker;
the shared stylesheet keeps it visible on touch screens and keyboard accessible.
Readers can click a title and copy the address, or copy the title's link directly.
The contents list must use the same targets. Keep the link as an ordinary HTML
anchor so sharing works without JavaScript. Use a short descriptive slug for new
sections, and retain it when editing the title or moving the section. Preserve
all previously published IDs, including the original retrospectives' `article-N`
IDs; if an ID ever changes, keep the old one as an alias. The builder rejects
duplicate article IDs. Verify that every heading permalink and contents link
resolves to exactly one target, and check a direct fragment URL on desktop and
mobile layouts before publishing.

The landing page and shared stylesheet are maintained in the site repository.
Andrew explicitly authorized adding each new weekly issue to this public archive
as part of the weekly generation task on September 11, 2026. Publication here is
part of completing the issue; no repeated approval is needed for that routine step.
This does not authorize Slack/email distribution or publication at other sites.

For every new issue, add the finished PDF, full printed cover thumbnail, cover art
and readable HTML edition; update the featured issue and weekly archive. Keep
retrospectives in their separate section and do not displace the latest regular
issue with a newly produced retrospective. Validate local links, article text,
image dimensions, responsive layout rules, the disclosure, and PDF integrity.
Check that the git diff contains only `hazel/weekly/`, fetch remote changes, then
commit and publish through the existing GitHub Pages `master` branch without
force-pushing or changing site-wide configuration. Verify the live HTML, PDF,
art and archive links before recording completion. Save the published URLs and
commit with the issue's production record, and notify Andrew with the live issue
link. If publication fails, retain the completed local issue and report the
specific failure; retry that publication without generating a duplicate issue.
