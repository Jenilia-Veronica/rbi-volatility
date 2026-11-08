# step 1: clean the raw price files from niftyindices
# reads raw/prices/*.csv, writes clean/prices_<index>_<event>.csv
# raw files are never touched

import glob
import re
import os
# always work from the project folder, even if the script is run from somewhere else
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import pandas as pd

# files look like nifty50_eventA_2026-11-07.csv
name_re = re.compile(r"^([a-z0-9]+)_(event[A-Za-z0-9]+)_(\d{4}-\d{2}-\d{2})\.csv$")

# the niftyindices files use "02 Aug 2017" or "02-Aug-17" depending on the index
date_formats = ["%d %b %Y", "%d-%b-%Y", "%d-%b-%y", "%d/%m/%Y", "%Y-%m-%d"]


def read_dates(col):
    # try each format one by one. letting pandas guess was dropping all the april
    # rows because it saw "May" first and decided the format was %B
    col = col.astype(str).str.strip()
    out = pd.Series(pd.NaT, index=col.index)
    for fmt in date_formats:
        left = out.isna()
        out[left] = pd.to_datetime(col[left], format=fmt, errors="coerce")
    return out


files = {}
for f in sorted(glob.glob("raw/prices/*.csv")):
    m = name_re.match(os.path.basename(f))
    if m is None:
        print("skipping (bad file name):", f)
        continue
    # sorted, so if there are two downloads the later one wins
    files[(m.group(1), m.group(2))] = f

if len(files) == 0:
    raise SystemExit("no csv files found in raw/prices/")

for (index, event), f in files.items():
    df = pd.read_csv(f)
    df.columns = [c.strip().lower() for c in df.columns]
    df["date"] = read_dates(df["date"])
    df["close"] = pd.to_numeric(df["close"].astype(str).str.replace(",", "").str.strip(), errors="coerce")

    bad = df["date"].isna() | df["close"].isna()
    if bad.sum() > 0:
        print("warning:", f, "-", bad.sum(), "rows could not be read and were dropped")

    df = df[~bad].drop_duplicates("date").sort_values("date")
    df[["date", "close"]].to_csv("clean/prices_%s_%s.csv" % (index, event), index=False)
    print(index, event, len(df), "rows,", df["date"].min().date(), "to", df["date"].max().date())
