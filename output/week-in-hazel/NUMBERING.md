# Week in Hazel issue numbering

Issue numbers identify UTC reporting weeks, regardless of when an issue is produced.

- Issue 001: September 4-10, 2026; cutoff September 11 at 00:00 UTC.
- Issue 000: August 28-September 3, 2026.
- Issue -001: August 21-27, 2026.
- Earlier weeks continue backward; future weeks continue 002, 003, and so on.

Each week begins Friday at 00:00 UTC and ends the following Friday at 00:00 UTC, exclusive. For a week beginning S, its signed number is `1 + (S - 2026-09-04).days // 7`. Validate that S is a Friday at midnight. A skipped week still occupies its number; issue numbers never count published artifacts or revisions. Keep revision numbers separately.

Display nonnegative numbers with three digits; display negatives with an ASCII minus sign and at least three magnitude digits, e.g. -019. For filenames use `week-in-hazel-neg019.pdf` for Issue -019, so the sign is unambiguous and there is no double hyphen. Dates remain in every cover and ledger record. Keep the existing 001 filenames.

Back issues are labeled retrospective editions, produced from historical evidence today. The date on the cover is the reporting window, not an invented publication date. A brief retrospective label is enough in the magazine; reconstruction details belong in source notes. Do not import later outcomes into the week without an explicit later-looking-back note. Mutable PR bodies, current branch names and current screenshots cannot establish past state by themselves.

Historical git counts use only objects reachable from the chosen development head at the week’s end, filtered by committer timestamp. Selection may screen today’s reachable history, but final historical metrics must use the period head. Report that narrower denominator; it is not directly comparable to the pilot’s current remote-branch census. Reconstruct issue/PR state from dated events when possible. Do not display today’s issue backlog as a past-week backlog. Never claim historical branch-push counts from surviving refs.

The ledger stores a signed integer `number`, display `id`, date window, `edition: retrospective`, production date and historical source heads. Read entries by reporting date, not insertion order. Weekly automation computes the current completed window and ignores retrospective production dates when checking coverage.
