# -*- coding: utf-8 -*-
"""Builds assets/data/s151-directory.json from reviewed research files.

Usage: python3 _build/data_directory.py reviewed.json "October 2026"
reviewed.json is a list of {"council","name","title","interim","source","url","date"} using MHCLG council names.
Council types come from assets/data/s151-reserves.json. Only names taken from councils' own published sources.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "assets", "data")
DISPLAY = [(" UA", ""), (" BC", ""), (" DC", ""), (" CC", " County Council"), ("&", "and")]


def tidy(n):
    for a, b in DISPLAY:
        if n.endswith(a.strip()) and a.startswith(" ") and n.endswith(a):
            n = n[: -len(a)] + b
    return n.replace(" & ", " and ")


def main(src, checked):
    types = {c["n"]: c["c"] for c in json.load(open(os.path.join(DATA, "s151-reserves.json")))["councils"]}
    rows = {r["council"]: r for r in json.load(open(src))}
    out = []
    for n, t in types.items():
        r = rows.get(n, {})
        e = {"council": tidy(n), "type": t}
        if r.get("name"):
            e.update({k: r.get(k) for k in ("name", "title", "interim", "source", "url", "date")})
        out.append(e)
    json.dump({"checked": checked, "entries": out}, open(os.path.join(DATA, "s151-directory.json"), "w"), separators=(",", ":"))
    print(f"{sum(1 for x in out if x.get('name'))} of {len(out)} councils with a confirmed S151 officer")


if __name__ == "__main__":
    main(*sys.argv[1:3])
