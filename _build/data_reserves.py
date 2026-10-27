# -*- coding: utf-8 -*-
"""Builds assets/data/s151-reserves.json from MHCLG's revenue outturn summary (RS).

Usage:  python3 _build/data_reserves.py path/to/RS_LA_Data_YYYY-YY_data_by_LA.ods "2025-26" "17 September 2026" URL
Needs:  pip install pandas odfpy
Source: "Local authority revenue expenditure and financing: individual local authority data - outturn" on GOV.UK.
Figures are in £ thousands, as reported by each council (not audited accounts).
"""
import json
import os
import sys

import pandas as pd

CLASSES = {"SD": "Shire district", "UA": "Unitary authority", "MD": "Metropolitan district",
           "LB": "London borough", "SC": "County council"}


def find(cols, *needles):
    for c in cols:
        if all(n.lower() in c.lower() for n in needles):
            return c
    raise KeyError(needles)


def main(path, year, published, url):
    xl = pd.ExcelFile(path, engine="odf")
    sheet = [s for s in xl.sheet_names if s.startswith("RS_LA_Data")][0]
    raw = pd.read_excel(xl, sheet_name=sheet, header=None)
    hdr = raw.index[raw.iloc[:, 0].astype(str).str.strip() == "E-code"][0]
    df = pd.read_excel(xl, sheet_name=sheet, header=hdr).copy()
    cols = list(df.columns)
    c = {
        "nre": find(cols, "Revenue Expenditure Financing", "NET REVENUE EXPENDITURE"),
        "oe01": find(cols, "other earmarked financial reserves level at 1 April"),
        "oe31": find(cols, "other earmarked financial reserves level at 31 March"),
        "un01": find(cols, "unallocated financial reserves level at 1 April"),
        "un31": find(cols, "unallocated financial reserves level at 31 March"),
        "hra31": find(cols, "HRA) Reserves at 31 March"),
    }
    num = lambda s: pd.to_numeric(s, errors="coerce")
    out = []
    councils = df[df["Class"].isin(CLASSES) & df["E-code"].astype(str).str.match(r"^E\d+$")]
    for _, r in councils.iterrows():
        v = {k: num(pd.Series([r[col]])).iloc[0] for k, col in c.items()}
        rec = {"n": str(r["Local authority"]).strip(), "c": r["Class"]}
        ok = pd.notna(v["nre"]) and pd.notna(v["oe31"]) and pd.notna(v["un31"]) and v["nre"] > 0
        if ok and (v["oe31"] + v["un31"]) > 0:
            rec.update({
                "nre": round(float(v["nre"])), "r31": round(float(v["oe31"] + v["un31"])),
                "u31": round(float(v["un31"])),
                "r01": round(float(v["oe01"] + v["un01"])) if pd.notna(v["oe01"]) and pd.notna(v["un01"]) else None,
            })
            if pd.notna(v["hra31"]) and v["hra31"] > 0:
                rec["hra"] = round(float(v["hra31"]))
        else:
            # "x": return not received in time; "z": return received but reserves reported as nil or incomplete
            rec["nd"] = "x" if str(r[c["oe31"]]).strip() == "[x]" or str(r[c["nre"]]).strip() == "[x]" else "z"
        out.append(rec)
    out.sort(key=lambda x: x["n"].lower())
    data = {"year": year, "published": published, "source": url, "units": "£000",
            "classes": CLASSES, "councils": out}
    dest = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "data", "s151-reserves.json")
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))
    have = sum(1 for x in out if "r31" in x)
    print(f"Wrote {dest}: {len(out)} councils, {have} with reserves data")


if __name__ == "__main__":
    main(*sys.argv[1:5])
