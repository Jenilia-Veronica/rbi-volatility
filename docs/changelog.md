# Changelog (rules and parameters)
| Date | Change | Reason |
|---|---|---|
| 2026-11-07 | Initial rules: log returns; baseline -20..-1; event window 0..+2; day 0 per timing rule with 15:30 IST close | Starting protocol, set before looking at results |
| 2026-11-07 | Event C date set to 2025-02-07 in event log (was 2024-12-06) | Uploaded RBI press release and price CSVs for Event C all cover the 7 Feb 2025 MPC decision; pending confirmation of intended event |
| 2026-11-07 | 03_event_windows.py: when release time is blank, run both cases (before close / after close) and label them "scenario"; results table has a new `case` column | Times are not in the RBI press releases; day 0 cannot be fixed yet. Scenarios are not a guess at the time, they show whether the result depends on it |
| 2026-11-07 | Baseline uses whatever days are in the file; `n_baseline_days` is reported (13-15 of 20 for A and B with current downloads) | Price files too short; re-download longer history to get the full 20 |
| 2026-11-08 | Docs aligned with Event C = 2025-02-07 (protocol.md, sources.md); holiday PDF moved from raw/ to docs/ and labelled as compiled; event log times stored as text, tracking text removed from links, overlap flags updated; notebook outputs cleared; requirements given minimum versions | Repository review: documents disagreed with each other and with the data; the calendar is not an untouched download |
| 2026-11-08 | Removed duplicate raw/calendar/ folder (compiled calendar lives in docs/); tidied wording in event log (Event B what_changed, Event C notes) | Repository review follow-up |
