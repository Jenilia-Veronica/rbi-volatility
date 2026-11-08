# step 3: find day 0 for each event, then compare the baseline and event windows
# reads docs/event_log.xlsx + clean/returns_<event>.csv
# writes results/event_summary.csv and one chart per event (results/figures/)
#
# timing rule (full version is in protocol.md, still provisional):
#   - released on a trading day before 15:30 IST  -> day 0 is that day ("intraday release")
#   - released on a trading day at/after 15:30    -> day 0 is the next session ("after close")
#   - released on a non trading day               -> day 0 is the next session ("non-trading day")
#   - trading days = dates that are in the NSE index files
#
# if the release time is blank in the event log we do NOT guess it. instead the
# script runs both cases (before close / after close) and labels them as
# scenarios, so you can see whether the answer depends on the time at all.

import datetime as dt
import os
# always work from the project folder, even if the script is run from somewhere else
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

MARKET_CLOSE = dt.time(15, 30)   # IST
BASELINE = (-20, -1)             # trading days, inclusive
EVENT_WIN = (0, 2)
PLOT_WIN = (-20, 5)


def get_time(x):
    # time cell in the excel sheet can be empty, text like "14:00" or a real time
    if x is None or pd.isna(x) or str(x).strip() == "":
        return None
    if isinstance(x, dt.datetime):
        return x.time()
    if isinstance(x, dt.time):
        return x
    return pd.to_datetime(str(x)).time()


def day0_options(trading_days, event_date, t):
    # returns a list of (case, day0, tag)
    trading_set = set(trading_days)
    is_trading = event_date in trading_set
    later = [d for d in trading_days if d > event_date]
    next_day = later[0] if later else None

    if t is None:
        opts = []
        if is_trading:
            opts.append(("scenario: before close", event_date, "time not stated"))
        if next_day is not None:
            opts.append(("scenario: after close", next_day, "time not stated"))
        return opts

    if is_trading and t < MARKET_CLOSE:
        return [("time in log", event_date, "intraday release")]
    if next_day is None:
        return []
    if is_trading:
        return [("time in log", next_day, "after close")]
    return [("time in log", next_day, "non-trading day")]


# the log can be the excel file or a csv copy of it
if os.path.exists("docs/event_log.xlsx"):
    events = pd.read_excel("docs/event_log.xlsx", sheet_name="events")
elif os.path.exists("docs/event_log.csv"):
    events = pd.read_csv("docs/event_log.csv")
else:
    raise SystemExit("no event log found, put event_log.xlsx (or event_log.csv) in the docs folder")
rows = []

for _, e in events.iterrows():
    eid = str(e["event_id"]).strip()
    try:
        rets = pd.read_csv("clean/returns_%s.csv" % eid, parse_dates=["date"])
    except FileNotFoundError:
        print(eid, "- no returns file yet, skipping")
        continue

    event_date = pd.Timestamp(e["date"])
    t = get_time(e["release_time_ist"])

    # case -> {index: dataframe with rel_day}, used for the charts
    plots = {}

    for index, g in rets.groupby("index"):
        g = g.sort_values("date").reset_index(drop=True)
        options = day0_options(list(g["date"]), event_date, t)

        if len(options) == 0:
            print(eid, index, "- could not find a day 0 in the data")
            continue

        for case, day0, tag in options:
            i0 = g.index[g["date"] == day0][0]
            w = g.copy()
            w["rel_day"] = w.index - i0

            base = w[w["rel_day"].between(*BASELINE)]["abs_ret"]
            evt = w[w["rel_day"].between(*EVENT_WIN)]["abs_ret"]

            wanted = BASELINE[1] - BASELINE[0] + 1
            if len(base) < wanted:
                print("%s %s (%s): only %d of %d baseline days, need more history" % (eid, index, case, len(base), wanted))
            if len(evt) < EVENT_WIN[1] - EVENT_WIN[0] + 1:
                print("%s %s (%s): event window is incomplete" % (eid, index, case))

            rows.append({
                "event_id": eid,
                "event_type": e["event_type"],
                "release_date": event_date.date(),
                "release_time_ist": t,
                "case": case,
                "timing_tag": tag,
                "index": index,
                "day0": day0.date(),
                "n_baseline_days": len(base),
                "n_event_days": len(evt),
                "baseline_mean_abs": base.mean(),
                "event_mean_abs": evt.mean(),
                "difference": evt.mean() - base.mean(),
                "ratio": evt.mean() / base.mean(),
                "overlap_flags": e.get("overlap_flags"),
                "status": "provisional until reviewed",
            })
            plots.setdefault(case, {})[index] = w[w["rel_day"].between(*PLOT_WIN)]

    # one chart per case
    for case, by_index in plots.items():
        plt.figure(figsize=(8, 4))
        for index, w in by_index.items():
            plt.plot(w["rel_day"], w["abs_ret"] * 100, marker="o", markersize=3, label=index)
        plt.axvline(0, color="black", linestyle="--", linewidth=1, label="day 0")
        plt.xlabel("trading days from day 0")
        plt.ylabel("absolute return (%)")
        plt.title("%s - %s (provisional)" % (eid, case))
        plt.legend()
        plt.tight_layout()
        suffix = "" if case == "time in log" else "_" + case.split(": ")[1].replace(" ", "_")
        plt.savefig("results/figures/%s_abs_returns%s.png" % (eid, suffix), dpi=150)
        plt.close()

summary = pd.DataFrame(rows)
summary.to_csv("results/event_summary.csv", index=False)
print("done,", len(summary), "rows in results/event_summary.csv")
