# rbi-volatility-protocol-v1

Does the Indian equity market move more than usual right after an RBI policy announcement? This mini-protocol measures the absolute daily returns of the **Nifty 50** and **Nifty Midcap 100** around three RBI announcements and compares them with a pre-announcement baseline.

> **Status: provisional.** Three events only, so the output is descriptive (no significance tests, no causal claims). The price files currently hold 13 (A), 15 (B) and 19 (C) of the 20 baseline days, so the numbers in `results/` are not final until longer history is downloaded. Release times are still to be confirmed from a primary source.

## Events

| ID | Type | Date | What changed |
|---|---|---|---|
| A | Scheduled | 2 Aug 2017 | Repo rate cut 25 bp to 6.00% |
| B | Off-cycle | 4 May 2022 | Repo rate raised 40 bp to 4.40% |
| C | Scheduled | 7 Feb 2025 (to be confirmed; originally planned as 6 Dec 2024) | Repo rate cut 25 bp to 6.25% |

Release times are recorded in `docs/event_log.xlsx`; the RBI press releases (in `raw/rbi/`) state no time, so each time still needs a primary source.

## Method

- **Return:** daily log return, r<sub>t</sub> = ln(P<sub>t</sub> / P<sub>t-1</sub>), from daily closing values. Volatility proxy = |r<sub>t</sub>|.
- **Day 0:** the first NSE trading session that can reflect the announcement.
  - Released on a trading day before the 15:30 IST close: day 0 is that day (tagged *intraday release*).
  - Released after the close: day 0 is the next session (*after close*).
  - Released on a non-trading day: day 0 is the next session (*non-trading day*).
  - If the release time is missing, the script reports both cases as labelled *scenarios* instead of guessing.
- **Baseline:** mean absolute return over trading days -20 to -1.
- **Event window:** mean absolute return over days 0 to +2.
- **Output per event and index:** baseline mean, event mean, difference and ratio (event / baseline), plus overlap flags (other events inside the window, such as a Fed decision).

The full rule, formulas and limitations are in `protocol.md` (master copy).

## Folder layout

```
raw/         untouched downloads (never edited)
  prices/      index price CSVs from niftyindices.com
  rbi/         RBI press releases (PDF)
clean/       script output: cleaned prices and returns
scripts/     01_clean_prices.py, 02_compute_returns.py, 03_event_windows.py
notebooks/   mini_protocol_analysis.ipynb (table and charts)
results/     event_summary.csv and figures/
docs/        event_log.xlsx, sources.md, changelog.md, results_columns.md,
             nse_holidays_2017-2024_compiled.pdf (compiled from NSE circulars, not an NSE file)
review/      mini_protocol_v1.pdf goes here once written (not added yet)
```

## Quick start

1. Install Python 3 and the packages:
   ```
   python -m venv .venv
   .venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Put the price CSVs in `raw/prices/`. Name them `<index>_<event>_<download-date>.csv`, all lowercase, for example `nifty50_eventA_2026-11-08.csv` and `niftymidcap100_eventB_2026-11-08.csv`. If an index/event has several downloads, the latest one is used.
3. Fill in `docs/event_log.xlsx` (date, release time in IST, source, overlap flags).
4. Run the scripts in order (they work from any folder):
   ```
   python scripts/01_clean_prices.py
   python scripts/02_compute_returns.py
   python scripts/03_event_windows.py
   ```
5. Open `results/event_summary.csv` and `results/figures/`, or run the notebook.

## Data needed for each event

Download daily closes for both indices from roughly **30 trading days before to 10 trading days after** the event. The baseline needs 21 closes before day 0 (20 returns plus one close to compute the first return), and the chart runs to day +5. If the history is too short, the script prints a warning and `n_baseline_days` in the summary shows how many days it actually had.

## Outputs

- `results/event_summary.csv`: one row per event, index and case, marked "provisional until reviewed".
- `results/figures/<event>_abs_returns.png`: absolute returns from day -20 to +5 for both indices, with day 0 marked.

## Reproducibility rules

1. `raw/` is read-only. All cleaning happens in scripts.
2. `clean/` and `results/` are written by scripts only, never by hand.
3. Every download is logged in `docs/sources.md` with its URL and download date.
4. Every change to a rule or parameter is logged in `docs/changelog.md` with the date and reason.
5. Parameters (window lengths, 15:30 close) are fixed before looking at results.

## Data and licence note

Price data comes from NSE Indices and press releases from the RBI. Check their terms of use before publishing raw data; this repository should stay private until sharing is agreed.
