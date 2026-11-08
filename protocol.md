# Mini-protocol: RBI announcements and short-run volatility (PROVISIONAL until reviewed)

## 1. Question
Is the absolute daily return of the Nifty 50 and Nifty Midcap 100 higher in the first sessions after an RBI announcement than in the preceding baseline? Descriptive only.

## 2. Timing rule (provisional)
Day 0 is the first NSE trading session whose price series can reflect the announcement.
- Released on a trading day before the 15:30 IST close: day 0 is that date, tagged "intraday release" (part of that day's move precedes the news).
- Released after the close: day 0 is the next trading session, tagged "after close".
- Released on a non-trading day: day 0 is the next trading session, tagged "non-trading day".
- Release times should come from an official RBI source. The three press releases state no time, so each time is still to be confirmed (see section 8).
- While a release time is blank, the script reports both cases (before close / after close) as labelled scenarios. These are not results until the time is confirmed.
- Trading days are the dates in the NSE index files, cross-checked against the NSE holiday calendar (docs/nse_holidays_2017-2024_compiled.pdf).
- The cutoff is the constant `MARKET_CLOSE` in `scripts/03_event_windows.py`.

## 3. Measures (fixed before looking at results)
- Daily log return r_t = ln(P_t / P_(t-1)); absolute return = |r_t|, from daily closes.
- Baseline: mean absolute return over days -20 to -1.
- Event window: mean absolute return over days 0 to +2.
- Report difference and ratio (event / baseline) per index per event. No significance tests (n = 3).

## 4. Events
| ID | Type | Date | What changed (from the RBI press release) | Release time (IST) | Source | Overlap flags |
|---|---|---|---|---|---|---|
| A | scheduled | 2017-08-02 | Repo rate cut 25 bp to 6.00%; neutral stance | to confirm (event log says 10:00) | PR 2017-2018/325 | to verify: GST rollout, Doklam standoff |
| B | off-cycle | 2022-05-04 | Repo rate raised 40 bp to 4.40%; accommodative stance, focus on withdrawal of accommodation | to confirm (event log says 14:00) | PR 2022-2023/154 | to verify: US Fed decision on 4 May (after the Indian close), global selloff |
| C | scheduled | 2025-02-07 (to be confirmed; originally planned as 2024-12-06) | Repo rate cut 25 bp to 6.25%; neutral stance | to confirm (event log says 10:00) | PR 2024-2025/2094 | to verify: Union Budget 1 Feb 2025 (inside baseline), US tariff news, Fed meeting late Jan 2025 |

Day 0 and timing tags per event are in `results/event_summary.csv` (column guide: `docs/results_columns.md`).

## 5. Data sources
See `docs/sources.md`.

## 6. Results
Not final. The current files hold only 13 (A), 15 (B) and 19 (C) of the 20 baseline days, so the numbers in `results/event_summary.csv` are not comparable across events. Re-download longer price history (about 30 trading days before day 0), rerun the scripts, then copy the table here.

## 7. Limitations
- Three events only: description, not inference. Association, not causation.
- Daily data cannot separate pre- and post-announcement moves on an intraday-release day.
- Overlapping events in the windows (see overlap flags) may contaminate results.
- A rule for handling overlaps (flag only, exclude, or sensitivity check) has to be set before results are read.

## 8. Open decisions for the reviewer
- Event C: 2025-02-07 or 2024-12-06.
- Official release times for A, B and C.
- Window lengths (baseline, event window); daily vs intraday data.
- Treatment of overlapping events.

## Changelog
See `docs/changelog.md`. Record date and reason for every rule change.
