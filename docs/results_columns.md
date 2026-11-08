# Columns in results/event_summary.csv
| Column | Meaning |
|---|---|
| event_id, event_type | eventA/B/C; scheduled or off-cycle |
| release_date, release_time_ist | from docs/event_log.xlsx |
| case | "time in log" (time given) or "scenario: before/after close" (time blank, both cases shown) |
| timing_tag | intraday release, after close or non-trading day (see protocol.md section 2) |
| index | nifty50 or niftymidcap100 |
| day0 | first trading session that can reflect the announcement |
| n_baseline_days | days actually available in days -20 to -1 (20 expected) |
| n_event_days | days actually available in days 0 to +2 (3 expected) |
| baseline_mean_abs | mean absolute log return, days -20 to -1 |
| event_mean_abs | mean absolute log return, days 0 to +2 |
| difference, ratio | event minus baseline; event divided by baseline |
| overlap_flags | other events inside the window, from the event log |
| status | always "provisional until reviewed" for now |
