# -*- coding: utf-8 -*-
"""Builds assets/data/s151-audit.json from PSAA's detailed monthly audit opinion data.

Usage:  python3 _build/data_audit.py path/to/Opinion-data-detailed-*.xlsx "30 September 2026" URL
Needs:  pip install pandas openpyxl. Run data_reserves.py first (it supplies the council list).
Source: PSAA, "Monthly audit opinion data". The file shows whether and when each opinion was
signed, not whether it was unmodified, qualified or disclaimed.
"""
import json
import os
import re
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "assets", "data")
SECT = {"District Council", "Unitary Authority", "Metropolitan District Council", "London Borough Council", "County Council"}
YEARS = ["2023-2024", "2024-2025", "2025-2026"]
STATUS = {"Delivered by backstop": "B", "Post backstop opinion delivered": "L", "Unsigned": "U"}


def norm(s):
    s = s.lower().replace("&", " and ").replace("'", "")
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[^a-z ]", " ", s)
    for w in ["royal borough of", "london borough of", "borough of", "city of", "city and district", "and district",
              "metropolitan borough", "metropolitan district", "metropolitan", "borough", "district", "county", "city",
              "council of the", "council", "london", "towns", "ua", "bc", "dc", "mbc", "cc", "the", "upon", "on", "of"]:
        s = re.sub(r"\b" + w + r"\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def main(path, as_at, url):
    councils = json.load(open(os.path.join(DATA, "s151-reserves.json"), encoding="utf-8"))["councils"]
    keys = {}
    for c in councils:
        k = norm(c["n"])
        if k:
            assert k not in keys, f"duplicate key {k}"
            keys[k] = c["n"]
    xl = pd.ExcelFile(path)
    out = {}
    for yr in YEARS:
        t = pd.read_excel(xl, sheet_name=yr)
        t.columns = [str(c).strip() for c in t.columns]
        t = t[t["Sector Type"].isin(SECT)]
        for _, r in t.iterrows():
            name = keys.get(norm(str(r["Organisation Name"])))
            if not name:
                continue
            st = STATUS.get(str(r["Audit Status"]).strip())
            if not st:
                continue
            dt = r["Audit Signed Date"]
            dt = pd.to_datetime(dt, errors="coerce")
            out.setdefault(name, {})[yr[:4] + "/" + yr[7:]] = [st, None if pd.isna(dt) else dt.strftime("%Y-%m-%d")]
    data = {"asAt": as_at, "source": url, "years": [y[:4] + "/" + y[7:] for y in YEARS], "councils": out}
    with open(os.path.join(DATA, "s151-audit.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))
    print(f"Wrote s151-audit.json: {len(out)} of {len(councils)} councils matched")


if __name__ == "__main__":
    main(*sys.argv[1:4])
