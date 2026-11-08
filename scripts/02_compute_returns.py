# step 2: daily log returns and absolute returns
# r = ln(P_t / P_t-1), abs_ret = |r|
# reads clean/prices_*.csv, writes clean/returns_<event>.csv (both indices together)

import glob
import re
import os
# always work from the project folder, even if the script is run from somewhere else
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import pandas as pd

per_event = {}

for f in sorted(glob.glob("clean/prices_*.csv")):
    m = re.match(r"prices_([a-z0-9]+)_(event[A-Za-z0-9]+)\.csv", os.path.basename(f))
    if m is None:
        continue
    index, event = m.group(1), m.group(2)

    df = pd.read_csv(f, parse_dates=["date"]).sort_values("date")
    df["index"] = index
    df["ret"] = np.log(df["close"] / df["close"].shift(1))
    df["abs_ret"] = df["ret"].abs()
    df = df.dropna(subset=["ret"])   # first day has no return
    per_event.setdefault(event, []).append(df)

for event, parts in per_event.items():
    out = pd.concat(parts)[["date", "index", "close", "ret", "abs_ret"]]
    out.to_csv("clean/returns_%s.csv" % event, index=False)
    print("returns_%s.csv" % event, len(out), "rows")
